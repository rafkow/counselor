import requests
import logging
from decouple import config


logging.basicConfig(
    level=logging.INFO,
    filename="logs/log.log",
    filemode="w"
)

logger = logging.getLogger(__name__)


class Portal:
    url = "https://portal.gdansk.sa.gov.pl/api"

    def __init__(self):
        self.__login()

    def __login(self):
        user_credentials = config("USER_CREDENTIALS", "")
        page = requests.post(Portal.url + "/authenticate", json=user_credentials)
        logger.info("test logowania")
        print(f"{page.status_code}")
        logger.warning(f"{page.status_code}")


p = Portal()

