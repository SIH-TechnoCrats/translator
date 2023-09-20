from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
import os

def merge(lang):
    
    video_clip = VideoFileClip("file.mp4")
    video_clip = video_clip.without_audio()
    for i in lang:
        title = "final"+i
        audio_clip = AudioFileClip("output"+i+".wav")
        final_clip = video_clip.set_audio(audio_clip)
        final_clip.write_videofile(title + ".mp4")
