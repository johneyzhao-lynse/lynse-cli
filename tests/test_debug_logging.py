import io
import os
import unittest
from contextlib import redirect_stderr
from unittest import mock

import lynse


class DebugLoggingTests(unittest.TestCase):
    def setUp(self):
        self.api = object.__new__(lynse.LynseAPI)

    def test_debug_request_log_never_exposes_credentials_or_values(self):
        stderr = io.StringIO()
        with mock.patch.dict(os.environ, {"LYNSE_HTTP_DEBUG": "1"}, clear=False):
            with redirect_stderr(stderr):
                self.api._log_lynse_request(
                    method="POST",
                    url="https://user:password@api.example.com/resource/private-id?token=secret-query",
                    headers={
                        "Authorization": "secret-access-token",
                        "X-API-Key": "dk_secret-api-key",
                        "Content-Type": "application/json",
                    },
                    params={"search": "private meeting"},
                    json_data={"password": "secret-password", "title": "private title"},
                )

        log = stderr.getvalue()
        self.assertEqual(log.count("[REDACTED]"), 2)
        self.assertNotIn("secret-access-token", log)
        self.assertNotIn("dk_secret-api-key", log)
        self.assertNotIn("private meeting", log)
        self.assertNotIn("secret-password", log)
        self.assertNotIn("private title", log)
        self.assertNotIn("user:password", log)
        self.assertNotIn("private-id", log)
        self.assertNotIn("secret-query", log)
        self.assertIn('"destination": "https://api.example.com"', log)
        self.assertIn('"param_names": ["search"]', log)
        self.assertIn('"json_fields": ["password", "title"]', log)

    def test_debug_response_log_omits_message_and_body(self):
        stderr = io.StringIO()
        with mock.patch.dict(os.environ, {"LYNSE_HTTP_DEBUG": "1"}, clear=False):
            with redirect_stderr(stderr):
                self.api._log_lynse_response(
                    method="GET",
                    url="https://api.example.com/resource",
                    status_code=400,
                    data={
                        "code": 400,
                        "message": "private server detail",
                        "data": {"secret": "value"},
                    },
                    text_preview='{"secret":"value"}',
                )

        log = stderr.getvalue()
        self.assertNotIn("private server detail", log)
        self.assertNotIn('"secret": "value"', log)
        self.assertIn('"business_code": 400', log)
        self.assertIn('"data_keys": ["secret"]', log)


if __name__ == "__main__":
    unittest.main()
