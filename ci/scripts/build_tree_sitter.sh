# create a directory to store sources
mkdir tree-sitter
cd tree-sitter

# currently only Java is supported
git clone https://github.com/tree-sitter/tree-sitter-java.git

# return to base directory
cd ..

# build!
python build_tree_sitter.py
