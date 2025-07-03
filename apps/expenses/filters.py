import datetime
from django.utils import timezone
from django_filters import rest_framework as filters
from .models import Expense


class ExpenseFilter(filters.FilterSet):
    date_range = filters.CharFilter(method="filter_date_range")
    start_date = filters.DateFilter(field_name="payment_date", lookup_expr="gte")
    end_date = filters.DateFilter(field_name="payment_date", lookup_expr="lte")

    class Meta:
        model = Expense
        fields = ["user", "type", "start_date", "end_date", "date_range"]

    def filter_date_range(self, queryset, name, value):
        today = timezone.now().date()

        if value == "last_week":
            start_date = today - datetime.timedelta(days=7)
            return queryset.filter(payment_date__gte=start_date)

        elif value == "last_month":
            start_date = today - datetime.timedelta(days=30)
            return queryset.filter(payment_date__gte=start_date)

        elif value == "last_3_months":
            start_date = today - datetime.timedelta(days=90)
            return queryset.filter(payment_date__gte=start_date)

        return queryset
