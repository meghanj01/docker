import json
from dataclasses import dataclass, field
from fastapi import  FastAPI, HTTPException, Response

app = FastAPI()

@dataclass
class Channel:
    id:str
    name:str
    tags:list[str] = field(default_factory = list)
    description : str = ''

Channels: dict[str, Channel] = {}

with open("channel.json", encoding= 'utf-8') as file:
    channels_raw = json.load(file)
    for channel_raw in channels_raw:
        channel = Channel(**channel_raw)
        Channels[channel.id] = channel

@app.get('/')
def read_root() -> Response:
    return Response('This server is running')

@app.get("/channels/{channel_id}", response_model = Channel)
def read_item(channel_id:str) -> Channel:
    if channel_id not in Channels:
        raise HTTPException(status_code = 404, detail = "Channel not found")
    return Channels[channel_id]
