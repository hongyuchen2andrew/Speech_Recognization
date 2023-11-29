import os
import time
import azure.cognitiveservices.speech as speechsdk
#from playsound import playsound

speech_key = 'c480332d305f4ffaa8d777e972e4d305'
service_region = 'westus'
    
def transcribe_from_file(KEY = speech_key, LOCATION = service_region):
    translation_config = speechsdk.translation.SpeechTranslationConfig(
        subscription=speech_key, region=service_region,
        speech_recognition_language='en-US',)
    audio_config = speechsdk.audio.AudioConfig(filename="/Users/chenhongyu/Desktop/MIT_calculus_test_voice.wav")
    # Creates a translation recognizer using and audio file as input.
    recognizer = speechsdk.SpeechRecognizer(
        speech_config=translation_config, audio_config=audio_config)
    
    #continuous recognition is event based
    done = False
    def stop_cb(evt: speechsdk.SessionEventArgs):
        """callback that signals to stop continuous recognition upon receiving an event `evt`"""
        print('CLOSING on {}'.format(evt))
        nonlocal done
        done = True
    
    recognizer.recognizing.connect(lambda evt: print('RECOGNIZING: {}'.format(evt.result.text)))#持续输出
    recognizer.recognized.connect(lambda evt: print('RECOGNIZED: {}'.format(evt.result.text)))#一次性输出
    recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
    recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
    recognizer.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))
    # Stop continuous recognition on either session stopped or canceled events
    recognizer.session_stopped.connect(stop_cb)
    recognizer.canceled.connect(stop_cb)

    recognizer.start_continuous_recognition()
    while not done:
        time.sleep(.5)

    recognizer.stop_continuous_recognition()

    #translation_recognition_result = recognizer.start_continuous_recognition()
    #result = translation_recognition_result
    #print(result.reason == speechsdk.ResultReason.TranslatedSpeech)
    #print(result.reason == speechsdk.ResultReason.RecognizedSpeech)
    #if result.reason == speechsdk.ResultReason.TranslatedSpeech:
    #    print("""Recognized: {}
    #    German translation: {}
    #    French translation: {}""".format(
    #        result.text, result.translations['zh-Hans'], result.translations['fr']))
    #elif result.reason == speechsdk.ResultReason.RecognizedSpeech:
    #    print("Recognized: {}".format(result.text))
    #elif result.reason == speechsdk.ResultReason.NoMatch:
    #    print("No speech could be recognized: {}".format(result.no_match_details))
    #elif result.reason == speechsdk.ResultReason.Canceled:
    #    print("Translation canceled: {}".format(result.cancellation_details.reason))
    #    if result.cancellation_details.reason == speechsdk.CancellationReason.Error:
    #        print("Error details: {}".format(result.cancellation_details.error_details))
transcribe_from_file()
