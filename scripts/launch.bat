@echo off
echo start to initialize the terminal
:: 设置终端大小和颜色
mode con cols=80 lines=30
color 2  :: 设置文字颜色为绿色
echo getTickMode

:menu
cls
taskkill /F /IM python.exe /T 2>nul
echo -------------------------------------------------------
echo         Enter the following character to run
echo -------------------------------------------------------
echo.
echo 0. Initialize, download requirements list. (Run this for the first time loading)
echo.
echo 1. Start the program, press Enter to stop the program.
echo --Notice: press Enter will shut down the running programs!--
color 2  :: 设置文字颜色为绿色
echo.
echo 2. Adjust the json file. (after modifying the code, run 1 again)
echo.
echo Q. Quit.
echo.

set /p "choice=Please enter a character: "

if "%choice%"=="0" (
    :: 初始化
    cd ..
    cd main || exit /b
    pip install -r requirements.txt
    echo requirements have installed.
    python creat_config.py
    echo config.json has created.
    cd ..
    cd scripts || exit /b
    pause
) else if "%choice%"=="1" (
    :: 启动程序
    cd ..
    cd main || exit /b
    start python server_side.py
    timeout /t 4 /nobreak
    start python client_side.py
    echo Program has started.
    cd ..
    cd scripts || exit /b
    pause
) else if "%choice%"=="2" (
    :: 调整json文件
    cd ..
    cd main || exit /b
    notepad config.json
    echo Json has opened.
    cd ..
    cd scripts || exit /b
    pause
) else if /i "%choice%"=="Q" (
    :: 退出
    echo Exiting the program.
    exit /b 0
) else (
    :: 未识别的字符
    echo Unrecognized character, please re-enter the correct character!
    pause
)
goto menu
