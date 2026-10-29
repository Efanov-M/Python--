# Тестирование Django-приложения с использованием Pytest

Необходимо выполнить и предоставить на проверку задачу:

[Тестирование Django-приложения с использованием Pytest](./django_testing).

(testvenv) mikhailefanov@Mac-mini-Mikhail django_testing % python -m pytest -v
======================================================================================================================================== test session starts =========================================================================================================================================
platform darwin -- Python 3.14.4, pytest-9.1.1, pluggy-1.6.0 -- /Users/mikhailefanov/Cloud/VSCODE/home_work/Python-разработчик- расширенный курс/Django/dj-homeworks/3.4-django-testing/django_testing/testvenv/bin/python
cachedir: .pytest_cache
django: version: 5.2.17, settings: django_testing.settings (from ini)
rootdir: /Users/mikhailefanov/Cloud/VSCODE/home_work/Python-разработчик- расширенный курс/Django/dj-homeworks/3.4-django-testing/django_testing
configfile: pytest.ini
plugins: django-4.13.0
collected 7 items

tests/students/test_courses_api.py::test_retrieve_course PASSED                                                                                                                                                                                                                                [ 14%]
tests/students/test_courses_api.py::test_list_courses PASSED                                                                                                                                                                                                                                   [ 28%]
tests/students/test_courses_api.py::test_filter_courses_by_id PASSED                                                                                                                                                                                                                           [ 42%]
tests/students/test_courses_api.py::test_filter_courses_by_name PASSED                                                                                                                                                                                                                         [ 57%]
tests/students/test_courses_api.py::test_create_course PASSED                                                                                                                                                                                                                                  [ 71%]
tests/students/test_courses_api.py::test_update_course PASSED                                                                                                                                                                                                                                  [ 85%]
tests/students/test_courses_api.py::test_delete_course PASSED                                                                                                                                                                                                                                  [100%]

========================================================================================================================================= 7 passed in 0.66s ==========================================================================================================================================
(testvenv) mikhailefanov@Mac-mini-Mikhail django_testing %
