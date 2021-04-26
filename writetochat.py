import asyncio
from asyncio.events import set_child_watcher
import configargparse
from dotenv import load_dotenv
import logging
import json
from contextlib import asynccontextmanager

logger = logging.getLogger(__file__)


@asynccontextmanager
async def open_socket(host, port):
    try:
        reader, writer = await asyncio.open_connection(host, port)
        answer = await reader.readline()
        logger.debug(answer.decode())
        yield reader, writer
    except ConnectionError:
        logger.error('Writing error!')
    finally:
        writer.close()
        await writer.wait_closed()


async def write_message_to_chat(host, port, token, message, nickname):
    async with open_socket(host, port) as stream:
        reader, writer = stream[0], stream[1]
        if token:
            error = await authorize(reader, writer, token)
        else:
            token = await register(reader, writer, nickname)
            error = await authorize(reader, writer, token)
        if not error:
            await submit_message(reader, writer, message)


async def register(reader, writer, nickname):  
    writer.write('\n'.encode())
    await writer.drain()
    logger.debug('Registering a new token...')
    answer = await reader.readline()
    logger.debug(answer.decode())
    nickname = nickname.replace('\n', '')
    writer.write(f'{nickname}\n'.encode())
    await writer.drain()
    answer = await reader.readline()
    logger.debug(answer.decode())
    decoded_answer = json.loads(answer.decode())
    return decoded_answer['account_hash']


async def authorize(reader, writer, token):
    writer.write(f'{token}\n'.encode())
    await writer.drain()
    logger.debug(f'{token} has been sent!')
    answer = await reader.readline()
    decoded_answer = answer.decode()
    logger.debug(f'{decoded_answer}')
    if decoded_answer.startswith('Welcome'):
        return False
    elif decoded_answer == 'null\n':
        logger.debug('The token isn\'t valid, check it or register again.')
        return True
    answer = await reader.readline()
    logger.debug(f'{answer.decode()}')
    return False

async def submit_message(reader, writer, message):
    message = message.replace('\n', '')
    writer.write(f'{message}\n\n'.encode())
    await writer.drain()
    logger.debug(f'Sending a message {message}...')
    answer = await reader.readline()
    logger.debug(answer.decode())


def parse_args():
    load_dotenv()
    parser = configargparse.ArgParser()
    parser.add('--host', help='address of host', env_var='CHAT_HOST')
    parser.add('--port', help='number of port', env_var='CHAT_PORT_TO_WRITE')
    parser.add('--token', help='chat token', env_var='CHAT_TOKEN')
    parser.add('--nickname', help='your nickname', env_var='CHAT_NICKNAME')
    parser.add('-m', '--message', help='message to send', required=True)
    parser.add('--log', help='enable logs', action='store_true')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    if args.log:
        logging.basicConfig(
            format="%(levelname)s sender: %(message)s",
            level=logging.DEBUG
        )
    asyncio.run(
        write_message_to_chat(args.host, args.port, args.token, args.message, args.nickname)
    )
