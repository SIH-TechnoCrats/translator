import videotoaudio
import audiotosrt
import whisper

if __name__ == "__main__":
    #videotoaudio.convert("Test1.mp4")
    whisper_model = whisper.load_model("large")
    transcription = whisper_model.transcribe("audio.wav", fp16=False)
    print(transcription)
