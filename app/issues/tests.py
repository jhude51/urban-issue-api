from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Issue


class IssueAPITest(APITestCase):
    def setUp(self):
        self.issue = Issue.objects.create(
            title="Broken traffic light",
            description="The traffic light is not functioning.",
            location="Ring Road, Ibadan",
            reporter="citizen",
        )

        self.list_url = reverse("issue-list")
        self.detail_url = reverse(
            "issue-detail",
            args=[self.issue.pk],
        )

    def test_list_issues(self):
        response = self.client.get(self.list_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data[0]["title"],
            self.issue.title,
        )

    def test_list_issues_returns_newest_first(self):
        newer_issue = Issue.objects.create(
            title="Blocked drainage channel",
            description="Waste is blocking the drainage channel.",
            location="Challenge, Ibadan",
            reporter="vendor",
        )

        response = self.client.get(self.list_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            response.data[0]["id"],
            newer_issue.id,
        )

    def test_create_issue(self):
        payload = {
            "title": "Damaged streetlight",
            "description": "The streetlight has fallen.",
            "location": "Bodija, Ibadan",
            "reporter": "citizen",
        }

        response = self.client.post(
            self.list_url,
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )
        self.assertEqual(Issue.objects.count(), 2)
        self.assertEqual(
            response.data["title"],
            payload["title"],
        )

    def test_retrieve_issue(self):
        response = self.client.get(self.detail_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            response.data["id"],
            self.issue.id,
        )

    def test_replace_issue_with_put(self):
        payload = {
            "title": "Repaired traffic light",
            "description": "The traffic light has been repaired.",
            "location": "Ring Road, Ibadan",
            "reporter": "vendor",
        }

        response = self.client.put(
            self.detail_url,
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.issue.refresh_from_db()

        self.assertEqual(
            self.issue.title,
            payload["title"],
        )
        self.assertEqual(
            self.issue.reporter,
            payload["reporter"],
        )

    def test_partially_update_issue_with_patch(self):
        payload = {
            "location": "Ring Road Roundabout, Ibadan",
        }

        response = self.client.patch(
            self.detail_url,
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.issue.refresh_from_db()

        self.assertEqual(
            self.issue.location,
            payload["location"],
        )
        self.assertEqual(
            self.issue.title,
            "Broken traffic light",
        )

    def test_reject_short_title_during_update(self):
        response = self.client.patch(
            self.detail_url,
            {"title": "Bad"},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
        self.assertIn("title", response.data)

    def test_return_404_for_missing_issue(self):
        missing_url = reverse(
            "issue-detail",
            args=[999999],
        )

        response = self.client.get(missing_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_delete_issue(self):
        response = self.client.delete(self.detail_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )
        self.assertFalse(
            Issue.objects.filter(pk=self.issue.pk).exists()
        )