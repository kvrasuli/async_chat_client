import asyncio
import aiofiles
import datetime
import configargparse
from dotenv import load_dotenv
import logging
from contextlib import asynccontextmanager

logger = logging.getLogger(__file__)


@asynccontextmanager
async def open_socket(host, port): 
    try:
        reader, writer = await asyncio.open_connection(host, port)
        yield reader, writer
    except ConnectionError:
        logger.error('Reading error!')
        await asyncio.sleep(10)
    finally:
        writer.close()
        await writer.wait_closed()


async def get_messages_from_chat(host, port, path):
    async with open_socket(host, port) as stream:
        while True:
            reader, _ = stream[0], stream[1]
            chat_line = await reader.readline()
            timestamp = datetime.datetime.now().strftime('%d.%m.%y %H:%M:%S')
            chat_line_with_timestamp = f'[{timestamp}] {chat_line.decode()}'
            print(chat_line_with_timestamp, end='')
            async with aiofiles.open(path, 'a', encoding='utf-8') as file:
                await file.write(chat_line_with_timestamp)


def parse_args():
    load_dotenv()
    parser = configargparse.ArgParser()
    parser.add('--host', help='address of host', env_var='CHAT_HOST')
    parser.add('--port', help='number of port', env_var='CHAT_PORT_TO_READ')
    parser.add(
        '--path', help='path to chat history file',
        env_var='CHAT_HISTORY_FILE_PATH'
    )
    return parser.parse_args()


if __name__ == '__main__':
    logging.basicConfig(
        format="%(levelname)s reader: %(message)s",
        level=logging.DEBUG
    )
    args = parse_args()
    asyncio.run(get_messages_from_chat(args.host, args.port, args.path))
