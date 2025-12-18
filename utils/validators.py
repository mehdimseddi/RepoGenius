import re

def validate_github_url(url: str) -> bool:
    """
    Validates a GitHub repository URL.
    """
    if not url:
        return False
    # Regex to match github.com/<user>/<repo> format, allowing for .git at the end
    pattern = r'^https://github\.com/[a-zA-Z0-9\-_]+/[a-zA-Z0-9\-_.]+(?:\.git)?/?$'
    return re.match(pattern, url) is not None
