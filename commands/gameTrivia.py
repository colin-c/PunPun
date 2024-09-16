import os
import random
import discord
import requests
import random
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

# where trivia answer is stored
current_trivia = {}

# IGDG API Credentials
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
IGDB_API_URL = os.getenv('IGDB_API_URL')

# Gets the API token for
def get_IGDB_token():
    AUTH_URL = os.getenv('AUTH_URL')

    auth_response = requests.post(AUTH_URL, {
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
    'grant_type': 'client_credentials'
    })

    auth_response.raise_for_status()
    return auth_response.json()['access_token']

# Gets the current number of games saved in the database
def get_total_games(token):
    IGDB_URL = os.getenv('IGDB_API_URL') + '/count'

    header = {
            'Client-ID': CLIENT_ID,
            'Authorization': 'Bearer ' + token,
        }
    
    response = requests.post(IGDB_URL, headers=header)
    response.raise_for_status()
    return response.json()['count']

# Gets the cover for the game
def get_cover(token, cover_id):
    IGDB_URL = 'https://api.igdb.com/v4/covers'

    header = {
            'Client-ID': CLIENT_ID,
            'Authorization': 'Bearer ' + token,
        }
    
    body = f"fields url; where id = {cover_id};"
    response = requests.post(IGDB_URL, headers=header, data=body)
    response.raise_for_status()
    data = response.json()
    if data:
        return data[0]['url'].replace('t_thumb', 't_cover_big')
    else:
        return None

# Use API to get the game and its summar
def game_trivia():
    token = get_IGDB_token()
    total_games = get_total_games(token)
    random_game = random.randint(0, total_games - 1)
    header = {
        'Client-ID': CLIENT_ID,
        'Authorization': 'Bearer ' + token,
    }

    body = f"fields name,summary,cover; limit 1; offset {random_game};"
    response = requests.post(IGDB_API_URL, headers=header, data=body)
    response.raise_for_status()
    data = response.json()
    game = data[0]
    cover = None

    # checks if there is a cover for the game
    if 'cover' in game:
        cover_id = game['cover']
        cover = get_cover(token, cover_id)
        print(cover)


    question = f"What is the name this game: {game['summary']}"
    answer = game['name']
    return question, answer, cover


# contains all commands for Game Trivia
class gameTrivia(commands.Cog):
    def __init___(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Game Trivia File Loaded")

    @commands.command()
    async def trivia(self, ctx):
        user_id = ctx.author.id
        question, answer, cover = game_trivia()
        current_trivia[user_id] = {'answer' : answer, 'cover': cover}
        message = discord.Embed(title=f"Game Trivia", description=f"{question}", color=discord.Color.blue())
        await ctx.send(embed = message)
    
    @commands.command()
    async def answer(self, ctx, *, user_answer: str):
        user_id = ctx.author.id

        if user_id in current_trivia:
            correct_answer = current_trivia[user_id]['answer']
            cover = current_trivia[user_id]['cover']
            
            print(correct_answer)
            print(cover)

            if user_answer.lower() == correct_answer.lower():
                message = discord.Embed(title=f"Game Trivia", description=f"Correct! The game was {correct_answer}.", color=discord.Color.green())

            else:
                message = discord.Embed(title=f"Game Trivia", description=f"Wrong! The correct answer was {correct_answer}.", color=discord.Color.red())

            if cover:
                message.set_image(url=cover)
            
            await ctx.send(embed=message)
            del current_trivia[user_id]

        else:
            await ctx.send("Please start a trivia by typing b!trivia.")


async def setup(client):
    await client.add_cog(gameTrivia(client))