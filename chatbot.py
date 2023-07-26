import discord
import openai

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
TOKEN = 'YOUR_BOT_TOKEN'
PREFIX = '!'  # Change this prefix to your desired command prefix

# Define the intents you need (you may need to adjust these based on your bot's functionality)
intents = discord.Intents.default()

# Initialize the Discord client with intents
client = discord.Client(intents=intents)

# Initialize the OpenAI API client with your API key
openai.api_key = "API_KEY"  # Replace this with your actual API key

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

        # Use the OpenAI API to generate a response using ChatGPT-3
        response = openai.Completion.create(
            engine="davinci",  # Choose the engine you have access to
            prompt=user_input,
            max_tokens=100,
            stop=["\n", "You:"],  # Stop the response generation at newline or after "You:"
        )

        # Get the generated response from the API
        bot_response = response.choices[0].text.strip()

        # Send the response back to the user
        await message.channel.send(bot_response)

# Run the bot
client.run(TOKEN)
