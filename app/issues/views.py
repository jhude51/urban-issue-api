from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics

from .models import Issue
from .pagination import IssuePagination
from .serializers import IssueSerializer

class IssueList(generics.ListCreateAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    pagination_class = IssuePagination

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = [
        "reporter",
        "category",
        "priority",
        "status",
    ]

    search_fields = [
        "title",
        "description",
        "location",
    ]

    ordering_fields = [
        "id",
        "title",
        "location",
        "created_at",
        "updated_at",
    ]

    ordering = ["-created_at"]


class IssueDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
