from rest_framework import serializers

from .models import Issue


class IssueSerializer(serializers.ModelSerializer):
    STATUS_TRANSITIONS = {
        "reported": {"acknowledged"},
        "acknowledged": {"in_progress"},
        "in_progress": {"resolved"},
        "resolved": {"closed", "in_progress"},
        "closed": set(),
    }

    def validate_title(self, value):
        if len(value) < 5:
            raise serializers.ValidationError(
                "Title must be at least 5 characters long."
            )
        return value

    def validate_status(self, value):
        # New issues must always begin as reported.
        if self.instance is None:
            if value != "reported":
                raise serializers.ValidationError(
                    "New issues must start with a status 'reported'."
                )
            return value

        current_status = self.instance.status

        # No actual transition is taking place.
        if value == current_status:
            return value

        allowed_statuses = self.STATUS_TRANSITIONS.get(
            current_status,
            set(),
        )

        if value not in allowed_statuses:
            raise serializers.ValidationError(
                f"Cannot transition issue from "
                f"'{current_status}' to '{value}'."
            )

        return value

    class Meta:
        model = Issue
        fields = [
            "id",
            "title",
            "description",
            "location",
            "reporter",
            "category",
            "priority",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

        extra_kwargs = {
            "title": {
                "help_text": "Short summary of the reported urban issue."
            },
            "description": {
                "help_text": "Detailed description of the problem."
            },
            "location": {
                "help_text": "Human-readable location where the issue is located."
            },
            "reporter": {
                "help_text": "Type of party reporting the issue."
            },
            "category": {
                "help_text": "Infrastructure category assigned to the issue."
            },
            "priority": {
                "help_text": "Operational priority of the reported issue."
            },
            "status": {
                "help_text": (
                    "Current lifecycle state. New issues begin as 'reported'."
                ),
            },
        }
