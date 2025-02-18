# atg-visualizer

Web-based visualization tool for adjacent transposition graphs (ATGs) and associated poset covers

## Setup

1. Install dependencies

   ```shell
   cd ./backend
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   cd ../frontend
   npm install
   cd ../
   ```

2. Run backend

   Note: Make sure that the environment is activated (`source .venv/bin/activate`)

   ```shell
   cd ./backend
   fastapi run
   ```

3. Run frontend

   Open up another terminal and then:

   ```shell
   cd ./frontend
   npm run dev
   ```
