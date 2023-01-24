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

import requests
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

print(f"Importing .env configuration...")

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
SAMPLE_SPREADSHEET_ID = os.getenv('SAMPLE_SPREADSHEET_ID')
DISCORD_SERVER_ID = os.getenv('DISCORD_SERVER_ID')
LINEAR_API = os.getenv('LINEAR_API')

class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync(guild = discord.Object(id=DISCORD_SERVER_ID))
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

# To convert Discord IDs to the nicknames used in the sheet that has conditional formatting as well as the Linear
# Nicknames and IDs have been removed for privacy
def getNickname(discordID):
    nicknames = {
        'ID1': 'N1',
        'ID2': 'N2',
        'ID3': 'N3',
        'ID4': 'N4',
        'ID5': 'N5',
        'ID6': 'N6',
        'ID7': 'N7',
        }
    return nicknames.get(discordID)

# To convert nicknames to Discord IDs
# Nicknames and IDs have been removed for privacy
def getDiscordID(nickname):
    discordIDs = {
        'N1': 'ID1',
        'N2': 'ID2',
        'N3': 'ID3',
        'N4': 'ID4',
        'N5': 'ID5',
        'N6': 'ID6',
        'N7': 'ID7',
        }
    return discordIDs.get(nickname)

# To convert nicknames (and in the /approve command, the collab_manager field) to Linear IDs
# Nicknames and IDs have been removed for privacy
def getLinearID(nickname):
    linearIDs = {
        'N1': 'ID1',
        'N2': 'ID2',
        'N3': 'ID3',
        'N4': 'ID4',
        'N5': 'ID5',
        'N6': 'ID6',
        'N7': 'ID7',
        }
    return linearIDs.get(nickname)

# Command to add a project and its overview to the Collab Tracker sheet. Asks for project name, Discord username, and description.
# The command also adds three reactions for the voting of the project. Once it has collected the information and reposted it on the
# Discord channel, it will update the sheet and let you know that the overview has been uploaded.
@tree.command(name="add", description="Add a project and its overview to the Collab Tracker", guild=discord.Object(id=DISCORD_SERVER_ID))

# The following lines serve as decorators/instructions for each inputted field
@app_commands.describe(name="Enter the project's name")
@app_commands.describe(contact="Enter your contact's name (N/A is fine)")
@app_commands.describe(supply="Enter the project's supply (TBD is fine)")
@app_commands.describe(mint_price="Enter the project's mint price (TBD is fine)")
@app_commands.describe(overview="Enter the project's overview")
@app_commands.describe(links="Enter the project's links")
@app_commands.describe(contract_auditing="Will the contract be audited?")
@app_commands.describe(team_doxxed="Is the team doxxed?")

# The choices for the contract_auditing field
@app_commands.choices(contract_auditing=[
    discord.app_commands.Choice(name='Contract audited and will be released before mint', value=1),
    discord.app_commands.Choice(name='Contract not audited but will be released before mint', value=2),
    discord.app_commands.Choice(name='Contract audited but will not be released before mint', value=3),
    discord.app_commands.Choice(name='Contract will not be audited and will not be released before mint', value=4),
    discord.app_commands.Choice(name='Unsure if contract will be audited or if it will be released before mint', value=5),
])

# The choices for the team_doxxed field
@app_commands.choices(team_doxxed=[
    discord.app_commands.Choice(name='Yes', value=1),
    discord.app_commands.Choice(name='No', value=2),
    discord.app_commands.Choice(name='Partially', value=3),
    discord.app_commands.Choice(name='Unsure', value=4),
])

