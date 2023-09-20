import time
import json
from videoaudiomerge import merge
import moviepy.editor as mp 
from googletrans import Translator
import azure.cognitiveservices.speech as speechsdk
from translateusingazure import translateazure
import os, shutil
import wave
from trimwavfile import trim_wav
from mergewavs import merge_wav_files
from fastforward import adjust_speed

class VideoTranslator:
    def __init__(self, video_path, speech_subscription, speech_region, translation_src_lang="en", translation_dest_lang="hi", synthesis_voice="hi-IN-MadhurNeural"):
        self.video_path = video_path
        self.speech_subscription = speech_subscription
        self.speech_region = speech_region
        self.translation_src_lang = translation_src_lang
        self.translation_dest_lang = translation_dest_lang
        self.synthesis_voice = synthesis_voice

    def convert_video_to_audio(self, output_audio_path):
        clip = mp.VideoFileClip(self.video_path)
        clip.audio.write_audiofile(output_audio_path)

    def audio_to_text(self, audio_path):
        speech_config = speechsdk.SpeechConfig(subscription=self.speech_subscription, region=self.speech_region)
        speech_config.speech_recognition_language = "en-US"
        speech_config.output_format = speechsdk.OutputFormat.Detailed
        speech_config.request_word_level_timestamps()
        audio_config = speechsdk.audio.AudioConfig(filename=audio_path)
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
        done = False

        def stop_cb(evt: speechsdk.SessionEventArgs):
            nonlocal done
            done = True
        
        def text(evt: speechsdk.SessionEventArgs):
            self.result += evt.result.text
            json_result = json.loads(evt.result.json)
            self.words += [json_result['NBest'][0]['Words']]

        def empty():
            pass

        # Connect callbacks to the events fired by the speech recognizer
        speech_recognizer.recognizing.connect(empty)
        speech_recognizer.recognized.connect(text)
        speech_recognizer.session_started.connect(empty)
        speech_recognizer.session_stopped.connect(empty)
        speech_recognizer.canceled.connect(empty)
        # Stop continuous recognition on either session stopped or canceled events
        speech_recognizer.session_stopped.connect(stop_cb)
        speech_recognizer.canceled.connect(stop_cb)

        # Start continuous speech recognition
        self.result = ""
        self.words = []
        speech_recognizer.start_continuous_recognition_async()
        while not done:
            time.sleep(0)

        speech_recognizer.stop_continuous_recognition()
        if self.result:
            # print("Detailed results - Word timing:\nWord:\tOffset:\tDuration:")
            # for w in self.words:
            #     for word in w: 
            #         print(f"{word['Word']}\t{word['Offset']//10000000}\t{word['Duration']//10000000}")
            return self.result
        else:
            print("No speech could be recognized.")
            return ""

    def text_to_subtitle(self, video_audio_path):
        self.convert_video_to_audio(video_audio_path)
        self.audio_to_text(video_audio_path)
        self.result=self.result.replace(".",",")
        self.result = self.result.replace(", ",",")
        self.result = self.result.replace(" ,",",")
        self.result = self.result.split(",")
        print(self.result)

        self.resultwords = []
        for i in range(len(self.result)):
            self.resultwords.append(self.result[i].split(" "))
        
        print(self.resultwords)
        j = 0
        b = 0
        self.timestamp = []
        for word in self.words:
            for w in word:
                if w['Word'] == self.resultwords[j][b].lower() and b == 0:
                    temp = {"sentence":self.result[j],"start":w['Offset']}
                    b=-1
                elif w['Word'] == self.resultwords[j][b].lower() and b == -1:
                    temp['end'] = w['Offset']+w['Duration']
                    temp['duration'] = temp['end'] - temp['start']
                    self.timestamp.append(temp)
                    j+=1
                    b=0
        print(self.timestamp)
        print(len(self.result))
        print(len(self.timestamp))
        # self.words
    def translate_text(self, text, lang):
        translator = Translator()
        translation = translator.translate(text, src=self.translation_src_lang, dest=lang)
        return translation.text
    
    def translate_caption(self, langs):
        for i in self.timestamp:
            temp = {}
                # temp[lang] = self.translate_text(i['sentence'],lang)
            print(translateazure(i['sentence'],langs))
            ans = translateazure(i['sentence'],langs)[0]['translations']
            for j in ans:
                temp[j['to']] = j['text']
            i['translated'] = temp
        
        print(self.timestamp)
            

    def translate_and_synthesize(self, video_audio_path):
        # self.convert_video_to_audio(video_audio_path)
        # text_from_audio = self.audio_to_text(video_audio_path)

        # if text_from_audio:
        #     translated_text = self.translate_text(text_from_audio)
        #     if translated_text:
        #         speech_config = speechsdk.SpeechConfig(subscription=self.speech_subscription, region=self.speech_region)
        #         speech_config.speech_synthesis_voice_name = self.synthesis_voice
        #         speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)
        #         result = speech_synthesizer.speak_text_async(translated_text).get()

        #         if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        #             stream = speechsdk.AudioDataStream(result)
        #             stream.save_to_wav_file(output_audio_path)
        #             print("Audio Translated")
        #         else:
        #             print("Translation synthesis failed.")
        #     else:
        #         print("Translation of text failed.")
        # else:
        #     print("Audio to text conversion failed.")
        self.text_to_subtitle(video_audio_path)
        with open("language.json") as json_file:
            self.lang = json.load(json_file)
        self.translate_caption(self.lang)
        self.createaudios()

    def text_to_speech(self,counter,translate_sentence,translate_to,path,duration):
        speech_config = speechsdk.SpeechConfig(subscription=self.speech_subscription, region=self.speech_region)
        self.speech_synth = {"hi":"hi-IN-MadhurNeural","ta":"ta-IN-ValluvarNeural","te":"te-IN-MohanNeural","bn":"bn-IN-BashkarNeural","ur":"ur-IN-SalmanNeural","ne":"ne-NP-SagarNeural","gu":"gu-IN-NiranjanNeural","mr":"mr-IN-ManoharNeural","ml":"ml-IN-MidhunNeural","kn":"kn-IN-GaganNeural"}
        speech_config.speech_synthesis_voice_name = self.speech_synth[translate_to]
        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)
        result = speech_synthesizer.speak_text_async(translate_sentence).get()
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            stream = speechsdk.AudioDataStream(result)
            val = path+"/"+translate_to+"/"+str(counter)+".wav"
            stream.save_to_wav_file(val)
            with wave.open(val,"r") as wf:
                duration_seconds = wf.getnframes() / wf.getframerate()
            speaking_rate=(duration_seconds/duration)
