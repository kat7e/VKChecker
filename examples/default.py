import asyncio
import VKChecker

def get_accounts(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read().readlines()
    
async def main():
    accounts = get_accounts('accounts.txt')
    client = VKChecker.Client(accounts)
    await client.start()

asyncio.run(main())