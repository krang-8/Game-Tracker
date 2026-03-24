Discord bot that interacts with the FACEIT API to collect and publish data

Current Implementations include : 
- Able to get player stats from the API and send it in an embedded message on a discord channel
- Automatically keeps checking hubs and looks for new matches that are ongoing, and posts an embed that includes some match details (such as the matchroom link, players on each team, ELO gain/loss) on a discord channel that correlates to the division/hub
- Stores the ongoing matches and keeps checking on when they are no longer live, then deletes the message that was posted about them.


Examples of Implementations : 

Live matches embed.

<img width="827" height="327" alt="image" src="https://github.com/user-attachments/assets/a9818759-e8e2-4a2f-949e-155e797039ee" />


The following image shows both stat commands, regular one and the stats command for the past 20 games average.

<img width="521" height="529" alt="image" src="https://github.com/user-attachments/assets/7ad20531-3cc0-475b-97d8-9f294b03349f" />


While this repo is public, please do not redistribute it.
