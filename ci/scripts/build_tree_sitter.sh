# create a directory to store sources
mkdir tree-sitter
cd tree-sitter

# currently only certain versions of tree-sitter are supported
git clone https://github.com/tree-sitter/tree-sitter-java.git
cd tree-sitter-java
git checkout 6c8329e2da78fae78e87c3c6f5788a2b005a4afc
cd ..

git clone https://github.com/tree-sitter/tree-sitter-cpp.git
cd tree-sitter-cpp
git checkout 0e7b7a02b6074859b51c1973eb6a8275b3315b1d
cd ..

git clone https://github.com/tree-sitter/tree-sitter-javascript.git
cd tree-sitter-javascript
git checkout f772967f7b7bc7c28f845be2420a38472b16a8ee
cd ..

# return to base directory
cd ..

# build!
python build_tree_sitter.py tree-sitter
