import os
import random
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip, clips_array, vfx, afx
from PIL import Image
import numpy as np

input_folder = "videos"
output_folder = "ready"

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Define the available fps options
fps_options = [24, 30, 60]

for filename in os.listdir(input_folder):
    if filename.endswith(".mp4"):
        video_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)

        # Step 1: Remove metadata
        video = VideoFileClip(video_path)
        video = video.copy().resize((video.w, video.h))

        # Step 2: Remove sound
        # video = video.without_audio()
        # Step 3: Speed - 0.9x
        video = video.fx(vfx.speedx, 0.9)

        # Step 4: Mirror video
        # video = video.fx(vfx.mirror_x)

        audio = video.audio

        # Add a little bit of noise to the audio
        audio = afx.audio_loop(afx.audio_fadein(afx.audio_fadeout(audio, 1), 1), nloops=10, duration=audio.duration)


        # Step 5: Rotate by +1 degree
        video = video.rotate(1)

        # Step 6: Overlay png picture on video
        overlay_image = Image.open("overlay.png")
        overlay_array = np.array(overlay_image)
        overlay_clip = ImageClip(overlay_array, ismask=False)
        overlay_clip = overlay_clip.resize(video.size)
        overlay_clip = overlay_clip.set_duration(video.duration)

        # Merge the audio with the processed video
        video = video.set_audio(audio)

        # Choose a random fps from available options
        final_fps = random.choice(fps_options)

        # Change the frame rate (fps) of the video
        video = video.set_fps(final_fps)

        # Get original video codec from file extension
        original_video_codec = filename.split('.')[-1]

        # Generate random video codec that is different from the original video codec
        video_codec_options = ['libx264', 'mpeg4', 'mp4']
        video_codec_options.remove(original_video_codec)  # Remove original video codec from options
        final_video_codec = random.choice(video_codec_options)

        # Get original audio codec
        original_audio_codec = audio.clips[0].reader.acodec

        # Generate random audio codec that is different from the original audio codec
        audio_codec_options = ['aac', 'pcm_s16le']
        audio_codec_options.remove(original_audio_codec)  # Remove original audio codec from options
        final_audio_codec = random.choice(audio_codec_options)

        # Generate random bitrate for video encoding
        final_bitrate = f"{random.randint(2000, 5000)}k"

        # Export the final video
        final_clip = CompositeVideoClip([video, overlay_clip])
        print(final_video_codec, final_audio_codec, final_bitrate)
        final_clip.write_videofile(output_path, codec=final_video_codec, audio_codec=final_audio_codec, bitrate=final_bitrate)