#!/usr/bin/env bash

mkdir -p build

cp -R ../src build/
pip install --target ./build -r ../requirements-lambda.txt

cd build
zip -r lambda-structured-logging.zip *
