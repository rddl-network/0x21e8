#!/bin/bash

sudo cp 0x21e8.service /etc/systemd/system
sudo systemctl daemon-reload
sudo systemctl enable 0x21e8.service
sudo systemctl start 0x21e8.service