async def self(
    interaction: discord.Interaction,
    name: str,
    contact: str,
    supply: str,
    mint_price: str, 
    overview: str,
    links: str,
    contract_auditing: discord.app_commands.Choice[int],
    team_doxxed: discord.app_commands.Choice[int]):
    team_role = discord.utils.get(interaction.guild.roles, id=YOUR_TEAM_ID) # To prepare the role mention. Insert role ID here.

    # Sending the message with all the info + role mention
    await interaction.response.send_message(
        f"**Project posted by:** {interaction.user.mention} \n\n**Project Name:** {name} \n\n**Contact:** {contact} \n\n**Supply:** {supply}\
            \n\n**Mint Price:** {mint_price} \n\n**Overview:** {overview} \n\n**Links:** {links} \n\n**{contract_auditing.name}.**\
            \n\n**Team Doxxed?** {team_doxxed.name}")
    
    # Adding the reactions to the message
    message = await interaction.original_response()
    await message.add_reaction('\U0001F7E2') # Green circle emoji reaction
    await message.add_reaction('\U0001F7E1') # Yellow circle emoji reaction
    await message.add_reaction('\U0001F534') # Red circle emoji reaction

    # The values that will be inputted in the sheet.
    values = [
        ['', str(name), getNickname(str(interaction.user.id)), "Contact: " + str(contact) + "\n" + str(overview) 
        + "\n \nSupply: " + str(supply) + "\nMint Price: " + str(mint_price) + "\n\nLinks: " + str(links) + "\n\n" 
        + str(contract_auditing.name) + "\nTeam Doxxed?: " + str(team_doxxed.name), '', 'Posted in Server']
    ]
    request_body = {
        'values': values
    }
    # Inputting the values in the sheet in a new row.
    sheet.values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID, range='YOUR_RANGE1', valueInputOption='USER_ENTERED', insertDataOption='INSERT_ROWS', body=request_body).execute()
    await message.reply("Project overview uploaded! \n\nVotes please <3 " + str(team_role.mention))



# Command that checks if a given project name is present in the Collab Tracker sheet to avoid duplicates.
@tree.command(name="check", description="Check if a project is present in the Collab Tracker", guild=discord.Object(id=DISCORD_SERVER_ID))
async def self(interaction:discord.Interaction, name:str):
    ranges = ['YOUR_RANGE1', 'YOUR_RANGE2', 'YOUR_RANGE3'] # Designating the ranges in the 3 separate sheets
    resultingValues = sheet.values().batchGet(spreadsheetId=SAMPLE_SPREADSHEET_ID, ranges=ranges).execute()
    valueRanges = resultingValues.get('valueRanges', [])
    for i, rangeName in enumerate(ranges): # Going through each range and checking if the value is present
        sheetValues = valueRanges[i].get('values', []) 
        if any(str(name).lower() in value.lower() for row in sheetValues for value in row): # Nested list compregension to iterate over the values in each row
            await interaction.response.send_message(str(name) + " is already in the Collab Tracker! Found it in " + str(rangeName)[:-4])
            break
    else:
        await interaction.response.send_message(str(name) + " is not present in the Collab Tracker!")

# Query to fetch issueLabels, teams, and users from Linear App
query = gql('''
    query {
        issueLabels {
            nodes {
                id
                name
            }
        }
        teams {
            nodes {
                id
                name
            }
        }
        users {
            nodes {
            id
            name  
            }
        }
    }
''')

# Use the requests transport to send the query
transport = RequestsHTTPTransport(
    url='https://api.linear.app/graphql',
    headers={
        "Content-type": "application/json",
        "Authorization": "Bearer " + LINEAR_API # Linear Personal API Key
    },
    use_json=True,
)

# Create the client
linear_client = Client(transport=transport)

# Send the request
response = linear_client.execute(query)

# Print the issueLabel names and IDs
for issueLabel in response['issueLabels']['nodes']:
    print("Issue name: " + issueLabel['name'] + " ID: " + issueLabel['id'])

# Print the team names and IDs
for team in response['teams']['nodes']:
    print("Team name: " + team['name'] + " ID: " + team['id'])

# Print the user names and IDs
for user in response['users']['nodes']:
    print("User name: " + user['name'] + " ID: " + user['id'])


# Command that through Linear App integration automatically creates a task assigned to a set user to DM a project on Twitter
@tree.command(name="dm", description="Create a Linear issue to DM a Project's Twitter.", guild=discord.Object(id=DISCORD_SERVER_ID))

# The following lines serve as decorators/instructions for each inputted field
@app_commands.describe(project_name="Enter the project's name")
@app_commands.describe(project_twitter="Enter the project's Twitter (without the @)")

