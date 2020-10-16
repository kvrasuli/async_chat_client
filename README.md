# Async chat client

These are console scripts for connecting to a Minecraft fan chat. 

### How to run
- Install requirements
```
pip3 install -r requirements.txt
```
#### To read from chat
- Create 3 environment variables:
    ```
    CHAT_HOST='address of chat host'
    CHAT_PORT_TO_READ='number of port to read'
    CHAT_HISTORY_FILE_PATH='path to chat history file'
    ```
- OR it is possible to set the same settings using command line arguments:
    ```
    --host [address of chat host]
    --port [number of port]
    --path [path to chat history file]
    ```
- Run the python script:
    ```
    python3 readfromchat.py [optional arguments]
    ```
#### To write to chat
- Create 3 environment variables:
    ```
    CHAT_HOST='address of chat host'
    CHAT_PORT_TO_WRITE='number of port to write'
    ```
    If you already have a token, set
    ```
    CHAT_TOKEN='your personal token'
    ```
    If you don't, set your preferred nickname:
    ```
    CHAT_NICKNAME='Vasyan'
    ```
- OR it is possible to set the same settings using command line arguments:
    ```
    --host [address of chat host]
    --port [number of port]
    --token [your personal token]
    --nickname [your preferred nickname]
    ```
    To enter message you want to send use this required command line argument:
    ```
    -m [message]
    --message [message]
    ```
    To enable logs use:
    ```
    --log
    ```
- Run the python script:
    ```
    python3 writetochat.py [optional arguments] -m [message]
    ```
