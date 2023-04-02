import os
import io
import azure.cognitiveservices.speech as speechsdk
import wave
import time
import json

def datenow():
    current_time = time.time() # returns current Unix timestamp in seconds
    current_time_ms = int(round(current_time * 1000)) # convert seconds to milliseconds
    return current_time_ms

speakers_json = None
with open('./speakers.json', 'r') as f:
  speakers_json = json.load(f)

def get_speaker_list():
    return speakers_json

def tts(text: str, speaker: str) -> io.BytesIO | None:
    speech_config = speechsdk.SpeechConfig(subscription=os.environ.get(
        'SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))
    speech_config.speech_synthesis_voice_name = speaker
    speech_synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, audio_config=None)
    result = speech_synthesizer.speak_text_async(text).get()

    if result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print("Error details: {}".format(cancellation_details.error_details))
        return None 

    stream = speechsdk.AudioDataStream(result)

    # placehodler with "1"
    audio = b'1'
    audio_buffer = bytes(16000)
    filled_size = stream.read_data(audio_buffer)

    while filled_size > 0:
        audio += audio_buffer[:filled_size]
        filled_size = stream.read_data(audio_buffer)

    file = io.BytesIO()
    file.name = f'{datenow()}.wav'
    with wave.open(file, 'wb') as output:  # Open temporary file as bytes
        output.setparams((1, 2, 16000, 0, 'NONE', 'not compressed'))
        output.writeframes(audio[1:])
    file.seek(0)  # Rewind the file
    
    return file

if __name__ == '__main__':
    print(tts("hello world", "en-US-JessaNeural"))
