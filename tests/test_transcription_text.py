"""Tests for fetching meeting transcription text, not AI summaries."""

import unittest

from lynse import LynseAPI, _resolve_alias, _transcription_entries_to_text


class TranscriptionTextTests(unittest.TestCase):
    def setUp(self):
        self.api = LynseAPI.__new__(LynseAPI)
        self.calls = []

    def test_get_transcription_record_uses_transcription_endpoint(self):
        self.api._sanitize_param = lambda value, _kind: str(value).strip()

        def fake_request(method, path, params=None, **_kwargs):
            self.calls.append((method, path, params))
            return {"code": 200, "data": []}

        self.api._request = fake_request

        result = self.api.get_transcription_record(" file-123 ")

        self.assertEqual(result["code"], 200)
        self.assertEqual(
            self.calls,
            [("GET", "/api/business/file/trans/get", {"fileId": "file-123"})],
        )

    def test_get_transcription_text_builds_text_without_conclusion(self):
        self.api.get_transcription_record = lambda file_id: {
            "code": 200,
            "data": [
                {"beginTime": 1234, "speakerName": "Alice", "text": "开场介绍"},
                {"beginTime": 65000, "speakerId": 2, "text": "讨论转写接口"},
            ],
        }
        self.api.get_conclusion = lambda _file_id: self.fail("summary endpoint must not be called")

        result = self.api.get_transcription_text("file-123")

        self.assertEqual(result["code"], 200)
        self.assertEqual(result["data"], "[00:01.234] Alice: 开场介绍\n[01:05.000] Speaker 2: 讨论转写接口")

    def test_transcription_text_handles_nested_records(self):
        text = _transcription_entries_to_text({
            "records": [
                {"beginTime": "00:00:03", "speakerName": "张三", "text": "第一句"},
                {"timestamp": "00:00:08", "speakerName": "李四", "text": "第二句"},
            ]
        })

        self.assertEqual(text, "[00:00:03] 张三: 第一句\n[00:00:08] 李四: 第二句")

    def test_transcript_text_alias_is_explicit_and_text_is_not_supported(self):
        self.assertEqual(
            _resolve_alias("meetings", ["transcript-text", "file-123"]),
            ("getTranscriptionText", ["file-123"], True),
        )
        with self.assertRaises(SystemExit):
            _resolve_alias("meetings", ["text", "file-123"])


if __name__ == "__main__":
    unittest.main()
