import unittest
from .java_test_base import JavaSnippetTestBase


class TestJavaVarDecl(JavaSnippetTestBase):

    def test_simple_variable_decl(self):
        self._stmt_round_trip('int a;')
        self._stmt_round_trip('int a = 1;')
        self._stmt_round_trip('float a = b;')
        self._stmt_round_trip('float a = b + 1;')

    def test_multiple_decl(self):
        self._stmt_round_trip('int a, b;')
        self._stmt_round_trip('int a, b = 1;')
        self._stmt_round_trip('float a, b = c;')
        self._stmt_round_trip('float a = 1.0, b = 2.32;')

    def test_array_decl(self):
        self._stmt_round_trip('int[] a;')
        self._stmt_round_trip('int a, b[];')
        self._stmt_round_trip('float[][] a, b;')
        self._stmt_round_trip('float[][] a, b[];')
        # TODO: add initializer tests

    def test_custom_types(self):
        self._stmt_round_trip('MyClass a;')
        self._stmt_round_trip('MyClass a = myClassFactory.getNewInstance();')
        self._stmt_round_trip('MyClass a, b, c[];')


class TestJavaForStmt(JavaSnippetTestBase):

    def test_simple_for(self):
        self._stmt_round_trip('for (int i = 0; i < 10; i++) { }')
        self._stmt_round_trip('for (int i = 0; i < 10; i++);')
        self._stmt_round_trip('for (i = 0; i <= 5; i++) { }')
        self._stmt_round_trip('for (i = 0; i <= 5; i++);')

    def test_empty_for(self):
        self._stmt_round_trip('for (;;) { }')
        self._stmt_round_trip('for (;;) ;')
        self._stmt_round_trip('for (i = 1;;) { }')
        self._stmt_round_trip('for (; i < 10;) { }')
        self._stmt_round_trip('for (;; i++) { }')

    def test_multi_init(self):
        self._stmt_round_trip('for (int i = 0, j = 0; i < 10; i++) { }')
        self._stmt_round_trip('for (i = 0, j = 0; i < 10; i++);')

    def test_multi_update(self):
        self._stmt_round_trip('for (int i = 0; i < 10; i++, j++) { }')
        self._stmt_round_trip('for (i = 0; i < 10; i++, j++);')

    def test_block(self):
        code = 'for (int i = 0; i < 10; ++i) { int j = 2 * i; sum += j; }'
        self._stmt_round_trip(code)

    def test_nested_for(self):
        code = 'for (i = 0; i < 10; ++i) { for (int j = 0; j < 10; ++j) { k = i * j; }}'
        self._stmt_round_trip(code)

        code = 'for (i = 0; i < 10; ++i) for (int j = 0; j < 10; ++j) k = i * j;'
        self._stmt_round_trip(code)

    def test_for_while(self):
        code = 'for (int i = 0; i < 10; ++i) { while (j < 2 * i) { j = 2 * j; } }'
        self._stmt_round_trip(code)


class TestJavaWhileStmt(JavaSnippetTestBase):

    def test_simple_while(self):
        self._stmt_round_trip('while (i < 10) { }')
        self._stmt_round_trip('while (i < 10);')

    def test_empty_while(self):
        self._stmt_round_trip('while (true) { }')
        self._stmt_round_trip('while (true);')

    def test_block(self):
        code = 'while (i < 10) { int j = 2 * i; sum += j; i++; }'
        self._stmt_round_trip(code)

    def test_nested_while(self):
        code = 'while (i < 10) { while (j < 10) { k = i * j; } }'
        self._stmt_round_trip(code)

        code = 'while (i < 10) while (j < 10) k = i * j;'
        self._stmt_round_trip(code)

    def test_while_for(self):
        code = 'while (true) { for (int i = 0; i < 10; ++i) { j = i * 2; } }'
        self._stmt_round_trip(code)


class TestJavaAssertStmt(JavaSnippetTestBase):

    def test_assert(self):
        self._stmt_round_trip('assert true;')
        self._stmt_round_trip('assert true : "message";')
        self._stmt_round_trip('assert true : message;')
        self._stmt_round_trip('assert value : "message" + value;')


class TestJavaBreakContinue(JavaSnippetTestBase):

    def test_break(self):
        self._stmt_round_trip('while (true) { break; }')
        self._stmt_round_trip('while (true) break label;')

    def test_continue(self):
        self._stmt_round_trip('while (true) { continue; }')
        self._stmt_round_trip('while (true) continue label;')


class TestJavaDoWhileStmt(JavaSnippetTestBase):

    def test_do_while(self):
        self._stmt_round_trip('do { something(); } while (true);')
        self._stmt_round_trip('do { something(); other.things(); } while (i < 10);')


class TestJavaEnhancedForStmt(JavaSnippetTestBase):

    def test_for_in(self):
        self._stmt_round_trip('for (int i : array) { doSomethingWith(i); }')
        self._stmt_round_trip('for (int i : array) doSomethingWith(i);')

        self._stmt_round_trip(
            'for (MyClass obj : objects.getObjs()) { doSomethingWith(obj); }')


class TestJavaIfStmt(JavaSnippetTestBase):

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


class TestJavaLabeledStmt(JavaSnippetTestBase):

    def test_labeled(self):
        self._stmt_round_trip('label: while (true) { break label; }')


class TestJavaReturnStmt(JavaSnippetTestBase):

    def test_return(self):
        self._stmt_round_trip('if (true) return;')
        self._stmt_round_trip('if (true) return 1;')
        self._stmt_round_trip('if (true) return actuallyFalse;')


class TestJavaSwitchStmt(JavaSnippetTestBase):

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


if __name__ == '__main__':
    unittest.main()
