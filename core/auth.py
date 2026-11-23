import os
import secrets

from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    expected_token = os.environ.get("NOC_API_TOKEN")

    if not expected_token:
        raise HTTPException(
            status_code=503,
            detail="API authentication not configured"
        )

    if not secrets.compare_digest(
        credentials.credentials,
        expected_token
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid API token"
        )

    return True