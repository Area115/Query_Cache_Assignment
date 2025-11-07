from antlr4 import InputStream, CommonTokenStream, ParseTreeWalker
from grammer.SQLiteLexer import SQLiteLexer
from grammer.SQLiteParser import SQLiteParser


class ParseNormalizeQuery():
    def __init__(self):
        self.query = ""
        self.literals_list = []


    def replace_literals_and_inner_selects(self, sql: str):
        input_stream = InputStream(sql)
        lexer = SQLiteLexer(input_stream)
        token_stream = CommonTokenStream(lexer)
        parser = SQLiteParser(token_stream)
        tree = parser.sql_stmt_list()

        flag = True  # Tracks if we're inside the outermost SELECT

        def replace_node_with_placeholder(ctx):
            start = ctx.start.tokenIndex
            stop = ctx.stop.tokenIndex
            for i in range(start, stop + 1):
                token_stream.tokens[i].text = ""
            token_stream.tokens[start].text = "?"

        def traverse(node):
            nonlocal flag

            if hasattr(node, "getRuleIndex"):
                rule = parser.ruleNames[node.getRuleIndex()]

                # Replace literal values
                if rule == "literal_value":
                    self.literals_list.append(node.getText())
                    replace_node_with_placeholder(node)
                    return

                # Replace quoted any_name (string identifiers)
                if rule == "any_name":
                    text = node.getText()
                    if text.startswith('"') and text.endswith('"'):
                        self.literals_list.append(text)
                        replace_node_with_placeholder(node)
                        return

                # Replace only inner SELECTs (not outermost)
                if rule == "select_core":
                    if flag:
                        flag = False
                    else:
                        replace_node_with_placeholder(node)
                        return

            # Recursive traversal
            for i in range(node.getChildCount()):
                traverse(node.getChild(i))

        traverse(tree)

        final_sql = " ".join(
            t.text for t in token_stream.tokens
            if t.text.strip() != "" and t.type != parser.EOF
        )

        return final_sql

    def get_sql_text_from_context(self, ctx, token_stream: CommonTokenStream):
        start = ctx.start.tokenIndex
        stop = ctx.stop.tokenIndex
        tokens = token_stream.tokens[start:stop + 1]
        sql_text = " ".join(t.text for t in tokens if t.text.strip() != "")
        return sql_text

    def extract_select_blocks(self, node, parser, token_stream, results):
        if hasattr(node, "getRuleIndex"):
            rule = parser.ruleNames[node.getRuleIndex()]
            if rule == "select_core":
                sql_text = self.get_sql_text_from_context(node, token_stream)
                results.append(sql_text)

        for i in range(node.getChildCount()):
            self.extract_select_blocks(node.getChild(i), parser, token_stream, results)

    def parse_and_extract(self, sql_query):
        input_stream = InputStream(sql_query)
        lexer = SQLiteLexer(input_stream)
        token_stream = CommonTokenStream(lexer)
        parser = SQLiteParser(token_stream)
        tree = parser.sql_stmt_list()

        results = []
        self.extract_select_blocks(tree, parser, token_stream, results)
        return results