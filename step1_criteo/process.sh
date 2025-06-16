#!/bin/bash

PYTHON_SCRIPT="/data3/ieug22/ly322/summer_research/step1_criteo/step1.py"  # 替换为您的脚本名
INPUT_FILE="/data3/ieug22/ly322/summer_research/criteo_dataset/day_2.txt"       # 替换为输入数据文件

for i in {1..26}; do
    echo "Processing feature C$i..."
    python3 "$PYTHON_SCRIPT" "$INPUT_FILE" --features "$i" --output "/data3/ieug22/ly322/summer_research/step1_criteo/day2/criteo_C${i}.csv"
    echo "---------------------------"
done

echo "All features processed!"
