from django_filters.rest_framework import DjangoFilterBackend
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, OAuth2Authentication
from rest_framework import status, exceptions
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from util.messages.hundle_messages import success_response
from .models import Orders
from .serializers import OrderSerializer


class CustomView(ModelViewSet):
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticated, TokenHasReadWriteScope]
    authentication_classes = [OAuth2Authentication]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    def create(self, request, *args, **kwargs):
        """Upload resource to the database"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.create(serializer.validated_data)
        response = success_response(status_code=status.HTTP_200_OK, message_code="upload_data",
                                    message={"message": f"{data.order_id} Created successfully"})
        return Response(response, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        """
        Fetch resource by the orderID
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        response = success_response(status_code=status.HTTP_200_OK, message_code="get_data", message={"data": data})
        return Response(data=response)

    def update(self, request, *args, **kwargs):
        """
        Modify resource details
        :param request:
        :param args:
        :param kwargs:
        :return:

        """
        instance = self.get_object()
        if not instance:
            raise exceptions.NotFound("Resource not found", "not_found")
        serializer = self.get_serializer(instance, many=isinstance(request.data, list), partial=True, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.update(instance, request.data)
        data = success_response(status_code=status.HTTP_200_OK, message_code="update_success",
                                message=f"{instance} updated successfully")
        return Response(data=data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        """
        Delete resource from the database
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        response_data = success_response(status_code=status.HTTP_204_NO_CONTENT, message_code="delete_success",
                                         message=f"{instance} deleted successfully.")

        return Response(data=response_data, status=status.HTTP_204_NO_CONTENT)


class OrderView(CustomView):
    queryset = Orders.objects.all()
    serializer_class = OrderSerializer
    search_fields = ('^order_id', '^amount', '^order_   status')
    ordering_fields = ['-created_at']
