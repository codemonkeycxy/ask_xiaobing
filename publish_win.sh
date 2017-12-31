#!/bin/bash

# set up virtual environment
pip install virtualenv
rm -rf ./env
virtualenv env
. ./env/Scripts/activate

# install dependencies
pip install https://github.com/pyinstaller/pyinstaller/archive/develop.zip
pip install itchat

# clean rebuild
rm -rf ./build
rm ask_xiaobing.spec ./dist/ask_xiaobing ./dist/ask_xiaobing_win-64.exe
pyinstaller -F ./ask_xiaobing.py
mv ./dist/ask_xiaobing.exe ./dist/ask_xiaobing_win-64.exe
deactivate

# push to master
git add ./dist/ask_xiaobing_win-64.exe
git commit -m "rebuild windows executable"
git push
