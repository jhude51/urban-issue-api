from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Issue
from .serializers import IssueSerializer

class IssueList(APIView):
    def get(self, request):
        issues = Issue.objects.all().order_by('-created_at')
        serializer = IssueSerializer(issues, many=True)
        return Response(serializer.data)
