# Advent of Code Discord Bot #

## Disclaimer ##
If you're reading this now, I'd like to apologize in advance for what you're about to see. This code is awful. Hopefully next time you're here I'll have it cleaned up. There are probably a million ways to do this better but I was just focused on getting it working before my lunch break ended. 

## Setup ##
1. Create an application on the [Discord Developers](https://discord.com/developers/applications) page.
2. Add a bot, copy the token and save it in this directory in a file called `token.txt`, name your bot, and enable all intents.
3. Under OAuth2, go to URL generator, check 'bot' under scopes, then check all the text permissions, then copy your generated URL, enter this into your browser and choose the server you'd like it to join.
You have deployed the bot! Now three more steps.
4. Go to the AoC site, inspect element while logged in and navigate to the 'Network' tab. You may need to reload again while this is open, but a request to 'adventocode.com/' of type html should be here. Click this, go to 'headers' and look for 'request headers' and then the 'cookie' section. Here, there should be a single cookie which reads session={your_session_id}. Copy the part after 'session=' and save it in a file in this directory called `session.txt`.
5. Navigate to your private leaderboard page on AoC and click the link at the top where it says 'use an [[API]]()'. This will take you to the .json of your private leaderboard. Copy the URL and paste in into a file in this directory called `leaderboard_url.txt`.
6. Start the bot!: `python main.py`.

## Usage ##
Two discord commands have been implemented so far:

`$scoreboard`: displays the scoreboard for your private leaderboard

`$stats {aoc-name}`: displays the overall and daily stats for a member of your private leaderboard

Hopefully some more coming soon!