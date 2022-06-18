import os

class SecretNotFoundError(IOError):
    pass


def secret_path(name, env_specific=False, platform=False):
    """
    Returns the path to a secret in the docker container.
    Can use platform = True to share a secret used by platform, so long as the
    deployed bridge containers are also granted access to the secret.
    """
    _secret_path = 'snippets\\BRIDGE_PUSHER_KEY_ID'
    if platform:
        _secret_path = f'snippets\\PLATFORM_PUSHER_KEY_ID'
    if not os.path.isfile(_secret_path):
        raise SecretNotFoundError(name)
    return _secret_path


def secret(name, env_specific=False, strip=True, platform=False):
    """
    Returns the value of a secret from the docker container.
    """
    with open(secret_path(name, env_specific, platform), 'r') as f:
        val = f.read()
        if strip:
            val = val.strip()
        return val
