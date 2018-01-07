import pygame
import Files
import typing
music :pygame.mixer.Sound = None

musicChannel :pygame.mixer.Channel = None
soundChannels :typing.Sequence[pygame.mixer.Channel] = None

def init():
    global musicChannel
    global soundChannels
    soundChannelC =20
    musicChannelC =1
    pygame.mixer.set_num_channels(musicChannelC+soundChannelC+7)
    pygame.mixer.set_reserved(musicChannelC+soundChannelC)
    musicChannel = pygame.mixer.Channel(0)
    soundChannels=[pygame.mixer.Channel(musicChannelC+i) for i in range(soundChannelC)]



def playMusic(name ,fadeout=0,fadein=500):
    global music
    global musicChannel

    if(music is not None):
        music.fadeout(fadeout)
    music = Files.getSound(name)
    musicChannel.set_volume(0.5)
    musicChannel.play(music,-1)
def getSound(sound):
    return Files.getSound(sound)
def playSound(sound):
#
    for soundC in soundChannels:
        if(soundC.get_sound() is None):
            soundC.play(Files.getSound(sound))
            return
    print("SoundOverflow")

    Files.getSound(sound).stop()
    Files.getSound(sound).play()

def stopMusic(name=None, fadeout=0):
    if name is not None:
        Files.getSound(name).fadeout(fadeout)
        return
    if (music is not None):
        music.fadeout(fadeout)