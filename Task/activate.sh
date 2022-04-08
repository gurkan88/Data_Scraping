#!/bin/bash
python -m venv project_env
source ./project_env/Scripts/activate
pip install -r requirements.txt
python main.py
$SHELL