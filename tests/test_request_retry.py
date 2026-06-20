"""Tests for transient-5xx retry in LynseAPI._request."""

import unittest
from unittest import mock

import lynse
from lynse import LynseAPI, LynseAPIError


class FakeResp:
    def __init__(self, status, payload=None, text=None):
        self.status_code = status
        self._p = payload or {}
        self.text = text or "{}"

    def json(self):
        return self._p


class RequestRetryTests(unittest.TestCase):
    def setUp(self):
        self.api = LynseAPI.__new__(LynseAPI)
        self.api.api_host = "https://api.example.com"
        self.api.api_key = "dk_test"
        self.api._get_token = lambda *a, **k: "aaaa.bbbb.cccc"
        self.api._build_auth_headers = lambda token, extra=None: {"Authorization": token}
        self.api._log_lynse_request = lambda *a, **k: None
        self.api._log_lynse_response = lambda *a, **k: None
        patcher = mock.patch("lynse.time.sleep")
        self.addCleanup(patcher.stop)
        patcher.start()

    @mock.patch("lynse.requests.request")
    def test_retries_503_then_succeeds(self, m_req):
        m_req.side_effect = [
            FakeResp(503, text="unavailable"),
            FakeResp(200, {"code": 200, "msg": "ok", "data": {"done": True}}),
        ]
        data = self.api._request("POST", "/api/business/x", json_data={"a": 1})
        self.assertEqual(m_req.call_count, 2)
        self.assertEqual(data["data"]["done"], True)

    @mock.patch("lynse.requests.request")
    def test_gives_up_after_three_attempts(self, m_req):
        m_req.return_value = FakeResp(503, text="unavailable")
        with self.assertRaises(LynseAPIError):
            self.api._request("POST", "/api/business/x")
        # initial attempt + 2 retries = 3
        self.assertEqual(m_req.call_count, 3)

    @mock.patch("lynse.requests.request")
    def test_does_not_retry_4xx(self, m_req):
        m_req.return_value = FakeResp(404, text="nope")
        with self.assertRaises(LynseAPIError):
            self.api._request("GET", "/api/business/missing")
        self.assertEqual(m_req.call_count, 1)


if __name__ == "__main__":
    unittest.main()
