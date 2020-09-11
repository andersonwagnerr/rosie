from gtts import gTTS

tts = gTTS('Oi, eu sou a Rose', lang='pt-br')
tts.save('audios/hello.mp3')
