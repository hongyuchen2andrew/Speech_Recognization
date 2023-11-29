import os
import time
import wave
import threading
import azure.cognitiveservices.speech as speechsdk

speech_key = 'c480332d305f4ffaa8d777e972e4d305'
service_region = 'westus'
fileName = "/Users/chenhongyu/Desktop/MIT_calculus_test_voice.wav"

def push_stream_writer(stream):
    # The number of bytes to push per buffer
    n_bytes = 3200
    wav_fh = wave.open(fileName)
    # Start pushing data until all data has been read from the file
    try:
        while True:
            frames = wav_fh.readframes(n_bytes // 2)
            if not frames:
                break
            stream.write(frames)
            time.sleep(.1)
    finally:
        wav_fh.close()
        stream.close()  # must be done to signal the end of stream


def transcribe_from_stream(KEY = speech_key, LOCATION = service_region):
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    # Setup the audio stream
    stream = speechsdk.audio.PushAudioInputStream()
    audio_config = speechsdk.audio.AudioConfig(stream=stream)

    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    recognition_done = threading.Event()

    def session_stopped_cb(evt):
        """callback that signals to stop continuous recognition upon receiving an event `evt`"""
        print('SESSION STOPPED: {}'.format(evt))
        recognition_done.set()

    speech_recognizer.recognizing.connect(lambda evt: print('RECOGNIZING: {}'.format(evt.result.text)))
    #speech_recognizer.recognized.connect(lambda evt: print('RECOGNIZED: {}'.format(evt.result.text)))
    speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
    speech_recognizer.session_stopped.connect(session_stopped_cb)
    speech_recognizer.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))

    push_stream_writer_thread = threading.Thread(target=push_stream_writer, args=[stream])
    push_stream_writer_thread.start()

    # Start continuous speech recognition
    speech_recognizer.start_continuous_recognition()

    # Wait until all input processed
    recognition_done.wait()

    # Stop recognition and clean up
    speech_recognizer.stop_continuous_recognition()
    push_stream_writer_thread.join()

transcribe_from_stream()