import os, io, wave
from pydub import AudioSegment
from pydub.utils import make_chunks as mc
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path_to_json"

client = speech.SpeechClient()

path = "/Users/Jeffjnr/Downloads/trial.wav"

path2 = AudioSegment.from_wav(path)
path2 = path2.set_channels(1)

chunk_length_ms = 58000

chunks = mc(path2, chunk_length_ms)

au_list = []

for i, chunk in enumerate(chunks):

    chunk_name = "chunk{0}.wav".format(i)

    chunk.export(chunk_name, format="wav")

    with io.open(chunk_name, 'rb') as audio_file:
        content = audio_file.read()

    audio = types.RecognitionAudio(content=content)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=44100,
        language_code='en-US')

    operation = client.long_running_recognize(config, audio)

        print('Transcription {}'.format(i))
        response = operation.result(timeout=100)

        # print('Waiting for operation to complete...')
        # response = operation.result(timeout=180)
        # Each result is for a consecutive portion of the audio. Iterate through
        # them to get the transcripts for the entire audio file.
        for result in response.results:
            # The first alternative is the most likely one for this portion.
            print('Transcript: {}'.format(result.alternatives[0].transcript))
            print('Confidence: {}'.format(result.alternatives[0].confidence))
