import motor_controller as MC
import ultrasonic as US
import RPi.GPIO as GPIO
import subprocess

#set GPIO mode to BCM
GPIO.setmode(GPIO.BCM)

# create objects for motor controller and distance sensor
vikingbotMotors = MC.MotorController()
ultrasonicSensorBack = US.Ultrasonic()

#GPIO.cleanup()

# setup the motors
vikingbotMotors.setup_GPIO(1,0)

# setup and start PWM set the dulty cycles to 90
vikingbotMotors.setup_PWM()
vikingbotMotors.start_PWM()
vikingbotMotors.set_motorSpeed(55,100)

# set the delay between motions to 2 seconds
vikingbotMotors.set_SleepTime(2)

#Test the movements

#Test singing frog
GPIO.setup(19, GPIO.OUT)
GPIO.output(19, GPIO.HIGH)
print "Frog is singing"
vikingbotMotors.set_SleepTime(15)
GPIO.output(19, GPIO.LOW)

#test for distance sensor
#setup the distance sensor
ultrasonicSensorBack.setup_GPIO()
subprocess.call(["espeak","-s 120 -v en ", "Zebra is moving now"] , stdout=None, stderr=subprocess.STDOUT)
while(True):
#if distance is more than 10 cm. go back. Ig there is an obstacle stop
#        if (ultrasonicSensorBack.get_distance() > 10):
#                vikingbotMotors.goBack()

    cmd = raw_input("Enter the command ")
    if cmd == 'k' :
        vikingbotMotors.set_motorSpeed(55,100)
        vikingbotMotors.set_SleepTime(2)
        vikingbotMotors.goForward()
        
    if cmd == 'i' :
        vikingbotMotors.set_motorSpeed(55,100)
        vikingbotMotors.set_SleepTime(2)
        vikingbotMotors.goBack()
    if cmd == 'l' :
        vikingbotMotors.set_motorSpeed(55,100)
        vikingbotMotors.set_SleepTime(0.75)
        vikingbotMotors.turnLeft()
    if cmd == 'j' :
        vikingbotMotors.set_motorSpeed(55,100)
        vikingbotMotors.set_SleepTime(0.75)
        vikingbotMotors.turnRight()
     

GPIO.cleanup()
