from typing import Any

from rich import print


def handle_ex(parent: Any, ex: Exception):
    print(parent)
    print(ex)
    raise ex
