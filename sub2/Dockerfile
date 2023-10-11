FROM python:3.11-slim-bullseye
EXPOSE 8090
RUN apt-get update && pip install --upgrade pip
RUN pip install aiohttp==3.8.6
ADD sub2.py ./
CMD ["python", "-u", "./sub2.py"]