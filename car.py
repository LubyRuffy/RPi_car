#!/usr/bin/env python
#coding: utf-8
from evdev import InputDevice
from select import select
import RPi.GPIO as GPIO
import time
import os

#os.system( "sudo raspivid -o - -t 0 -w 640 -h 360 -fps 25|cvlc -vvv stream:///dev/stdin --sout '#standard{access=http,mux=ts,dst=:8090}' :demux=h264" )

J = 5
IN1 = 6
IN2 = 13
IN3 = 19
IN4 = 26
TRIG = 23
ECHO = 24
L = 17
R = 27
T = 21

s = 7.5
t = 0.3
tt = 0.2

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)
GPIO.setup(J, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(T, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(IN1, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(IN2, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(IN3, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(IN4, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(TRIG, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(L, GPIO.IN)
GPIO.setup(R, GPIO.IN)

p = GPIO.PWM(T,50)
p.start(s)

def power():
	GPIO.output(J, 0)

def off():
	GPIO.output(J, 1)

def p_left():
	global s
	s = s + 0.5
	p.ChangeDutyCycle(s)

def p_right():
	global s
	s = s - 0.5
	p.ChangeDutyCycle(s)

def distance():
	GPIO.output(TRIG,GPIO.HIGH)
	time.sleep(0.000015)
	GPIO.output(TRIG,GPIO.LOW)
	while not GPIO.input(ECHO):
		pass
	t1 = time.time()
	while GPIO.input(ECHO):
		pass
	t2 = time.time()
	return (t2-t1)*340/2

def run():
	GPIO.output(IN1, 0)
	GPIO.output(IN2, 1)
	GPIO.output(IN3, 0)
	GPIO.output(IN4, 1)
	time.sleep(t)

def go():
	GPIO.output(IN1, 0)
	GPIO.output(IN2, 1)
	GPIO.output(IN3, 0)
	GPIO.output(IN4, 1)	

def back():
	GPIO.output(IN1, 1)
	GPIO.output(IN2, 0)
	GPIO.output(IN3, 1)
	GPIO.output(IN4, 0)
	time.sleep(t)
		

def left():
	GPIO.output(IN1, 1)
	GPIO.output(IN2, 0)
	GPIO.output(IN3, 0)
	GPIO.output(IN4, 1)
	time.sleep(tt)
	

def right():
	GPIO.output(IN1, 0)
	GPIO.output(IN2, 1)
	GPIO.output(IN3, 1)
	GPIO.output(IN4, 0)
	time.sleep(tt)

def stop():
	GPIO.output(IN1, 0)
	GPIO.output(IN2, 0)
	GPIO.output(IN3, 0)
	GPIO.output(IN4, 0)

def auto():
	for i in xrange(5):
		go()
		while 1:
			if GPIO.input(L) == 0 :
				back()
				right()
				break
			if GPIO.input(R) == 0 :
				back()
				left()
				break
			time.sleep(0.02)

dev = InputDevice('/dev/input/event0')
while 1:
	select([dev], [], [])
	for event in dev.read():
		if(event.value == 1 and event.code != 0):
			a = event.code
			if a == 44 :	#z
			    stop()
			if a == 17 :	#w
			    run()
			    stop()
			if a == 31 :	#s
			    back()
			    stop()
			if a == 30 :	#a
			    left()
			    stop()
			if a == 32 :	#d
			    right()
			    stop()
			if a == 16 :	#q
				off()
				GPIO.cleanup()
				os._exit()
			if a == 18 :	#e
				auto()
				stop()
			if a == 25 :	#p
				power()
			if a == 24 :	#o
				off()
			if a == 36 :	#j
				p_left()
			if a == 37 :	#k
				p_right()

			print distance()
			print "left:",GPIO.input(L)
			print "right:",GPIO.input(R)
