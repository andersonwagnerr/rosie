import speech_recognition as sr
from playsound import playsound
from requests import get
from bs4 import BeautifulSoup
from gtts import gTTS
import webbrowser as browser
from paho.mqtt import publish
import json

##### CONFIGURAÇÕES #####
hotword = 'rose'


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
                    print('Comando: ', trigger)
                    responde('feedback')
                    executa_comandos(trigger)
                    break

            except sr.UnknownValueError:
                print("Google not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Cloud Speech service; {0}".format(e))
        return trigger;


def responde(resposta):
    caminhoArquivo = 'audios/' + resposta + '.mp3';
    playsound(caminhoArquivo)


def cria_audio(mensagem, nomeAudio):
    tts = gTTS(mensagem, lang='pt-br')
    caminhoArquivo = 'audios/' + nomeAudio + '.mp3'
    tts.save(caminhoArquivo)
    print('ROSIE: ', mensagem);
    playsound(caminhoArquivo)


def executa_comandos(trigger):
    if 'notícias' in trigger:
        ultimas_noticias()
    elif 'toca' in trigger and 'bee gees' in trigger:
        playlists('bee_gees')
    elif 'toca' in trigger and 'taylor davis' in trigger:
        playlists('taylor_davis')
    elif 'tempo agora' in trigger:
        previsao_tempo(tempo=True)
    elif 'temperatura hoje' in trigger:
        previsao_tempo(minmax=True)
    elif 'ligar a tv' in trigger:
        publica_mqtt('office/tv/status', '1')
    elif 'desliga a tv' in trigger:
        publica_mqtt('office/tv/status', '0')
    else:
        cria_audio('Oooooooops, parece que seu comando não é válido!', 'comando-invalido');


##### Funções Comandos #####
def ultimas_noticias():
    site = get('https://news.google.com/rss?hl=pt-BR&gl=BR&ceid=BR:pt-419');
    noticias = BeautifulSoup(site.text, 'html.parser')
    for item in noticias.find_all('item')[:5]:
        mensagem = item.title.text;
        cria_audio(mensagem, 'mensagens')


def playlists(album):
    if album == 'bee_gees':
        browser.open('https://open.spotify.com/track/0MEaPVD5sOZ17HhhjBZs3Z?si=b4u9B-usRimjSJKCgEgpEQ')
    elif album == 'taylor_davis':
        browser.open('https://open.spotify.com/track/4U2v1vLfpfNjOEXVuY1aHd')


def previsao_tempo(tempo=False, minmax=False):
    site = get(
        'https://api.openweathermap.org/data/2.5/weather?q=Joinville&appid=5e4b94887de335437f2fe88877677b93&units=metric&lang=pt');
    clima = site.json()
    # print(json.dumps(clima,indent=4))
    temperatura = clima['main']['temp']
    minima = clima['main']['temp_min']
    maxima = clima['main']['temp_max']
    descricao = clima['weather'][0]['description']
    if tempo:
        mensagem = f'No momento fazem {temperatura} graus com: {descricao}'

    if minmax:
        mensagem = f'Minima de {minima} e máxima de {maxima}'
    cria_audio(mensagem, 'previsao')


def publica_mqtt(topic, payload):
    publish.single(topic, payload=payload, qos=0, retain=True, hostname="mqtt.eclipse.org",
                   port=1883, client_id="rosie")
    if payload == '1':
        mensagem = 'Tv ligada'

    elif payload == '0':
        mensagem = 'Tv desligada'

    cria_audio(mensagem, 'tv')

def main():
    while True:
        monitora_audio()


main()
