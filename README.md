# Lord Vorldemort bot:

> **Note (4 months later):**  
> After revisiting this project, I realized there's still some polish left to do.  
> planing to:
> - Add proper **User response handling** for better usability
> - A few **minor bugs** are still lurking around needed to be overlooked... (my bad)
> Growth is real—stay tuned for the upgrade (no one is waiting for those updates but still i have to be semi pro).

## Overview

This Discord bot is designed to facilitate a programming challenge system within a Discord server. It utilizes the Gemini API to generate programming challenges and questions for users. The bot summons eligible users based on their roles and waits for their responses.

## Features

- **Summoning Users**: The bot can summon users with a specific role to participate in programming challenges.
- **Random User Selection**: Selects a random subset of eligible users to challenge.
- **Response Handling**: Waits for users to respond and issues penalties for non-responses.
- **Programming Challenge Generation**: Generates unique C programming challenges and questions using the Gemini API.

## Requirements

- Python 3.8+
- Discord.py library
- A valid API key for the Gemini API
- Discord bot token

## Commands

- **/bocal_starts_now**: Admin command to start the challenge and summon users.
- **/here**: Used by summoned users to indicate their presence.
- **/test**: Admin command to check if the bot is operational.
- **/check_roles**: Admin command to print all members' roles in the server.

## Configuration

### Role Configuration
The bot requires a role named `1337plx` to identify eligible users for summoning. Ensure this role exists in your Discord server.

### Summoning Hours
You can adjust the summoning hours by modifying the `is_within_summoning_hours` function. The current setting allows summoning between 11:00 AM and 3:30 AM.

## Error Handling
The bot includes basic error handling for API requests and user interactions. Any unexpected errors will be logged to the console.

## License
This bot is provided as-is and is not intended for commercial use. Please respect the original code and its author.

## Acknowledgments
- This bot utilizes the Discord API for its operations.
- The Gemini API is used for generating programming challenges.

# Disclaimer
Please do not steal or misuse this bot's code. Respect the original creator's work which is me ...
