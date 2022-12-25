import discord
import youtube_dl

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as', client.user)

@client.event
async def on_message(message):
    # If the message is from the bot itself, ignore it
    if message.author == client.user:
        return

    if message.content.startswith('!play'):
        # Get the video URL from the message
        video_url = message.content.split(' ')[1]

        # Use youtube-dl to get the audio from the video
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            audio_url = info['url']

        # Connect to the voice channel and play the audio
        voice_channel = message.author.voice.channel
        vc = await voice_channel.connect()
        vc.play(discord.FFmpegPCMAudio(audio_url))
        while vc.is_playing():
            await asyncio.sleep(1)
        vc.disconnect()

client.run('YOUR_BOT_TOKEN_HERE')
