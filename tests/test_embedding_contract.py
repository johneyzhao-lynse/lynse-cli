import unittest
from unittest.mock import patch

import lynse


class FakeHttp:
    def request(self, *args, **kwargs):  # pragma: no cover - network sentinel
        raise AssertionError("unexpected network request")


class EmbeddingContractTests(unittest.TestCase):
    def make_api(self):
        with patch.dict(
            "os.environ",
            {
                "LYNSE_API_HOST": "https://api.lynse.cn",
                "LYNSE_API_KEY": "",
                "LYNSE_ACCESS_TOKEN": "",
            },
            clear=False,
        ):
            return lynse.LynseAPI(
                api_host="https://api.lynse.cn",
                access_token="a.b.c",
                owner_id="owner-1",
                http_client=FakeHttp(),
            )

    def test_version_is_1_7_0(self):
        self.assertEqual(lynse.CLI_VERSION, "1.7.0")

    def test_constructor_supports_embedded_consumers(self):
        api = self.make_api()
        self.assertEqual(api.owner_id, "owner-1")
        self.assertEqual(api._get_token(), "a.b.c")
        self.assertIsInstance(api._http, FakeHttp)

    def test_injected_token_does_not_leak_saved_api_key(self):
        with patch.object(
            lynse,
            "_load_user_config",
            return_value={"api_host": "https://api.lynse.cn", "api_key": "saved-key"},
        ):
            api = lynse.LynseAPI(
                api_host="https://api.lynse.cn",
                access_token="a.b.c",
                http_client=FakeHttp(),
            )
        headers = api._build_auth_headers("a.b.c")
        self.assertNotIn("X-API-Key", headers)

    def test_environment_token_does_not_leak_saved_api_key(self):
        with patch.dict("os.environ", {"LYNSE_ACCESS_TOKEN": "a.b.c"}, clear=False):
            with patch.object(
                lynse,
                "_load_user_config",
                return_value={"api_host": "https://api.lynse.cn", "api_key": "saved-key"},
            ):
                api = lynse.LynseAPI(api_host="https://api.lynse.cn")
            headers = api._build_auth_headers("a.b.c")
        self.assertNotIn("X-API-Key", headers)

    def test_todo_write_contracts(self):
        api = self.make_api()
        calls = []
        api._request = lambda method, path, **kwargs: calls.append(
            (method, path, kwargs)
        ) or {"code": 200}

        api.add_todo("Prepare report", owner="Lin", deadline="2026-08-13")
        api.reschedule_todo("todo-1", "2026-08-14")

        self.assertEqual(calls[0][1], "/api/business/file/todo/update")
        self.assertEqual(
            calls[0][2]["json_data"],
            {
                "todoUpdateList": [
                    {
                        "todoContent": "Prepare report",
                        "owner": "Lin",
                        "expectedCompleteTime": "2026-08-13",
                    }
                ]
            },
        )
        self.assertEqual(
            calls[1][2]["json_data"],
            {
                "todoUpdateList": [
                    {
                        "todoId": "todo-1",
                        "expectedCompleteTime": "2026-08-14",
                    }
                ]
            },
        )

    def test_folder_extension_contracts(self):
        api = self.make_api()
        calls = []
        api._request = lambda method, path, **kwargs: calls.append(
            (method, path, kwargs)
        ) or {"code": 200}

        api.count_files_by_folder()
        api.delete_folders(["folder-1"])

        self.assertEqual(calls[0][:2], ("GET", "/api/business/file/category/count"))
        self.assertEqual(calls[1][0], "DELETE")
        self.assertEqual(calls[1][2]["params"], {"folderIds": ["folder-1"]})

    def test_audio_contract_uses_presigned_download(self):
        api = self.make_api()
        api.get_file_info = lambda file_id: {
            "code": 200,
            "data": {
                "id": file_id,
                "originalFilename": "meeting.wav",
                "contentType": "audio/wav",
                "size": 4096,
            },
        }
        calls = []
        api._request = lambda method, path, params=None: calls.append(
            (method, path, params)
        ) or {
            "code": 200,
            "data": "https://files.example.test/meeting.wav?signature=short-lived",
        }

        result = api.get_audio_file("meeting-1")

        self.assertEqual(
            calls,
            [
                (
                    "GET",
                    "/api/business/file/presign/download",
                    {"fileId": "meeting-1"},
                )
            ],
        )
        self.assertEqual(result["data"]["mimeType"], "audio/wav")
        self.assertEqual(result["data"]["size"], 4096)


if __name__ == "__main__":
    unittest.main()
