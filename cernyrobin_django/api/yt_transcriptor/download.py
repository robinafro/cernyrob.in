from pytube import YouTube
from moviepy.video.io.VideoFileClip import VideoFileClip
from colorama import Fore
import os

def download_and_convert_audio(youtube_url, output_dir, name, output_format="wav", temp_format="mp4"):
    print(f"{Fore.YELLOW}Downloading video from {youtube_url}...{Fore.RESET}")

    video_path = os.path.join(output_dir, f"temp_video.{temp_format}")
    audio_path = os.path.join(output_dir, f"{name}.{output_format}")

    youtube = YouTube(youtube_url)
    video = youtube.streams.filter().first()
    video.download(output_path=output_dir, filename=f"temp_video.{temp_format}")
    
    print(f"{Fore.YELLOW}Converting video to audio ({output_format})...{Fore.RESET}")

    video_clip = VideoFileClip(video_path)
    audio_clip = video_clip.audio
    audio_clip.write_audiofile(audio_path)
    
    print(f"{Fore.GREEN}Successfully downloaded and converted video to audio.{Fore.RESET}")
    
    video_clip.close()
    audio_clip.close()
    os.remove(video_path)

    return audio_path