from rest_framework import generics

from .models import Issue
from .serializers import IssueSerializer

class IssueList(generics.ListCreateAPIView):
    queryset = Issue.objects.all().order_by("-created_at")
    serializer_class = IssueSerializer


class IssueDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
