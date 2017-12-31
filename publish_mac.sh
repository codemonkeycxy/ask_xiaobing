#!/bin/bash

# set up virtual environment
pip install virtualenv
rm -rf ./env
virtualenv env
. ./env/bin/activate

# install dependencies
pip install https://github.com/pyinstaller/pyinstaller/archive/develop.zip
pip install itchat

# clean rebuild
rm -rf ./build
rm ask_xiaobing.spec ./dist/ask_xiaobing ./dist/ask_xiaobing_mac.zip
pyinstaller -F ./ask_xiaobing.py
zip ./dist/ask_xiaobing_mac.zip ./dist/ask_xiaobing
deactivate

# push to master
git add ./dist/ask_xiaobing_mac.zip
git commit -m "rebuild mac executable"
git push
