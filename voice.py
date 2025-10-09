# voice.py - reconhecimento de voz simples (modo básico)
# Nota: no Termux é recomendado usar termux-voice or SpeechRecognition com microfone configurado
try:
    import speech_recognition as sr
except Exception:
    sr = None

def listen_once(timeout=5, phrase_time_limit=6):
    if sr is None:
        print('[voice] speech_recognition não instalado ou não disponível')
        return None
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('[voice] ouvindo... fale algo')
        try:
            audio = r.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            text = r.recognize_google(audio, language='pt-BR')
            print('[voice] reconhecido:', text)
            return text
        except Exception as e:
            print('[voice] erro/timeout:', e)
            return None
