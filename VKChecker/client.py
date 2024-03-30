from aiohttp import ClientSession
from asyncio import gather
from typing import (
    Optional, 
    List, 
    Dict, 
    Any, 
    Callable
    )

from VKchecker.errors.exceptions import (
    InvalidTokenError, 
    InvalidAuthError, 
    CaptchaError,
    FloodControl
)

class Client:
    def __init__(self, 
            accounts: List[str], 
            session: Optional[ClientSession] = None,
            ):
        self.captcha_handler = None
        self.__accounts__ = accounts
        self.session = session if not session is None else ClientSession

    async def __create_request__(
        self, 
        url: str, 
        **kwargs: Optional[Dict[str, Any]]
    ) -> bool:
        """
        Send a request to the given URL and handle errors if any.

        Args:
            url (str): The URL to send the request to.
            **kwargs: Optional keyword arguments to pass to the session.get method.

        Raises:
            InvalidTokenError: If the access token in the response is invalid.
            InvalidAuthError: If the authentication is invalid.
            CaptchaError: If a captcha is detected.
            FloodControl: If flood control is detected.

        Returns:
            bool: True if the request was successful, False otherwise.
        """
        async with self.session() as session:
            async with session.get(url, **kwargs) as response:
                response = await response.json()
        if "error_msg" in response["error"]:
            raise InvalidTokenError(f"Account is invalid: {response['error']['error_msg']}")
        elif "error_description" in response:
            raise InvalidAuthError(f"Account is invalid: {response['error_description']}")
        elif "captcha_sid" in response:
            if self.captcha_handler is not None: 
                url = await self.captcha_handler(response, url)
                return await self.__create_request__(url, kwargs)
            else:
                raise CaptchaError(f"Captcha detected while checking account: {response['error']}")
        elif "Flood Control" in response:
            raise FloodControl(f"Flood Control detected while checking account: {response['error']}")

    def add_captcha_handler(self, handler: Callable[Any]) -> None:
        """
        Add a captcha handler to handle captchas.
        It must return new link with solved captcha.
        Args:
            handler (Callable[Any]): The captcha handler.
        """
        self.captcha_handler = handler    

    async def __check_account__(self, _account: str, **kwargs: Optional[Dict[str, Any]]) -> bool:
        """
        Check a account.

        Args:
            _account (str): The access token or username:password combination.
            **kwargs (Optional[Dict[str, Any]]): Keyword arguments for the session.get method.

        Returns:
            bool: True if the request was successful, False otherwise.
        """
        url = f"https://api.vk.com/method/users.get?access_token={_account}&v=5.131"
        account =  _account.split(":")
        if len(account) == 2:
            url = (
                f"https://oauth.vk.com/token?grant_type=password&client_id=6146827"
                f"&client_secret=qVxWRF1CwHERuIrKBnqe&username={account[0]}&password={account[1]}&v=5.131&2fa_supported=1"
            )
        try:
            await self.__create_request__(url, kwargs)
        except (InvalidTokenError, InvalidAuthError, CaptchaError, FloodControl):
            return False
        return True

    async def start(self, 
            **kwargs: Optional[Dict[str, Any]]) -> List[bool]:
        """
        Start checking the accounts.

        Args:
            **kwargs (Optional[Dict[str, Any]]): Keyword arguments for the session.get method.

        Returns:
            List[bool]: A list of booleans indicating the success of each account check.
        """
        tasks = [self.__check_account__(account, **kwargs) for account in self.__accounts__]
        result = await gather(*tasks)
        return [account for account in self.__accounts__ if result[self.__accounts__.index(account)] == True]  