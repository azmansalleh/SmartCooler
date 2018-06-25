import pyaudio
import wave
import bingSpeech
import myluis
import audioop
import time

def startListening():
	while True:

		try:
			FORMAT = pyaudio.paInt16
			CHANNELS = 2
			RATE = 44100
			CHUNK = 1024
			RECORD_SECONDS = 5
			WAVE_OUTPUT_FILENAME = "recording.wav"
			THRESHOLD = 0
			 
			audio = pyaudio.PyAudio()
			 
			# start Recording
			stream = audio.open(format=FORMAT, channels=CHANNELS,
			                rate=RATE, input=True,
			                frames_per_buffer=CHUNK)
			# print "recording..."
			print("calibrating...")

			frames = []
			input_vols = []
			  
			for i in range(0, int(RATE / CHUNK * 2)):
			    data = stream.read(CHUNK)
			    # Get actual input volume levels
			    rms = audioop.rms(data, 2) 
			    # print(rms) 
			    frames.append(data)
			    if rms != 0:
			    	input_vols.append(rms)

			# print("finished recording")
			 

			input_vol_avg = (sum(input_vols)/len(input_vols))
			THRESHOLD = input_vol_avg

			print("AVERAGE = " + str(input_vol_avg))


			while True:	

				for i in range(0, int(RATE / CHUNK * 2)):
				    print('recording')
				    data = stream.read(CHUNK)
				    # Get actual input volume levels
				    rms = audioop.rms(data, 2) 
				    print(rms) 
				    frames.append(data)

				data = stream.read(CHUNK)
				rms = audioop.rms(data,2)
				frames.append(data)
				
				if rms <= THRESHOLD:
					print("silence")
					break

			 
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

			# Run bing to analyze recorded audio file (Speech) and convert to Text
			bingSpeech.main()
			# bingSpeech.getText()


			# myluis.findIntent()
			break

		except:
			print('Try again')
