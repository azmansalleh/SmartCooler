from voicerecogntion import VerificationServiceHttpClientHelper
from SpeechAndVoice import voice
import pyaudio as pyaudio
import wave
# import stt
import asyncio
import sys
import threading
import numpy as np
import os



def create_profile(subscription_key, locale):
    helper = VerificationServiceHttpClientHelper.VerificationServiceHttpClientHelper(
        subscription_key)

    creation_response = helper.create_profile(locale)

    print('Profile ID = {0}'.format(creation_response.get_profile_id()))


def delete_profile(subscription_key, profile_id):
    """Delete the given profile from the server

    Arguments:
    subscription_key -- the subscription key string
    profile_id -- the profile ID of the profile to reset
    """

    helper = VerificationServiceHttpClientHelper.VerificationServiceHttpClientHelper(subscription_key)

    helper.delete_profile(profile_id)

    print('Profile {0} has been successfully deleted.'.format(profile_id))

def print_all_profiles(subscription_key):
    helper = VerificationServiceHttpClientHelper.VerificationServiceHttpClientHelper(
        subscription_key)

    profiles = helper.get_all_profiles()

    print('Profile ID, Locale, Enrollments Count, Remaining Enrollments Count,'
          ' Created Date Time, Last Action Date Time, Enrollment Status')
    for profile in profiles:
        print('{0}, {1}, {2}, {3}, {4}, {5}, {6}'.format(
            profile.get_profile_id(),
            profile.get_locale(),
            profile.get_enrollments_count(),
            profile.get_remaining_enrollments_count(),
            profile.get_created_date_time(),
            profile.get_last_action_date_time(),
            profile.get_enrollment_status()))

def reset_enrollments(subscription_key, profile_id):

    helper = VerificationServiceHttpClientHelper.VerificationServiceHttpClientHelper(subscription_key)

    helper.reset_enrollments(profile_id)

    print('Profile {0} has been successfully reset.'.format(profile_id))

def enroll_profile(subscription_key, profile_id, file_path):

    helper = VerificationServiceHttpClientHelper.VerificationServiceHttpClientHelper(
        subscription_key)

    enrollment_response = helper.enroll_profile(profile_id, file_path)

    print('Enrollments Completed = {0}'.format(enrollment_response.get_enrollments_count()))
    print('Remaining Enrollments = {0}'.format(enrollment_response.get_remaining_enrollments()))
    print('Enrollment Status = {0}'.format(enrollment_response.get_enrollment_status()))
    print('Enrollment Phrase = {0}'.format(enrollment_response.get_enrollment_phrase()))

def verify_file(subscription_key, file_path, profile_id):

    for ID,value in profile_id.items():
        helper = VerificationServiceHttpClientHelper.VerificationServiceHttpClientHelper(
            subscription_key)
        verification_response = helper.verify_file(file_path, ID)
        print('Verification Result = {0}'.format(verification_response.get_result()))
        print('Confidence = {0}'.format(verification_response.get_confidence()))
        if verification_response.get_result() == "Accept":
            print("Verified, Welcome "+ value +"!")
            break
    if verification_response.get_result() == "Accept":
        return True
    else:
        return False


def record(file_path):
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    CHUNK = 1024
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = file_path

    audio = pyaudio.PyAudio()

    # start Recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    print ("recording...")
    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print ("finished recording")

    # stop Recording
    stream.stop_stream()
    stream.close()
    audio.terminate()

    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

on_what = 0
phrases = []
listen = True


