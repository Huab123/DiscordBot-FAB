from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import getResponse
from tictactoe import tictactoe
from vidUp import newVid


# Load token
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

# Bot Setup
intents: Intents = Intents.default()
intents.message_content = True  # NOQA
client: Client = Client(intents=intents)


# Message Function
async def sendMessage(message: Message, userMessage: str) -> None:

    if command := userMessage[0:4] == '/ah ':
        userMessage = userMessage[4:]

    try:
        if userMessage.startswith('tictactoe'):
            if '2p' in userMessage:
                mentions = message.mentions
                if len(mentions) != 1:
                    await message.channel.send("Please mention one opponent to play against!")
                    return

                opponentID = mentions[0].id
                if opponentID == message.author.id:
                    await message.channel.send("You cannot play against yourself!")
                    return

                # Start a two-player game
                await tikTac(message, mode="pvp", opponentID=opponentID)

            else:
                # Start a game against the computer
                await tikTac(message, mode="pvc")
        elif command:
            response: str = getResponse(userMessage)
            await message.channel.send(response)
    except Exception as e:
        print(e)


# Bot Startup
@client.event
async def on_ready() -> None:
    print(f'{client.user} is now running!')
    client.loop.create_task(getNewVidLoop())

# Incoming messages
@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return

    username: str = str(message.author)
    userMessage: str = message.content
    channel: str = str(message.channel)

    print(f'[{channel}] {username}: "{userMessage}"')
    await sendMessage(message, userMessage)


async def getNewVidLoop():
    while True:
        channelID = input("Channel name (@):")
        discChannel = client.get_channel(1306109885850714204)
        await newVid(channelID, discChannel)


async def tikTac(message, mode="pvc", opponentID=None):
    player1ID = message.author.id
    player2ID = opponentID if mode == "pvp" else None

    discChannel = client.get_channel(1306109885850714204)
    await tictactoe(discChannel, client, player1ID, player2ID, mode)


# Entry Point
def main() -> None:
    client.run(token=TOKEN)


if __name__ == '__main__':
    main()