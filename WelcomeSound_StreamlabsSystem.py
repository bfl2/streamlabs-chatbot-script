import sys
import json
import os
import ctypes
import codecs

### Default Variables

ScriptName = "Welcome Sound"
Website = "github.org/bfl2"
Description = "Script do canal ursope para tocar sons especiais para subs ao entrarem no canal"
Creator="ursope"
Version="1.0.0"

configFile = "config.json"
volume = 0.1
command = "!WelcomeSound"
soundspath = ""
soundsAvailable = []
greetedUsers = []

verbose = True

### Functions


### Obligatory function
def Init():
    global soundsAvailable, soundspath, volume, words, settings
    path = os.path.dirname(__file__)
    soundspath = path + "/soundfiles"

    updateVolumeReading()

    soundsAvailable = os.listdir(soundspath)

    return

def Execute(data):
    global greetedUsers, verbose
    userId = data.User
    username = data.UserName
    paramCount = data.GetParamCount()

    hasUserBeenGreeted =  userId in greetedUsers

    if not hasUserBeenGreeted and userId!="":
        playRandomSound()
        greetedUsers.append(userId)
    else:
        return

    if verbose:
        log("userId = "+str(userId))
        log("userName = "+str(username))
        log("paramCount = "+str(paramCount))
        log("Greeted Users count = " + str(len(greetedUsers)))

    return

def Tick():
    updateVolumeOnTick = True
    if(updateVolumeOnTick):
        updateVolumeReading()
    return

### Auxiliary functions
def updateVolumeReading():
    global volume
    path = os.path.dirname(__file__)
    try:
        with codecs.open(os.path.join(path, configFile), encoding='utf-8-sig', mode='r') as file:
		    settings = json.load(file, encoding='utf-8-sig')
    except:
		settings = {
			"liveOnly": True,
			"volume": 50.0,
		}

    volume = settings["volume"]/100.0


def playSound(soundFile):
    soundFullpath = soundspath + "/" + soundFile
    Parent.PlaySound(soundFullpath, volume)

    return

def playRandomSound():

    seed = Parent.GetRandom(0, len(soundsAvailable) - 1)
    return playSound(soundsAvailable[seed])

def log(message):
    Parent.Log(command, message)
    return