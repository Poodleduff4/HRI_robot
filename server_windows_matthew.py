import json
import socket
import keyboard

ADDR_A = ('192.168.0.173', 9999)
ADDR_B = ('192.168.0.165', 9999)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(ADDR_A)

data=''

def callback(e:keyboard.KeyboardEvent):
    c = e.scan_code
    print(c)
    # l = ''
    # match c:
    #     case 1:
    #         l='s'
    #     case 2:
    #         l='d'
    #     case 3:
    #         l='f'
    #     case 14:
    #         l='e'
    #     case _:
    #         l='None'
    # print(l)
    data=c

def get_pressed_keys():
    w = keyboard.is_pressed(17)
    a = keyboard.is_pressed(30)
    s = keyboard.is_pressed(31)
    d = keyboard.is_pressed(32)
    boost = keyboard.is_pressed(20)
    return map(lambda x:int(x), [w,a,s,d,boost])
    

while True:
    #continuously send and receive info to program B until some breaking condition reached
    # print("A sending...")
    data=''
    # keyboard.hook(callback=callback, suppress=False)
    keys = list(get_pressed_keys())
    
    # print(keys)
    # Note: this will be silently dropped if the client is not up and running yet
    # And even if the the client is running, it may still be silently dropped since UDP is unreliable.
    sock.sendto(json.dumps(''.join(map(str,keys))).encode("utf-8"), ADDR_B)
    print("A receiving...")
    recv_data = sock.recv(1024)
    print(recv_data.decode('utf-8'))

    # print(f"A received {recv_data}")
