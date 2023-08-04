#!/bin/bash
# 杀死之前正在运行的 app.py
pkill -f app.py

# 等待一会儿，让进程有足够的时间关闭
sleep 2

# 启动新的app.py在后台
nohup python app.py > output.log 2>&1 &
