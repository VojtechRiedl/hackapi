from fastapi import HTTPException, Security, status
from fastapi.security.api_key import APIKeyHeader
from .settings import Settings

api_key_header = APIKeyHeader(name="secret", auto_error=False)

settings = Settings()

def check_secret_key(api_key_header: str = Security(api_key_header)):
    if api_key_header and api_key_header in settings.key:
        return api_key_header
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API klíč nebyl ověřen.",
        )
