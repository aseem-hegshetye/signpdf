pip install twine pathlib wheel
python setup.py sdist bdist_wheel
twine upload dist/*
pip uninstall twine pathlib wheel