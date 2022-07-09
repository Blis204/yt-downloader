from pytube import YouTube, Playlist
import os
from pytube.cli import on_progress
import math
import time
from moviepy.video.io.ffmpeg_tools import ffmpeg_merge_video_audio

link = input("Enter YouTube url: ")
choose = int(input("Video(1) Audio(2): "))


def convert_size(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])

def download_audio(url):
        yt = YouTube(url, on_progress_callback=on_progress)
        video = yt.streams.filter(only_audio=True).first()
        print("Downloading audio...")
        video.download()

        extension = video.mime_type.replace("audio/", "")

        time.sleep(0.5)

        video_title = video.title.translate({ord(i): None for i in '~"#%&*:<>?/\{|}.'})

        os.rename(f'{video_title}.{extension}', f'{video_title}.mp3')
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

            print(" ")
            print("Finishing up...")

            ysf_title = ysf.title.translate({ord(i): None for i in '~"#%&*:<>?/\{|}.'})

            vid_name = f'{ysf_title}.{extension}'
            aud_name = f'{ysf_title}.mp3'
            out_name = f'{ysf_title}-Finished.mp4'
            fps = ysf.fps

            ffmpeg_merge_video_audio(vid_name,
                                     aud_name,out_name,
                                     vcodec='copy',
                                     acodec='copy',
                                     ffmpeg_output=False,
                                     logger=None)

            os.remove(vid_name)
            os.remove(aud_name)
            print("Done!")
            
            


if choose == 1:
    download_video(link)
elif choose == 2:
    download_audio(link)
else:
    print("Please type 1 or 2!")
        



