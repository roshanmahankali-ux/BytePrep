#!/bin/bash

echo "Starting the Flahcard App..."

#Backend Start Commands
cd backend
source venv/bin/activate
uvicorn app.main:app --reload &
BACKEND_PROCESS_ID=$!
echo "Backend started successfully!!...."
echo "Open browser http://localhost:8000"
echo "Open browser http://localhost:8000/docs for API documentation"
cd ..

#Frontend Start Commands - using vite for react deployment
cd frontend
npm run dev &
FRONTEND_PROCESS_ID=$!
echo "Frontend started successfully!!...."
echo "Open browser http://localhost:5173"
cd ..

#Kill both process using the process id captured from $!
echo "Press Keys CTLR +C to stop the application"
trap "echo 'shutting down....'; kill $BACKEND_PROCESS_ID $FRONTEND_PROCESS_ID; stty sane; exec </dev/tty; echo''" EXIT INT TERM

#keep script alive
wait

