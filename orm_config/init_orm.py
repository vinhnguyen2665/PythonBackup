import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
import mysql.connector


class OrmConfig:
    engine = None
    factory = None
    session = None
    load_dotenv()

    def __init__(self) -> None:
        if not self.engine:
            self.url_object = URL.create(
                drivername=os.getenv('DATABASE_DRIVER'),
                username=os.getenv('DATABASE_USERNAME'),
                password=os.getenv('DATABASE_PASSWORD'),  # plain (unescaped) text
                host=os.getenv('DATABASE_HOST'),
                port=os.getenv('DATABASE_PORT'),
                database=os.getenv('DATABASE_NAME'),
            )
            self.engine = create_engine(self.url_object)
        super().__init__()

    def get_session(self):
        if not self.session:
            self.factory = sessionmaker(bind=self.engine)
            self.session = self.factory()
        else:
            self.session.close()
            self.factory = sessionmaker(bind=self.engine)
            self.session = self.factory()
        return self.session

    # def __init__(self):
    #     if None == self.engine:
    #         url_object = URL.create(
    #             drivername="mysql+mysqlconnector",
    #             username="root",
    #             password="123456",  # plain (unescaped) text
    #             host="172.18.101.75",
    #             database="database_backup",
    #         )
    #         self.engine = create_engine(url_object)
    #         self.factory = sessionmaker(bind=self.engine)
    #         self.session = self.factory()
