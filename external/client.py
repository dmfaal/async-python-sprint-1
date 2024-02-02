import json
import logging
from http import HTTPStatus
from typing import Any
from urllib.request import urlopen
from urllib.error import HTTPError

ERR_MESSAGE_TEMPLATE = "Unexpected error: {error}"


logger = logging.getLogger()


class YandexWeatherAPI:
    """
    Base class for requests
    """

    @staticmethod
    def __do_req(url: str) -> Any:
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
            if not data:  # Проверка на пустой JSON
                logger.error("Пустой JSON-ответ: %s", url)
                return None
            return data
        # Обработка ошибки 404
        except HTTPError as http_err:
            if http_err.code == 404:
                logger.error("Страница не найдена: %s", url)
                return None
        # Обработка неверного JSON
            else:
                logger.error("Произошла ошибка при выполнении запроса: %s", http_err)
                raise Exception(ERR_MESSAGE_TEMPLATE.format(error=http_err))
        except json.JSONDecodeError as json_error:
            logger.error("Ошибка разбора JSON: %s", json_error)
            logger.error("URL ошибки выше: %s", url)
            return None
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
