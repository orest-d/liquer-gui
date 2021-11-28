#!/bin/bash

npm run build

mkdir liquer-gui/liquer_gui/assets
cp -R dist/liquer/web/gui/* liquer-gui/liquer_gui/assets
cp README.md liquer-gui/README.md

cd liquer-gui
python setup.py sdist bdist_wheel
cd ..
