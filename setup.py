import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='signpdf2',
    version='1',
    scripts=['signpdf2'],
    author="Aseem Hegshetye",
    author_email="aseem.hegshetye@gmail.com",
    description="Python package to sign a pdf",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aseem-hegshetye/signpdf",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
