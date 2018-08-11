import pygame
import Files
import typing
music :pygame.mixer.Sound = None

musicChannel :pygame.mixer.Channel = None
soundChannels :typing.Sequence[pygame.mixer.Channel] = None

musicVolume =100
soundVolume = 100

def setVolume():#ustawienie glośniści we wszyskich kanałach
    musicChannel.set_volume(musicVolume/100)
    for soundC in soundChannels:
        soundC.set_volume(soundVolume / 100)

def init(): #inicjalizacja dzwieku
    global musicChannel
    global soundChannels
    soundChannelC =20
    musicChannelC =1
    pygame.mixer.set_num_channels(musicChannelC+soundChannelC+7)
    pygame.mixer.set_reserved(musicChannelC+soundChannelC)
    musicChannel = pygame.mixer.Channel(0)
    soundChannels=[pygame.mixer.Channel(musicChannelC+i) for i in range(soundChannelC)]



def playMusic(name ,fadeout=0,fadein=500): # odtwarzanie muzyki - ciagłego dzwięku w tle
    global music
    global musicChannel

    if(music is not None):
        music.fadeout(fadeout)
    music = Files.getSound(name)
    musicChannel.set_volume(musicVolume/100)
    musicChannel.play(music,-1)
def getSound(sound):
    return Files.getSound(sound)

def playSound(sound): # odtwarzewnie dzwieku - którtkiego dzwięku w pierwszym kanale który nic nie odtwarza
#
    for soundC in soundChannels:
        if(soundC.get_sound() is None):
            soundC.set_volume(soundVolume / 100)
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