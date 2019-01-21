#!/bin/bash
python setup.py install --record files.txt
cat files.txt | xargs rm -rf
rm -rf build
rm -rf dist
rm -rf pytorch.egg-info
rm -rf files.txt
