import json
from datetime import timedelta as td
from django.utils.timezone import now

from hc.api.models import Check
from hc.test import BaseTestCase


class ListChecksTestCase(BaseTestCase):

    def setUp(self):
        super(ListChecksTestCase, self).setUp()

        self.now = now().replace(microsecond=0)

        self.a1 = Check(user=self.alice, name="Alice 1")
        self.a1.timeout = td(seconds=3600)
        self.a1.grace = td(seconds=900)
        self.a1.last_ping = self.now
        self.a1.n_pings = 1
        self.a1.status = "new"
        self.a1.save()

        self.a2 = Check(user=self.alice, name="Alice 2")
        self.a2.timeout = td(seconds=86400)
        self.a2.grace = td(seconds=3600)
        self.a2.last_ping = self.now
        self.a2.status = "up"
        self.a2.save()

    def get(self):
        return self.client.get("/api/v1/checks/", HTTP_X_API_KEY="abc")

    def test_it_works(self):
        r = self.get()
        ### Assert the response status code
        self.assertEqual(r.status_code, 200)

        doc = r.json()
        self.assertTrue("checks" in doc)

        checks = {check["name"]: check for check in doc["checks"]}
        ### Assert the expected length of checks
        self.assertEqual(len(checks), 2)
        ### Assert the checks Alice 1 and Alice 2's timeout, grace, ping_url, status,
        self.assertIn('timeout', checks['Alice 1'])
        self.assertIn('grace', checks['Alice 1'])
        self.assertIn('status', checks['Alice 1'])
        self.assertIn('status', checks['Alice 1'])

        self.assertIn('timeout', checks['Alice 2'])
        self.assertIn('grace', checks['Alice 2'])
        self.assertIn('status', checks['Alice 2'])
        self.assertIn('status', checks['Alice 2'])

        ### last_ping, n_pings and pause_url
        self.assertIn('last_ping', checks['Alice 2'])
        self.assertIn('n_pings', checks['Alice 2'])
        self.assertIn('pause_url', checks['Alice 2'])

    def test_it_shows_only_users_checks(self):
        bobs_check = Check(user=self.bob, name="Bob 1")
        bobs_check.save()

        r = self.get()
        data = r.json()
        self.assertEqual(len(data["checks"]), 2)
        for check in data["checks"]:
            self.assertNotEqual(check["name"], "Bob 1")

    ### Test that it accepts an api_key in the request
    def test_that_it_accepts_an_api_key(self):
        """
        This checks api then returns a response.
        """
        response = self.client.get("/api/v1/checks/",
                                   HTTP_X_API_KEY="abc"
                                   )
        self.assertEqual(response.status_code, 200)

    def test_that_it_rejects_a_wrong_api_key(self):
        """
        This does a check for the api coming in is wrong then returns a response.
        """
        response = self.client.get("/api/v1/checks/",
                                   HTTP_X_API_KEY="abghdsghhdshdsc"
                                   )
        self.assertEqual(response.json()['error'], 'wrong api_key')
        self.assertTrue(response.status_code == 400)