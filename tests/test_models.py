"""Unit tests for models, validation schemas, and enum invariants."""
import unittest
from pydantic import ValidationError

from tracker.models import (
    AppStatus,
    LocationType,
    EventType,
    ApplicationCreate,
    ApplicationStatusUpdate,
    ApplicationResponse,
    TimelineEventResponse,
    MetricsResponse
)

class TestModels(unittest.TestCase):
    def test_enums_integrity(self):
        self.assertEqual(AppStatus.APPLIED.value, "APPLIED")
        self.assertEqual(AppStatus.TECHNICAL.value, "TECHNICAL")
        self.assertEqual(AppStatus.OFFER.value, "OFFER")
        self.assertEqual(LocationType.NAIROBI.value, "NAIROBI")
        self.assertEqual(LocationType.REMOTE_EMEA.value, "REMOTE_EMEA")
        self.assertEqual(EventType.STATUS_CHANGE.value, "STATUS_CHANGE")

    def test_application_create_valid_minimal(self):
        app = ApplicationCreate(company="Safaricom", role="Cloud Architect")
        self.assertEqual(app.company, "Safaricom")
        self.assertEqual(app.role, "Cloud Architect")
        self.assertEqual(app.location_type, LocationType.REMOTE_GLOBAL)
        self.assertEqual(app.channel, "Direct")
        self.assertEqual(app.status, AppStatus.APPLIED)
        self.assertIsNone(app.compensation)
        self.assertIsNone(app.job_url)

    def test_application_create_valid_complete(self):
        app = ApplicationCreate(
            company="Microsoft ADC",
            role="Systems Engineer",
            location_type=LocationType.NAIROBI,
            compensation="KES 500,000",
            channel="Referral",
            job_url="https://careers.microsoft.com",
            contact_person="Lead Recruiter",
            notes="Deep Linux kernel focus",
            status=AppStatus.SCREENING
        )
        self.assertEqual(app.company, "Microsoft ADC")
        self.assertEqual(app.status, AppStatus.SCREENING)
        self.assertEqual(app.compensation, "KES 500,000")

    def test_application_create_missing_required_fields(self):
        with self.assertRaises(ValidationError):
            ApplicationCreate(company="OnlyCompany")
        with self.assertRaises(ValidationError):
            ApplicationCreate(role="OnlyRole")

    def test_application_create_empty_strings(self):
        with self.assertRaises(ValidationError):
            ApplicationCreate(company="", role="ValidRole")
        with self.assertRaises(ValidationError):
            ApplicationCreate(company="ValidCompany", role="")

    def test_application_status_update_validation(self):
        update = ApplicationStatusUpdate(status=AppStatus.TECHNICAL, note="Passed screen")
        self.assertEqual(update.status, AppStatus.TECHNICAL)
        self.assertEqual(update.note, "Passed screen")

        with self.assertRaises(ValidationError):
            ApplicationStatusUpdate(status="INVALID_STATUS")

    def test_metrics_response_structure(self):
        metrics = MetricsResponse(
            total_applications=10,
            active_applications=6,
            interview_count=4,
            offer_count=1,
            rejection_count=3,
            interview_rate_pct=40.0,
            offer_rate_pct=10.0,
            funnel={"APPLIED": 4, "SCREENING": 2, "OFFER": 1, "REJECTED": 3}
        )
        self.assertEqual(metrics.total_applications, 10)
        self.assertEqual(metrics.interview_rate_pct, 40.0)

if __name__ == "__main__":
    unittest.main()
