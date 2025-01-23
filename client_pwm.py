import json
import socket
import RPi.GPIO as GPIO
import time

IR_1 = 21
IR_2 = 20
GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering
GPIO.setup(IR_1, GPIO.IN)  # Set GPIO 21 as an input pin
GPIO.setup(IR_2, GPIO.IN)

TRIG_PIN = 23
ECHO_PIN = 24

# Set up the trigger and echo pins
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

MOTOR_L_1 = 26
MOTOR_L_2 = 19
MOTOR_R_1 = 13
MOTOR_R_2 = 6

GPIO.setup(MOTOR_L_1, GPIO.OUT)
GPIO.setup(MOTOR_L_2, GPIO.OUT)
GPIO.setup(MOTOR_R_1, GPIO.OUT)
GPIO.setup(MOTOR_R_2, GPIO.OUT)

# Set up PWM for motor control
motor_l_pwm = GPIO.PWM(MOTOR_L_1, 100)  # 100Hz frequency
motor_r_pwm = GPIO.PWM(MOTOR_R_1, 100)
motor_l_pwm.start(0)  # Start with 0% duty cycle
motor_r_pwm.start(0)

motor_l_2_pwm = GPIO.PWM(MOTOR_L_2, 100)  # 100Hz frequency
motor_r_2_pwm = GPIO.PWM(MOTOR_R_2, 100)
motor_l_2_pwm.start(0)  # Start with 0% duty cycle
motor_r_2_pwm.start(0)


ADDR_A = ('192.168.0.110', 9999)
ADDR_B = ('192.168.0.165', 9999)

def get_distance():
    GPIO.output(TRIG_PIN, False)
    time.sleep(0.03)

    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, False)

    while GPIO.input(ECHO_PIN) == 0:
        pulse_start = time.time()
    while GPIO.input(ECHO_PIN) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = (pulse_duration * 34300) / 2
    return distance


class Task:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(ADDR_B)
        self.ir_input_1 = 0
        self.ir_input_2 = 0
        self.ultrasonic_input = 0
        self.up = 0
        self.down = 0
        self.left = 0
        self.right = 0

    def step(self):
        self.read_sensors()
        self.send_data()
        self.receive_data()
        self.set_motors()

    def read_sensors(self):
        self.ir_input_1 = GPIO.input(IR_1)
        self.ir_input_2 = GPIO.input(IR_2)
        print(str(self.ir_input_2) + ' | ' + str(self.ir_input_1))

    def send_data(self):
        control_cmd = "This is a control command sent by B"
        self.sock.sendto(bytes(str(self.ultrasonic_input), encoding='utf-8'), ADDR_A)
        print(f"B sent {control_cmd}")

    def receive_data(self):
        try:
            data = self.sock.recv(1024)
            data = bytearray(data)
            data_dict = json.loads(data.decode('utf-8'))
            if data_dict != '':
                res = str(data_dict)
                keys = list(map(int, list(res)))
                self.up, self.left, self.down, self.right = map(bool, keys)
                print(self.up, self.down, self.left, self.right)
        except Exception as e:
            print(f"B exception {e} in receive_data")

    def set_motors(self):
        motor_speed = 100  # Default speed (can be adjusted)

        if self.up:
            motor_l_pwm.ChangeDutyCycle(motor_speed)
            motor_r_pwm.ChangeDutyCycle(motor_speed)
            GPIO.output(MOTOR_L_2, GPIO.LOW)
            GPIO.output(MOTOR_R_2, GPIO.LOW)

        elif self.down:
            motor_l_2_pwm.ChangeDutyCycle(motor_speed)
            motor_r_2_pwm.ChangeDutyCycle(motor_speed)
            GPIO.output(MOTOR_L_1, GPIO.LOW)
            GPIO.output(MOTOR_R_1, GPIO.LOW)

        elif self.left:
            motor_l_pwm.ChangeDutyCycle(0)  # Stop left motor
            motor_r_pwm.ChangeDutyCycle(motor_speed)

        elif self.right:
            motor_l_pwm.ChangeDutyCycle(motor_speed)
            motor_r_pwm.ChangeDutyCycle(0)  # Stop right motor

        else:
            # Stop motors
            motor_l_pwm.ChangeDutyCycle(0)
            motor_r_pwm.ChangeDutyCycle(0)
            motor_l_2_pwm.ChangeDutyCycle(0)
            motor_r_2_pwm.ChangeDutyCycle(0)
            #GPIO.output(MOTOR_L_2, GPIO.LOW)
            #GPIO.output(MOTOR_L_2, GPIO.LOW)
            #GPIO.output(MOTOR_R_2, GPIO.LOW)



task = Task()

try:
    while True:
        task.step()
except KeyboardInterrupt:
    print("Stopping...")
finally:
    motor_l_pwm.stop()
    motor_r_pwm.stop()
    GPIO.cleanup()

