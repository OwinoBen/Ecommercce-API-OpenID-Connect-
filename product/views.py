from django_filters.rest_framework import DjangoFilterBackend
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, OAuth2Authentication
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from util.messages.hundle_messages import success_response
from .serializers import ProductSerializer
from .models import Product


class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticated, TokenHasReadWriteScope]
    authentication_classes = [OAuth2Authentication]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.create(serializer.validated_data)
        response_data = success_response(status_code=status.HTTP_201_CREATED, message_code="upload_success", message={
            "message": [f"{serializer.data['product_title']} uploaded successfully."]},)
        return Response(data=response_data, status=status.HTTP_201_CREATED)
