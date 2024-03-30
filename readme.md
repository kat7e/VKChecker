## Usage

Install requirements

`pip3 install -r requirements.txt` 

```
from VKChecker import Client
from asyncio imprt run

async def main() -> None:
    accounts = ("num:pass", "token", ...)
    async with Client(accounts) as client:
        valid_accounts = client.start()
    
    return valid_accounts

run(main())
```

## Information
- Async
- Support format with login:password and default tokens
- For information about usage view examples
