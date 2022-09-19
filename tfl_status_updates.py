#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from datetime import datetime
from itertools import cycle

import discord
import requests
from fake_useragent import UserAgent


def tfl_api_call(url: str) -> list:
    """Send a request to the server and return the html"""
    headers = {"user-agent": UserAgent().random}

    r = requests.get(url, headers=headers)
    if r.ok:
        return r.json()
    else:
        return r.status_code


def parse_json(response: list) -> dict:
    """Parse the json response and get status of the lines"""
    if isinstance(response, list):
        line_statuses = {}
        for line in response:
            name = line["name"]
            if line['lineStatuses'][0]['statusSeverity'] == 10:  # if there is a good service
                status = line["lineStatuses"][0]["statusSeverityDescription"]
                line_statuses[name] = f"{name}: {status}"
            else:
                status = line["lineStatuses"][0]["reason"]  # if there is a delay
                try:  # somethimes the line name isn't included in the status
                    status = status.split(":", 1)[1]
                except:
                    continue

                line_statuses[name] = status
                line_statuses[name] = f"{name}: {status}"

        return line_statuses
    else:
        return f"Oops I was unable to retrieve the TFL line statuses!\nStatus code: {response}"


def build_message(statuses: dict, favourites: list) -> str:
    """Create and format the message to be sent to the output stream"""
    bot_message = "Hey peeps! Here are the current TFL line statuses:\n\n"
    switch = cycle(["", "**"])  # create a generator that makes the message alternate between bold or not

    emoji_mappings = {
        "Bakerloo": "🟫",
        "Central": "🟥",
        "Circle": "🟨",
        "District": "🟩",
        "Hammersmith & City": "🔨",
        "Jubilee": "⬜",
        "Metropolitan": "🟪",
        "Northern": "🧭",
        "Piccadilly": "🟦",
        "Victoria": "👑",
        "Waterloo & City": "🚽",
    }

    for line in favourites:
        bold = next(switch)
        bot_message += f"> {bold}{emoji_mappings[line]} {statuses[line]}{bold}\n"
        statuses.pop(line)

    for line in statuses:
        bold = next(switch)
        bot_message += f"> {bold}{emoji_mappings[line]} {statuses[line]}{bold}\n"

    bot_message += "\nFor more information click https://tfl.gov.uk/tube-dlr-overground/status/"

    return bot_message


def main():
    url = "https://api.tfl.gov.uk/line/mode/tube/status"
    response = tfl_api_call(url)
    parsed_response = parse_json(response)

    if isinstance(parsed_response, dict):
        favourites = ["Jubilee", "Bakerloo", "Metropolitan"]  # lines to display at the top of the message
        message = build_message(parsed_response, favourites)
        return message
    else:
        return parsed_response  # returns the error


if __name__ == "__main__":
    client = discord.Client()
    token = os.environ.get("DISCORD_BOT_TOKEN")
    channel_id = int(os.environ.get("DISCORD_CHANNEL_ID"))
    date = datetime.now().strftime("%Y/%m/%d %H:%M:%S BST")

    @client.event
    async def on_ready():
        channel = client.get_channel(channel_id)
        tfl_status = main()
        # discord limits a message to 2000 characters so this splits the message into 2 if it's too long
        if len(tfl_status) < 2000:
            await channel.send(tfl_status)
        else:
            split_point = "> **🟩 District"
            split_message = tfl_status.split(split_point)
            split_message[1] = split_point + split_message[1]

            for message in split_message:
                await channel.send(message)

        await client.close()

    client.run(token)
