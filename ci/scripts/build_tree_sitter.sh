# create a directory to store sources
mkdir tree-sitter
cd tree-sitter

# currently only Java is supported
git clone https://github.com/tree-sitter/tree-sitter-java.git
git clone https://github.com/tree-sitter/tree-sitter-cpp.git
git clone https://github.com/tree-sitter/tree-sitter-javascript.git

# return to base directory
cd ..

# build!
python build_tree_sitter.py tree-sitter