#            adjust_speed(val,speaking_rate)            
            # speech_config.speech_rate = (duration_seconds/duration)*100
            # speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)
            # result = speech_synthesizer.speak_text_async(translate_sentence).get()
            # print(result,duration,duration_seconds)
            # if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            #     stream = speechsdk.AudioDataStream(result)
            #     val = path+"/"+translate_to+"/"+str(counter)+".wav"
            #     stream.save_to_wav_file(val)
        else:
            print("Translation synthesis failed.")

    def createaudios(self):
        self.audiofiles = {}
        temp = 0
        counter = 1
        shutil.rmtree("audios")
        os.mkdir("audios")
        for i in self.lang:
            os.mkdir("audios/"+i)
        i = 0

        while (i<len(self.timestamp)):
            if(temp!=self.timestamp[i]["start"]):
                for f in self.lang:
                    trim_wav("convert.wav","audios/"+f+"/"+str(counter)+".wav",temp/10000000,self.timestamp[i]["start"]/10000000)
                temp = self.timestamp[i]["start"]
            else:
                for f in self.lang:
                    self.text_to_speech(counter,self.timestamp[i]["translated"][f],f,"audios",self.timestamp[i]["duration"]/10000000)
                temp = self.timestamp[i]["end"]
                i+=1

            counter += 1
        
        merge_wav_files(counter,self.lang)
        merge(self.lang)
# Example usage:
translator = VideoTranslator("file.mp4", "73aa00a13a4b4784ae4cb86be3a91cba", "eastus")
translator.translate_and_synthesize("convert.wav")


