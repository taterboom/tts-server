import os
import io
import azure.cognitiveservices.speech as speechsdk
import wave


def tts(text: str, speaker: str):
    speech_config = speechsdk.SpeechConfig(subscription=os.environ.get(
        'SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))
    # The language of the voice that speaks.
    speech_config.speech_synthesis_voice_name = 'en-US-JennyNeural'
    speech_synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, audio_config=None)
    result = speech_synthesizer.speak_text_async("hello S3, world").get()
    stream = speechsdk.AudioDataStream(result)

    # placehodler with "1"
    audio = b'1'
    audio_buffer = bytes(16000)
    filled_size = stream.read_data(audio_buffer)

    while filled_size > 0:
        audio += audio_buffer[:filled_size]
        filled_size = stream.read_data(audio_buffer)

    file = io.BytesIO()
    with wave.open(file, 'wb') as output:  # Open temporary file as bytes
        output.setparams((1, 2, 16000, 0, 'NONE', 'not compressed'))
        output.writeframesraw(audio[1:])
    file.seek(0)  # Rewind the file

    return file
