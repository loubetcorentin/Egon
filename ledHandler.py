from pyfirmata import Arduino, util
import time
import math
import random
import re

"""-----------------------------------------------------------------------
                               ARDUINO 2
-----------------------------------------------------------------------"""
while True:
    try:


        port2 = '/dev/ttyACM1'
        board2 = Arduino(port2)
        pin1 = [board2.get_pin('d:10:p'),board2.get_pin('d:9:p'),board2.get_pin('d:11:p')]
        pin2 = [board2.get_pin('d:5:p'),board2.get_pin('d:6:p'),board2.get_pin('d:3:p')]

        breathTime = 180
        oxygen = 0.0
        breathing = True
        heartbeatTime = 0
        bloodPressure = 0.0
        excitement = 1.0
        thinkTime = 0
        cognitiveLoad = 0
        inMemory = True
        transitionTime = 0
        memory = 0.0
        nextState = "excited"
        excitedTime = 0


        inMemory=False
        currentState="calm"


        with open('state.txt') as f:
            line = f.readline()


        def extract_currentState(currentState,inMemory):
            global line
            li = list(line.split(","))
            currentState=li[0].split("[")[1]
            currentState = re.sub("'", "", currentState)
            inMemory=bool(li[1].split("]")[0])
            return currentState,inMemory
            #print(currentState,inMemory)
            

        #extract_currentState()

        def think():
            global thinkTime, excitement
            if thinkTime == 0:
                thinkTime = 160
            thinkTime -= 1
            interest = (excitement + math.sin(2.0*math.pi/80.0*float(thinkTime))*excitement)
            interest2 = (excitement + math.sin(math.pi/2.0+2.0*math.pi/80.0*float(thinkTime))*excitement)
            cognitiveLoad = interest
            pin2[0].write((cognitiveLoad+interest2)/2.0)
            pin2[1].write(cognitiveLoad)
            pin2[2].write(interest2/2.0)
            #analogWrite(PIN_LED_1[0], (int)(cognitiveLoad+interest2)/2.0);
            #analogWrite(PIN_LED_1[1], cognitiveLoad);
            #analogWrite(PIN_LED_1[2], interest2);

        def transition(pin, duration, t):
            global transitionTime, currentState
            if (t <= duration):
                v = .5+(.5/(t*0.1))*math.sin(math.pi/10.0*float(t))
                pin.write(v)
            else:
                transitionTime = 1
                currentState = nextState

        def breathe():
            global oxygen, excitement, breathTime, breathing
            if breathTime == 0:
                breathTime = random.randint(int(180-excitement*200), int(200-excitement*200))
                breathing = not breathing
            if breathing:
                oxygen = constrain(oxygen + 0.01,0,1) #+excitement/2000.0
            else:
                oxygen = constrain(oxygen - 0.02,0,1) 
            breathTime-=1
            pin1[2].write(constrain(oxygen,0,1))

        def beat():
            global heartbeatTime, excitement, bloodPressure
            if (heartbeatTime == 20 - int(excitement*5)): 
                bloodPressure = 20
            if (heartbeatTime == 0):
                heartbeatTime = 150-int(excitement*10)
                bloodPressure = 100
            heartbeatTime-=1
            bloodPressure = bloodPressure * 0.8
            pin1[0].write(constrain(bloodPressure, 0, 255)/255.0)

        def goLoco():
            global excitedTime,pin1,pin2

            v1 = constrain(math.sin(float(excitedTime)*.2*excitement),0,1)*.5
            v2 = constrain(math.sin(math.pi/3.0+float(excitedTime)*.2*excitement),0,1)*.5
            blue = .5*constrain(math.sin(float(excitedTime)*.5*excitement),0.0,1.0)*constrain(math.sin(float(excitedTime)*.04*excitement),0.0,1.0)
            yellow = constrain(excitedTime/10000,0.0,1.0)*.5
            pin1[0].write(v2+yellow)
            pin1[1].write(yellow)
            pin1[2].write(v2+blue)
            pin2[0].write(v1+yellow)
            pin2[1].write(yellow)
            pin2[2].write(v1+blue)



        def constrain(v, mini, maxi):
            return max(min(v,maxi),mini)


        while True:
            # pin1[0].write(0)
            # pin1[1].write(0)
            # pin1[2].write(1)
            # pin2[0].write(0)
            # pin2[1].write(0)
            # pin2[2].write(0)
            with open('state.txt') as f:
                line = f.readline()

            currentState,inMemory= extract_currentState(currentState,inMemory)
            print(currentState,inMemory)
            
            if currentState == "transition":
                
                transitionTime += 1
                transition(pin2[0], 80, transitionTime);
                transition(pin2[1], 80, transitionTime);
                transition(pin2[2], 80, transitionTime);

            elif currentState == "calm":
                excitement = constrain(excitement-0.001,0,1)
                breathe()
                beat()
                think()

            elif currentState == "interested":
                excitement = constrain(excitement + 0.001, 0, .5)
                think()
                breathe()
                beat()
                if (inMemory):
                    memory = constrain(memory+.01,0,1)
                else:
                    memory = constrain(memory-.01,0,1)
                pin1[1].write(memory)

            elif currentState == "excited":
                excitement = constrain(excitement + 0.01, 0, 1.0)
                excitedTime+=1
                goLoco()


            time.sleep(0.01)

    except:
    	print("error loop")



    
