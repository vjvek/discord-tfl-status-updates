# discord-tfl-status-updates

This python script uses the TFL api to get status updates for London underground tube lines and uses a bot to output that information into a user defined discord channel.

## Requirements

Python 3.7.x or newer

## Dependencies

Dependencies for your python environment are listed in requirements.txt. Install them using the below command. Ensure the py part is correct for your environment, eg py, python, or python3, etc.

`py -m pip install -r requirements.txt`

or

`pip3 install -r requirements.txt`

## Usage

A bot account needs to be created before using the script, see here for how to do so:
https://discordpy.readthedocs.io/en/stable/discord.html

There are 2 variables that need to be set; _token_ and _channel\_id_ which are the respective bot token and id of the discord channel where the bot will post the message. These variables can either be set in the script or as an environment variable.

It can also be setup as on a schedule via Task Scheduler on *Windows*, launchd on *MacOS* or cron on *Linux*