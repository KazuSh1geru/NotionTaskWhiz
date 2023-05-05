#!/bin/bash
pip install -r requirements.txt
pip install black && black ./src/*.py ./local/*.py
# pip install pytest && pytest .
pip install "flake8==6.0.0" && flake8 ./local/*.py