def initiate_hearing(name):
    global listen
    global phrases
    global on_what
    print("Calibrating audio...")
    import pyaudio
    import wave
    from array import array
    FORMAT=pyaudio.paInt16
    CHANNELS=1
    RATE=16000
    CHUNK=256
    RECORD_SECONDS=1.5


    audio=pyaudio.PyAudio() #instantiate the pyaudio
    stream=audio.open(format=FORMAT,channels=CHANNELS,
                      rate=RATE,
                      input=True,
                      frames_per_buffer=CHUNK)


    volume_levels = []
    for i in range(0,int(RATE/CHUNK*RECORD_SECONDS)):



        data=stream.read(CHUNK)
        data_chunk=array('h',data)
        vol=max(data_chunk)
        volume_levels.append(float(vol))


    silent_audio_level = sum(volume_levels)/len(volume_levels)

    if silent_audio_level > 6500:
        silent_audio_level = 6500
    elif silent_audio_level < 500:
        silent_audio_level =500


    print("Beginning to listen with a silent audio level of " + str(silent_audio_level))

    while True:
        listen = True
        try:
            if listen == False:
                # print("Mid speak...")
                pass
            else:
                import pyaudio
                import wave
                from array import array


                on_what += 1
                FORMAT=pyaudio.paInt16
                CHANNELS=1
                RATE=16000
                CHUNK=256
                RECORD_SECONDS=15000
                # FILE_NAME="verify_voice/request"+str(on_what)+".wav"
                FILE_NAME="verify_voice/request.wav"

                audio=pyaudio.PyAudio() #instantiate the pyaudio


                #recording prerequisites
                stream=audio.open(format=FORMAT,channels=CHANNELS,
                                  rate=RATE,
                                  input=True,
                                  frames_per_buffer=CHUNK)

                #starting recording
                frames=[]
                consecutive_nothings = 0
                consecutive_spikes = 0
                started = False
                print("Listening...")

                for i in range(0,int(RATE/CHUNK*RECORD_SECONDS)):


                    if listen == False:
                        break
                    if consecutive_nothings > 90:
                        break

                    data=stream.read(CHUNK, exception_on_overflow = False)
                    data_chunk=array('h',data)
                    vol=max(data_chunk)
                    if(vol>=silent_audio_level * 7):
                        consecutive_spikes = consecutive_spikes + 1
                        if consecutive_spikes == 8:
                            if started is False:
                                started = True
                                print("Began recording data at volume of " + str(vol))
                        frames.append(data)
                        # print("True audio..")

                        print("recording...")
                        consecutive_nothings = 0
                    elif (vol < silent_audio_level * 3):
                        if started is True:
                            # frames.append(data)
                            if vol < silent_audio_level*3:
                                consecutive_spikes = 0
                                consecutive_nothings += 1

                        frames.append(data)

                    else:
                        frames.append(data)

                #end of recording


                if listen == False:
                    pass
                else:
                    stream.stop_stream()
                    stream.close()
                    audio.terminate()
                    #writing to file
                    wavfile=wave.open(FILE_NAME,'wb')
                    wavfile.setnchannels(CHANNELS)
                    wavfile.setsampwidth(audio.get_sample_size(FORMAT))
                    wavfile.setframerate(RATE)
                    wavfile.writeframes(b''.join(frames))#append frames recorded to file
                    wavfile.close()

                    # Start Of Verifying

                    APIkey = "6f3152ac5fa249aa93c78092efc01fb6"
                    profile_id = {"162372a1-6600-47e1-86cc-d4d504910029":'Darren',"96304ada-1ba3-4a38-abf8-fd949e28cf43":'Azman'}
                    counter = 0
                    newID = ""
                    print ("Verifying Please Wait...")
                    for ID, value in profile_id.items():
                        if name == value:
                            newID = ID
                    helper = VerificationServiceHttpClientHelper.VerificationServiceHttpClientHelper(
                        APIkey)
                    verification_response = helper.verify_file(FILE_NAME, newID)
                    print('Verification Result = {0}'.format(verification_response.get_result()))
                    print('Confidence = {0}'.format(verification_response.get_confidence()))
                    if verification_response.get_result() == "Accept":
                        os.remove(FILE_NAME)
                        print("Verified, Welcome " + value + "!")
                        name = value
                        return name
                    else:
                        counter += 1

                    if counter == 1:
                        voice.speak_text("Please Try Again")
        except:
            voice.speak_text("Please Try Again")
            print ("Please Try Again")
       

def stop_listening():
    print("Stop listening!")
    global listen
    listen = False
    # sys.exit()

def destroy_hearing():
    sys.exit()
