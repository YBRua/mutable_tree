import os
import sys
from tree_sitter import Language


if len(sys.argv) != 2:
    raise ValueError('Usage: python build_treesitter_langs.py <path/to/lang-repos>')

lib_dir = sys.argv[1]
libs = [os.path.join(lib_dir, d) for d in os.listdir(lib_dir)]

Language.build_library(
    # Store the library in the `build` directory
    'parser/languages.so',
    libs,
)
