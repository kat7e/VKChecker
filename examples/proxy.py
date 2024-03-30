import asyncio
import VKChecker
from aiohttp import BasicAuth, ClientSession

def get_accounts(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read().readlines()
    
async def main():
    auth_proxy = BasicAuth('login', 'password')
    session = ClientSession(auth=auth_proxy)

    accounts = get_accounts('accounts.txt')
    client = VKChecker.Client(accounts, session)
    return await client.start(proxy = '127.0.0.1:8080')

asyncio.run(main())