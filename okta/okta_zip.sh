#!/bin/zsh
mkdir -p package
pip3 install --target ./package requests
cd package
zip -r9 ${OLDPWD}/function.zip .
cd $OLDPWD
zip -g function.zip okta.py
