# Game-Tracker
Discord bot that interacts with the FACEIT API to collect and publish data

Current Implementations include : 
- Able to get player stats from the API and send it in an embedded message on a discord channel
- Automatically keeps checking hubs and looks for new matches that are ongoing, and posts an embed that includes some match details such as the matchroom link, players on each team, ELO gain/loss on a discord channel that correlates to the division/hub
- Stores the ongoing matches and keeps checking on when they are no longer live, then deletes the message that was posted about them.


Examples of Implementations : 

Live matches embed.

![image](https://media.discordapp.net/attachments/737581188893638666/739916371655131166/unknown.png) 

The following image shows both stat commands, regular one and the stats command for the past 20 games average.

![image2](https://media.discordapp.net/attachments/737581188893638666/739916722693472286/unknown.png?width=488&height=495)

While this repo is public, please do not redistribute it.
