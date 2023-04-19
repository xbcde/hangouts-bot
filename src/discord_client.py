import discord

from events import Event


class HangoutsClient(discord.Client):
    def __init__(self, text_channel_id, on_sync, **options):
        self.text_channel_id = text_channel_id
        self.on_sync = on_sync

        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True

        super().__init__(intents=intents, **options)

    def sync(self):
        print("Syncing...")
        text_channel = self.get_channel(self.text_channel_id)

        events = []
        for thread in text_channel.threads:
            try:
                events.append(Event.from_gibberish(thread.name))
            except ValueError:
                print(f"Could not parse: {thread.name}")

        print(f"Found {len(events)} events.")
        self.on_sync(events)

    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")
        self.sync()

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content == "/sync":
            self.sync()
            await message.channel.send("synced")

    async def on_thread_create(self, thread):
        print(f"Thread created (ID: {thread.id})")
        if thread.parent_id != self.text_channel_id:
            print(f"Thread did not belong to any relevant text channels")
            return
        self.sync()

    async def on_thread_update(self, _before, after):
        print(f"Thread updated (ID: {after.id})")
        if after.parent_id != self.text_channel_id:
            print(f"Thread did not belong to any relevant text channels")
            return
        self.sync()

    async def on_thread_delete(self, thread):
        print(f"Thread deleted (ID: {thread.id})")
        if thread.parent_id != self.text_channel_id:
            print(f"Thread did not belong to any relevant text channels")
            return
        self.sync()
