#!/bin/zsh
cd ../package
zip -r9 ${OLDPWD}/function.zip .
cd $OLDPWD
zip -g function.zip sync_customer.py
