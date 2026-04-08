# File (文件管理)

> Prerequisites: see root `../SKILL.md` for setup, auth, and API call method.

API base path: `/api/business/file`

## 接口决策表

| 用户意图 | Wrapper命令 | HTTP | 路径 | 关键参数 |
|---|---|---|---|---|
| 获取用户所有文件列表 | `listFiles` | GET | `/api/business/file/list` | 无 |
| 获取文件详情 | `getFileInfo <fileId>` | GET | `/api/business/file/info?fileId=<id>` | fileId (query) |
| 获取文件总结 | `getConclusion <fileId>` | GET | `/api/business/file/conclusion/list?fileId=<id>` | fileId (query) |
| 获取文件大纲 | `getOutline <fileId>` | GET | `/api/business/file/outline/get?fileId=<id>` | fileId (query) |
| 导出文件大纲 | `exportOutline <fileId>` | GET | `/api/business/file/outline/export?fileId=<id>` | fileId (query) |
| 获取转写记录 | `getTranscriptionRecord <fileId>` | GET | `/api/business/file/trans/get?fileId=<id>` | fileId (query) |
| 按时间范围查询文件 | `listFilesByTimeRange [days]` | GET | `/api/business/file/timeRange/list` | startTime, endTime (query) |
| 分页查询文件 | CLI B: `page` | GET | `/api/business/file/page` | dto, pageQuery |
| 按分类查询文件 | CLI B: `listByCategory` | GET | `/api/business/file/category/list` | dto |
| 按分类分页查询 | CLI B: `pageByCategory` | GET | `/api/business/file/category/page` | queryReq, pageQuery |
| 统计分类数量 | CLI B: `countByCategory` | GET | `/api/business/file/category/count` | 无 |
| 删除文件 | CLI B: `delete` | DELETE | `/api/business/file/delete` | fileIds, folderIds |
| 恢复文件 | CLI B: `recover` | POST | `/api/business/file/recover` | Body: fileIdsReq |
| 清空回收站（选中） | CLI B: `cleanBin` | POST | `/api/business/file/cleanBin` | Body: fileIdsReq |
| 清空回收站（全部） | CLI B: `cleanBinAll` | POST | `/api/business/file/cleanBinAll` | 无 |
| 编辑文件 | CLI B: `edit` | PUT | `/api/business/file/{fileId}` | fileId (path), Body |
| 获取 STS Token（上传用） | CLI B: `getStsToken` | POST | `/api/business/file/getStsToken` | Body: preUploadReq |
| 预签名上传 | CLI B: `presign4Upload` | POST | `/api/business/file/presign/upload` | Body |
| 预签名下载 | CLI B: `presign4Download` | GET | `/api/business/file/presign/download` | queryReq |
| 标记已读 | CLI B: `markFileAsRead` | GET | `/api/business/file/markRead` | fileId |
| 移动文件夹 | CLI B: `changeFolder` | GET | `/api/business/file/changeFolder` | oldFolderId, newFolderId, fileIds |
| 获取可用 AI 模型 | CLI B: `getAvailableAIModelList` | GET | `/api/business/file/getAvailableAIModelList` | 无 |
| 获取支持语言 | CLI B: `getSupportLanguage` | GET | `/api/business/file/getSupportLanguage` | 无 |
| 获取评估列表 | CLI B: `getEvaluationList` | GET | `/api/business/file/getEvaluationList` | optionType (可选) |
| 添加评估 | CLI B: `addEvaluation` | POST | `/api/business/file/evaluation/add` | Body |
| 提交音频合并 | CLI B: `submitAudioMerge` | POST | `/api/business/file/audio/merge` | Body |
| 查询合并状态 | CLI B: `queryAudioMergeStatus` | GET | `/api/business/file/audio/merge/status` | taskId |
| 文件转移 | CLI B: `transferFile` | POST | `/api/business/file/transferFile` | Body |

### 高级文件操作（CLI B 专属）

