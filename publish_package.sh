pip install twine pathlib wheel bumpversion

# use current version below
bumpversion --current-version 3.0.0 major setup.py signpdf2/__init__.py

# empty build folder
rm -rf ./build

# create build package to deploy
python setup.py sdist bdist_wheel

# deploy
twine upload dist/*

pip uninstall twine pathlib wheel bumpversion -y