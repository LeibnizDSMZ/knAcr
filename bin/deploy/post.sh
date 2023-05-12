#!/bin/bash

PYT="$(pwd)/.venv/bin"

echo "installing python-radon"
if "$PYT"/python -m pip install "radon>=5.1,<6"; then
    echo "radon successfully installed"
else
    echo "radon already installed"
fi

if ln -s "$PYT"/radon "/usr/bin/radon"; then
    echo "link created"
fi
