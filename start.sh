cd frontend/
live-server --port=8000 &
cd ..
python main.py
trap "killall node" EXIT