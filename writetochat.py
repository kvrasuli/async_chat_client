import asyncio
import configargparse
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__file__)


async def write_message_to_chat(host, port, token, message):
    global logger
    reader, writer = await asyncio.open_connection(host, port)
    answer = await reader.readline()
    logger.debug(answer.decode())
    writer.write(f'{token}\n'.encode())
    logger.debug(f'{token} has been sent!')
    answer = await reader.readline()
    logger.debug(answer.decode())
    answer = await reader.readline()
    logger.debug(answer.decode())
    writer.write(f'{message}\n\n'.encode())
    logger.debug(f'Sending a message {message}...')
    answer = await reader.readline()
    logger.debug(answer.decode())
    writer.close()


def parse_args():
    load_dotenv()
    parser = configargparse.ArgParser()
    parser.add('--host', help='address of host', env_var='CHAT_HOST')
    parser.add('--port', help='number of port', env_var='CHAT_PORT_TO_WRITE')
    parser.add('--token', help='chat token', env_var='CHAT_TOKEN')
    parser.add('-m', '--message', help='message to send', required=True)
    return parser.parse_args()


if __name__ == '__main__':
    logging.basicConfig(format="%(levelname)s sender: %(message)s")
    logger.setLevel(logging.DEBUG)
    args = parse_args()
    asyncio.run(
        write_message_to_chat(args.host, args.port, args.token, args.message)
    )
