from pytube import YouTube, Playlist
import os
from pytube.cli import on_progress
import math
import time
from moviepy.video.io.ffmpeg_tools import ffmpeg_merge_video_audio
import urllib.request
import random

link = input("Enter YouTube url: ")
choose = int(input("Video(1) Audio(2) Thumbnail(3): "))


def convert_size(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])


def download_thumbnail(url):
    yt = YouTube(url)
    x = ["sddefault.jpg", "hqdefault.jpg"]
    for t in x:
        thumbnail = yt.thumbnail_url.replace(t, "maxresdefault.jpg")

    urllib.request.urlretrieve(thumbnail, f"{random.randint(1000000, 9999999)}.jpg")


def download_audio(url):
        yt = YouTube(url, on_progress_callback=on_progress)
        video = yt.streams.filter(only_audio=True).first()
        print("Downloading audio...")
        video.download()

        time.sleep(0.5)

        video_title = video.get_file_path().split("\\")[-1]

        os.rename(video_title, f'{video_title[:-4]}.mp3')
        print(" ")
        print("Downloaded audio!")


def download_video(url):
        yt = YouTube(url, on_progress_callback=on_progress)
        print("\nFetching video...")
        ys = yt.streams.filter(only_video=True)

        for s in ys:
            print(f"{s.itag}: Res: {s.resolution}, Format: {s.mime_type} Filesize: {convert_size(s.filesize)}")


        itag = input("Enter the number: ")
        ysf = yt.streams.get_by_itag(int(itag))
        

        if ysf.is_progressive == True:
            print(f"\nDownloading...\nTitle: {ysf.title}\nQuality: {ysf.resolution}\nSize: {convert_size(ysf.filesize)}")
            ysf.download()
        else:
            print(f"\nDownloading...\nTitle: {ysf.title}\nQuality: {ysf.resolution}\nSize: {convert_size(ysf.filesize)}")

            download_audio(link)

            extension = ysf.mime_type.replace("video/", "")
            print("Downloading video...")
            ysf.download()
            path = ysf.get_file_path()

            print(" ")
            print("Finishing up...")

            ysf_title = path.split("\\")[-1]

            if ysf_title.endswith(".webm"):
                aud_name = ysf_title[:-5]  + ".mp3"
                out_name = ysf_title[:-5]  + "-f.mp4"
            elif ysf_title.endswith(".mp4"):
                aud_name = ysf_title[:-4] + ".mp3"
                out_name = ysf_title[:-4] + "-f.mp4"

            ffmpeg_merge_video_audio(ysf_title,
                                     aud_name,out_name,
                                     vcodec='copy',
                                     acodec='copy',
                                     ffmpeg_output=False,
                                     logger=None)

            os.remove(ysf_title)
            os.remove(aud_name)
            os.rename(out_name, ysf_title[:-6]+".mp4")
            print("Done!")
            
            


if choose == 1:
    download_video(link)
elif choose == 2:
    download_audio(link)
elif choose == 3:
    download_thumbnail(link)
else:
    print("Please type 1,2 or 3!")
        



