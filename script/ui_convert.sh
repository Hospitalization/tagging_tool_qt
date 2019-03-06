#!/usr/bin/env bash
# Remove all .py in ../ui and convert all .ui to .py
cd ../ui
rm ui_*.py
for entry in *.ui
do
  echo "$entry"
  entry_=(${entry//./ })
  echo "ui_${entry_}.py"
  /home/heim/.conda/envs/tf/bin/pyuic5 "$entry" -o "ui_${entry_}.py"
done
