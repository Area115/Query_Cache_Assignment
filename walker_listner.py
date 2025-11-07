# file: normalize_full_query.py
from antlr4 import InputStream, CommonTokenStream, ParseTreeWalker
from grammer.SQLiteLexer import SQLiteLexer
from grammer.SQLiteParser import SQLiteParser
from grammer.SQLiteParserListener import SQLiteParserListener
import re
import copy

PLACEHOLDER = "?"  # change to ">" if you prefer


class LiteralExtractorListener(SQLiteParserListener):
    def __init__(self):
        self.literals = []

    def enterLiteral_value(self, ctx):
        # ctx.getText() gives the literal as string
        self.literals.append(ctx.getText())

    def enterExpr(self, ctx):
        # handle booleans like TRUE/FALSE (SQLite sometimes parses these as expr)
        text = ctx.getText().lower()
        if text in ("true", "false", "null"):
            self.literals.append(text)

    def enterAny_name(self, ctx):
        text = ctx.getText()
        # capture double-quoted identifiers or string-like values
        if text.startswith('"') and text.endswith('"'):
            self.literals.append(text)


class SubqueryCollector(SQLiteParserListener):
    """
    Collect ONLY leaf select_core nodes (no nested SELECT inside).
    """
    def __init__(self, parser, tokens):
        self.parser = parser
        self.tokens = tokens
        self.subqueries = []

    def get_sql_text(self, ctx):
        start, stop = ctx.start.tokenIndex, ctx.stop.tokenIndex
        toks = self.tokens.tokens[start:stop + 1]
        sql = " ".join(t.text for t in toks if t.text.strip())
        return re.sub(r"\s+", " ", sql).strip()

    def has_nested_select(self, ctx):
        """Check if current select_core contains another select_core inside."""
        for child in ctx.getChildren():
            if hasattr(child, "getRuleIndex"):
                rule_name = self.parser.ruleNames[child.getRuleIndex()]
                if rule_name == "select_core":
                    return True
                if self.has_nested_select(child):
                    return True
        return False

    def enterSelect_core(self, ctx):
        # capture only leaf select_core (those without nested SELECT inside)
        if not self.has_nested_select(ctx):
            sql_text = self.get_sql_text(ctx)
            self.subqueries.append(sql_text)


class MaskInnerSelectsListener(SQLiteParserListener):
    """
    Old behavior: mask ALL inner select_core nodes (used by existing process()).
    """
    def __init__(self, parser, tokens):
        self.parser = parser
        self.tokens = tokens
        self.first_select_seen = False   # outermost tracker
        self.inner_select_count = 0

    def _replace_ctx_with_placeholder(self, ctx):
        start, stop = ctx.start.tokenIndex, ctx.stop.tokenIndex
        # clear this subquery body
        for i in range(start, stop + 1):
            self.tokens.tokens[i].text = ""
        self.tokens.tokens[start].text = PLACEHOLDER

    def enterSelect_core(self, ctx):
        if not self.first_select_seen:
            self.first_select_seen = True
            return
        self.inner_select_count += 1
        self._replace_ctx_with_placeholder(ctx)


class MaskNonLeafSelectsListener(SQLiteParserListener):
    """
    NEW behavior: mask ONLY non-leaf select_core nodes.
    Leaf subqueries remain (so they can appear inline in the outer query).
    """
    def __init__(self, parser, tokens):
        self.parser = parser
        self.tokens = tokens
        self.first_select_seen = False

    def _has_nested_select(self, ctx):
        for child in ctx.getChildren():
            if hasattr(child, "getRuleIndex"):
                rule_name = self.parser.ruleNames[child.getRuleIndex()]
                if rule_name == "select_core":
                    return True
                if self._has_nested_select(child):
                    return True
        return False

    def _replace_ctx_with_placeholder(self, ctx):
        start, stop = ctx.start.tokenIndex, ctx.stop.tokenIndex
        for i in range(start, stop + 1):
            self.tokens.tokens[i].text = ""
        self.tokens.tokens[start].text = PLACEHOLDER

    def enterSelect_core(self, ctx):
        if not self.first_select_seen:
            self.first_select_seen = True  # keep the outermost intact
            return
        # mask only if this select_core contains another select_core
        if self._has_nested_select(ctx):
            self._replace_ctx_with_placeholder(ctx)


