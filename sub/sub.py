import os
from aiohttp import web
import asyncio
from ast import literal_eval

messages_list = {}
latency = int(os.getenv('LATENCY', 0))


async def handle_post(request):
    content = await request.content.read()
    msg = literal_eval(content.decode('utf-8'))
    print("POST handler <- Message received:", msg['message'])
    await asyncio.sleep(latency)
    if msg['index'] in messages_list.keys():  # Message deduplication by preventing saving copies of the same message
        print("POST handler ERROR <- Message", msg['message'], "already saved!")
        return web.Response(status=400, text='Deduplication. Message already saved.')
    messages_list.update({msg['index']: msg['message']})
    message = "Message received:" + str(msg['message'])
    return web.Response(text=message)


async def handle_get(request):
    str_messages = ',\n'.join(str(msg) for msg in messages_list.values())
    print("GET handler -> Listing saved messages...")
    return web.Response(text=str_messages)


app = web.Application()
app.router.add_post('/', handle_post)
app.router.add_get('/', handle_get)

if __name__ == '__main__':
    print("Server started...")
    web.run_app(app, host='0.0.0.0', port=8080)