async def self(
    interaction: discord.Interaction,
    project_name: str, 
    project_twitter: str):

    # Define the GraphQL mutation
    mutation = gql('''
        mutation createIssue($input: IssueCreateInput!) {
            issueCreate(input: $input) {
                success
                issue {
                    id
                }
            }
        }
    ''')
    
    # Define the variables for the mutation
    variables = {
        "input": {
            "teamId": "YOUR_TEAM_ID", # Input Linear team ID here
            "title": "DM " + str(project_name) + " on Twitter @" + str(project_twitter),
            "description": "Requested by " + getNickname(str(interaction.user.id)) + "\n\n https://twitter.com/" + str(project_twitter),
            "assigneeId": "ASSIGNEE_ID", # Input the Linear ID of the person you want to assign this task to
            "labelIds": "LABEL_ID" # Input the Label IDs here
        }
    }
    # Use the requests transport to send the query
    transport = RequestsHTTPTransport(
        url='https://api.linear.app/graphql',
        headers={
            "Content-type": "application/json",
            "Authorization": "Bearer " + LINEAR_API # Linear Personal API Key
        },
        use_json=True,
    )

    # Create the client
    linear_client = Client(transport=transport)
    # Send the request to the Linear API
    response = linear_client.execute(mutation, variables)
    issue_id = response["issueCreate"]["issue"]["id"]
    # Send a message to the discord channel with the issue id
    await interaction.response.send_message(f"**Issue created:** DM " + str(project_name) + " on Twitter @" + str(project_twitter))

# Command that through Linear App integration automatically creates a task when a project is approved
# It asks for the Project Name, the Collab Manager that brought in the project, and a Choice between if it was approved
# with a call or without one. This will be assigned to the Collab Manager through linear
@tree.command(name="approve", description="Approve a project and create a task on Linear to finalize the project", guild=discord.Object(id=DISCORD_SERVER_ID))

# The following lines serve as decorators/instructions for each inputted field
@app_commands.describe(project_name="Enter the project's name")
@app_commands.describe(contact="Enter the contact given (N/A is fine)")
@app_commands.describe(collab_manager="What collab manager posted this collab?")
@app_commands.describe(call_needed="Is a call needed?")

# The choices for the collab manager field
@app_commands.choices(collab_manager=[ # Names taken out for privacy
    discord.app_commands.Choice(name='CM1', value=1),
    discord.app_commands.Choice(name='CM2', value=2),
    discord.app_commands.Choice(name='CM3', value=3),
    discord.app_commands.Choice(name='CM4', value=4),
    discord.app_commands.Choice(name='CM5', value=5),
    discord.app_commands.Choice(name='CM6', value=6),
    discord.app_commands.Choice(name='CM7', value=7)
])

# The choices for the call needed field
@app_commands.choices(call_needed=[
    discord.app_commands.Choice(name='Call needed', value=1),
    discord.app_commands.Choice(name='No call needed', value=2)
])

async def self(
    interaction: discord.Interaction,
    project_name: str, 
    contact: str,
    collab_manager: discord.app_commands.Choice[int],
    call_needed: discord.app_commands.Choice[int]): 

    # Define the GraphQL mutation to create an issue
    mutation = gql('''
        mutation createIssue($input: IssueCreateInput!) {
            issueCreate(input: $input) {
                success
                issue {
                    id
                }
            }
        }
    ''')
    
    # To define the two possible titles for the Linear task
    taskTitle = str(project_name) + ": Invite contact to server and finalize (no call needed)"
    if str(call_needed.name) == "Call needed":
        taskTitle = str(project_name) + ": Invite contact to server (call needed)"
    
    # Define the variables for the mutation
    variables = {
        "input": {
            "teamId": "YOUR_TEAM_ID", # Input Linear team ID here
            "title": taskTitle,
            "description": "Contact: " + str(contact),
            "assigneeId": getLinearID(str(collab_manager.name)), # The Linear ID of the person you want to assign this task to
            "labelIds": ["LABEL_ID1", "LABEL_ID2"] # Input the Label IDs here
        }
    }
    # Use the requests transport to send the query
    transport = RequestsHTTPTransport(
        url='https://api.linear.app/graphql',
        headers={
            "Content-type": "application/json",
            "Authorization": "Bearer " + LINEAR_API # Linear Personal API Key
        },
        use_json=True,
    )

    # Create the client
    linear_client = Client(transport=transport)
    # Send the request to the Linear API
    response = linear_client.execute(mutation, variables)
    issue_id = response["issueCreate"]["issue"]["id"] # Issue ID (to store)

    # Send a message to the discord channel with the issue id
    collab_manager_id = getDiscordID(str(collab_manager.name)) # To ping the correct user
    await interaction.response.send_message(f"**Issue created: **\n\n" + taskTitle + "\n\n<@" + collab_manager_id + ">") 

client.run(TOKEN)