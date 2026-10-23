from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiResponse,
    extend_schema,
    extend_schema_view,
)
from rest_framework import filters, generics

from .models import Issue
from .pagination import IssuePagination
from .serializers import IssueSerializer


@extend_schema_view(
    get=extend_schema(
        tags=["Issues"],
        summary="List urban issues",
        description=(
            "Return a paginated list of reported urban issues. "
            "Results can be filtered by reporter, category, priority, "
            "and status. Text search is supported across title, "
            "description, and location. Results can also be ordered "
            "using supported ordering fields."
        ),
    ),
    post=extend_schema(
        tags=["Issues"],
        summary="Report a new urban issue",
        description=(
            "Create a new urban issue report. "
            "New issues always begin with status 'reported'. "
            "If category or priority are omitted, the defaults are "
            "'other' and 'medium' respectively."
        ),
        responses={
            201: IssueSerializer,
            400: OpenApiResponse(
                description="Invalid issue data.",
            ),
        },
        examples=[
            OpenApiExample(
                "Road issue report",
                value={
                    "title": "Large pothole on major road",
                    "description": (
                        "A large pothole is causing vehicles to leave their lane."
                    ),
                    "location": "Ring Road, Ibadan",
                    "reporter": "citizen",
                    "category": "road",
                    "priority": "high",
                },
                request_only=True,
            ),
            OpenApiExample(
                "Created issue",
                value={
                    "id": 12,
                    "title": "Large pothole on major road",
                    "description": (
                        "A large pothole is causing vehicles to leave their lane."
                    ),
                    "location": "Ring Road, Ibadan",
                    "reporter": "citizen",
                    "category": "road",
                    "priority": "high",
                    "status": "reported",
                    "created_at": "2026-10-15T16:30:00Z",
                    "updated_at": "2026-10-15T16:30:00Z",
                },
                response_only=True,
                status_codes=["201"],
            ),
        ],
    ),
)
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


@extend_schema_view(
    get=extend_schema(
        tags=["Issues"],
        summary="Retrieve an issue",
        description=("Return the complete details of a single urban issue."),
        responses={
            200: IssueSerializer,
            404: OpenApiResponse(
                description="Issue not found.",
            ),
        },
    ),
    put=extend_schema(
        tags=["Issues"],
        summary="Replace an issue",
        description=(
            "Replace the writable fields of an existing issue. "
            "Any status change must follow the configured lifecycle rules."
        ),
        responses={
            200: IssueSerializer,
            400: OpenApiResponse(
                description="Invalid issue data or status transition.",
            ),
            404: OpenApiResponse(
                description="Issue not found.",
            ),
        },
    ),
    patch=extend_schema(
        tags=["Issues"],
        summary="Partially update an issue",
        description=(
            "Update one or more writable fields without replacing "
            "the entire issue. Status changes must follow this lifecycle: "
            "reported → acknowledged → in_progress → resolved → closed. "
            "A resolved issue may also transition back to in_progress."
        ),
        responses={
            200: IssueSerializer,
            400: OpenApiResponse(
                description="Invalid issue data or status transition.",
            ),
            404: OpenApiResponse(
                description="Issue not found.",
            ),
        },
        examples=[
            OpenApiExample(
                "Acknowledge issue",
                value={
                    "status": "acknowledged",
                },
                request_only=True,
            ),
            OpenApiExample(
                "Update priority",
                value={
                    "priority": "critical",
                },
                request_only=True,
            ),
        ],
    ),
    delete=extend_schema(
        tags=["Issues"],
        summary="Delete an issue",
        description=("Permanently delete an existing urban issue."),
        responses={
            204: OpenApiResponse(
                description="Issue deleted successfully.",
            ),
            404: OpenApiResponse(
                description="Issue not found.",
            ),
        },
    ),
)
class IssueDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
