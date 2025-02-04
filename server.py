import json
import socket
import keyboard
import socket
import platform

# IP Adresses, last 3 digits
# Noah: 123
# Luke: 110
# Matthew: 173

# Get the host name, print it and then set ADDR_A based on the ip address
hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)

print("Your Computer Name is: " + hostname)
print("Your Computer IP Address is: " + IPAddr)

# Gets the current system
currentPlatform = platform.system()

print("Your Computer Platform is: " + currentPlatform)

ADDR_A = (IPAddr, 9999)
ADDR_B = ('192.168.0.165', 9999)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(ADDR_A)

data=''

def callback(e:keyboard.KeyboardEvent):
    c = e.scan_code
    print(c)
    data=c

def get_pressed_keys():
    if (currentPlatform == "Windows"):
        w = keyboard.is_pressed(17)
        a = keyboard.is_pressed(30)
        s = keyboard.is_pressed(31)
        d = keyboard.is_pressed(32)
        boost = keyboard.is_pressed(20)
        left = keyboard.is_pressed(37) 
        right = keyboard.is_pressed(39)
    else:
        w = keyboard.is_pressed(13)
        a = keyboard.is_pressed(0)
        s = keyboard.is_pressed(1)
        d = keyboard.is_pressed(2)
        boost = keyboard.is_pressed(49)
        left = keyboard.is_pressed(123) 
        right = keyboard.is_pressed(124)

    return map(lambda x:int(x), [w,a,s,d,boost,left,right])
    

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
