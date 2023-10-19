##simple chat service with basic functionality


for start
```
docker build . -t chat-app
docker run --rm -it  -p 8001:8001/tcp chat-app:latest
```

or

```
uvicorn main:app --host 0.0.0.0 --port 8001  --reload
```