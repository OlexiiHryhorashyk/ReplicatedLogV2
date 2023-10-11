import aiohttp
import asyncio
from aiohttp import web
from ast import literal_eval

messages_list = []
ports = [8080, 8090]  # local ports to link with same ports of other nodes in the network
# url = [f'http://localhost:{port}/' for port in ports] # for running without Docker locally
url = [f'http://node1:{ports[0]}', f'http://node2:{ports[1]}']  # for Docker containers


async def send_to_sub(url_address, msg):
    try:
        msg = {'message': msg}
        async with aiohttp.ClientSession() as session:
            async with session.post(url_address, json=msg) as response:
                print(f"POST request -> Message sent to {url.index(url_address) + 1} subsequent server - {msg['message']}")
    except aiohttp.ClientError:
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
    messages_list.append(msg_str)
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
    str_messages = ',\n'.join(str(msg) for msg in messages_list)
    print("GET handler -> Listing saved messages...")
    return web.Response(text=str_messages)


app = web.Application()
app.router.add_post('/', handle_post)
app.router.add_get('/', handle_get)

if __name__ == '__main__':
    print("Server started...")
    web.run_app(app, host='0.0.0.0', port=8000)
