import asyncio
import VKChecker

def get_accounts(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read().readlines()
    
def ch(response, url):
    """Your captcha handler"""
    ...
    return solved_captcha_url

async def main():
    accounts = get_accounts('accounts.txt')
    client = VKChecker.Client(accounts)
    client.add_captcha_handler(ch)
    await client.start()

asyncio.run(main())