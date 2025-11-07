# Generated from SQLiteParser.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .SQLiteParser import SQLiteParser
else:
    from SQLiteParser import SQLiteParser

# This class defines a complete generic visitor for a parse tree produced by SQLiteParser.

class SQLiteParserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by SQLiteParser#parse.
    def visitParse(self, ctx:SQLiteParser.ParseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#sql_stmt_list.
    def visitSql_stmt_list(self, ctx:SQLiteParser.Sql_stmt_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#sql_stmt.
    def visitSql_stmt(self, ctx:SQLiteParser.Sql_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#alter_table_stmt.
    def visitAlter_table_stmt(self, ctx:SQLiteParser.Alter_table_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#analyze_stmt.
    def visitAnalyze_stmt(self, ctx:SQLiteParser.Analyze_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#attach_stmt.
    def visitAttach_stmt(self, ctx:SQLiteParser.Attach_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#begin_stmt.
    def visitBegin_stmt(self, ctx:SQLiteParser.Begin_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#commit_stmt.
    def visitCommit_stmt(self, ctx:SQLiteParser.Commit_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#rollback_stmt.
    def visitRollback_stmt(self, ctx:SQLiteParser.Rollback_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#savepoint_stmt.
    def visitSavepoint_stmt(self, ctx:SQLiteParser.Savepoint_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#release_stmt.
    def visitRelease_stmt(self, ctx:SQLiteParser.Release_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#create_index_stmt.
    def visitCreate_index_stmt(self, ctx:SQLiteParser.Create_index_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#indexed_column.
    def visitIndexed_column(self, ctx:SQLiteParser.Indexed_columnContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#create_table_stmt.
    def visitCreate_table_stmt(self, ctx:SQLiteParser.Create_table_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#column_def.
    def visitColumn_def(self, ctx:SQLiteParser.Column_defContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#type_name.
    def visitType_name(self, ctx:SQLiteParser.Type_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#column_constraint.
    def visitColumn_constraint(self, ctx:SQLiteParser.Column_constraintContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#signed_number.
    def visitSigned_number(self, ctx:SQLiteParser.Signed_numberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#table_constraint.
    def visitTable_constraint(self, ctx:SQLiteParser.Table_constraintContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#foreign_key_clause.
    def visitForeign_key_clause(self, ctx:SQLiteParser.Foreign_key_clauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#conflict_clause.
    def visitConflict_clause(self, ctx:SQLiteParser.Conflict_clauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#create_trigger_stmt.
    def visitCreate_trigger_stmt(self, ctx:SQLiteParser.Create_trigger_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#create_view_stmt.
    def visitCreate_view_stmt(self, ctx:SQLiteParser.Create_view_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#create_virtual_table_stmt.
    def visitCreate_virtual_table_stmt(self, ctx:SQLiteParser.Create_virtual_table_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#with_clause.
    def visitWith_clause(self, ctx:SQLiteParser.With_clauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#cte_table_name.
    def visitCte_table_name(self, ctx:SQLiteParser.Cte_table_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#recursive_cte.
    def visitRecursive_cte(self, ctx:SQLiteParser.Recursive_cteContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#common_table_expression.
    def visitCommon_table_expression(self, ctx:SQLiteParser.Common_table_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#delete_stmt.
    def visitDelete_stmt(self, ctx:SQLiteParser.Delete_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#delete_stmt_limited.
    def visitDelete_stmt_limited(self, ctx:SQLiteParser.Delete_stmt_limitedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#detach_stmt.
    def visitDetach_stmt(self, ctx:SQLiteParser.Detach_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#drop_stmt.
    def visitDrop_stmt(self, ctx:SQLiteParser.Drop_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#expr.
    def visitExpr(self, ctx:SQLiteParser.ExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#raise_function.
    def visitRaise_function(self, ctx:SQLiteParser.Raise_functionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#literal_value.
    def visitLiteral_value(self, ctx:SQLiteParser.Literal_valueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#value_row.
    def visitValue_row(self, ctx:SQLiteParser.Value_rowContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#values_clause.
    def visitValues_clause(self, ctx:SQLiteParser.Values_clauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#insert_stmt.
    def visitInsert_stmt(self, ctx:SQLiteParser.Insert_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#returning_clause.
    def visitReturning_clause(self, ctx:SQLiteParser.Returning_clauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#upsert_clause.
    def visitUpsert_clause(self, ctx:SQLiteParser.Upsert_clauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#pragma_stmt.
    def visitPragma_stmt(self, ctx:SQLiteParser.Pragma_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#pragma_value.
    def visitPragma_value(self, ctx:SQLiteParser.Pragma_valueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#reindex_stmt.
    def visitReindex_stmt(self, ctx:SQLiteParser.Reindex_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#select_stmt.
    def visitSelect_stmt(self, ctx:SQLiteParser.Select_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#join_clause.
    def visitJoin_clause(self, ctx:SQLiteParser.Join_clauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#select_core.
    def visitSelect_core(self, ctx:SQLiteParser.Select_coreContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#factored_select_stmt.
    def visitFactored_select_stmt(self, ctx:SQLiteParser.Factored_select_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#simple_select_stmt.
    def visitSimple_select_stmt(self, ctx:SQLiteParser.Simple_select_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#compound_select_stmt.
    def visitCompound_select_stmt(self, ctx:SQLiteParser.Compound_select_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#table_or_subquery.
    def visitTable_or_subquery(self, ctx:SQLiteParser.Table_or_subqueryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#result_column.
    def visitResult_column(self, ctx:SQLiteParser.Result_columnContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#join_operator.
    def visitJoin_operator(self, ctx:SQLiteParser.Join_operatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#join_constraint.
    def visitJoin_constraint(self, ctx:SQLiteParser.Join_constraintContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#compound_operator.
    def visitCompound_operator(self, ctx:SQLiteParser.Compound_operatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#update_stmt.
    def visitUpdate_stmt(self, ctx:SQLiteParser.Update_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#column_name_list.
    def visitColumn_name_list(self, ctx:SQLiteParser.Column_name_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#update_stmt_limited.
    def visitUpdate_stmt_limited(self, ctx:SQLiteParser.Update_stmt_limitedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#qualified_table_name.
    def visitQualified_table_name(self, ctx:SQLiteParser.Qualified_table_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#vacuum_stmt.
    def visitVacuum_stmt(self, ctx:SQLiteParser.Vacuum_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#filter_clause.
    def visitFilter_clause(self, ctx:SQLiteParser.Filter_clauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#window_defn.
    def visitWindow_defn(self, ctx:SQLiteParser.Window_defnContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#over_clause.
    def visitOver_clause(self, ctx:SQLiteParser.Over_clauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#frame_spec.
    def visitFrame_spec(self, ctx:SQLiteParser.Frame_specContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#frame_clause.
    def visitFrame_clause(self, ctx:SQLiteParser.Frame_clauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#simple_function_invocation.
    def visitSimple_function_invocation(self, ctx:SQLiteParser.Simple_function_invocationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#aggregate_function_invocation.
    def visitAggregate_function_invocation(self, ctx:SQLiteParser.Aggregate_function_invocationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#window_function_invocation.
    def visitWindow_function_invocation(self, ctx:SQLiteParser.Window_function_invocationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#common_table_stmt.
    def visitCommon_table_stmt(self, ctx:SQLiteParser.Common_table_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#order_by_stmt.
    def visitOrder_by_stmt(self, ctx:SQLiteParser.Order_by_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#limit_stmt.
    def visitLimit_stmt(self, ctx:SQLiteParser.Limit_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#ordering_term.
    def visitOrdering_term(self, ctx:SQLiteParser.Ordering_termContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#asc_desc.
    def visitAsc_desc(self, ctx:SQLiteParser.Asc_descContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#frame_left.
    def visitFrame_left(self, ctx:SQLiteParser.Frame_leftContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#frame_right.
    def visitFrame_right(self, ctx:SQLiteParser.Frame_rightContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#frame_single.
    def visitFrame_single(self, ctx:SQLiteParser.Frame_singleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#window_function.
    def visitWindow_function(self, ctx:SQLiteParser.Window_functionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#offset.
    def visitOffset(self, ctx:SQLiteParser.OffsetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#default_value.
    def visitDefault_value(self, ctx:SQLiteParser.Default_valueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#partition_by.
    def visitPartition_by(self, ctx:SQLiteParser.Partition_byContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#order_by_expr.
    def visitOrder_by_expr(self, ctx:SQLiteParser.Order_by_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#order_by_expr_asc_desc.
    def visitOrder_by_expr_asc_desc(self, ctx:SQLiteParser.Order_by_expr_asc_descContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#expr_asc_desc.
    def visitExpr_asc_desc(self, ctx:SQLiteParser.Expr_asc_descContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#initial_select.
    def visitInitial_select(self, ctx:SQLiteParser.Initial_selectContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#recursive_select.
    def visitRecursive_select(self, ctx:SQLiteParser.Recursive_selectContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#unary_operator.
    def visitUnary_operator(self, ctx:SQLiteParser.Unary_operatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#error_message.
    def visitError_message(self, ctx:SQLiteParser.Error_messageContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#module_argument.
    def visitModule_argument(self, ctx:SQLiteParser.Module_argumentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#column_alias.
    def visitColumn_alias(self, ctx:SQLiteParser.Column_aliasContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#keyword.
    def visitKeyword(self, ctx:SQLiteParser.KeywordContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#name.
    def visitName(self, ctx:SQLiteParser.NameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#function_name.
    def visitFunction_name(self, ctx:SQLiteParser.Function_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#schema_name.
    def visitSchema_name(self, ctx:SQLiteParser.Schema_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#table_name.
    def visitTable_name(self, ctx:SQLiteParser.Table_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#table_or_index_name.
    def visitTable_or_index_name(self, ctx:SQLiteParser.Table_or_index_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#column_name.
    def visitColumn_name(self, ctx:SQLiteParser.Column_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#collation_name.
    def visitCollation_name(self, ctx:SQLiteParser.Collation_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#foreign_table.
    def visitForeign_table(self, ctx:SQLiteParser.Foreign_tableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#index_name.
    def visitIndex_name(self, ctx:SQLiteParser.Index_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#trigger_name.
    def visitTrigger_name(self, ctx:SQLiteParser.Trigger_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#view_name.
    def visitView_name(self, ctx:SQLiteParser.View_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#module_name.
    def visitModule_name(self, ctx:SQLiteParser.Module_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#pragma_name.
    def visitPragma_name(self, ctx:SQLiteParser.Pragma_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#savepoint_name.
    def visitSavepoint_name(self, ctx:SQLiteParser.Savepoint_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#table_alias.
    def visitTable_alias(self, ctx:SQLiteParser.Table_aliasContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#transaction_name.
    def visitTransaction_name(self, ctx:SQLiteParser.Transaction_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#window_name.
    def visitWindow_name(self, ctx:SQLiteParser.Window_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#alias.
    def visitAlias(self, ctx:SQLiteParser.AliasContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#filename.
    def visitFilename(self, ctx:SQLiteParser.FilenameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#base_window_name.
    def visitBase_window_name(self, ctx:SQLiteParser.Base_window_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#simple_func.
    def visitSimple_func(self, ctx:SQLiteParser.Simple_funcContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#aggregate_func.
    def visitAggregate_func(self, ctx:SQLiteParser.Aggregate_funcContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#table_function_name.
    def visitTable_function_name(self, ctx:SQLiteParser.Table_function_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SQLiteParser#any_name.
    def visitAny_name(self, ctx:SQLiteParser.Any_nameContext):
        return self.visitChildren(ctx)



del SQLiteParser