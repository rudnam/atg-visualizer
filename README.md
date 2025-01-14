# atg-visualizer

Web-based visualization tool for adjacent transposition graphs (ATGs) and associated poset covers

## Setup

1. Set up backend

   ```shell
   ./backend
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   python3 main.py
   ```

2. Set up frontend

   Open up a separate terminal and then:

   ```shell
   ./frontend
   npm install
   npm run dev
   ```
