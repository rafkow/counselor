import requests
import logging
import ast
from decouple import config
from datetime import datetime
from datetime import timedelta


logging.basicConfig(
    level=logging.INFO,
    filename="logs/log.log",
    filemode="w"
)

logger = logging.getLogger(__name__)


class Portal:
    url = "https://portal.gdansk.sa.gov.pl/api"
    token = ''
    token_exp = datetime.now()

    @classmethod
    def __login(cls):
        user_credentials = ast.literal_eval(config("USER_CREDENTIALS", ""))
        response = requests.post(cls.url+"/authenticate", json=user_credentials)
        logger.info(f"logowanie {response.status_code}")

        if response.status_code == 200:
            if response.json().get('id_token'):
                cls.token = response.json().get('id_token')
                logger.info(f"token {cls.token}")
                cls.token_exp = datetime.now() + timedelta(minutes=15)

    @classmethod
    def __get_token(cls):
        if cls.token_exp < datetime.now():
            cls.__login()
        return f"Bearer {cls.token}"

    @classmethod
    def __get_headers(cls):
        headers = {"Content-Type": "application/json; charset=utf-8",
                   "Authorization": cls.__get_token(),
                   }
        return headers

    @classmethod
    def __renew_token(cls, response):
        if response.headers['Authorization']:
            cls.token = response.headers['Authorization'].split()[1]
            logger.info(f"token renew {cls.token}")
            cls.token_exp = datetime.now() + timedelta(minutes=15)

    @classmethod
    def get_case_by_court_reference_number(cls, signature):
        params = f"/lawsuits/light?signature.contains={signature}"
        response = requests.get(cls.url+params, headers=cls.__get_headers())
        logger.info(f"{response.status_code}  {response.json()}")
        cls.__renew_token(response)
        return response.json()




