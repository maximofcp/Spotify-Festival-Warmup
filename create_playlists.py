import logging
import sys

from dotenv import load_dotenv

from factories import AuthFactory, ServiceFactory, UserFactory


def logging_config():
    logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='-> %(message)s')


if __name__ == "__main__":
    load_dotenv()
    logging_config()

    auth = AuthFactory.create_from_env()
    user = UserFactory(auth).me()
    service_factory = ServiceFactory(auth)
    festivals = service_factory.festivals().read_all()
    service_factory.playlists().create_or_update_playlists_for_festivals(festivals, user)
