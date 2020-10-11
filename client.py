import asyncio
import aiofiles
import datetime


async def tcp_echo_client():
    reader, writer = await asyncio.open_connection(
        'minechat.dvmn.org', 5000
    )
    while True:
        chat_line = await reader.readline()
        timestamp = datetime.datetime.now().strftime('%d.%m.%y %H:%M:%S')
        async with aiofiles.open('chathistory.txt', 'a') as file:
            await file.write(f'[{timestamp}] {chat_line.decode()}')


asyncio.run(tcp_echo_client())
