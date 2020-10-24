import speech_recognition as sr
from playsound import playsound
from requests import get
from bs4 import BeautifulSoup
from gtts import gTTS

##### CONFIGURAÇÕES #####
hotword = 'rose';

##### FUNÇÕES PRINCIPAIS #####
def monitora_audio():
    microfone = sr.Recognizer()
    with sr.Microphone() as source:
        while True:
            print("Aguardando o Comando: ")
            audio = microfone.listen(source)
            try:
                trigger = microfone.recognize_google(audio, language="pt-BR")
                trigger = trigger.lower()

                if hotword in trigger:
                    print("Comando: ", trigger)
                    responde('feedback')
                    executa_comandos(trigger)
                    break;

            except sr.UnknownValueError:
                print("Google not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Cloud Speech service; {0}".format(e))
        return trigger;

def responde(resposta):
    caminhoArquivo = 'audios/' + resposta + '.mp3';
    playsound(caminhoArquivo)

def executa_comandos(trigger):
    if 'notícias' in trigger:
        ultimas_noticias()
    else:
        cria_audio('Oooooooops, parece que seu comando não é válido!', 'comando-invalido');

def cria_audio(mensagem, nomeAudio):
    tts = gTTS(mensagem, lang='pt-br')
    caminhoArquivo = 'audios/' + nomeAudio + '.mp3'
    tts.save(caminhoArquivo)
    print('ROSIE: ', mensagem);
    playsound(caminhoArquivo)

##### Funções Comandos #####
def ultimas_noticias():
    site = get('https://news.google.com/rss?hl=pt-BR&gl=BR&ceid=BR:pt-419');
    noticias = BeautifulSoup(site.text, 'html.parser')
    for item in noticias.find_all('item')[:10]:
        mensagem = item.title.text;
        cria_audio(mensagem, 'mensagens');

def main():
    while True:
        monitora_audio()


main()




