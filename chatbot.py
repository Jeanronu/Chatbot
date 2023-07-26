import discord
import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
TOKEN = 'YOUR_BOT_TOKEN'
PREFIX = '!'  # Change this prefix to your desired command prefix

# Define the intents you need (you may need to adjust these based on your bot's functionality)
intents = discord.Intents.default()

# Initialize the Discord client with intents
client = discord.Client(intents=intents)

# Load the GPT-2 model and tokenizer
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2", pad_token_id=tokenizer.eos_token_id)

# Set the model to evaluation mode
model.eval()

@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")

@client.event
async def on_message(message):
    # Ignore messages sent by the bot itself
    if message.author == client.user:
        return

    # Process the user's message
    if message.content.startswith(PREFIX):
        user_input = message.content[len(PREFIX):]

        # Tokenize the user input and convert to tensor
        input_ids = tokenizer.encode(user_input, return_tensors="pt")

        # Generate a response using the GPT-2 model
        with torch.no_grad():
            output = model.generate(input_ids, max_length=100, num_return_sequences=1, pad_token_id=tokenizer.eos_token_id)
            bot_response = tokenizer.decode(output[0], skip_special_tokens=True)

        # Send the response back to the user
        await message.channel.send(bot_response)

# Run the bot
client.run(TOKEN)