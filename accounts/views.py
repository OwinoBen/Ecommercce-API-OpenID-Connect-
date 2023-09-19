import requests
from django.http import JsonResponse
from oauth2_provider.models import get_application_model
from rest_framework import status, exceptions, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from util.messages.hundle_messages import success_response, error_response
from util.authorization.config import Config
from .serializers import AuthSerializer, ObtainTokenSerializer, RefreshTokenSerializer

Application = get_application_model()


class AuthViewSet(viewsets.GenericViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = AuthSerializer

    def create(self, request, *args, **kwargs):
        """Create new customer for authentication"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.create(serializer.validated_data)
        if user:
            response_data = success_response(status_code=status.HTTP_200_OK, message_code="authentication",
                                             message="account registered")
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenObtainView(viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    serializer_class = ObtainTokenSerializer

    def create(self, request, *args, **kwargs):
        """Create Obtain Oauth2 OPENID CONNECT tokens"""
        serializer = self.get_serializer(data=request.data)
        url = 'http://' + request.get_host() + '/api/v1/token/'
        if serializer.is_valid():
            response = requests.post(
                url=url,
                data=Config.get_payload(
                    self,
                    client_id=serializer.validated_data['client_id'],
                    client_secret=serializer.validated_data['client_secret'],
                    verification_code=serializer.validated_data['verification_code'],
                    grant_type="authorization_code",
                    callback_url=serializer.validated_data['callback_url']
                ), headers=Config.header).json()
            if "error" in response and response['error'] == 'invalid_grant':
                url = f'http://{request.get_host()}/api/v1/authorize/?response_type=code%20token&client_id' \
                      f'={serializer.validated_data["client_id"]}&nonce=asd&redirect_uris' \
                      f'={serializer.validated_data["callback_url"]}' \
                      f'&scope=openid%20profile%20read%20email%20write%20phone'
                response = {
                    "auth_url": url
                }
                response_data = error_response(status_code=status.HTTP_401_UNAUTHORIZED,
                                               message=response, error_code="app_authorization")
                return Response(response_data, status=status.HTTP_401_UNAUTHORIZED)
            else:
                response_data = success_response(status_code=status.HTTP_200_OK, message_code="token_obtain",
                                                 message=response)
                return Response(response_data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=["POST"], serializer_class=RefreshTokenSerializer, detail=False)
    def refresh(self, request):
        """Generate access_token with refresh_token"""
        serializer = RefreshTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        url = 'http://' + request.get_host() + '/api/v1/token/'
        response = requests.post(url, data=Config.get_payload(self, grant_type='refresh_token',
                                                              refresh=serializer.validated_data['refresh_token'],
                                                              client_id=serializer.validated_data['client_id'],
                                                              client_secret=serializer.validated_data['client_secret']
                                                              )).json()
        if 'error' in response and response['error'] == 'invalid_grant':
            raise exceptions.AuthenticationFailed("Invalid or expired refresh_token", "authorization")

        return Response(success_response(status_code=status.HTTP_200_OK, message_code="refresh_token",
                                         message=response), status=status.HTTP_200_OK)

    @action(methods=["POST"], detail=False)
    def callback(self, request):
        # Retrieve the authorization code from the request
        authorization_code = request.GET.get('code')
        if authorization_code:
            # Exchange the authorization code for access token
            # Send a POST request to the token endpoint
            token_url = 'http://' + request.get_host() + '/api/v1/token/'

            response = requests.post(
                url=token_url,
                data=Config.get_payload(
                    self,
                    client_id='tj18QznRCj4vD2MBZY001WcJlJCziSwW0WDNsBp3',
                    client_secret='yWPM67AHWlt3jFTER2Z9jb4s7m6IIuctiBsW0rMkRDS4MN2WzpLwj0LFKD3hmtLrnCHaqRHltGU57XEDsdXqtexcEp8us0Jnr8Mlb2GSTi9j2z9MTLBS55rWPtYP1bKN',
                    verification_code=authorization_code,
                    grant_type="authorization_code",
                    callback_url='http://127.0.0.1:8001/api/v1/auth/callback'
                ), headers=Config.header).json()

            if response.status_code == 200:
                token_data = response
                return Response({'access_token': token_data})
            else:
                return Response({'error': 'Failed to issue access token'})

        return Response({'error': 'Invalid request'})
