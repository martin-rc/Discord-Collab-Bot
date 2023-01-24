# Discord Collab Bot

Personal Discord bot to facilitate the uploading and voting process of potential collaborations.

Through a command, the bot takes the project's name and overview and then: 
- Uploads that to a Google Sheet that keeps track of all collaborations
- Pastes the project information and tags a role for members to look at the new posting
- Adds 3 emojis to vote on the potential collaboration
- Updates you once the information has been passed to the Google Sheet with a message confirmation

Additionally, the bot also has a `/check` command to check if a certain project name appears in any of the sheets in the spreadsheet.

Note: A lot of the values and tokens in the bot.py have been modified for privacy/security reasons :)

# **Jan 23, 2023 updates:**

- The /add command now includes a contact field to include the contact for the collab. This is also automatically added in the Google Sheet
- Two new commands have been added, `/dm` and `/approve`

## **Linear App Implementation**
- Implemented the Linear App API to the project using GraphQL
- Certain commands, like the two new ones, will now have a direct effect on a Linear organization

## **/dm command**
- You can now type `/dm ProjectName ProjectTwitter` to create a Linear task assigned to a specific person. 
  - The task will have a "Reach Out" label
  - Used to ask the assignee to DM a certain project on Twitter
  - Lets you know that the issue has been created through a message

![image](https://user-images.githubusercontent.com/113465033/214195623-a62d42c8-3691-484f-b6ac-93a9bd39da5d.png)

![image](https://user-images.githubusercontent.com/113465033/214195845-0cdf9aad-b1ec-4789-a9b0-5b485380015c.png)

![image](https://user-images.githubusercontent.com/113465033/214195794-9225e20a-309f-47a2-83c1-b1ac8f292e7d.png)


## **/approve command**
- New command to be used by collaboration managers to approve of a project and consequently create a task on Linear
- Use: `/approve ProjectName Contact CollabManager CallNeeded?`
  - The approved project's name, the contact for the project, the collab manager that posted the project, and if a call is needed or note based on votes
  - Automatically creates a Linear task with the labels "Invite to Server" and "Finalize" and assigns it to the collab manager
  - Pings the collab manager and lets you know that the issue has been created through a message

![image](https://user-images.githubusercontent.com/113465033/214195967-d059543f-d166-442f-a355-f7db9e520fe4.png)

![image](https://user-images.githubusercontent.com/113465033/214196114-ce751fc5-e5d2-4b91-9e74-acbcd4bd4a19.png)

![image](https://user-images.githubusercontent.com/113465033/214196361-7efe1354-037d-4b7c-b467-ae6243a94a5d.png)



