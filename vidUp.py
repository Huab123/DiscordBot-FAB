import asyncio
import scrapetube

def getVideo(channelID, limit = 1):
    try:
        videos = scrapetube.get_channel(channel_username=channelID, limit=int(limit))
        videosList = list(videos)
        if not videosList:
            print("No videos found.")
            return None
        lastVideo = videosList[0]
        return lastVideo
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

async def newVid(channelID, channel):
    latestVideoID = None
    while True:
        latestVideo = getVideo(channelID)
        if latestVideo and latestVideoID != latestVideo['videoId']:
            latestVideoID = latestVideo['videoId']
            videoUrl = f'https://www.youtube.com/watch?v={latestVideo['videoId']}'

            try:
                await channel.send(videoUrl)
            except Exception as e:
                print(e)

        await asyncio.sleep(600)  # Check every 60 seconds

