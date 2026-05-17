import unittest

from lynse import LynseAPI


class TodoOrganizationTests(unittest.TestCase):
    def test_organize_todos_groups_by_deadline_bucket_and_keeps_agent_fields(self):
        api = LynseAPI.__new__(LynseAPI)

        def fake_list_todos(page_size=100, is_completed=None):
            return {
                "code": 200,
                "msg": "SUCCESS",
                "total": 5,
                "data": [
                    {
                        "id": "expired",
                        "todoContent": "follow up overdue",
                        "owner": "Ada",
                        "expectedCompleteTime": "2026-05-16 10:00:00",
                        "fileId": "file-1",
                        "isCompleted": 0,
                        "extra": "not needed by agents",
                    },
                    {
                        "id": "week",
                        "todoContent": "ship this week",
                        "owner": "Ben",
                        "expectedCompleteTime": "2026-05-20",
                        "fileId": "file-2",
                        "isCompleted": 0,
                    },
                    {
                        "id": "month",
                        "todoContent": "prepare next month",
                        "owner": "",
                        "expectedCompleteTime": "2026-06-10",
                        "fileId": "file-3",
                        "isCompleted": 0,
                    },
                    {
                        "id": "future",
                        "todoContent": "later project",
                        "owner": None,
                        "expectedCompleteTime": "2026-07-01T09:30:00",
                        "fileId": "file-4",
                        "isCompleted": 1,
                    },
                    {
                        "id": "no-date",
                        "todoContent": "someday maybe",
                        "owner": "Cai",
                        "expectedCompleteTime": "",
                        "fileId": "file-5",
                        "isCompleted": 0,
                    },
                ],
            }

        api.list_todos = fake_list_todos

        result = api.organize_todos(status="all", now="2026-05-17T00:00:00")

        self.assertEqual(result["code"], 200)
        self.assertEqual(result["total"], 5)
        self.assertEqual(result["summary"]["expired"], 1)
        self.assertEqual(result["summary"]["nearWeek"], 1)
        self.assertEqual(result["summary"]["nearMonth"], 1)
        self.assertEqual(result["summary"]["future"], 1)
        self.assertEqual(result["summary"]["noDate"], 1)
        self.assertEqual(
            set(result["groups"]["expired"][0].keys()),
            {
                "todoContent",
                "owner",
                "expectedCompleteTime",
                "fileId",
                "isCompleted",
            },
        )


if __name__ == "__main__":
    unittest.main()
