from aiohttp import web
from ast import literal_eval
import time

messages_list = []


async def handle_post(request):
    content = await request.content.read()
    msg = literal_eval(content.decode('utf-8'))
    print("POST handler <- Message received:", msg['message'])
    messages_list.append(msg['message'])
    message = "Message received:" + str(msg['message'])
    time.sleep(3)  # simulated latency 5 seconds
    return web.Response(text=message)


async def handle_get(request):
    str_messages = ',\n'.join(str(msg) for msg in messages_list)
    print("GET handler -> Listing saved messages...")
    return web.Response(text=str_messages)


app = web.Application()
app.router.add_post('/', handle_post)
app.router.add_get('/', handle_get)

if __name__ == '__main__':
    print("Server started...")
    web.run_app(app, host='0.0.0.0', port=8080)
