
import asyncio
import sys
import threading
import numpy as np






on_what = 0
phrases = []
listen = True


def initiate_hearing():
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


    print("Beginning to listen with a silent audio level of " + str(silent_audio_level))

    while True:
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
            FILE_NAME="data/request"+str(on_what)+".wav"

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
                if consecutive_nothings > 70:
                    if started == False:
                        frames = []
                    else:
                        break

                data=stream.read(CHUNK, exception_on_overflow = False)
                data_chunk=array('h',data)
                vol=max(data_chunk)
                if(vol>=silent_audio_level * 7):
                    consecutive_spikes = consecutive_spikes + 1
                    if consecutive_spikes == 5:
                        if started is False:
                            started = True
                            consecutive_nothings = 0
                            print("Began recording data at volume of " + str(vol))
                    frames.append(data)
                    # print("True audio..")

                    print("recording...")
                    consecutive_nothings = 0
                elif (vol < silent_audio_level * 3):
                    # if started is True:
                        # frames.append(data)
                    if vol < silent_audio_level*3:
                        consecutive_spikes = 0
                        consecutive_nothings += 1

                    frames.append(data)

                else:
                    frames.append(data)

            #end of recording

            if listen == False or started == False or len(frames) < 10:
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





    #     ms_asr.get_speech_token()
    #     text, confidence = ms_asr.transcribe('data/recording.wav')
    #     print "Text: ", text
    #     print "Confidence: ", confidence
        # s = threading.Thread(name=FILE_NAME, target=client.analyze, args=[FILE_NAME])
        # s.start()
def start_listening():


    global listen

    print("Resume listening...")
    listen = True

        # print "Text: ", text
        # print "Confidence: ", confidence


        # future = asyncio.run_coroutine_threadsafe(client.start(api_key,language,response_format,recognition_mode,FILE_NAME), loop)
        # result = future.result(timeout)
          # Wait for the result with a timeout
         # client.start(api_key,language,response_format,recognition_mode,FILE_NAME)
#         loop = client.asyncio.get_event_loop()
# # Blocking call which returns when the display_date() coroutine is done
#         loop.run_until_complete(client.start(api_key,language,response_format,recognition_mode,FILE_NAME))
#         loop.close()

        # client.start(api_key,language,response_format,recognition_mode,FILE_NAME)
        # asyncio.run_coroutine_threadsafe(client.start(api_key,language,response_format,recognition_mode,FILE_NAME), client.asyncio.get_event_loop())
#
        # phrase = asyncio.client.start(api_key,language,response_format,recognition_mode,FILE_NAME)
        # print(phrase)
        # phrases.append(phrase)

    # print(client.record_voice(FILE_NAME))

def stop_listening():
    print("Stop listening!")
    global listen
    listen = False
    # sys.exit()

def destroy_hearing():
    sys.exit()
