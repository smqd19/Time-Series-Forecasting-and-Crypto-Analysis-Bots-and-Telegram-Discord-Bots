import websocket #pip install websocket-client
import json
import threading
import time
import requests
def send_json_request(ws, request):
    ws.send(json.dumps(request))

def recieve_json_response(ws):
    response = ws.recv()
    if response:
        return json.loads(response)

def heartbeat(interval, ws):
    print('Heartbeat begin')
    while True:
        time.sleep(interval)
        heartbeatJSON = {
            "op": 1,
            "d": "null"
        }
        send_json_request(ws, heartbeatJSON)
        print("")

ws = websocket.WebSocket()
ws.connect('wss://gateway.discord.gg/?v=6&encording=json')   
event = recieve_json_response(ws)

heartbeat_interval = event['d']['heartbeat_interval'] / 1000
threading._start_new_thread(heartbeat, (heartbeat_interval, ws))

token = "NzIzODM5Mjc0NDI4MTM3NTQ0.YW2Z-A.xez4qSJHKA5Y6kYH5nIiwexyH2o" # should not be change belongs to Ahmed account with walsh wealth subscription
payload = {
    'op': 2,
    "d": {
        "token": token,
        "properties": {
            "$os": "windows",
            "$browser": "chrome",
            "$device": 'pc'
        }
    }
}
send_json_request(ws, payload)





def send_msg(msg,user,flag): # message sending part  ONLY PART THAT SHOULD BE CHANGED
    msg=user+":"+msg
    if flag==1:
      msg="This is from trades channel \n" + msg
    elif flag==2:
      msg="This is from active futures chanell \n" + msg
    payload={
    'content':msg
        }
    header={
        'authorization':"NzIzODM5Mjc0NDI4MTM3NTQ0.YW2Z-A.xez4qSJHKA5Y6kYH5nIiwexyH2o"
    }
    r=requests.post('https://discord.com/api/v8/channels/723839467202281515/messages',data=payload,headers=header)




def event_handler(event): # Should not chnage it message retrieving part 
  flag=0
  if(event['d']['channel_id']=='890962441926758420'):
    user1=event['d']['author']['username']
    msg=event['d']['content']
    print(f"{user1} {msg}")
    flag=1
    if len(event['d']['attachments'])!=0:
      msg=msg+ " \n img:" + event['d']['attachments'][0]['url']
    send_msg(msg,user1,flag)
  elif(event['d']['channel_id']=='777712667094810624'):
    user1=event['d']['author']['username']
    msg=event['d']['content']
    print(f"{user1} {msg}")
    flag=2
    if len(event['d']['attachments'])!=0:
        msg=msg+ " \n img:" + event['d']['attachments'][0]['url']
    send_msg(msg,user1,flag)

def send_img(event):
  
    print(event['d']['attachments'][0]['url'])
    send_msg(event['d']['attachments'][0]['url'],event['d']['author']['username'])

# Main 
  
while True:
    flag=0
    event = recieve_json_response(ws)  
    try:
        event_handler(event)
        op_code = event['op']
        if op_code == 11:
            print('')
    except:
        pass