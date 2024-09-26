import asyncio
import os
from telethon import TelegramClient, errors
from telethon.tl.functions.channels import JoinChannelRequest

api_id = os.getenv("TELEGRAM_API_ID")
api_hash = os.getenv("TELEGRAM_API_HASH")

class TelegramScraperCLI:
    def __init__(self):
        self.client = TelegramClient('anon', api_id, api_hash)

    async def join_channel(self, channel_link):
        try:
            await self.client.start()
            await self.client(JoinChannelRequest(channel_link))
            print(f"Successfully joined the channel: {channel_link}")
        except errors.FloodWaitError as e:
            print(f"Flood wait error. Please wait for {e.seconds} seconds before trying again.")
        except errors.ChannelPrivateError:
            print("Unable to join channel: The channel is private.")
        except errors.InviteHashExpiredError:
            print("Unable to join channel: The invite link has expired.")
        except Exception as e:
            print(f"Failed to join channel: {str(e)}")

    async def scrape_messages(self, channel_link, limit=10):
        try:
            await self.client.start()
            async for message in self.client.iter_messages(channel_link, limit=limit):
                if message.text:
                    print(message.text)
                    print('-' * 40)
        except Exception as e:
            print(f"Error scraping messages: {str(e)}")

    async def run(self):
        while True:
            print("\nTelegram Channel Scraper")
            print("1. Join Channel")
            print("2. Scrape Messages")
            print("3. Exit")
            choice = input("Enter your choice (1-3): ")

            if choice == '1':
                channel_link = input("Enter the channel link: ")
                await self.join_channel(channel_link)
            elif choice == '2':
                channel_link = input("Enter the channel link: ")
                limit = int(input("Enter the number of messages to scrape: "))
                await self.scrape_messages(channel_link, limit)
            elif choice == '3':
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    scraper = TelegramScraperCLI()
    asyncio.get_event_loop().run_until_complete(scraper.run())
