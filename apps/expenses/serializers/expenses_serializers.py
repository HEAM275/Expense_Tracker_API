from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from ..models import Expense


class ExpenseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ('amount', 'description', 'type', 'user', 'payment_date')
        read_only_fields = fields


class ExpenseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ('amount', 'description', 'type', 'user', 'payment_date')

    def validate_amount(self, value):
        if value < 0:
            raise serializers.ValidationError(
                _("El monto no puede ser negativo."))
        return value

    def validate_type(self, value):
        valid_choices = dict(Expense.EXPENSE_TYPE_CHOICES).keys()
        if value not in valid_choices:
            raise serializers.ValidationError(_("Tipo de gasto no válido."))
        return value


class ExpenseUpdateSerializer(serializers.ModelSerializer):
    payment_date = serializers.DateTimeField(required=True)

    class Meta:
        model = Expense
        fields = [
            'id',
            'amount',
            'description',
            'type',
            'user',
            'payment_date'
        ]
        read_only_fields = ['user']

    # Validación: amount >= 0
    def validate_amount(self, value):
        if value < 0:
            raise serializers.ValidationError(
                _("El monto no puede ser negativo."))
        return value

    def validate_type(self, value):
        valid_choices = dict(Expense.EXPENSE_TYPE_CHOICES).keys()
        if value not in valid_choices:
            raise serializers.ValidationError(_("Tipo de gasto no válido."))
        return value

    # def validate(self, data):
    #
    #     return data
