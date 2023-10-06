@ECHO off
ECHO start to initialize the window
mode con cols=80 lines=30 & color 0a
TITLE getTickMode
rem ECHO window has initialized

:interface
Cls
ECHO ------------------------------------------
ECHO    Enter the following character to run
ECHO ------------------------------------------
ECHO.
ECHO 0. Initialize, download requirements list. (Run this for the first time loading)
ECHO.
ECHO 1. Start the program, press enter to stop the program.
ECHO.
ECHO 2. adjust the json file. (after modifying the code, run 1 again)
ECHO.
ECHO Q. quit.
ECHO.

:options
Set /p a=Please enter an character upon:
If "%a%"=="0" goto :initialize
If "%a%"=="1" goto :startProgram
If "%a%"=="2" goto :adjustJson
If /I "%a%"=="Q" goto :quit
ECHO Unrecognized character,  please re input the right character!
Pause
Goto :options

:initialize
pip install pipreqs
pipreqs
pip3 install -r requirements.txt
ECHO Requirements has been installed.
Pause
Goto :interface

:startProgram
cd ..
start python server_side.py
timeout /t 4
start python client_side.py
ECHO Program has started.
cd scripts
Pause
Goto :interface

:adjustJson
json-server --watch launch.json
start vscode launch.json
ECHO json has been modified.
Pause
Goto :interface

:quit exit
REM quit the program
