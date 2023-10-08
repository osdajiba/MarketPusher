#!/bin/bash
echo "start to initialize the terminal"
# 设置终端大小和颜色
tput cols 80
tput lines 30
tput setaf 2  # 设置文字颜色为绿色
echo "getTickMode"

# 用户界面菜单
while true; do
  clear
  sudo pkill -9 python
  echo "-------------------------------------------------------"
  echo "        Enter the following character to run"
  echo "-------------------------------------------------------"
  echo
  echo "0. Initialize, download requirements list. (Run this for the first time loading)"
  echo
  echo "1. Start the program, press enter to stop the program."
  echo -e "\033[31m--Notice: press Enter will shut down the running programmes!\033[0m"
  tput setaf 2  # 设置文字颜色为绿色
  echo
  echo "2. Adjust the json file. (after modifying the code, run 1 again)"
  echo
  echo "Q. Quit."
  echo
  # shellcheck disable=SC2162
  read -p "Please enter a character: " choice
  echo

  case "$choice" in
    0)
      # 初始化
      cd ..
      cd main || exit
      pip install -r requirements.txt
      echo "requirements have installed."
      python3 creat_config.py
      echo "config.json has created."
      cd ..
      cd scripts || exit
      # shellcheck disable=SC2162
      read -p "Press Enter to continue..."
      ;;
    1)
      # 启动程序
      cd ..
      cd main || exit
      python3 server_side.py &
      sleep 4
      python3 client_side.py &
      echo "Program has started."
      cd ..
      cd scripts || exit
      # shellcheck disable=SC2162
      read -p "Press Enter to continue..."
      ;;
    2)
      # 调整json文件
      cd ..
      cd main || exit
      vi config.json
      echo "Json has opened."
      cd ..
      cd scripts || exit
      # shellcheck disable=SC2162
      read -p "Press Enter to continue..."
      ;;
    [Qq])
      # 退出
      echo "Exiting the program."
      exit 0
      ;;
    *)
      # 未识别的字符
      echo "Unrecognized character, please re-enter the correct character!"
      # shellcheck disable=SC2162
      read -p "Press Enter to continue..."
      ;;
  esac
done

