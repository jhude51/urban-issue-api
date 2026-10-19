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
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(
            response.data["results"][0]["title"],
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
            response.data["results"][0]["id"],
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

    def test_new_issue_defaults_to_reported(self):
        payload = {
            "title": "Damaged road surface",
            "description": "Several large potholes are present.",
            "location": "Ibadan",
            "reporter": "citizen",
            "category": "road",
            "priority": "high",
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
        self.assertEqual(
            response.data["status"],
            "reported",
        )

    def test_new_issue_cannot_start_with_later_status(self):
        payload = {
            "title": "Damaged road surface",
            "description": "Several large potholes are present.",
            "location": "Ibadan",
            "reporter": "citizen",
            "status": "resolved",
        }

        response = self.client.post(
            self.list_url,
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
        self.assertIn("status", response.data)

    def test_valid_status_transition(self):
        response = self.client.patch(
            self.detail_url,
            {"status": "acknowledged"},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.issue.refresh_from_db()

        self.assertEqual(
            self.issue.status,
            "acknowledged",
        )

    def test_invalid_status_transition(self):
        response = self.client.patch(
            self.detail_url,
            {"status": "resolved"},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.issue.refresh_from_db()

        self.assertEqual(
            self.issue.status,
            "reported",
        )

    def test_resolved_issue_can_be_reopened(self):
        self.issue.status = "resolved"
        self.issue.save()

        response = self.client.patch(
            self.detail_url,
            {"status": "in_progress"},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.issue.refresh_from_db()

        self.assertEqual(
            self.issue.status,
            "in_progress",
        )

    def test_closed_issue_cannot_be_reopened(self):
        self.issue.status = "closed"
        self.issue.save()

        response = self.client.patch(
            self.detail_url,
            {"status": "in_progress"},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.issue.refresh_from_db()

        self.assertEqual(
            self.issue.status,
            "closed",
        )

    def test_create_issue_with_category_and_priority(self):
        payload = {
            "title": "Collapsed drainage channel",
            "description": "The drainage wall has collapsed.",
            "location": "Ring Road, Ibadan",
            "reporter": "citizen",
            "category": "drainage",
            "priority": "high",
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
        self.assertEqual(
            response.data["category"],
            "drainage",
        )
        self.assertEqual(
            response.data["priority"],
            "high",
        )

    def test_new_issue_uses_default_category_and_priority(self):
        payload = {
            "title": "Unclassified urban issue",
            "description": "An issue has been reported.",
            "location": "Ibadan",
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
        self.assertEqual(
            response.data["category"],
            "other",
        )
        self.assertEqual(
            response.data["priority"],
            "medium",
        )

    def test_reject_invalid_category(self):
        payload = {
            "title": "Electrical infrastructure issue",
            "description": "An electrical issue has been reported.",
            "location": "Ibadan",
            "reporter": "citizen",
            "category": "electricity",
        }

        response = self.client.post(
            self.list_url,
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
        self.assertIn("category", response.data)


    def test_reject_invalid_priority(self):
        payload = {
            "title": "Serious drainage issue",
            "description": "A drainage problem requires attention.",
            "location": "Ibadan",
            "reporter": "citizen",
            "priority": "urgent",
        }

        response = self.client.post(
            self.list_url,
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
        self.assertIn("priority", response.data)

    def test_updating_issue_changes_updated_at(self):
        original_updated_at = self.issue.updated_at

        response = self.client.patch(
            self.detail_url,
            {"location": "New Bodija, Ibadan"},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.issue.refresh_from_db()

        self.assertGreater(
            self.issue.updated_at,
            original_updated_at,
        )

    def test_server_managed_fields_are_read_only(self):
        payload = {
            "title": "Damaged road surface",
            "description": "Several potholes require repair.",
            "location": "Ibadan",
            "reporter": "citizen",
            "id": 999,
            "created_at": "2035-01-01T00:00:00Z",
            "updated_at": "2035-01-01T00:00:00Z",
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

        created_issue = Issue.objects.get(
            pk=response.data["id"],
        )

        self.assertNotEqual(created_issue.id, 999)
        self.assertNotEqual(
            str(created_issue.created_at),
            "2035-01-01T00:00:00Z",
        )
        self.assertNotEqual(
            str(created_issue.updated_at),
            "2035-01-01T00:00:00Z",
        )

    def test_filter_issues_by_category(self):
        Issue.objects.create(
            title="Blocked drainage channel",
            description="Drainage is blocked.",
            location="Challenge, Ibadan",
            reporter="citizen",
            category="drainage",
            priority="high",
        )

        response = self.client.get(
            self.list_url,
            {"category": "drainage"},
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(
            response.data["results"][0]["category"],
            "drainage",
        )

    def test_filter_issues_by_multiple_fields(self):
        Issue.objects.create(
            title="Serious road damage",
            description="Road surface has collapsed.",
            location="Ibadan",
            reporter="citizen",
            category="road",
            priority="high",
            status="reported",
        )

        Issue.objects.create(
            title="Minor road damage",
            description="Small pothole.",
            location="Ibadan",
            reporter="citizen",
            category="road",
            priority="low",
            status="reported",
        )

        response = self.client.get(
            self.list_url,
            {
                "category": "road",
                "priority": "high",
                "status": "reported",
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(response.data["count"], 1)
        self.assertEqual(
            response.data["results"][0]["title"],
            "Serious road damage",
        )

    def test_search_issues_by_location(self):
        Issue.objects.create(
            title="Broken drainage channel",
            description="Waste is preventing water flow.",
            location="Bodija, Ibadan",
            reporter="citizen",
        )

        Issue.objects.create(
            title="Broken streetlight",
            description="Streetlight is not working.",
            location="Mokola, Ibadan",
            reporter="citizen",
        )

        response = self.client.get(
            self.list_url,
            {"search": "Bodija"},
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(response.data["count"], 1)
        self.assertEqual(
            response.data["results"][0]["location"],
            "Bodija, Ibadan",
        )

    def test_order_issues_by_title(self):
        Issue.objects.create(
            title="Zebra crossing issue",
            description="Road marking is damaged.",
            location="Ibadan",
            reporter="citizen",
        )

        response = self.client.get(
            self.list_url,
            {"ordering": "title"},
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        titles = [
            issue["title"]
            for issue in response.data["results"]
        ]

        self.assertEqual(
            titles,
            sorted(titles),
        )

    def test_default_ordering_is_newest_first(self):
        newer_issue = Issue.objects.create(
            title="Newer reported issue",
            description="This issue was created later.",
            location="Ibadan",
            reporter="citizen",
        )

        response = self.client.get(self.list_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["results"][0]["id"],
            newer_issue.id,
        )

    def test_issue_list_is_paginated(self):
        for number in range(6):
            Issue.objects.create(
                title=f"Reported issue {number}",
                description="Test pagination issue.",
                location="Ibadan",
                reporter="citizen",
            )

        response = self.client.get(self.list_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertIn("count", response.data)
        self.assertIn("next", response.data)
        self.assertIn("previous", response.data)
        self.assertIn("results", response.data)

        self.assertEqual(response.data["count"], 7)
        self.assertEqual(
            len(response.data["results"]),
            5,
        )
        self.assertIsNotNone(response.data["next"])

    def test_client_can_request_page_size(self):
        for number in range(4):
            Issue.objects.create(
                title=f"Pagination issue {number}",
                description="Testing custom page size.",
                location="Ibadan",
                reporter="citizen",
            )

        response = self.client.get(
            self.list_url,
            {"page_size": 2},
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(response.data["count"], 5)
        self.assertEqual(
            len(response.data["results"]),
            2,
        )


class APIDocumentationTest(APITestCase):
    def test_openapi_schema_is_available(self):
        response = self.client.get(
            reverse("api-schema"),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        schema_content = response.content.decode()

        self.assertIn("openapi:", schema_content)
        self.assertIn("/issues/", schema_content)

    def test_swagger_ui_is_available(self):
        response = self.client.get(
            reverse("swagger-ui"),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_redoc_ui_is_available(self):
        response = self.client.get(
            reverse("redoc"),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )