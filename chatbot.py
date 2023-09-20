# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> GPT2 code: <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
import discord
import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
TOKEN = 'MTEyNjE3Mjg3MTcwMjYxNDA4Ng.Grzbrl.IGjX1L1-WH0ksidyJphpPJZTYdwVoSlCEV8ZLQ'
PREFIX = '!'  # Change this prefix to your desired command prefix

# Define the intents you need (you may need to adjust these based on your bot's functionality)
intents = discord.Intents.default()

# Initialize the Discord client with intents
client = discord.Client(intents=intents)

# Load the GPT-2 model and tokenizer
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2", pad_token_id=tokenizer.eos_token_id)
model.eval()

# Initialize conversation history for each channel
conversation_history = {}

@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")

@client.event
async def on_message(message):
    # Ignore messages sent by the bot itself
    if message.author == client.user:
        return

    # Get or create conversation history for this channel
    channel_id = message.channel.id
    if channel_id not in conversation_history:
        conversation_history[channel_id] = []

    # Check if the user's message is a command
    if message.content.startswith(PREFIX):
        command = message.content[len(PREFIX):].strip().lower()

        if command == "help":
            # Provide a help message with available commands
            help_message = (
                "Available commands:\n"
                "!ask [your question]: Ask a question and get an answer.\n"
                "!calculate [expression]: Perform a math calculation.\n"
            )
            await message.channel.send(help_message)

        elif command.startswith("ask "):
            # Answer a user's question
            user_question = command[len("ask "):]
            # Generate a response using the GPT-2 model
            with torch.no_grad():
                output = model.generate(tokenizer.encode(user_question, return_tensors="pt"), max_length=100, num_return_sequences=1, pad_token_id=tokenizer.eos_token_id)
                bot_response = tokenizer.decode(output[0], skip_special_tokens=True)
            await message.channel.send(f"You asked: {user_question}\nAnswer: {bot_response}")

        elif command.startswith("calculate "):
            # Perform a math calculation
            math_expression = command[len("calculate "):]
            try:
                result = eval(math_expression)
                await message.channel.send(f"Result of {math_expression}: {result}")
            except Exception as e:
                await message.channel.send(f"Error calculating: {e}")

        else:
            await message.channel.send("Invalid command. Use !help for a list of commands.")

    else:
        # Add the user's message to the conversation history
        user_input = message.content
        conversation_history[channel_id].append(user_input)

        # Combine the conversation history into a single string
        conversation_text = " ".join(conversation_history[channel_id])

        # Truncate the conversation text if it exceeds the token limit
        if len(tokenizer.encode(conversation_text)) > 1024:
            conversation_text = conversation_text[-1024:]

        # Tokenize the conversation text and convert to tensor
        input_ids = tokenizer.encode(conversation_text, return_tensors="pt")

        # Generate a response using the GPT-2 model
        with torch.no_grad():
            output = model.generate(input_ids, max_length=100, num_return_sequences=1, pad_token_id=tokenizer.eos_token_id)
            bot_response = tokenizer.decode(output[0], skip_special_tokens=True)

        # Add the bot's response to the conversation history
        conversation_history[channel_id].append(bot_response)

        # Send the bot's response back to the user
        await message.channel.send(bot_response)

# Run the bot
client.run(TOKEN)

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> GPT3 code: <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# import discord
# import openai

# # Replace 'YOUR_BOT_TOKEN' with your actual bot token
# TOKEN = 'MTEyNjE3Mjg3MTcwMjYxNDA4Ng.Grzbrl.IGjX1L1-WH0ksidyJphpPJZTYdwVoSlCEV8ZLQ'
# PREFIX = '!'  # Change this prefix to your desired command prefix

# # Define the intents you need (you may need to adjust these based on your bot's functionality)
# intents = discord.Intents.default()

# # Initialize the Discord client with intents
# client = discord.Client(intents=intents)

# # Initialize the OpenAI API client with your API key
# openai.api_key = "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"  # Replace this with your actual API key

# @client.event
# async def on_ready():
#     print(f"We have logged in as {client.user}")

# @client.event
# async def on_message(message):
#     # Ignore messages sent by the bot itself
#     if message.author == client.user:
#         return

#     # Process the user's message
#     if message.content.startswith(PREFIX):
#         user_input = message.content[len(PREFIX):]

#         # Use the OpenAI API to generate a response using ChatGPT-3
#         response = openai.Completion.create(
#             engine="davinci",  # Choose the engine you have access to
#             prompt=user_input,
#             max_tokens=100,
#             stop=["\n", "You:"],  # Stop the response generation at newline or after "You:"
#         )

#         # Get the generated response from the API
#         bot_response = response.choices[0].text.strip()

#         # Send the response back to the user
#         await message.channel.send(bot_response)

# # Run the bot
# client.run(TOKEN)
