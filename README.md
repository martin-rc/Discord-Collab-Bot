# Discord Collab Bot

Personal Discord bot to facilitate the uploading and voting process of potential collaborations.

Through a command, the bot takes the project's name and overview and then: 
- Uploads that to a Google Sheet that keeps track of all collaborations
- Pastes the project information and tags a role for members to look at the new posting
- Adds 3 emojis to vote on the potential collaboration
- Updates you once the information has been passed to the Google Sheet with a message confirmation

Additionally, the bot also has a /check command to check if a certain project name appears in any of the sheets in the spreadsheet.

Note: A lot of the values and tokens in the bot.py have been modified for privacy/security reasons :)
