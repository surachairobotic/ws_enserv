from moviepy.editor import VideoFileClip

def compress_video(input_file, output_file, bitrate='250k'):
    # Load the video clip
    clip = VideoFileClip(input_file)

    # Write the compressed video to a new file with specified bitrate
    clip.write_videofile(output_file, codec='libx264', audio_codec='aac', ffmpeg_params=['-b:v', bitrate])

    print("Video compression complete.")

# Example usage
input_video = "C:/Users/surachair/Videos/2024-01-01_18-04-15.mp4"
output_video = "C:/Users/surachair/Videos/2024-01-01_18-04-15_reduce.mp4"
compress_video(input_video, output_video)
