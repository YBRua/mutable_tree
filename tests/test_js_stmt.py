import unittest
from .js_test_base import JavaScriptSnippetTestBase


class TestJavaScriptVarDecl(JavaScriptSnippetTestBase):

    def test_simple_variable_decl(self):
        self._stmt_round_trip('var a;')
        self._stmt_round_trip('var a = 1;')
        self._stmt_round_trip('var a = 1, b = 2;')
        self._stmt_round_trip('var a = 1, b, c = 3;')

    def test_lexical_decl(self):
        self._stmt_round_trip('let a;')
        self._stmt_round_trip('let a = 1;')
        self._stmt_round_trip('let a = 1, b = 2;')
        self._stmt_round_trip('let a = 1, b, c = 3;')

    def test_const_decl(self):
        self._stmt_round_trip('const a = 1;')
        self._stmt_round_trip('const a = 1, b = 2;')


class TestJavaScriptForStmt(JavaScriptSnippetTestBase):

    def test_simple_for(self):
        self._stmt_round_trip('for (var i = 0; i < 10; i++) { }')
        self._stmt_round_trip('for (let i = 0; i < 10; i++);')
        self._stmt_round_trip('for (const i = 0; i < 10; i++);')
        self._stmt_round_trip('for (i = 0; i <= 5; i++) { }')
        self._stmt_round_trip('for (i = 0; i <= 5; i++);')

    def test_empty_for(self):
        self._stmt_round_trip('for (;;) { }')
        self._stmt_round_trip('for (;;) ;')
        self._stmt_round_trip('for (i = 1;;) { }')
        self._stmt_round_trip('for (; i < 10;) { }')
        self._stmt_round_trip('for (;; i++) { }')

    def test_multi_init(self):
        self._stmt_round_trip('for (var i = 0, j = 0; i < 10; i++) { }')
        self._stmt_round_trip('for (const i = x.begin(), j = 0; i != x.end(); i++) { }')
        self._stmt_round_trip('for (i = 0, j = 0; i < 10; ++i, ++j);')

    def test_multi_update(self):
        self._stmt_round_trip('for (let i = 0; i < 10; i++, j++) { }')
        self._stmt_round_trip('for (i = 0; i < 10; i++, j++);')

    def test_block(self):
        code = 'for (let i = 0; i < 10; ++i) { let j = 2 * i; sum += j; }'
        self._stmt_round_trip(code)

    def test_nested_for(self):
        code = 'for (i = 0; i < 10; ++i) { for (let j = 0; j < 10; ++j) { k = i * j; }}'
        self._stmt_round_trip(code)

        code = 'for (i = 0; i < 10; ++i) for (let j = 0; j < 10; ++j) k = i * j;'
        self._stmt_round_trip(code)

    def test_for_while(self):
        code = 'for (let i = 0; i < 10; ++i) { while (j < 2 * i) { j = 2 * j; } }'
        self._stmt_round_trip(code)


class TestJavaScriptWhileStmt(JavaScriptSnippetTestBase):

    def test_simple_while(self):
        self._stmt_round_trip('while (i < 10) { }')
        self._stmt_round_trip('while (i < 10);')

    def test_empty_while(self):
        self._stmt_round_trip('while (true) { }')
        self._stmt_round_trip('while (true);')

    def test_block(self):
        code = 'while (i < 10) { let j = 2 * i; sum += j; i++; }'
        self._stmt_round_trip(code)

    def test_nested_while(self):
        code = 'while (i < 10) { while (j < 10) { k = i * j; } }'
        self._stmt_round_trip(code)

        code = 'while (i < 10) while (j < 10) k = i * j;'
        self._stmt_round_trip(code)

    def test_while_for(self):
        code = 'while (true) { for (let i = 0; i < 10; ++i) { j = i * 2; } }'
        self._stmt_round_trip(code)


