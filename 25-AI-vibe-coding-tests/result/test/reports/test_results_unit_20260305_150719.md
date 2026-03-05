# Test Execution Report

## Summary

| Metric | Value |
|--------|-------|
| **Test Type** | UNIT |
| **Execution Time** | 2026-03-05 15:07:22 |
| **Overall Status** | ✅ PASSED |
| **Total Tests** | 22 |
| **Passed** | 22 |
| **Failed** | 0 |
| **Skipped** | 0 |
| **Errors** | 0 |

## Test Configuration

- **Test Framework**: pytest
- **HTML Report**: [test_results_unit_20260305_150719.html](test_results_unit_20260305_150719.html)

## Console Output

```
============================= test session starts =============================
platform win32 -- Python 3.14.2, pytest-8.3.4, pluggy-1.6.0 -- C:\Program Files\Python314\python.exe
cachedir: .pytest_cache
metadata: {'Python': '3.14.2', 'Platform': 'Windows-11-10.0.26200-SP0', 'Packages': {'pytest': '8.3.4', 'pluggy': '1.6.0'}, 'Plugins': {'cov': '4.1.0', 'html': '4.1.1', 'metadata': '3.1.1'}}
rootdir: G:\My Drive\dev\GitHub\portfolio-SQAAILab\25-AI-vibe-coding-tests\result\test
configfile: pytest.ini
plugins: cov-4.1.0, html-4.1.1, metadata-3.1.1
collecting ... collected 22 items

unit/test_post_validation.py::TestPostSerialization::test_post_to_dict_contains_required_fields PASSED [  4%]
unit/test_post_validation.py::TestPostDefaults::test_post_default_published_false PASSED [  9%]
unit/test_post_validation.py::TestPostValidation::test_post_required_fields_validation PASSED [ 13%]
unit/test_post_validation.py::TestPostValidation::test_post_valid_data_passes_validation PASSED [ 18%]
unit/test_post_validation.py::TestPostValidation::test_post_optional_published_field PASSED [ 22%]
unit/test_post_validation.py::TestPostUpdateLogic::test_post_update_allowed_fields PASSED [ 27%]
unit/test_response_shapes.py::TestHealthResponseShape::test_health_response_has_required_keys PASSED [ 31%]
unit/test_response_shapes.py::TestUserResponseShape::test_create_user_response_shape PASSED [ 36%]
unit/test_response_shapes.py::TestUserResponseShape::test_list_users_response_shape PASSED [ 40%]
unit/test_response_shapes.py::TestPostResponseShape::test_create_post_response_shape PASSED [ 45%]
unit/test_response_shapes.py::TestPostResponseShape::test_list_posts_response_shape PASSED [ 50%]
unit/test_response_shapes.py::TestStatsResponseShape::test_stats_response_has_numeric_fields PASSED [ 54%]
unit/test_response_shapes.py::TestErrorResponseShape::test_error_400_response_shape PASSED [ 59%]
unit/test_response_shapes.py::TestErrorResponseShape::test_error_404_response_shape PASSED [ 63%]
unit/test_response_shapes.py::TestErrorResponseShape::test_error_409_response_shape PASSED [ 68%]
unit/test_user_validation.py::TestUserSerialization::test_user_to_dict_excludes_password PASSED [ 72%]
unit/test_user_validation.py::TestUserSerialization::test_user_to_dict_contains_required_fields PASSED [ 77%]
unit/test_user_validation.py::TestUserPasswordHandling::test_set_password_creates_hash PASSED [ 81%]
unit/test_user_validation.py::TestUserPasswordHandling::test_check_password_validates_correctly PASSED [ 86%]
unit/test_user_validation.py::TestUserPasswordHandling::test_check_password_rejects_wrong_password PASSED [ 90%]
unit/test_user_validation.py::TestUserValidation::test_user_required_fields_validation PASSED [ 95%]
unit/test_user_validation.py::TestUserValidation::test_user_valid_data_passes_validation PASSED [100%]

============================== warnings summary ===============================
unit/test_post_validation.py::TestPostSerialization::test_post_to_dict_contains_required_fields
unit/test_post_validation.py::TestPostSerialization::test_post_to_dict_contains_required_fields
unit/test_post_validation.py::TestPostSerialization::test_post_to_dict_contains_required_fields
unit/test_post_validation.py::TestPostDefaults::test_post_default_published_false
unit/test_post_validation.py::TestPostDefaults::test_post_default_published_false
unit/test_post_validation.py::TestPostDefaults::test_post_default_published_false
unit/test_user_validation.py::TestUserSerialization::test_user_to_dict_excludes_password
unit/test_user_validation.py::TestUserSerialization::test_user_to_dict_contains_required_fields
  C:\Users\ericl\AppData\Roaming\Python\Python314\site-packages\sqlalchemy\sql\schema.py:3624: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    return util.wrap_callable(lambda ctx: fn(), fn)  # type: ignore

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
- Generated html report: file:///G:/My%20Drive/dev/GitHub/portfolio-SQAAILab/25-AI-vibe-coding-tests/result/test/reports/test_results_unit_20260305_150719.html -
======================= 22 passed, 8 warnings in 1.91s ========================

```

---

*Report generated on 2026-03-05 15:07:22*
