# FileControllerApi

All URIs are relative to **

Method | HTTP request | Description
------------- | ------------- | -------------
[**addEvaluation**](FileControllerApi.md#addEvaluation) | **POST** /api/business/file/evaluation/add |
[**changeFolder**](FileControllerApi.md#changeFolder) | **GET** /api/business/file/changeFolder |
[**countByCategory**](FileControllerApi.md#countByCategory) | **GET** /api/business/file/category/count |
[**edit**](FileControllerApi.md#edit) | **PUT** /api/business/file/{fileId} |
[**getAvailableAIModelList**](FileControllerApi.md#getAvailableAIModelList) | **GET** /api/business/file/getAvailableAIModelList |
[**getEvaluationList**](FileControllerApi.md#getEvaluationList) | **GET** /api/business/file/getEvaluationList |
[**getStsToken**](FileControllerApi.md#getStsToken) | **POST** /api/business/file/getStsToken |
[**getSupportLanguage**](FileControllerApi.md#getSupportLanguage) | **GET** /api/business/file/getSupportLanguage |
[**handleAudioMergeCallback**](FileControllerApi.md#handleAudioMergeCallback) | **POST** /api/business/file/audio/merge/callback |
[**info1**](FileControllerApi.md#info1) | **GET** /api/business/file/info |
[**list**](FileControllerApi.md#list) | **GET** /api/business/file/list |
[**listByCategory**](FileControllerApi.md#listByCategory) | **GET** /api/business/file/category/list |
[**listByCategoryV1**](FileControllerApi.md#listByCategoryV1) | **GET** /api/business/file/category |
[**listByTimeRange**](FileControllerApi.md#listByTimeRange) | **GET** /api/business/file/timeRange/list |
[**markFileAsRead**](FileControllerApi.md#markFileAsRead) | **GET** /api/business/file/markRead |
[**notify**](FileControllerApi.md#notify) | **GET** /api/business/file/upload/notify |
[**page**](FileControllerApi.md#page) | **GET** /api/business/file/page |
[**pageByCategory**](FileControllerApi.md#pageByCategory) | **GET** /api/business/file/category/page |
[**presign4Download**](FileControllerApi.md#presign4Download) | **GET** /api/business/file/presign/download |
[**presign4Upload**](FileControllerApi.md#presign4Upload) | **POST** /api/business/file/presign/upload |
[**presign4UploadForPublic**](FileControllerApi.md#presign4UploadForPublic) | **POST** /api/business/file/presign/uploadPublic |
[**queryAudioMergeStatus**](FileControllerApi.md#queryAudioMergeStatus) | **GET** /api/business/file/audio/merge/status |
[**recover**](FileControllerApi.md#recover) | **POST** /api/business/file/recover |
[**submitAudioMerge**](FileControllerApi.md#submitAudioMerge) | **POST** /api/business/file/audio/merge |
[**testAudioMerge**](FileControllerApi.md#testAudioMerge) | **POST** /api/business/file/audio/merge/test |



## addEvaluation



### Example

```bash
 addEvaluation
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **evaluationResultAddReq** | [**EvaluationResultAddReq**](EvaluationResultAddReq.md) |  |

### Return type

[**ResultBoolean**](ResultBoolean.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## changeFolder



### Example

```bash
 changeFolder  oldFolderId=value  newFolderId=value  Specify as:  fileIds=value1 fileIds=value2 fileIds=...
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **oldFolderId** | **string** |  | [default to null]
 **newFolderId** | **string** |  | [default to null]
 **fileIds** | [**array[string]**](string.md) |  | [default to null]

### Return type

[**ResultBoolean**](ResultBoolean.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not Applicable
- **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## countByCategory



### Example

```bash
 countByCategory
```

### Parameters

This endpoint does not need any parameter.

### Return type

[**ResultFileCategoryVO**](ResultFileCategoryVO.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not Applicable
- **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## edit



### Example

```bash
 edit fileId=value
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **fileId** | **string** |  | [default to null]
 **fileUpdateReq** | [**FileUpdateReq**](FileUpdateReq.md) |  |

### Return type

[**ResultBoolean**](ResultBoolean.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## getAvailableAIModelList



### Example

```bash
 getAvailableAIModelList
```

### Parameters

This endpoint does not need any parameter.

### Return type

[**ResultListModelListDTO**](ResultListModelListDTO.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not Applicable
- **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## getEvaluationList



### Example

```bash
 getEvaluationList  optionType=value
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **optionType** | **integer** |  | [optional] [default to null]

### Return type

[**ResultListEvaluationOptions**](ResultListEvaluationOptions.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not Applicable
- **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## getStsToken



### Example

```bash
 getStsToken
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **preUploadReq** | [**PreUploadReq**](PreUploadReq.md) |  |

### Return type

[**ResultStsTokenVO**](ResultStsTokenVO.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## getSupportLanguage



### Example

```bash
 getSupportLanguage
```

### Parameters

This endpoint does not need any parameter.

### Return type

[**ResultListLanguageListDTO**](ResultListLanguageListDTO.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not Applicable
- **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## handleAudioMergeCallback



### Example

```bash
 handleAudioMergeCallback
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | **string** |  |

### Return type

[**ResultBoolean**](ResultBoolean.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## info1



### Example

```bash
 info1  queryReq=value
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **queryReq** | [**FileQueryReq**](.md) |  | [default to null]

### Return type

[**ResultFileEntity**](ResultFileEntity.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not Applicable
- **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## list



### Example

```bash
 list  dto=value
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **dto** | [**FileListQueryReq**](.md) |  | [default to null]

### Return type

[**ResultListFileInfoVO**](ResultListFileInfoVO.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not Applicable
- **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## listByCategory



### Example

```bash
 listByCategory  dto=value
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **dto** | [**FileCategoryQueryReq**](.md) |  | [default to null]

### Return type

[**ResultListFileInfoVO**](ResultListFileInfoVO.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not Applicable
- **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## listByCategoryV1



### Example

```bash
 listByCategoryV1  dto=value
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **dto** | [**FileCategoryQueryReq**](.md) |  | [default to null]

### Return type

[**ResultListFileInfoVO**](ResultListFileInfoVO.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not Applicable
- **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## listByTimeRange



### Example

```bash
 listByTimeRange  queryReq=value
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **queryReq** | [**FileTimeRangeQueryReq**](.md) |  | [default to null]

### Return type

[**ResultListFileInfoVO**](ResultListFileInfoVO.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not Applicable
- **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## markFileAsRead



### Example

```bash
 markFileAsRead  fileId=value
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **fileId** | **string** |  | [default to null]

### Return type

[**ResultBoolean**](ResultBoolean.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not Applicable
- **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## notify



### Example

```bash
 notify  fileId=value
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **fileId** | **string** |  | [default to null]

### Return type

[**ResultBoolean**](ResultBoolean.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not Applicable
- **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## page



### Example

```bash
 page  dto=value  pageQuery=value
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **dto** | [**FileListQueryReq**](.md) |  | [default to null]
 **pageQuery** | [**PageQuery**](.md) |  | [default to null]

### Return type

[**TableDataInfoFileInfoVO**](TableDataInfoFileInfoVO.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not Applicable
- **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## pageByCategory



### Example

```bash
 pageByCategory  queryReq=value  pageQuery=value
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **queryReq** | [**FileCategoryQueryReq**](.md) |  | [default to null]
 **pageQuery** | [**PageQuery**](.md) |  | [default to null]

### Return type

[**TableDataInfoFileInfoVO**](TableDataInfoFileInfoVO.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not Applicable
- **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## presign4Download



### Example

```bash
 presign4Download  queryReq=value
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **queryReq** | [**FileQueryReq**](.md) |  | [default to null]

### Return type

[**ResultString**](ResultString.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not Applicable
- **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## presign4Upload



### Example

```bash
 presign4Upload
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **preUploadReq** | [**PreUploadReq**](PreUploadReq.md) |  |

### Return type

[**ResultPreSignedUrlVO**](ResultPreSignedUrlVO.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## presign4UploadForPublic



### Example

```bash
 presign4UploadForPublic  filename=value
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **filename** | **string** |  | [default to null]

### Return type

[**ResultGeneratePresignedUrlResult**](ResultGeneratePresignedUrlResult.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not Applicable
- **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## queryAudioMergeStatus



### Example

```bash
 queryAudioMergeStatus  taskId=value
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **taskId** | **string** |  | [default to null]

### Return type

[**ResultAudioMergeTaskStatusVO**](ResultAudioMergeTaskStatusVO.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not Applicable
- **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## recover



### Example

```bash
 recover
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **fileIdsReq** | [**FileIdsReq**](FileIdsReq.md) |  |

### Return type

[**ResultBoolean**](ResultBoolean.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## submitAudioMerge



### Example

```bash
 submitAudioMerge
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **audioMergeSubmitReq** | [**AudioMergeSubmitReq**](AudioMergeSubmitReq.md) |  |

### Return type

[**ResultAudioMergeSubmitVO**](ResultAudioMergeSubmitVO.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## testAudioMerge



### Example

```bash
 testAudioMerge
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **aliyunAudioMergeReq** | [**AliyunAudioMergeReq**](AliyunAudioMergeReq.md) |  |

### Return type

[**ResultAliyunAudioMergeTaskVO**](ResultAliyunAudioMergeTaskVO.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

