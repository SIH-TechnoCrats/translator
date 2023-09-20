import wave

def trim_wav(input_wav, output_wav, start_time, end_time):
    """
    Trim a .wav audio file based on start and end time.

    Parameters:
    input_wav (str): Input .wav audio file path.
    output_wav (str): Output trimmed .wav audio file path.
    start_time (float): Start time in seconds.
    end_time (float): End time in seconds.
    """
    # Open the input .wav file
    with wave.open(input_wav, 'rb') as wav_in:
        framerate = wav_in.getframerate()
        start_frame = int(start_time * framerate)
        end_frame = int(end_time * framerate)

        # Set parameters for the output .wav file
        with wave.open(output_wav, 'wb') as wav_out:
            wav_out.setparams(wav_in.getparams())
            wav_out.setnframes(end_frame - start_frame)

            # Read and write audio frames
            wav_in.setpos(start_frame)
            frames = wav_in.readframes(end_frame - start_frame)
            wav_out.writeframes(frames)

# # Example usage:
# input_wav = "c:/Users/tanma/Downloads/convert.wav"  # Replace with your input WAV file path
# output_wav = "output.wav"  # Replace with the desired output WAV file path
# start_time = 10  # Replace with the start time in seconds
# end_time = 30    # Replace with the end time in seconds

# trim_wav(input_wav, output_wav, start_time, end_time)
