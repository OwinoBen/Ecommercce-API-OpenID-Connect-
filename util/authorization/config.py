import os


class Config:
    header = {
        'content-type': "application/x-www-form-urlencoded",
        'cache-control': "no-cache",
    }

    def get_payload(self, client_id, client_secret, grant_type, refresh=None, verification_code=None,
                    callback_url=None):
        payload = {
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": grant_type,
            "code": verification_code,
            "refresh_token": refresh,
            "code_verifier": "MUNGTzZRUk1CWVhDNzExM1RRN1pYMUhESDdZWkxBQURFOENGUERJSTBUUFY3TFpGRjJTTkoyVEpRSDJZQjBVTg==",
            "redirect_uris": callback_url
        }
        return payload

    authorize_url = f'http://localhost:8001/api/v1/authorize/' \
                    f'?response_type=code&code_challenge={os.environ.get("CODE_CHALLENGE")}' \
                    f'&code_challenge_method=S256&client_id=["client_id"]' \
                    f'&redirect_uris="[callback_url]"'
