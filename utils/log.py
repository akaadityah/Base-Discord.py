def _c(code: int, s: str) -> str:
    return f"\033[{code}m{s}\033[0m"


def red(s: str) -> str: return _c(31, s)
def green(s: str) -> str: return _c(32, s)
def yellow(s: str) -> str: return _c(33, s)
def blue(s: str) -> str: return _c(34, s)
