import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence

class Converter:
    def __init__(self, audio_file):
        self.audio_file = audio_file
        self.recognizer = sr.Recognizer()

    def convert_to_srt(self):
        audio = AudioSegment.from_wav(self.audio_file)
        audio_segments = split_on_silence(audio, silence_thresh=-50)

        srt_lines = []
        start_time = 0

        for i, segment in enumerate(audio_segments):
            with sr.AudioFile(segment.export(format="wav")) as source:
                audio_data = self.recognizer.record(source)
                try:
                    text = self.recognizer.recognize_google(audio_data)
                except sr.UnknownValueError:
                    text = ""

            end_time = start_time + len(segment) / 1000  # Convert milliseconds to seconds

            srt_line = f"{i + 1}\n{start_time:.3f} --> {end_time:.3f}\n{text}\n"
            srt_lines.append(srt_line)

            start_time = end_time

        srt_filename = "output.srt"
        with open(srt_filename, "w") as srt_file:
            srt_file.writelines(srt_lines)

        print(f"SRT file '{srt_filename}' created successfully.")


