import setuptools

long_description = """A mutable AST for source code manipulation with Python."""
__version__ = '0.0.1'


def packages():
    return setuptools.find_packages(exclude=['tests'])


setuptools.setup(
    name="mutable_tree",
    version=__version__,
    author="YBRua",
    author_email="ybybrua@outlook.com",
    description="A mutable AST for source code manipulation with Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/YBRua/mutable_tree",
    packages=packages(),
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['tree_sitter'],
    python_requires='~=3.8',
)
