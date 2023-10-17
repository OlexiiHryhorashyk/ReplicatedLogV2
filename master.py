import os
import aiohttp
import asyncio
from aiohttp import web
from ast import literal_eval
NODE_NAMES = os.getenv('NODE_NAMES', 'node1 node2')
nodes = NODE_NAMES.split()
messages_list = {}
url = [f'http://{node}:8080' for node in nodes]  # for Docker containers
message_index = 0


async def send_to_sub(url_address, msg):
    global message_index
    try:
        msg = {
            'message': msg,
            'index': message_index
            }
        async with aiohttp.ClientSession() as session:
            async with session.post(url_address, json=msg) as response:
                print(f"POST request -> Message sent to {url.index(url_address) + 1} subsequent server - {msg['message']}")
        message_index += 1
    except aiohttp.ClientError as error:
        print(error)
        print(f"POST ERROR -> No connection to the {url.index(url_address) + 1} sub server! Message not passed!")


async def handle_post(request):
    content = await request.content.read()
    msg = literal_eval(content.decode('utf-8'))

    print("POST handler <- Message received:", msg)
    message = msg.get('message', '')
    msg_str = message
    if message.startswith("w="):
        w = int(message[2])
        msg_str = message[3:]
    else:
        w = len(url)+1
    messages_list.update({message_index: msg_str})  # Saving as a dictionary to mach the type on secondary
    tasks = [asyncio.create_task(send_to_sub(url_address, msg_str)) for url_address in url]
    print("w=", w)
    if w <= 1:
        for task in tasks:
            asyncio.ensure_future(task)
    if w == 2:
        await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
    if w > 2:
        await asyncio.wait(tasks, return_when=asyncio.ALL_COMPLETED)
    return web.Response(text=f"Message received: {msg_str}")


async def handle_get(request):
    str_messages = ',\n'.join(str(msg) for msg in messages_list.values())
    print("GET handler -> Listing saved messages...")
    return web.Response(text=str_messages)


app = web.Application()
app.router.add_post('/', handle_post)
app.router.add_get('/', handle_get)

if __name__ == '__main__':
    print("Server started...")
    web.run_app(app, host='0.0.0.0', port=8000)
