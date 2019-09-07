print(" -------------------------------------------------")
print("| Running Youtube-Media-Schedular for Plex-Server  |")
print(" -------------------------------------------------")

from pytube import YouTube
from tqdm import tqdm
import json

local_queue = {}

pbar = tqdm(total=100)

def progress_func(self, stream, chunk, file_handle):
  #size = self.video.filesize
  pbar.update(10)


def downloadVideo(url):
    try:
        details = YouTube(url, on_progress_callback=progress_func)
        print("Downloading --> ", details.title)
        yt = details.streams.filter(subtype='mp4', res='360p').first()


        yt.download(output_path='/home/jayesh/Videos', filename=details.title)
        pbar.close()
        return 1
    except():
        print('Exception occurred...')
        return 0


#Permenant List storage using json file
with open('queue.json', 'r+') as queue:
    local_queue = json.loads(queue.read())

print(local_queue)

if(not local_queue):
    print('Nothing Queued...')
    exit()
elif(len(local_queue) > 0):
    for vid,stat in local_queue.items():
        if stat not in ('failed', 'done'):
            return_code = downloadVideo(vid)
            if(return_code == 0):
                local_queue[vid] = 'failed'
            else:
                local_queue[vid] = 'done'


print('Queue completed. Updating the queue json.')

with open('queue.json', 'r+') as queue:
    json.dump(local_queue, queue)


