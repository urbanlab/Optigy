#!/bin/bash

echo "Demo start"
python model/main.py &
node server/index.js
