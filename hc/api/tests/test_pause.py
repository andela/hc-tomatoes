from hc.api.models import Check
from hc.test import BaseTestCase


class PauseTestCase(BaseTestCase):

    def test_it_works(self):
        check = Check(user=self.alice, status="up")
        check.save()

        url = "/api/v1/checks/%s/pause" % check.code
        r = self.client.post(url, "", content_type="application/json",
                             HTTP_X_API_KEY="abc")

        ### Assert the expected status code and check's status
        # test if the request was successful
        self.assertEqual(r.status_code, 200)
        # test if the check status changed to paused
        check.refresh_from_db()
        self.assertEqual(check.status, "paused")

    def test_it_validates_ownership(self):
        check = Check(user=self.bob, status="up")
        check.save()

        url = "/api/v1/checks/%s/pause" % check.code
        r = self.client.post(url, "", content_type="application/json",
                             HTTP_X_API_KEY="abc")

        self.assertEqual(r.status_code, 400)

        ### Test that it only allows post requests
    def test_it_only_allows_post_requests(self):
        """ tests if the pause endpoint allows only post requests """
        check = Check(user=self.alice, status="up")
        check.save()

        url = "/api/v1/checks/{}/pause".format(check.code)
        r = self.client.get(url, HTTP_X_API_KEY="abc")
        self.assertEqual(r.status_code, 405)

