print(f"Starting bot...")

import time
startTime = time.time()

print(f"Importing modules...")

import os

import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


print(f"Importing .env configuration...")

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
SAMPLE_SPREADSHEET_ID = os.getenv('SAMPLE_SPREADSHEET_ID')

class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync(guild = discord.Object(id = 'Server ID')) # Input server ID
            self.synced = True
        print(f"We have logged in as {self.user}.")

client = aclient()
tree = app_commands.CommandTree(client)

print("Initializing Google Authentication...")

# To set up the Sheets API client
creds = None
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)
service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()


print(f"Startup complete!\t[ {(time.time()-startTime):.2f}s ]")

# Command to add a project and its overview to the Collab Tracker sheet. Asks for project name, Discord username, and description.
# The command also adds three reactions for the voting of the project. Once it has collected the information and reposted it on the
# Discord channel, it will update the sheet and let you know that the overview has been uploaded.
@tree.command(name="add", description="Add a project and its overview to the Collab Tracker", guild=discord.Object(id='Server ID')) # Input Server ID
async def self(interaction: discord.Interaction, name: str, description: str):
    await interaction.response.send_message(
        f"Project posted by {interaction.user.mention} \n \nProject Name: {name} \n \nOverview: {description} \n \nVotes please <3 <@&Role ID>") # Input Role ID
    message = await interaction.original_response()
    await message.add_reaction('\U0001F7E2') # Green circle emoji reaction
    await message.add_reaction('\U0001F7E1') # Yellow circle emoji reaction
    await message.add_reaction('\U0001F534') # Red circle emoji reaction
    
    # To convert Discord IDs to the nicknames used in the sheet that has conditional formatting.
    def getNickname(discordID):
        nicknames = { # Names and IDs taken out for privacy
            'ID1': 'Name1',
            'ID2': 'Name2',
            'ID3': 'Name3',
            'ID4': 'Name4',
            'ID5': 'Name5',
            'ID6': 'Name6',
            'ID7': 'Name7',
        }
        return nicknames.get(discordID)

    # The values that will be inputted in the sheet.
    values = [
        ['=NOW()', str(name), getNickname(str(interaction.user.id)), str(description), '', 'Posted in Server']
    ]
    request_body = {
        'values': values
    }
    # Inputting the values in the sheet in a new row.
    sheet.values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID, range='Range 1', valueInputOption='USER_ENTERED', insertDataOption='INSERT_ROWS', body=request_body).execute()
    await message.reply("Project overview uploaded!")



# Command that checks if a given project name is present in the Collab Tracker sheet to avoid duplicates.
@tree.command(name="check", description="Check if a project is present in the Collab Tracker.", guild=discord.Object(id='Server ID')) # Input server ID
async def self(interaction:discord.Interaction, name:str):
    ranges = ['Range 1', 'Range 2', 'Range 3'] # Designating the ranges in the 3 separate sheets
    resultingValues = sheet.values().batchGet(spreadsheetId=SAMPLE_SPREADSHEET_ID, ranges=ranges).execute()
    valueRanges = resultingValues.get('valueRanges', [])
    for i, rangeName in enumerate(ranges): # Going through each range and checking if the value is present
        sheetValues = valueRanges[i].get('values', []) 
        if any(str(name).lower() in value.lower() for row in sheetValues for value in row): # Nested list compregension to iterate over the values in each row
            await interaction.response.send_message(str(name) + " is already in the Collab Tracker! Found it in " + str(rangeName))
            break
    else:
        await interaction.response.send_message(str(name) + " is not present in the Collab Tracker!")

client.run(TOKEN)