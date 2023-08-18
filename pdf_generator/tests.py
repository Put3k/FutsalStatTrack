import datetime

# Create your tests here.
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from stat_track.models import League

from .models import Report


class BookTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user_1 = get_user_model().objects.create_user(
            username="reportuser_1",
            email="reportuser_1@email.com",
            password="testpass123",
            first_name="Julius",
            last_name="Caesar",
        )

        cls.league_1 = League.objects.create(
            owner=cls.user_1,
            name="report 1 league",
            start_date=datetime.date.today(),
        )

        cls.report_1 = Report.objects.create(
            league=cls.league_1,
            owner=cls.user_1,
            generated=datetime.date.today(),
        )


        cls.user_2 = get_user_model().objects.create_user(
            username="reportuser_2",
            email="reportuser_2@email.com",
            password="testpass123",
            first_name="Karol",
            last_name="Wojtyla",
        )

        cls.league_2 = League.objects.create(
            owner=cls.user_2,
            name="report 2 league",
            start_date=datetime.date.today(),
        )

        cls.report_2 = Report.objects.create(
            league=cls.league_2,
            owner=cls.user_2,
            generated=datetime.date.today(),
            temporary=True
        )

        cls.report_3 = Report.objects.create(
            league=cls.league_2,
            owner=cls.user_2,
            generated=datetime.date.today(),
            temporary=True
        )

    def test_report_default_temporary_value_case_1(self):
        """First created report by the user should have 'temporary' value set to True."""
        self.assertEqual(self.report_1.temporary, True)

    def test_report_default_temporary_value_case_2(self):
        """When user already created his first report, other reports cannot have 'temporary' value set to True."""
        self.assertEqual(self.report_3.temporary, False)

