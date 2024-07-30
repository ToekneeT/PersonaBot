# Setup

1. Will need at least Python 3.11+.
2. Inside `.env`, change the values to the specified keys `OPENAI_KEY` and `DISCORD_TOKEN`.
3. Install dependencies and run the bot.
	`pip install -r requirements.txt`
4. To run the bot, you only need to run `PersonaBot.py`, either by double clicking it, or running it in the terminal.

# Configuration

Inside `config.py`, you can adjust the personality of the bot by adjusting the `world_setting`, `writing_style`, and 'personality' variables.
`max_messages` is the total messages a specific user can send in the timeframe of `time_window` in seconds.
By default, it's set to 5 messages per user, every 60 seconds.
The bot by default remembers up to 50 previous chat messages, including non-pings and @mentions. It also remembers its own replies.
Can adjust the amount of messages it remembers by adjusting the `max_chat_history` variable.
This is the amount of messages it remembers per channel.
`user_rate_limit_reply` is the reply the bot gives to a user when they hit their rate limit.
`openai_rate_limit_reply` is the reply the bot gives when it reaches OpenAI's rate quota.

# Additional Information

The bot should respond only when someone @mentions the bot.
Or when someone replies directly to one of the Bot's messages.

Make sure the Bot is only given permission in the channels you want the bot to respond in.