from moviepy.editor import VideoFileClip

class convert:
    def __init__(self, filename):
        self.video_clip = VideoFileClip(filename)
        self.audio_clip = self.video_clip.audio
        self.audio_clip.write_audiofile("audio.wav")
        print("Extracted Audio Successfully")
