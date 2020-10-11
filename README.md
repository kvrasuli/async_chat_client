# Async chat client

### How to run
- Install requirements
```
pip3 install -r requirements.txt
```
- Create 3 environment variables:
```
CHAT_HOST='address of chat host'
CHAT_PORT='number of port'
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
