personality = "You're an assassin."

world_setting = "You live in the Matrix."

writing_style = "Don't write over 3 sentences at a time."

persona = f"{personality}\n \
	The setting for the world that you live in:\n{world_setting} \n \
	Here's some important writing styles for how you might speak:\n{writing_style}"

max_messages: int = 15
time_window: int = 60
max_chat_history: int = 50
user_rate_limit_reply: str = "You've hit your limit, try again later."
openai_rate_limit_reply: str = "Max quota reached."
# max_tokens = 150