| 用户意图 | CLI B 命令 | 说明 |
|---|---|---|
| 获取/编辑总结 | `getConclusion`, `editConclusion`, `batchGetConclusions`, `deleteConclusion` | 文件内容总结 |
| 获取/编辑大纲 | `getOutline`, `editOutline`, `exportOutline` | 文件大纲 |
| 获取/编辑思维导图 | `getMindMap`, `editMindMap` | 思维导图 |
| 转写记录管理 | `listTranscriptionRecord`, `editTransRecord`, `editSpeakerInfo`, `exportTransRecord` | 转写文本 |
| 获取转写状态 | `getTranscribeStatus` | 检查转写进度 |
| 获取 AI 任务结果 | `getAiTaskResult` | AI 处理任务结果 |
| AI 文本处理 | `aiModelProcessText` | 调用 AI 处理文本 |
| HTML 转 PDF | `exportHtmlToPdf` | 将 HTML 导出为 PDF |
| 上传通知 | `notify` | 通知文件上传完成 |
| 删除 OSS 文件 | `removeOss` | 清理 OSS 存储 |

## 常用工作流

### 查看文件列表和详情

```bash
# 列出所有文件
~/.claude/skills/lynse/api_wrapper.sh listFiles

# 查看文件详情
~/.claude/skills/lynse/api_wrapper.sh getFileInfo "<fileId>"

# 查看最近 7 天的文件
~/.claude/skills/lynse/api_wrapper.sh listFilesByTimeRange 7

# 查看最近 30 天的文件
~/.claude/skills/lynse/api_wrapper.sh listFilesByTimeRange 30
```

### 获取文件内容分析

```bash
# 获取文件总结（AI 生成的内容摘要）
~/.claude/skills/lynse/api_wrapper.sh getConclusion "<fileId>"

# 获取文件大纲（结构化目录）
~/.claude/skills/lynse/api_wrapper.sh getOutline "<fileId>"

# 导出大纲
~/.claude/skills/lynse/api_wrapper.sh exportOutline "<fileId>"

# 获取转写记录（音视频转文字）
~/.claude/skills/lynse/api_wrapper.sh getTranscriptionRecord "<fileId>"
```

### 文件上传流程

```bash
# 1. 获取 STS Token
~/.claude/skills/lynse/lynse_unified.sh getStsToken '{"fileName":"report.pdf","fileSize":1024}'

# 2. 使用 STS Token 上传到 OSS (外部操作)

# 3. 通知上传完成
~/.claude/skills/lynse/lynse_unified.sh notify fileId="<fileId>"
```

### 文件删除与恢复

```bash
# 删除文件（移入回收站）
~/.claude/skills/lynse/lynse_unified.sh delete fileIds='["<fileId1>","<fileId2>"]'

# 恢复文件
~/.claude/skills/lynse/lynse_unified.sh recover '{"fileIds":["<fileId1>"]}'

# 清空回收站（全部）
~/.claude/skills/lynse/lynse_unified.sh cleanBinAll
```

### 音频合并

```bash
# 提交合并任务
~/.claude/skills/lynse/lynse_unified.sh submitAudioMerge '{"fileIds":["<id1>","<id2>"]}'

# 查询合并状态
~/.claude/skills/lynse/lynse_unified.sh queryAudioMergeStatus taskId="<taskId>"
```

## 核心响应字段

**FileInfoVO**: `fileId`, `fileName`, `fileType`, `fileSize`, `duration`, `status`, `createTime`, `updateTime`, `folderId`, `transcribeStatus`, `conclusionStatus`.

**FileEntity**: `id`, `fileName`, `ossKey`, `fileType`, `fileSize`, `duration`, `status`, `customerId`, `folderId`, `createTime`.

**FileConclusionVO**: `id`, `fileId`, `conclusion`, `conclusionType`, `createTime`.

**FileOutlineVO**: `id`, `fileId`, `outline`, `createTime`.

**FileTransRecordVO**: `id`, `fileId`, `text`, `speakerInfo`, `segments`, `createTime`.

## 分页

- `page` / `pageByCategory`: 使用 `pageQuery` 参数（`pageNum`, `pageSize`），返回 `TableDataInfoFileInfoVO`（含 `total`, `rows`）

## 注意事项

- `listFilesByTimeRange` 的参数是天数（往前推 N 天），默认 7 天
- 文件 ID 在 wrapper 命令中通过命令行参数传递，在 CLI B 命令中通常通过 query 参数传递
- `delete` 是软删除（移入回收站），`cleanBin` 才是永久删除
- `getConclusion` 和 `getConclusionList` 在 wrapper 中等价，都调用同一个接口
- 转写状态（`transcribeStatus`）常见值：0=未开始, 1=处理中, 2=完成, 3=失败
