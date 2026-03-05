# Test Execution Report

## Summary

| Metric | Value |
|--------|-------|
| **Test Type** | INTEGRATION |
| **Execution Time** | 2026-03-05 15:07:42 |
| **Overall Status** | ✅ PASSED |
| **Total Tests** | 49 |
| **Passed** | 49 |
| **Failed** | 0 |
| **Skipped** | 0 |
| **Errors** | 0 |

## Test Configuration

- **Test Framework**: pytest
- **HTML Report**: [test_results_integration_20260305_150730.html](test_results_integration_20260305_150730.html)

## Console Output

```
============================= test session starts =============================
platform win32 -- Python 3.14.2, pytest-8.3.4, pluggy-1.6.0 -- C:\Program Files\Python314\python.exe
cachedir: .pytest_cache
metadata: {'Python': '3.14.2', 'Platform': 'Windows-11-10.0.26200-SP0', 'Packages': {'pytest': '8.3.4', 'pluggy': '1.6.0'}, 'Plugins': {'cov': '4.1.0', 'html': '4.1.1', 'metadata': '3.1.1'}}
rootdir: G:\My Drive\dev\GitHub\portfolio-SQAAILab\25-AI-vibe-coding-tests\result\test
configfile: pytest.ini
plugins: cov-4.1.0, html-4.1.1, metadata-3.1.1
collecting ... collected 49 items

integration/test_cors.py::TestCorsHeaders::test_cors_headers_on_api_response PASSED [  2%]
integration/test_cors.py::TestCorsHeaders::test_cors_allows_json_content_type PASSED [  4%]
integration/test_error_handling.py::TestErrorHandling::test_404_returns_json PASSED [  6%]
integration/test_error_handling.py::TestErrorHandling::test_400_returns_json PASSED [  8%]
integration/test_error_handling.py::TestErrorHandling::test_409_returns_json PASSED [ 10%]
integration/test_error_handling.py::TestErrorHandling::test_successful_response_is_json PASSED [ 12%]
integration/test_error_handling.py::TestErrorHandling::test_create_response_includes_message PASSED [ 14%]
integration/test_error_handling.py::TestErrorHandling::test_delete_response_includes_message PASSED [ 16%]
integration/test_health.py::TestHealthEndpoint::test_health_check_returns_200 PASSED [ 18%]
integration/test_health.py::TestHealthEndpoint::test_health_response_is_json PASSED [ 20%]
integration/test_posts.py::TestCreatePost::test_create_post_with_valid_data PASSED [ 22%]
integration/test_posts.py::TestCreatePost::test_create_post_missing_title PASSED [ 24%]
integration/test_posts.py::TestCreatePost::test_create_post_missing_content PASSED [ 26%]
integration/test_posts.py::TestCreatePost::test_create_post_missing_user_id PASSED [ 28%]
integration/test_posts.py::TestCreatePost::test_create_post_user_not_found PASSED [ 30%]
integration/test_posts.py::TestCreatePost::test_create_post_default_published_false PASSED [ 32%]
integration/test_posts.py::TestListPosts::test_list_all_posts PASSED     [ 34%]
integration/test_posts.py::TestListPosts::test_list_posts_empty_database PASSED [ 36%]
integration/test_posts.py::TestListPosts::test_list_posts_ordered_by_created_at_desc PASSED [ 38%]
integration/test_posts.py::TestListPosts::test_list_published_posts_only PASSED [ 40%]
integration/test_posts.py::TestListPosts::test_list_published_posts_empty PASSED [ 42%]
integration/test_posts.py::TestGetPostById::test_get_post_by_valid_id PASSED [ 44%]
integration/test_posts.py::TestGetPostById::test_get_post_not_found PASSED [ 46%]
integration/test_posts.py::TestUpdatePost::test_update_post_publish PASSED [ 48%]
integration/test_posts.py::TestUpdatePost::test_update_post_title_and_content PASSED [ 51%]
integration/test_posts.py::TestUpdatePost::test_update_post_refreshes_updated_at PASSED [ 53%]
integration/test_posts.py::TestUpdatePost::test_update_post_not_found PASSED [ 55%]
integration/test_posts.py::TestDeletePost::test_delete_post_success PASSED [ 57%]
integration/test_posts.py::TestDeletePost::test_delete_post_not_found PASSED [ 59%]
integration/test_stats.py::TestStatisticsEndpoint::test_stats_returns_200 PASSED [ 61%]
integration/test_stats.py::TestStatisticsEndpoint::test_stats_empty_database PASSED [ 63%]
integration/test_stats.py::TestStatisticsEndpoint::test_stats_reflect_created_data PASSED [ 65%]
integration/test_stats.py::TestStatisticsEndpoint::test_stats_cascade_impact PASSED [ 67%]
integration/test_stats.py::TestStatisticsEndpoint::test_stats_update_on_post_publish PASSED [ 69%]
integration/test_users.py::TestCreateUser::test_create_user_with_valid_data PASSED [ 71%]
integration/test_users.py::TestCreateUser::test_create_user_missing_username PASSED [ 73%]
integration/test_users.py::TestCreateUser::test_create_user_missing_email PASSED [ 75%]
integration/test_users.py::TestCreateUser::test_create_user_missing_password PASSED [ 77%]
integration/test_users.py::TestCreateUser::test_create_user_duplicate_username PASSED [ 79%]
integration/test_users.py::TestCreateUser::test_create_user_duplicate_email PASSED [ 81%]
integration/test_users.py::TestListUsers::test_list_users_returns_array PASSED [ 83%]
integration/test_users.py::TestListUsers::test_list_users_empty_database PASSED [ 85%]
integration/test_users.py::TestListUsers::test_list_users_contains_created_user PASSED [ 87%]
integration/test_users.py::TestListUsers::test_list_users_contains_required_fields PASSED [ 89%]
integration/test_users.py::TestGetUserById::test_get_user_by_valid_id PASSED [ 91%]
integration/test_users.py::TestGetUserById::test_get_user_not_found PASSED [ 93%]
integration/test_users.py::TestDeleteUser::test_delete_user_success PASSED [ 95%]
integration/test_users.py::TestDeleteUser::test_delete_user_cascade_posts PASSED [ 97%]
integration/test_users.py::TestDeleteUser::test_delete_user_not_found PASSED [100%]

============================== warnings summary ===============================
integration/test_cors.py: 1 warning
integration/test_error_handling.py: 3 warnings
integration/test_posts.py: 36 warnings
integration/test_stats.py: 14 warnings
integration/test_users.py: 10 warnings
  C:\Users\ericl\AppData\Roaming\Python\Python314\site-packages\sqlalchemy\sql\schema.py:3624: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    return util.wrap_callable(lambda ctx: fn(), fn)  # type: ignore

integration/test_error_handling.py: 1 warning
integration/test_posts.py: 9 warnings
integration/test_stats.py: 2 warnings
integration/test_users.py: 7 warnings
  C:\Users\ericl\AppData\Roaming\Python\Python314\site-packages\flask_sqlalchemy\query.py:30: LegacyAPIWarning: The Query.get() method is considered legacy as of the 1.x series of SQLAlchemy and becomes a legacy construct in 2.0. The method is now available as Session.get() (deprecated since: 2.0) (Background on SQLAlchemy 2.0 at: https://sqlalche.me/e/b8d9)
    rv = self.get(ident)

integration/test_posts.py: 13 warnings
integration/test_stats.py: 5 warnings
integration/test_users.py: 1 warning
  G:\My Drive\dev\GitHub\portfolio-SQAAILab\10-AI-vibe-coding\result\src\app\backend\app.py:150: LegacyAPIWarning: The Query.get() method is considered legacy as of the 1.x series of SQLAlchemy and becomes a legacy construct in 2.0. The method is now available as Session.get() (deprecated since: 2.0) (Background on SQLAlchemy 2.0 at: https://sqlalche.me/e/b8d9)
    user = User.query.get(data['user_id'])

integration/test_posts.py::TestUpdatePost::test_update_post_publish
integration/test_posts.py::TestUpdatePost::test_update_post_title_and_content
integration/test_posts.py::TestUpdatePost::test_update_post_refreshes_updated_at
integration/test_stats.py::TestStatisticsEndpoint::test_stats_update_on_post_publish
  G:\My Drive\dev\GitHub\portfolio-SQAAILab\10-AI-vibe-coding\result\src\app\backend\app.py:197: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    post.updated_at = datetime.utcnow()

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
- Generated html report: file:///G:/My%20Drive/dev/GitHub/portfolio-SQAAILab/25-AI-vibe-coding-tests/result/test/reports/test_results_integration_20260305_150730.html -
====================== 49 passed, 106 warnings in 9.95s =======================

```

---

*Report generated on 2026-03-05 15:07:42*
