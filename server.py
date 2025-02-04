import json
import socket
import keyboard
import socket
import time
# import serial

# IP Adresses, last 3 digits
# Noah: 123
# Luke: 110
# Matthew: 173

# Get the host name, print it and then set ADDR_A based on the ip address
hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)

print("Your Computer Name is: " + hostname)
print("Your Computer IP Address is: " + IPAddr)

ADDR_A = (IPAddr, 9999)
ADDR_B = ('192.168.0.165', 9999)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(ADDR_A)

# s = serial.Serial('/dev/cu.usbserial-130', 115200)
# s.close()
# s.open()

data=''

def callback(e:keyboard.KeyboardEvent):
    c = e.scan_code
    print(c)
    data=c

# def get_joystick():
#     data = s.readline().decode()
#     split = data.split('|')
#     return float(split[0]),float(split[1].strip())

def get_pressed_keys():
    w = keyboard.is_pressed("W")
    a = keyboard.is_pressed("A")
    s = keyboard.is_pressed("S")
    d = keyboard.is_pressed("D")
    boost = keyboard.is_pressed("Space")
    left = keyboard.is_pressed("Left") 
    right = keyboard.is_pressed("Right")

    return map(lambda x:int(x), [w,a,s,d,boost,left,right])
    
start_time = time.time()

while True:
    #continuously send and receive info to program B until some breaking condition reached
    # print("A sending...")
    data=''
    # keyboard.hook(callback=callback, suppress=False)
    keys = list(get_pressed_keys())
    # joystick = get_joystick()
    
    # Note: this will be silently dropped if the client is not up and running yet
    # And even if the the client is running, it may still be silently dropped since UDP is unreliable.
    sock.sendto(json.dumps(''.join(map(str,keys))).encode("utf-8"), ADDR_B)

    # recv_data = sock.recv(1024)
    
    if time.time() - start_time >= 0.1:
        print(keys)
        # print(joystick)
        # print("A receiving...")
        # print(recv_data.decode('utf-8'))
        start_time = time.time()