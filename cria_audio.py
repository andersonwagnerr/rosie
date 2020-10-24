from gtts import gTTS
from playsound import playsound

def cria_audio(audio, nomeAudio):
    tts = gTTS(audio, lang='pt-br')
    caminhoArquivo = 'audios/' + nomeAudio + '.mp3'
    tts.save(caminhoArquivo)

    playsound(caminhoArquivo)

#cria_audio('Oi, eu sou a Rose', 'bem-vindo')
cria_audio('Aguarde um momento', 'feedback')