class TestJavaScriptBreakContinue(JavaScriptSnippetTestBase):

    def test_break(self):
        self._stmt_round_trip('while (true) { break; }')
        self._stmt_round_trip('while (true) break label;')

    def test_continue(self):
        self._stmt_round_trip('while (true) { continue; }')
        self._stmt_round_trip('while (true) continue label;')


class TestJavaScriptDoWhileStmt(JavaScriptSnippetTestBase):

    def test_do_while(self):
        self._stmt_round_trip('do { something(); } while (true);')
        self._stmt_round_trip('do { something(); other.things(); } while (i < 10);')


class TestJavaScriptForInStmt(JavaScriptSnippetTestBase):

    def test_for_in(self):
        self._stmt_round_trip('for (let i in obj) { }')
        self._stmt_round_trip('for (var i in obj) { }')
        # self._stmt_round_trip('for (i in obj) { }')

    def test_for_of(self):
        self._stmt_round_trip('for (let i of obj) { }')
        self._stmt_round_trip('for (var i of obj) { }')
        # self._stmt_round_trip('for (i of obj) { }')


class TestJavaScriptIfStmt(JavaScriptSnippetTestBase):

    def test_if(self):
        self._stmt_round_trip('if (goingToFailUnitTest()) dont();')
        self._stmt_round_trip('if (goingToFailUnitTest()) { dont(); }')

    def test_if_else(self):
        code = """
        if (goingToFailUnitTest()) {
            dont();
        } else {
            declareVictory();
            goHome();
        }
        """
        self._stmt_round_trip(code)

        code = """
        if (goingToFailUnitTest())
            dont();
        else
            declareVictory();
        """
        self._stmt_round_trip(code)

    def test_if_elif(self):
        code = """
        if (goingToFailUnitTest()) {
            dont();
        } else if (goingToFailCicd() || hasLineTooLongs()) {
            alsoDont();
        } else {
            declareVictory();
            goHome();
        }
        """
        self._stmt_round_trip(code)


class TestJavaScriptLabeledStmt(JavaScriptSnippetTestBase):

    def test_labeled(self):
        self._stmt_round_trip('label: while (true) { break label; }')


class TestJavaScriptReturnStmt(JavaScriptSnippetTestBase):

    def test_return(self):
        self._stmt_round_trip('if (true) return;')
        self._stmt_round_trip('if (true) return 1;')
        self._stmt_round_trip('if (true) return actuallyFalse;')


class TestJavaScriptSwitchStmt(JavaScriptSnippetTestBase):

    def test_switch(self):
        code = """
        switch (value) {
            case 1:
                doSomething();
                break;
            case 2:
                doSomethingElse();
                break;
        }
        """
        self._stmt_round_trip(code)

    def test_default(self):
        code = """
        switch (value) {
            case 1:
                doSomething();
                break;
            default:
                doSomethingElse();
        }
        """
        self._stmt_round_trip(code)

    def test_empty_case(self):
        code = """
        switch (value) {
            case 1:
            case 2:
                doSomething();
                break;
            case 3:
                doAnother();
                break;
            case 4:
            default:
                doSomethingElse();
                break;
        }
        """
        self._stmt_round_trip(code)


class TestJavaScriptTryStmt(JavaScriptSnippetTestBase):

    def test_try(self):
        code = """
        try {
            somethingExplosive();
        } catch (e) {
            ohNo(e);
        }
        """
        self._stmt_round_trip(code)

        code = """
        try {
            somethingExplosive();
        } catch {
            ohNo();
        }
        """

    def test_finally(self):
        code = """
        try {
            somethingExplosive();
        } catch (e) {
            ohNo(e);
        } finally {
            cleanUp();
        }
        """
        self._stmt_round_trip(code)


class TestJavaScriptWithStmt(JavaScriptSnippetTestBase):
    
    def test_with(self):
        self._stmt_round_trip('with (obj) { doSomething(); }')


if __name__ == '__main__':
    unittest.main()
