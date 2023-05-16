# MutableTree

> A mutable AST for source code transformation with Python

## TODO

- CI/CD
- Perhaps a Python package
- Function-level support for Java and perhaps C/C++
- Refactor transformation visitors

## Getting Started

### Setting up the environment

Current implementation requires [tree sitter](https://tree-sitter.github.io/) to convert source code to ASTs. ~~because the author is too weak to write a parser.~~

```sh
pip install tree-sitter
```

After installing the `tree_sitter` package, clone and build parsers for programming languages.

```sh
# create a directory to store sources
mkdir tree-sitter
cd tree-sitter

# currently only Java is supported
git clone https://github.com/tree-sitter/tree-sitter-java.git

# return to base directory
cd ..
```

Then build the parsers with

```sh
python build_tree_sitter.py
```

### Running the tests

We have unittests that are unfortunately incomplete and unsound.

Test files can be found in `./test`. To run all tests,

```sh
python run_all_tests.py
```

To run a single test,

```sh
# python -m unittest tests.test_module.test_class
python -m unittest tests.test_java_expr.TestJavaCallExpr
```

Expect outputs like `AssertionError: True is not false` ~~(no you dont~~

### Using mutable trees

```python
from tree_sitter import Parser, Language
from mutable_tree.adaptor import JavaAdaptor

# the only transformation visitor available ><💦
from tree_manip.transforms import ForToWhileVisitor

code = """
for (int i = 0; i < 100; ++i) {
    for (int j; j < 100; ++j) {
        int k = i + j;
        System.out.println(k);
    }
}
"""

# parse code with tree_sitter
parser = Parser()
parser.set_language(Language('./parser/languages.so', 'java'))
tree = parser.parse(code.encode())

# convert to mutable tree with adaptors
# NOTE: functionality is extremely limited for now
mutable_root = JavaAdaptor.convert_program(tree.root_node)

# transforming all for-loops to while-loops
visitor = ForToWhileVisitor()
new_root = visitor.visit(mutable_root)

# convert trees back to source code
# NOTE: does not support indentations
new_code = new_root.to_string()
print(new_code)
```
