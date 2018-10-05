import pygame
import socket
import time
import math 

s=socket.socket()
host='192.168.0.21'
port=8087
s.bind((host,port))
s.listen(5)
c,addr = s.accept()

pygame.init()
done = False
clock = pygame.time.Clock()
parameter=[]
parameter_unweighted=[]
pygame.joystick.init()
scalefactor=500
button1=0
button2=0
button3=0
button4=0

# -------- Main Program Loop -----------
time.sleep(10)
print("Ready to start")
while not done:
    startingtime=time.time()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    
    
    joystick_count = pygame.joystick.get_count()
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()

        for i in range(4):
            button = joystick.get_button(i) 
            if(i==0):
              button1=button
            elif(i==1):
              button2=button
            elif(i==2):
              button3=button
            elif(i==3):
              button4=button

        for i in range(4):
            axis = joystick.get_axis(i) 
            if(i==0):
              axis=axis
              parameter_unweighted.append(axis)
              axis=(axis)*scalefactor+1500 
            elif(i==1):
              axis=-axis
              parameter_unweighted.append(axis)
              axis=(axis)*scalefactor+1500
            elif(i==2):
              parameter_unweighted.append(axis)
              axis=(axis**3)         
              axis=(axis)*300+1500 
            elif(i==3):
              axis=-axis
              parameter_unweighted.append(axis)
              axis=(axis**3)          
              axis=(axis)*300+1500 
            parameter.append(int(axis))


        print(parameter_unweighted)
        print(parameter)
        if(button2==1):
              c.send(str(1000)+"A"+str(2000)+"B"+str(1500)+"C"+str(1500))
        elif(button3==1):
              c.send(str(1000)+"A"+str(1000)+"B"+str(1500)+"C"+str(1500)) 
        else:
              c.send(str(parameter[0])+"A"+str(parameter[1])+"B"+str(parameter[2])+"C"+str(parameter[3]))
        parameter=[]
        parameter_unweighted=[]
    clock.tick(60)
    looptime=time.time()-startingtime
    time.sleep((8-looptime)/100)

pygame.quit()
