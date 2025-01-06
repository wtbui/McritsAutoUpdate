# import discord

# CHANNEL_ID = 1197129032962166805
# SERVER_ID = 1196901238428680324
# FETCH_LIMIT = 10

# class McritsClient(discord.Client):
#     def __init__(self, guild_id, channel_id, fetch_limit, *args, **kwargs):
#         self.guild_id = guild_id
#         self.channel_id = channel_id
#         self.fetch_limit = fetch_limit

#         super().__init__(*args, **kwargs)

#     async def on_ready(self):
#         print('Logged on as', self.user)

#     async def shutdown(self):
#         await self.close()

#     async def fetch_messages(self):
#         print("Getting guild")
#         guild = self.get_guild(self.guild_id)
#         if not guild:
#             print(f"Guild with ID {self.guild_id} not found!")
#             return
    
#         print("Getting channel")
#         channel = guild.get_channel(self.channel_id)
#         if not channel:
#             print(f"Channel with ID {self.channel_id} not found in the guild!")
#             return

#         print(f"Fetching the last {self.fetch_limit} messages from {channel.name} in {guild.name}")
#         try:
#             # Fetch messages from the specified channel
#             messages = await channel.history(limit=self.fetch_limit).flatten()
#             return messages

#         except Exception as e:
#             print(f"An error occurred while fetching messages: {e}")

# def start_dclient(token):
#     client = McritsClient(CHANNEL_ID, SERVER_ID, FETCH_LIMIT, chunk_guilds_at_startup=False)
#     client.run(token)
#     print("Client configured")

#     return client

# def fetch_update(token):
#     client = start_dclient(token)
    
#     print("Attempting to fetch messages")
#     messages = client.fetch_messages()
#     client.shutdown()
    
#     print("Messages found, fetching link")
#     for message in messages:
#         link = extract_pc_link(message.content)

#         if link:
#             print("Link found")
#             return link

#     return None

# def extract_pc_link(content):
#     pattern = r"\[PC\]\((https?://[^\s]+)\)"
#     match = re.search(pattern, content)
#     return match.group(1) if match else None
