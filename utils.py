
import base64
import webbrowser
from itertools import cycle
from typing import Dict, Any, Union

import constants


def get_obfuscated_data(key: str, app_config: Dict) -> str:

    if user_data := get_config_value(key, app_config['email_credentials']):
        user_data = decode_from_base64(user_data)
        out = obfuscator(user_data, constants.GIT_REPO_URL)

        return out.decode() if isinstance(out, bytes) else out


def obfuscator(data: Union[str, bytes], key: Union[str, bytes]) -> bytes:

    if isinstance(data, str):
        data = data.encode()

    if isinstance(key, str):
        key = key.encode()

    return bytes([b ^ k for b, k in zip(data, cycle(key))])


def encode_to_base64(data: Union[str, bytes]) -> str:
    try:
        if isinstance(data, str):
            data = data.encode()

        return base64.b64encode(data).decode()

    except Exception as e:
        print(f"Error encoding data to Base64: {str(e)}")
        return ''


def decode_from_base64(b64_string: bytes) -> bytes:
    try:
        return base64.b64decode(b64_string)

    except Exception as e:
        print(f"Error decoding Base64 string: {str(e)}")
        return bytes()


def open_url(url: str) -> None:
    webbrowser.open_new_tab(url)


def get_config_value(value: str, config: dict) -> Any:
    out = config.get(value)

    try:
        out = out.get()
        return out

    except AttributeError:
        return out if out else None
