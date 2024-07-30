import discord, os, time, openai
from openai import OpenAI
from collections import defaultdict
from dotenv import load_dotenv
from gpt import chatgpt_response
from config import max_messages, time_window, max_chat_history, user_rate_limit_reply, openai_rate_limit_reply

load_dotenv()
SECRET_KEY = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Dictionary that temporarily stores timestamps of when a user gets a response from the bot.
# Clears when the oldest timestamp elapsed is longer than time_interval.
user_message_count = defaultdict(list)

# Dictionary storing some recent converation history.
# Contains up to max_chat_history for each channel.
# Then the oldest chat starts to get replaced by newer ones.
conversation_history = defaultdict(list)


@client.event
async def on_ready() -> None:
	print(f"We have logged in as {client.user}")


# If a user hits the limit of how many messages they can receive from the bot, it'll prevent 
# the user from getting a new one. Resets based on time_window
def is_rate_limited(user_id) -> bool:
	current_time = time.time()
	user_message_time = user_message_count[user_id]

	# Checks the oldest timestamp, if it was longer than the set time_window, it'll clear all of
	# that user's timestamps.
	if len(user_message_time) > 0 and current_time - user_message_time[0] > time_window:
		user_message_time = []
	user_message_count[user_id] = user_message_time

	return len(user_message_time) >= max_messages


# Any time a user gets a response from the bot, it'll add the timestamp of their message
# to a list, which will be used to limit the amount of messages per user.
def increment_rate_counter(user_id) -> None:
	current_time = time.time()
	user_message_time = user_message_count[user_id]
	user_message_time.append(current_time)
	user_message_count[user_id] = user_message_time


# Adds both user messages and bot messages so that the bot can read and remember a bit of history.
# Once the message hits the max_chat_history, the oldest chat log gets removed and the new one gets added.
def add_to_conversation_history(id, prompt, role):
	if len(conversation_history[id]) >= max_chat_history:
		conversation_history[id].pop(0)
	conversation_history[id].append({"role": role, "content": prompt})


# Sends a default message if the user has sent too many messages within a time frame.
# Preventing the bot from making an API call to OpenAI.
async def reply_rate_limited(message, thread):
	if isinstance(message.channel, thread):
		await message.channel.send(user_rate_limit_reply)
	else:
		await message.reply(user_rate_limit_reply)


async def reply_to(message, thread, bot_response):
	if isinstance(message.channel, discord.Thread):
		await message.channel.send(bot_response)
	else:
		await message.reply(bot_response)


@client.event
async def on_message(message):
	if message.author == client.user:
		return


	# Ignore DMs.
	if message.guild is None:
		return


	channel_id = message.channel.id
	prompt = str(message.content)
	add_to_conversation_history(channel_id, f'{message.author}: {prompt}', "user")
	# Responds if it receives a reply.
	try:
		if message.reference:
			if is_rate_limited(message.author.id):
				await reply_rate_limited(message, discord.Thread)
				return

			try:
				referenced_message = await message.channel.fetch_message(message.reference.message_id)
				if referenced_message.author == client.user:
					bot_response = chatgpt_response(conversation_history[channel_id])
					add_to_conversation_history(channel_id, bot_response, "assistant")
					# print(f'\n{bot_response}\n')
					increment_rate_counter(message.author.id)
					await reply_to(message, discord.Thread, bot_response)

			except discord.errors.NotFound as e:
				# Exception when creating a new thread and the first response.
				# The bot can't find the first message and sends an error, but still functions normally.
				print(f"Discord not found error: {e}")
				return


		# Responds if it gets @'d in the chat.
		elif client.user in message.mentions:
			if is_rate_limited(message.author.id):
				await reply_rate_limited(message, discord.Thread)
				return

			bot_response = chatgpt_response(conversation_history[channel_id])
			add_to_conversation_history(channel_id, bot_response, "assistant")
			# print(f'\n{bot_response}\n')
			increment_rate_counter(message.author.id)
			await reply_to(message, discord.Thread, bot_response)

	except openai.RateLimitError as e:
		print(f"Max quota have been exceeded: {e}")
		await message.channel.send(openai_rate_limit_reply)
		time.sleep(60)
		return


client.run(SECRET_KEY)