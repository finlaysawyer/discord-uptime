import json

with open('servers.json') as f:
    servers = json.load(f)

with open('config.json') as f:
    config = json.load(f)
