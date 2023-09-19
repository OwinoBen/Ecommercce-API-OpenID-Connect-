from oauth2_provider.oauth2_validators import OAuth2Validator


class CustomeOauthValidator(OAuth2Validator):
    oidc_claim_scope = None

    def get_additional_claims(self, request):
        return {
            "given_name": request.user.first_name,
            "family_name": request.user.last_name,
            "name": ' '.join([request.user.first_name, request.user.last_name]),
            "username": request.user.username,
            "email": request.user.email,
        }

    def get_userinfo_claims(self, request):
        claims = super().get_userinfo_claims(request)
        claims['id'] = request.user.id
