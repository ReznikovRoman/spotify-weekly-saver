#bin/bash

# activate venv
source /path/to/venv/bin/activate

# run python script
cd /path/to/weekly_saver || exit
python weekly_saver.py

# deactivate venv
deactivate