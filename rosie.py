import speech_recognition as sr



##### CONFIGURAÇÕES #####
with open('rosie-python-assistente-fe02a8d39c53.json') as credenciais_google:
    credenciais_google = credenciais_google.read()


def monitora_audio():
    microfone = sr.Recognizer()
    with sr.Microphone() as source:
        print("Aguardando o Comando: ")
        audio = microfone.listen(source)
    try:
        print(microfone.recognize_google_cloud(audio, credentials_json=credenciais_google, language='pt-BR'))
    except sr.UnknownValueError:
        print("Google not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Cloud Speech service; {0}".format(e))


monitora_audio()




