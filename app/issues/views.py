from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Issue

class IssueList(APIView):
    def get(self, request):
        issues = Issue.objects.all().values()
        return Response(list(issues))
