## Project dedicated to understand Distributed Computing with Redis

### Usage:
  1. Fill All .env.
  2. Run the `pip install -r requirements. txt` command.
  3. Run the `docker compose up` command.
  4. Start the Main app to Generate some messages. <br>
      *In the App directory*
      ```
        python main.py
      ```
  5. Start as many workers you want to listen and wait for messages.<br>
      *In the Worker directory*
      ```
        python worker.py
      ```

---

Credits: [MathByte Academy](https://www.youtube.com/watch?v=XCSARhkRg7g)

