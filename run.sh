#!/bin/bash
# Entry point Azure runs for the WebJob (Linux App Service)
cd "$(dirname "$0")"
export PYTHONPATH="$PWD/.python_packages:$PYTHONPATH"
python3 run.py
