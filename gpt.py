from dotenv import load_dotenv
from openai import OpenAI
import os
from config import persona#, max_tokens


load_dotenv()
OPENAI_KEY = os.getenv('OPENAI_KEY')

client = OpenAI(api_key=OPENAI_KEY)

def chatgpt_response(prompt):

	system_message = {
		"role": "system",
		"content": persona
	}

	# Adds the personality to the chat conversation.
	# Personality is read first.
	messages = [system_message] + prompt

	response = client.chat.completions.create(
		model='gpt-4o-mini',
		messages=messages,
		# max_tokens=max_tokens
	)

	bot_response = response.choices[0].message.content.strip()
	
	return bot_response