class NormalizeQuery(SQLiteParserListener):
    """
    Replace literals (numbers/strings/bools) everywhere with PLACEHOLDER.
    """
    def __init__(self, parser, tokens):
        self.parser = parser
        self.tokens = tokens
        self.literals_seen = []

    def _replace_ctx_with_placeholder(self, ctx):
        start, stop = ctx.start.tokenIndex, ctx.stop.tokenIndex
        for i in range(start, stop + 1):
            self.tokens.tokens[i].text = ""
        self.tokens.tokens[start].text = PLACEHOLDER

    def enterLiteral_value(self, ctx):
        self.literals_seen.append(ctx.getText())
        self._replace_ctx_with_placeholder(ctx)

    def enterExpr(self, ctx):
        t = ctx.getText().lower()
        if t == "true" or t == "false":
            self.literals_seen.append(t)
            self._replace_ctx_with_placeholder(ctx)

    def enterAny_name(self, ctx):
        val = ctx.getText()
        if val.startswith('"') and val.endswith('"'):
            self._replace_ctx_with_placeholder(ctx)


class ExtractAndNormalize():
    def __init__(self):
        pass

    def parse(self, sql: str):
        inp = InputStream(sql)
        lexer = SQLiteLexer(inp)
        tokens = CommonTokenStream(lexer)
        parser = SQLiteParser(tokens)
        tree = parser.sql_stmt_list()
        return parser, tokens, tree

    def _rebuild_text(self, tokens, parser):
        txt = " ".join(t.text for t in tokens.tokens if t.text and t.text.strip() and t.type != parser.EOF)
        txt = re.sub(r"\s+", " ", txt).strip()
        # collapse IN ( ? , ? , ... , ? ) → IN ( ?? )
        txt = re.sub(r"\bIN\s*\(\s*(?:\?\s*,\s*)+\?\s*\)", "IN ( ?? )", txt, flags=re.IGNORECASE)
        # fix accidental multiple placeholders inside parentheses → ( ? )
        txt = re.sub(r"\(\s*\?\s*(?:\?\s*)*\)", "( ? )", txt)
        return txt

    def normalize_full_query(self, sql: str):
        # literals-only normalization across the whole SQL
        parser, tokens, tree = self.parse(sql)
        walker = ParseTreeWalker()
        walker.walk(NormalizeQuery(parser, tokens), tree)
        return self._rebuild_text(tokens, parser)
    
    def process(self, sql: str):
        # A) full normalized SQL (literals only)
        full_norm_sql = self.normalize_full_query(sql)

        # B) leaf subqueries (normalized)
        p2, t2, tr2 = self.parse(sql)
        leaf_collector = SubqueryCollector(p2, t2)
        ParseTreeWalker().walk(leaf_collector, tr2)
        leaf_norm_subqueries = [self.normalize_full_query(q) for q in leaf_collector.subqueries]
        leaf_norm_subqueries = list(dict.fromkeys(leaf_norm_subqueries))

        # C) outer with leaf kept: normalize literals, then mask ONLY non-leaf selects
        p3, t3, tr3 = self.parse(sql)
        walker = ParseTreeWalker()
        walker.walk(NormalizeQuery(p3, t3), tr3)                 # normalize literals
        walker.walk(MaskNonLeafSelectsListener(p3, t3), tr3)     # mask non-leaf selects, keep leaf selects inline
        outer_with_leaf_kept = self._rebuild_text(t3, p3)

        # D) literals
        p4, t4, tr4 = self.parse(sql)
        lit_listener = LiteralExtractorListener()
        ParseTreeWalker().walk(lit_listener, tr4)
        literals = copy.deepcopy(lit_listener.literals)

        return full_norm_sql, leaf_norm_subqueries, outer_with_leaf_kept, literals


if __name__ == "__main__":
    r = """SELECT * FROM customers WHERE id = 101 ;"""

    obj = ExtractAndNormalize()

    full_norm, leaf_list, outer_keep_leaf, literals = obj.process_three(r)
    print("full_norm_sql:", full_norm)
    print("leaf_norm_subqueries:", leaf_list)
    print("outer_with_leaf_kept:", outer_keep_leaf)
    print("literals:", literals)