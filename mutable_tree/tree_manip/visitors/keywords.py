JAVA_KEYWORDS = [
    'abstract', 'assert', 'boolean', 'break', 'byte', 'case', 'catch', 'char', 'class',
    'const', 'continue', 'default', 'do', 'double', 'else', 'enum', 'extends', 'final',
    'finally', 'float', 'for', 'goto', 'if', 'implements', 'import', 'instanceof', 'int',
    'interface', 'long', 'native', 'new', 'package', 'private', 'protected', 'public',
    'return', 'short', 'static', 'strictfp', 'super', 'switch', 'synchronized', 'this',
    'throw', 'throws', 'transient', 'try', 'void', 'volatile', 'while', 'sealed'
]

C_KEYWORDS = [
    'auto', 'break', 'bool', 'case', 'char', 'const', 'continue', 'class', 'default',
    'do', 'double', 'else', 'enum', 'extern', 'if', 'elif', 'else', 'endif', 'ifdef',
    'ifndef', 'define', 'undef', 'include', 'line', 'error', 'pragma', 'defined',
    '__has_c_attribute', 'float', 'for', 'goto', 'if', 'inline', 'int', 'long',
    'register', 'restrict', 'return', 'short', 'signed', 'sizeof', 'static', 'struct',
    'switch', 'typedef', 'union', 'unsigned', 'using', 'void', 'volatile', 'while',
    '_Alignas', '_Alignof', '_Atomic', '_Bool', '_Complex', '_Decimal128', '_Decimal32',
    '_Decimal64', '_Generic', '_Imaginary', '_Noreturn', '_Static_assert', '_Thread_local'
]

ALL_KEYWORDS_SET = set(JAVA_KEYWORDS + C_KEYWORDS)
