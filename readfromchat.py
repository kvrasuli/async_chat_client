import asyncio
import aiofiles
import datetime
import configargparse
from dotenv import load_dotenv


async def get_messages_from_chat(host, port, path):
    reader, _ = await asyncio.open_connection(host, port)
    while True:
        chat_line = await reader.readline()
        timestamp = datetime.datetime.now().strftime('%d.%m.%y %H:%M:%S')
        async with aiofiles.open(path, 'a') as file:
            await file.write(f'[{timestamp}] {chat_line.decode()}')


def parse_args():
    load_dotenv()
    parser = configargparse.ArgParser()
    parser.add('--host', help='address of host', env_var='CHAT_HOST')
    parser.add('--port', help='number of port', env_var='CHAT_PORT')
    parser.add(
        '--path', help='path to chat history file',
        env_var='CHAT_HISTORY_FILE_PATH'
    )
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    asyncio.run(get_messages_from_chat(args.host, args.port, args.path))
