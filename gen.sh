#!/bin/bash

# generate
echo "[Unit]
Description=vk2tgBot

[Service]
Type=simple
ExecStart=/usr/bin/python3 $PWD/vk2tg.py
Restart=always
RestartSec=10
RestartPreventExitStatus=100
User=$USER
WorkingDirectory=$PWD

[Install]
WantedBy=multi-user.target" > vk2tg.service

# apply
cp vk2tg.service /lib/systemd/system/vk2tg.service
systemctl daemon-reload
