echo Build Source Distribution
python setup.py sdist

echo Build universal package (--universal defaulted on setup.cfg)
python setup.py bdist_wheel