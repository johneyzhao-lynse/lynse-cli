"""Table formatting tests.

The ID column must never be truncated: downstream commands
(``meetings summary/transcript/outline/info``) copy the ID straight from the
``--table`` output, so a truncated ID silently breaks those lookups. Other
wide columns may be truncated, but must keep an explicit ``...`` marker.
"""

from lynse import _format_table


def test_format_table_keeps_full_long_id():
    items = [{
        "id": "1993855667662958593_1783500592708_7yq0h4qv",  # 42 chars
        "originalFilename": "短标题",
        "createTime": "2026-07-08 16:49:53",
    }]
    out = _format_table({"data": items}, "listFiles")
    # 完整 ID 必须出现在表格里，不能被 [:40] 截断
    assert "1993855667662958593_1783500592708_7yq0h4qv" in out


def test_format_table_truncates_wide_name_with_ellipsis():
    long_name = "x" * 100
    items = [{
        "id": "id1",
        "originalFilename": long_name,
        "createTime": "2026-07-08 16:49:53",
    }]
    out = _format_table({"data": items}, "listFiles")
    # 宽列应被截断并保留省略号标记，而不是静默丢信息
    assert "..." in out
    assert long_name not in out
