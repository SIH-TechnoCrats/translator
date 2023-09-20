from pydub import AudioSegment

def merge_wav_files(count,lang, output_wav="output.wav"):
    """
    Merge multiple .wav audio files into a single .wav file.

    Parameters:
    input_wav_files (list): List of input .wav file paths to merge.
    output_wav (str): Output merged .wav file path.
    """
    # Initialize an empty audio segment to hold the merged audio
    

    # Iterate through the input .wav files and append them to the merged audio
    for l in lang:
        merged_audio = AudioSegment.empty()
        for i in range(1,count):
            audio_segment = AudioSegment.from_file("audios/"+l+"/"+str(i)+".wav", format="wav")
            merged_audio += audio_segment
        merged_audio.export("output"+l+".wav", format="wav")

    # Export the merged audio to the output .wav file
    merged_audio.export(output_wav, format="wav")

# Example usage:
# input_wav_files = ["convert.wav", "output.wav", "file.wav"]  # Replace with your input WAV file paths
# output_wav = "output.wav"  # Replace with the desired output WAV file path

# merge_wav_files(input_wav_files, output_wav)

