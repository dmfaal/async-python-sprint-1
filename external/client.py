import json
import logging
from http import HTTPStatus
from urllib.request import urlopen
from urllib.error import HTTPError

ERR_MESSAGE_TEMPLATE = "Unexpected error: {error}"


logger = logging.getLogger()


class YandexWeatherAPI:
    """
    Base class for requests
    """

    def __do_req(url: str) -> str:
        """Base request method"""
        try:
            with urlopen(url) as response:
                resp_body = response.read().decode("utf-8")
                data = json.loads(resp_body)
            if response.status != HTTPStatus.OK:
                raise Exception(
                    "Error during execute request. {}: {}".format(
                        resp_body.status, resp_body.reason
                    )
                )
            return data
        # Обработка ошибки 404
        except HTTPError as http_err:
            if http_err.code == 404:
                logger.error("Страница не найдена: %s", url)
        # Обработка неверного JSON
        except json.JSONDecodeError as json_error:
            if json_error == {}:
                logger.error("пустые данные %s", url)
        except Exception as ex:
            logger.error(ex)
            raise Exception(ERR_MESSAGE_TEMPLATE.format(error=ex))

    @staticmethod
    def get_forecasting(url: str):
        """
        :param url: url_to_json_data as str
        :return: response data as json
        """
        return YandexWeatherAPI.__do_req(url)
