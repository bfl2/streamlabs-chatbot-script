import sys
import json
import os
import ctypes
import codecs
import time

### Default Variables

ScriptName = "Welcome Sound"
Website = "https://github.com/bfl2/streamlabs-chatbot-script"
Description = "Script do canal ursope para tocar sons especiais para viewers ao entrarem no canal"
Creator="ursope"
Version="1.0.0"
command = "!WelcomeSound"

configFile = "config.json"
volume = 0.5
settings = []

soundspath = ""
soundsAvailable = []

greetedUsers = []
toGreetList = [] # If a user is eligible to be greeted but there may be a greet going on

lastGreetingTimeStamp = 0
greetingCooldown = 18

debug = True

### Functions


### Obligatory function
def Init():
    global soundsAvailable, soundspath, volume, words, settings, debug
    path = os.path.dirname(__file__)
    soundspath = path + "/soundfiles"

    updateSettings()

    updateVolumeReading()
    debug = settings["debug"]/100.0

    soundsAvailable = os.listdir(soundspath)

    return

def Execute(data):
    global greetedUsers, debug
    userId = data.User
    username = data.UserName
    paramCount = data.GetParamCount()

    hasUserBeenGreeted =  userId in greetedUsers

    if (not hasUserBeenGreeted) and isGreetingWindow() and (len(toGreetList) > 0):
        ## If there is a window, greet users from the queue first
        userIdFromQueue = toGreetList.pop(0)
        res = greet(userIdFromQueue)

    elif (userId!="") and  (not hasUserBeenGreeted) and isGreetingWindow() :
        ## Greet user directly
        res = greet(userId)

    elif (userId!="") and (not hasUserBeenGreeted) and (not isGreetingWindow()) :
        #Add user to queue
        toGreetList.append(userId)
        res = "added to queue"
    else:
        return

    if debug:
        log("-----")
        log("userId = "+str(userId))
        log("userName = "+str(username))
        log("paramCount = "+str(paramCount))
        log("Greeted Users count = " + str(len(greetedUsers)))
        log("Users in toGreet list count = " + str(len(toGreetList)))
        log("res:"+str(res))

    updateSettings()

    return

def Tick():

    return

### Auxiliary functions

def greet(userToGreet):
    global lastGreetingTimeStamp
    res = playUserSound(userToGreet)
    greetedUsers.append(userToGreet)
    Parent.SendTwitchMessage("Bem vindo "+userToGreet+"!")
    if(res):
        lastGreetingTimeStamp = time.time()

    return res

def updateSettings():
    path = os.path.dirname(__file__)
    global settings
    try:
        with codecs.open(os.path.join(path, configFile), encoding='utf-8-sig', mode='r') as file:
		    settings = json.load(file, encoding='utf-8-sig')
    except:
		settings = {
			"singleGreeting": True,
			"volume": 50.0,
            "debug": False
		}

    return

def isGreetingWindow():
    global lastGreetingTimeStamp, greetingCooldown
    timeSinceLastGreeting = time.time() - lastGreetingTimeStamp
    if(debug):
        log("elapsed time"+str(timeSinceLastGreeting))
    if(timeSinceLastGreeting > greetingCooldown):
        return True
    else:
        return False

def updateVolumeReading():
    global volume
    volume = settings["volume"]/100.0

    return

def playSound(soundFile):
    soundFullpath = soundspath + "/" + soundFile
    return Parent.PlaySound(soundFullpath, volume)

def userMatchesFilename(userId, filename):
    match = False
    if(userId in filename):
        match = True
    return match

def playUserSound(userId):
    global soundsAvailable

    for filename in soundsAvailable:
        if(userMatchesFilename(userId, filename)):
            return playSound(filename)

    if(debug):
        log("No soundfile found for user"+userId)
    return False ### No sound found for user

def playRandomSound():

    seed = Parent.GetRandom(0, len(soundsAvailable) - 1)
    return playSound(soundsAvailable[seed])

def log(message):
    Parent.Log(command, message)
    return