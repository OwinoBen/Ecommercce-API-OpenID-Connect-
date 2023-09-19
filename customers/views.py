from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, OAuth2Authentication
from rest_framework import exceptions, status, response, permissions, filters
from rest_framework.viewsets import ModelViewSet
from accounts.serializers import AuthSerializer
from util.messages.hundle_messages import success_response


class CustomerViewSet(ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = AuthSerializer
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    authentication_classes = [OAuth2Authentication]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    def update(self, request, *args, **kwargs):
        """
        Modify Customer details/profile
        """
        instance = self.get_object()
        if not instance:
            raise exceptions.NotFound("Customer not found", "not_found")
        serializer = self.get_serializer(instance, many=isinstance(request.data, list), partial=True, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.update(instance, request.data)
        data = success_response(status_code=status.HTTP_200_OK, message_code="update_success",
                                message=f"{instance} updated successfully")
        return response.Response(data=data, status=status.HTTP_200_OK)
