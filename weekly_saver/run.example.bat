@echo off

REM cd to the project directory
cd path-to-weekly-saver

REM activate venv
CALL venv\Scripts\activate.bat

REM run weekly_saver
python weekly_saver\weekly_saver.py

REM deactivate venv
CALL deactivate