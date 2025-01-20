# atg-visualizer

Web-based visualization tool for adjacent transposition graphs (ATGs) and associated poset covers

## Setup

1. Set up backend

   ```shell
   cd ./backend
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   fastapi run
   ```

2. Set up frontend

   Open up a separate terminal and then:

   ```shell
   cd ./frontend
   npm install
   npm run dev
   ```
