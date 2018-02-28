import logging
from django.apps import AppConfig

class ApiConfig(AppConfig):
    name = 'api'
    login_time_duration_in_minutes = 10
    query_row_limit = 20
    order_expired_in_hour = 24

    def loggerWarning(error) -> None:
        logging_logger = logging.getLogger('sofia.api.warning')
        logging_logger.error('#' * 50 + ' ' + str(error) + ' ' + '#' * 50)

    def loggerCritical(error) -> None:
        logging_logger = logging.getLogger('sofia.api.critical')
        logging_logger.error('#' * 50 + ' ' + str(error) + ' ' + '#' * 50)
