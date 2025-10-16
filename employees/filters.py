import re
from django.db.models import Q, Value as V
from django.db.models.functions import Concat
from django_filters import rest_framework as filters
from .models import Employee, Department

class EmployeeFilter(filters.FilterSet):
    search = filters.CharFilter(method="filter_search")
    department = filters.ChoiceFilter(field_name="department", choices=Department.choices)

    class Meta:
        model = Employee
        fields = ["search", "email", "department"]

    def filter_search(self, queryset, name, value):
        q = (value or "").strip()
        if not q:
            return queryset
        terms = [t for t in re.split(r"\s+", q) if t]
        for t in terms:
            queryset = queryset.annotate(
                full_name=Concat("first_name", V(" "), "last_name")
            ).filter(
                Q(full_name__icontains=t) |
                Q(first_name__icontains=t) |
                Q(last_name__icontains=t)  |
                Q(email__icontains=t)
            )
        return queryset
