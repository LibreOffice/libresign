#! /bin/bash
# build and publish project on pypi.org

rm dist/*
python3 setup.py sdist bdist_wheel
python3 -m twine upload dist/*

