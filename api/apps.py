from django.apps import AppConfig


class ApiConfig(AppConfig):
    name = 'api'
    login_time_duration_in_minutes = 10
    query_row_limit = 20
    order_expired_in_hour = 24
