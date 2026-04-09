#!/bin/bash
echo "Starting Dish-Chat services..."
~/dish-chat/start-backend.sh
sleep 3
~/dish-chat/start-frontend.sh
echo ""
echo "Services starting..."
echo "Backend:  http://192.168.0.164:8000"
echo "Frontend: http://192.168.0.164:3000 (chats)"
echo "          http://192.168.0.164:3001 (beta-reports)"
