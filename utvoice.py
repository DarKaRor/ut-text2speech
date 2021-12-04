from subprocess import call
import keyboard
import os
import time
import sys
import pyglet
import random

class Voice():
    def __init__(self,sounds,upset=False,pitch=1):
        if not isinstance(sounds,list):
            sounds = [sounds]
        self.sounds = sounds
        self.pitch = pitch
        self.defaultSound = self.sounds[0]
        self.isMultiple = False
        self.upset = upset
        self.customs = {}
        if len(sounds)>1:
            self.isMultiple = True

    def setCustom(self,sound,msg):
        self.customs[msg] = sound            

    def playSound(self,type=1):
        if type == 1:
            self.defaultSound.play()
        else:
            self.upset.play()

    def getRandomSound(self):
        return random.choice(self.sounds)

dir_path = os.path.dirname(os.path.realpath(__file__))

keyAmount = 0
keyCounter = 0
speakable = 'abcdefghijklmnñopqrstuvwxyz1234567890.,;:?!'
waitable = '.,;:?!'
waitTimes = {
    '.':1,
    ',':0.5,
    ';':1,
    '?':1,
    '!':1,
    ':':0.5
}
cooldown = 2
cooling = 0
isPlaying = False
path = dir_path+'\\voices\\'
spacePos = []
waitTime = 0.08
isEeeing = False
shouldExit = False
shouldUpdate = False
message = []
isCustom = False

pyglet.resource.path = [path]
pyglet.resource.reindex()

def load_sound(s):
    return pyglet.resource.media(s, streaming=False)

def load_multiple(sounds,type):
    return [load_sound(s+'.'+type) for s in sounds]

sansVoice = Voice(load_sound('voice_sans.wav'))
temmieVoice = Voice(load_multiple(['snd_tem','snd_tem2','snd_tem3','snd_tem4','snd_tem5','snd_tem6'],'wav'))
floweyVoice = Voice(load_sound('snd_floweytalk1.wav'),load_sound('snd_floweytalk2.wav'))
floweyVoice.setCustom(load_sound('snd_floweylaugh.wav'),'HAHAHA')
manVoice = Voice(load_multiple(['snd_wngdng1','snd_wngdng2','snd_wngdng3','snd_wngdng4','snd_wngdng5','snd_wngdng6','snd_wngdng7'],'wav'))
alphysVoice = Voice(load_sound('snd_txtal.wav'))
asgoreVoice = Voice(load_sound('snd_txtasg.wav'))
asrielVoice = Voice(load_sound('snd_txtasr.wav'))
papsVoice = Voice(load_sound('snd_txtpap.wav'))
torielVoice = Voice(load_sound('snd_txttor.wav'))
undyneVoice = Voice(load_sound('snd_txtund.wav'))
mttVoice = Voice(load_multiple(['snd_mtt1','snd_mtt2','snd_mtt3','snd_mtt4','snd_mtt5','snd_mtt6','snd_mtt7','snd_mtt8','snd_mtt9'],'wav'))
mttVoice.setCustom(load_sound('snd_yeah.wav'),'yeah')
normalVoice = Voice(load_sound('SND_TXT1.wav'),load_sound('SND_TXT2.wav'))
voices = [sansVoice,temmieVoice,floweyVoice,manVoice,alphysVoice,asgoreVoice,asrielVoice,papsVoice,torielVoice,undyneVoice,mttVoice]
currentVoice = normalVoice
currentSound = currentVoice.defaultSound

def playText(e):
    global isPlaying
    global currentSound
    global isCustom
    isCustom = False
    isPlaying = True
    text = ''.join(message)
    
    currentSound = currentVoice.defaultSound 
    
    if len(message)==0: return   

    for custom in currentVoice.customs:
        if custom == text:
            isCustom = True
            currentSound = currentVoice.customs[text]
            return

    if text.isupper() and currentVoice.upset:
        currentSound = currentVoice.upset
        return
    
def Exit():
    global shouldExit
    shouldExit = True
    
def resetVariables():
    global shouldUpdate
    global spacePos
    global keyCounter
    global keyAmount
    global isCustom
    global message
    
    message.clear()
    isCustom = False
    shouldUpdate = True
    spacePos = []
    keyCounter = 0
    keyAmount = 0
    
def updateAmount(amount):
    global shouldUpdate
    global keyAmount
    shouldUpdate = True
    keyAmount+=amount
     
def chooseRandomVoice():
    global currentVoice
    global voices
    currentVoice = random.choice(voices)
    

# On press functions
keyboard.on_press_key('enter',callback=playText)
keyboard.add_hotkey('shift+f',callback=Exit)  
keyboard.add_hotkey('ctrl+backspace',callback=resetVariables)
keyboard.add_hotkey('shift+r',callback=chooseRandomVoice)


# Main Loop for Inputs
while True:
    
    if shouldExit:
        sys.exit()
    
    cooling+=1
    
    if isPlaying:
         currentTime = waitTime
         currentChar = ' ' 
         if len(message)>0:
            print(message,keyCounter)
            currentChar = message[keyCounter]

         if isCustom:
             currentSound.play()
             resetVariables()
             continue
         
         keyCounter+=1 
         
         if keyCounter in spacePos:
             time.sleep(waitTime)
             continue             
         # If the voice has multiple sounds
         if currentVoice.isMultiple:
             currentSound = currentVoice.getRandomSound()
         
         currentSound.play()
         print(currentChar)# If current character is a waitable character 
         if currentChar in waitable:
             currentTime = waitTimes[currentChar]
         time.sleep(currentTime)
         
         if keyCounter>=keyAmount:
             resetVariables()
             isPlaying = False
             
         continue

    key = keyboard.read_key()

    if cooling>=cooldown:
        if key.lower() in speakable:
            #print('spoke')
            updateAmount(1)
            if isEeeing:
                keyboard.press('backspace+e')
            message.append(key)
        
        if key == 'backspace':
            #print('delet')
            updateAmount(-1)
            spaces = len(spacePos)
            if spaces>0 and spacePos[spaces-1] == keyAmount:
                spacePos.remove(keyAmount)
            elif len(message)>0:                
                message.pop()
            
        if key == 'space':
            #print('space')
            updateAmount(1)
            spacePos.append(keyAmount)
            message.append(key)
        
    if shouldUpdate:
        cooling = 0
        shouldUpdate = False
           