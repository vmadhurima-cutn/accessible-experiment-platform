#!/bin/bash

source $(conda info --base)/etc/profile.d/conda.sh

conda activate accessible_lab

export QT_QPA_PLATFORM_PLUGIN_PATH=$CONDA_PREFIX/lib/python3.11/site-packages/PyQt6/Qt6/plugins/platforms

python main.py