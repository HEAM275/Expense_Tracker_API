from django.utils.translation import gettext_lazy as _
from drf_yasg import openapi as oa
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated

from apps.common.views import BaseModelViewSet
from apps.expenses.models import Expense
from apps.expenses.serializers import (
    ExpenseListSerializer,
    ExpenseCreateSerializer,
    ExpenseUpdateSerializer
)

from apps.expenses.filters import ExpenseFilter


class ExpenseViewSet(BaseModelViewSet):
    """
    API endpoints for management of expenses
    """
    queryset = Expense.objects.filter(is_active=True)
    serializer_class = ExpenseListSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = ExpenseFilter

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ExpenseListSerializer
        if self.action == 'create':
            return ExpenseCreateSerializer
        if self.action in ['update', 'partial_update']:
            return ExpenseUpdateSerializer
        return ExpenseListSerializer

    @swagger_auto_schema(
        operation_description='List all expenses with optional filters',
        manual_parameters=[
            oa.Parameter(
                name='date_range',
                in_=oa.IN_QUERY,
                description="Filter by date range (last_week, last_month, last_3_months)",
                type=oa.TYPE_STRING,
                required=False,
                enum=['last_week', 'last_month', 'last_3_months']
            ),
            oa.Parameter(
                name='start_date',
                in_=oa.IN_QUERY,
                description="Start date for custom range (YYYY-MM-DD)",
                type=oa.TYPE_STRING,
                format='date',
                required=False
            ),
            oa.Parameter(
                name='end_date',
                in_=oa.IN_QUERY,
                description="End date for custom range (YYYY-MM-DD)",
                type=oa.TYPE_STRING,
                format='date',
                required=False
            ),
            oa.Parameter(
                name='Authorization',
                in_=oa.IN_HEADER,
                description="Bearer <access_token>",
                type=oa.TYPE_STRING,
                required=True,
            ),
        ],
        responses={
            200: oa.Response(
                description='List of expenses',
                schema=ExpenseListSerializer(many=True)
            ),
            403: oa.Response(
                description='Forbidden',
                schema=oa.Schema(
                    type=oa.TYPE_OBJECT,
                    properties={
                        'detail': oa.Schema(type=oa.TYPE_STRING)
                    }
                )
            )
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description='Retrieve a specific expense',
        manual_parameters=[
            oa.Parameter(
                name='Authorization',
                in_=oa.IN_HEADER,
                description="Bearer <access_token>",
                type=oa.TYPE_STRING,
                required=True,
            ),
        ],
        responses={
            200: oa.Response(
                description='Expense details',
                schema=ExpenseListSerializer
            ),
            403: oa.Response(
                description='Forbidden',
                schema=oa.Schema(
                    type=oa.TYPE_OBJECT,
                    properties={
                        'detail': oa.Schema(type=oa.TYPE_STRING)
                    }
                )
            ),
            404: oa.Response(
                description='Expense not found',
                schema=oa.Schema(
                    type=oa.TYPE_OBJECT,
                    properties={
                        'detail': oa.Schema(type=oa.TYPE_STRING)
                    }
                )
            )
        }
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description='Create a new expense',
        request_body=ExpenseCreateSerializer,
        manual_parameters=[
            oa.Parameter(
                name='Authorization',
                in_=oa.IN_HEADER,
                description="Bearer <access_token>",
                type=oa.TYPE_STRING,
                required=True,
            ),
        ],
        responses={
            201: oa.Response(
                description='Expense created successfully',
                schema=ExpenseListSerializer
            ),
            400: oa.Response(
                description='Bad request',
                schema=oa.Schema(
                    type=oa.TYPE_OBJECT,
                    properties={
                        'message': oa.Schema(type=oa.TYPE_STRING),
                        'errors': oa.Schema(type=oa.TYPE_OBJECT)
                    }
                )
            ),
            403: oa.Response(
                description='Forbidden',
                schema=oa.Schema(
                    type=oa.TYPE_OBJECT,
                    properties={
                        'detail': oa.Schema(type=oa.TYPE_STRING)
                    }
                )
            )
        }
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():

            self.perform_create(serializer)
            return Response({
                'message': _('Expense created successfully'),
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'message': _('Expense could not be created'),
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description='Update an existing expense',
        request_body=ExpenseUpdateSerializer,
        manual_parameters=[
            oa.Parameter(
                name='Authorization',
                in_=oa.IN_HEADER,
                description="Bearer <access_token>",
                type=oa.TYPE_STRING,
                required=True,
            ),
        ],
        responses={
            200: oa.Response(
                description='Expense updated successfully',
                schema=ExpenseListSerializer
            ),
            400: oa.Response(
                description='Bad request',
                schema=oa.Schema(
                    type=oa.TYPE_OBJECT,
                    properties={
                        'message': oa.Schema(type=oa.TYPE_STRING),
                        'errors': oa.Schema(type=oa.TYPE_OBJECT)
                    }
                )
            ),
            403: oa.Response(
                description='Forbidden',
                schema=oa.Schema(
                    type=oa.TYPE_OBJECT,
                    properties={
                        'detail': oa.Schema(type=oa.TYPE_STRING)
                    }
                )
            ),
            404: oa.Response(
                description='Expense not found',
                schema=oa.Schema(
                    type=oa.TYPE_OBJECT,
                    properties={
                        'detail': oa.Schema(type=oa.TYPE_STRING)
                    }
                )
            )
        }
    )
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)

        if serializer.is_valid():

            self.perform_update(serializer)
            return Response({
                'message': _('Expense updated successfully'),
                'data': serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            'message': _('Expense could not be updated'),
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description='Delete an expense (soft delete)',
        manual_parameters=[
            oa.Parameter(
                name='Authorization',
                in_=oa.IN_HEADER,
                description="Bearer <access_token>",
                type=oa.TYPE_STRING,
                required=True,
            ),
        ],
        responses={
            204: oa.Response(
                description='Expense deleted successfully'
            ),
            403: oa.Response(
                description='Forbidden',
                schema=oa.Schema(
                    type=oa.TYPE_OBJECT,
                    properties={
                        'detail': oa.Schema(type=oa.TYPE_STRING)
                    }
                )
            ),
            404: oa.Response(
                description='Expense not found',
                schema=oa.Schema(
                    type=oa.TYPE_OBJECT,
                    properties={
                        'detail': oa.Schema(type=oa.TYPE_STRING)
                    }
                )
            )
        }
    )
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
