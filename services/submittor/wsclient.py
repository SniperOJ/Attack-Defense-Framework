import json
import websocket

host = "127.0.0.1"
port = 8000
path = "ws/flag/"
ssl = False
endpoint = "ws://%s:%d/%s" % (host, port, path)
token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTM3NTE1NTg0LCJqdGkiOiIyNzJlNDBkMzRjYjQ0MmFmYjFmNDVjYjZiZjM3MWI2YSIsInVzZXJfaWQiOjF9.kyc7VCgphJQUcmjmp4WTFNDNuuhI6GNLCosAc1Anv5w"

AUTH_MESSAGE = 0
FLAG_MESSAGE = 1

def auth(conn):
    message = json.dumps({
        "type":AUTH_MESSAGE,
        "data":token,
    })
    print("Sending auth message: %s" % message)
    conn.send(message)
    print("Auth message sent")
    data = conn.recv()
    print(data)
    response = json.loads(data)
    print("Got auth response: %s" % response)
    if response['data']['status']:
        return True
    return False

ws = websocket.create_connection(endpoint)
print("Connected")
if not auth(ws):
    print("Auth failed")
    exit(-1)
print("Auth succeed")
while True:
    print("Starting message loop")
    message = json.loads(ws.recv())
    print("Message received: %s" % (message))
    message_type = message['type']
    message_data = message['data']
    if message_type == FLAG_MESSAGE:
        print(message_data)

ws.close()
