import logging
from django.apps import AppConfig

class ApiConfig(AppConfig):
    name = 'api'
    token_time_client = 60
    token_time_admin = 10080
    query_row_limit = 20
    order_expired_in_hour = 24

    def loggerWarning(error) -> None:
        logging_logger = logging.getLogger('sofia.api.warning')
        logging_logger.warning('#' * 10 + ' ' + str(error) + ' ' + '#' * 10)

        if error.error_exception:
            ApiConfig.loggerCritical(error.error_exception)

    def loggerCritical(error) -> None:
        logging_logger = logging.getLogger('sofia.api.critical')
        logging_logger.critical('#' * 10 + ' ' + str(error) + ' ' + '#' * 10)
