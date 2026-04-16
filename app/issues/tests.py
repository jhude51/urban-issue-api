from django.test import TestCase
from .models import Issue

class IssueModelTest(TestCase):
    def test_issue_creation(self):
        issue = Issue.objects.create(
            title="Test Issue",
            description="Test",
            location="Test City",
            reporter="vendor"
        )
        self.assertEqual(issue.title, "Test Issue")
