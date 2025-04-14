import os
import asyncio
import json
from typing import Any, Callable, Dict, Optional

import httpx
from urllib.parse import quote  # for URL encoding
from pydantic import BaseModel

# Define the ApiResponseWrapper equivalent
class ApiResponseWrapper(BaseModel):
    success: bool = False
    message: Optional[str] = None
    payload: Optional[Any] = None

# MspClient in Python
class MspClient:
    def __init__(self, server_id: str, api_base_url: str, api_access_token: str, api_refresh_token: str):
        self._server_id = server_id
        # Create an asynchronous HTTP client with the base URL.
        self._client = httpx.AsyncClient(base_url=api_base_url)
        self._default_error_handler: Optional[Callable[[Exception], None]] = None
        self._api_access_token = None
        self._api_refresh_token = None
        self.api_access_token = api_access_token  # setter sets the header
        self.api_refresh_token = api_refresh_token

    @property
    def api_access_token(self) -> str:
        return self._api_access_token

    @api_access_token.setter
    def api_access_token(self, value: str):
        if value is None:
            raise ValueError("api_access_token cannot be None")
        self._api_access_token = value
        # Set the default Authorization header
        self._client.headers["Authorization"] = f"Bearer {self._api_access_token}"

    @property
    def api_refresh_token(self) -> str:
        return self._api_refresh_token

    @api_refresh_token.setter
    def api_refresh_token(self, value: str):
        if value is None:
            raise ValueError("api_refresh_token cannot be None")
        self._api_refresh_token = value

    def set_default_error_handler(self, on_error: Optional[Callable[[Exception], None]]) -> None:
        self._default_error_handler = on_error

    async def http_post(self, uri: str, post_values: Dict[str, str], headers: Optional[Dict[str, str]] = None) -> None:
        """Performs a POST and returns nothing if successful; otherwise raises an exception."""
        wrapper = await self._http_post_internal(uri, post_values, headers)
        if not wrapper.success:
            msg = wrapper.message if wrapper.message else "Unknown error"
            exception = Exception(msg)
            if self._default_error_handler:
                self._default_error_handler(exception)
            raise exception

    async def http_post_generic(self, uri: str, post_values: Dict[str, str],
                                  headers: Optional[Dict[str, str]] = None,
                                  target_type: Callable[[Any], Any] = None) -> Any:
        """
        Performs a POST and returns a parsed result of type target_type
        (if target_type is provided, it should be a callable that takes a dict and returns an instance).
        """
        wrapper = await self._http_post_internal(uri, post_values, headers)
        try:
            result = wrapper.payload
            if result is None:
                raise Exception(f"Post request for {uri} failed: JSON Decode Failed")
            if not wrapper.success:
                raise Exception(wrapper.message if wrapper.message else "Unknown error")
            if target_type:
                return target_type(result)
            return result
        except Exception as e:
            if self._default_error_handler:
                self._default_error_handler(e)
            raise

    async def _http_post_internal(self, uri: str, post_values: Dict[str, str],
                                  headers: Optional[Dict[str, str]] = None) -> ApiResponseWrapper:
        # Check for XDEBUG_TRIGGER in environment
        xdebug_trigger = os.getenv("XDEBUG_TRIGGER")
        if xdebug_trigger:
            # Append query parameter (assumes no existing query parameters)
            uri = f"{uri}?XDEBUG_TRIGGER={quote(xdebug_trigger)}"

        # Prepare form data; in httpx, you can pass data as a dict.
        data = {k: v for k, v in post_values.items() if k is not None}

        # Build the request; httpx will combine base_url and relative uri automatically.
        request_headers = headers.copy() if headers else {}
        request_headers["X-Server-Id"] = self._server_id
        request_headers.setdefault("Accept", "application/json")

        try:
            response = await self._client.post(uri, data=data, headers=request_headers)
        except Exception as e:
            if self._default_error_handler:
                self._default_error_handler(e)
            raise

        if response.status_code < 200 or response.status_code >= 300:
            error_message = f"HTTP request failed with status code {response.status_code}"
            http_exc = httpx.HTTPStatusError(error_message, request=response.request, response=response)
            if self._default_error_handler:
                self._default_error_handler(http_exc)
            raise http_exc

        # Read response text and parse JSON
        try:
            text = response.text
        except Exception as e:
            if self._default_error_handler:
                self._default_error_handler(e)
            raise

        try:
            wrapper_dict = json.loads(text)
            wrapper = ApiResponseWrapper(**wrapper_dict)
            if wrapper is None or not wrapper.success:
                err_msg = wrapper.message if wrapper and wrapper.message else "JSON Decode Failed"
                raise Exception(f"Post request for {uri} failed: {err_msg}")
            return wrapper
        except Exception as ex:
            if self._default_error_handler:
                self._default_error_handler(ex)
            raise

# Example usage:
# async def main():
#     client = MspClient("server-id", "https://api.example.com/", "access_token", "refresh_token")
#     # Set an error handler:
#     client.set_default_error_handler(lambda e: print("Error:", e))
#     post_data = {"key1": "value1", "key2": "value2"}
#     result = await client.http_post_generic("/api/some-endpoint", post_data)
#     print(result)
#
# asyncio.run(main())
