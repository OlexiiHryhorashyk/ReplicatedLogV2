FROM python:3.11-slim-bullseye
EXPOSE 8000
RUN apt-get update && pip install --upgrade pip
RUN pip install requests==2.31.0
RUN pip install aiohttp==3.8.6
RUN pip install asyncio==3.4.3
ADD master.py ./
CMD ["python", "-u", "./master.py"]