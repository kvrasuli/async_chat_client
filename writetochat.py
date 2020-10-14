import asyncio
import configargparse
from dotenv import load_dotenv
import logging
import json

logger = logging.getLogger(__file__)


async def write_message_to_chat(host, port, token, message, nickname):
    if token:
        reader, writer = await authorize(host, port, token)
    else:
        token = await register(host, port, nickname)
        reader, writer = await authorize(host, port, token)
    await submit_message(reader, writer, message)


async def register(host, port, nickname):
    reader, writer = await asyncio.open_connection(host, port)
    answer = await reader.readline()
    logger.debug(answer.decode())
    writer.write('\n'.encode())
    logger.debug('Registering a new token...')
    answer = await reader.readline()
    logger.debug(answer.decode())
    nickname = nickname.replace('\n', '')
    writer.write(f'{nickname}\n'.encode())
    answer = await reader.readline()
    logger.debug(answer.decode())
    decoded_answer = json.loads(answer.decode())
    writer.close()
    return decoded_answer['account_hash']


async def authorize(host, port, token):
    reader, writer = await asyncio.open_connection(host, port)
    answer = await reader.readline()
    logger.debug(answer.decode())
    writer.write(f'{token}\n'.encode())
    logger.debug(f'{token} has been sent!')
    answer = await reader.readline()
    logger.debug(answer.decode())
    decoded_answer = json.loads(answer.decode())
    if not decoded_answer:
        logger.debug('The token isn\'t valid, check it or register again.')
        return
    return reader, writer


async def submit_message(reader, writer, message):
    answer = await reader.readline()
    logger.debug(answer.decode())
    message = message.replace('\n', '')
    writer.write(f'{message}\n\n'.encode())
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
    return parser.parse_args()


if __name__ == '__main__':
    logging.basicConfig(format="%(levelname)s sender: %(message)s")
    logger.setLevel(logging.DEBUG)
    args = parse_args()
    asyncio.run(
        write_message_to_chat(args.host, args.port, args.token, args.message, args.nickname)
    )
