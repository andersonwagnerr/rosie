from gtts import gTTS
from playsound import playsound

def cria_audio(audio):
    tts = gTTS(audio, lang='pt-br')
    tts.save('audios/bem_vindo.mp3')

    playsound('audios/bem_vindo.mp3')

cria_audio('Oi, eu sou a Rose')