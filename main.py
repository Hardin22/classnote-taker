import os
from vosk import Model, KaldiRecognizer
import pyaudio
import json
import signal
import sys

# Funzione per gestire l'interruzione
def signal_handler(sig, frame):
    print('Interruzione rilevata, terminazione dello script...')
    stream.stop_stream()
    stream.close()
    p.terminate()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Percorso del modello
model_path = "vosk-model-it-0.22"
if not os.path.exists(model_path):
    print("Modello Vosk non trovato.")
    exit(1)

model = Model(model_path)
rec = KaldiRecognizer(model, 16000)

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
stream.start_stream()

# Apri un file per scrivere la trascrizione
with open("trascrizione.txt", "a") as file:
    while True:
        data = stream.read(4096)
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            if result.get("text", ""):  # Scrivi solo se c'è del testo
                file.write(result["text"] + "\n")
                print(result["text"])
        else:
            partial = json.loads(rec.PartialResult())
            if partial.get("partial", ""):  # Opzionale: stampa i risultati parziali
                print(partial["partial"])

# Chiudi lo stream e PyAudio
stream.stop_stream()
stream.close()
p.terminate()
