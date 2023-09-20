from pydub import AudioSegment

def adjust_speed(wav_file_path, speed):
    """Adjusts the speed of the given wav file.

    Args:
        wav_file_path (str): The path to the wav file.
        speed (float): The speed factor. A value of 1.0 is the original speed.

    Returns:
        The adjusted wav file.
    """
    print("setting speed",speed)

    audio = AudioSegment.from_file(wav_file_path,format="wav")
    if(speed>1):
        adjusted_audio = audio.speedup(playback_speed=speed)
    else:
        adjusted_audio = audio.speeddown(playback_speed=speed)
    #wav_file = wav_file.set_frame_rate(int(wav_file.frame_rate * speed))
    adjusted_audio.export(wav_file_path, format="wav")
