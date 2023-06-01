from orm_config.init_orm import OrmConfig
import jwt
import uvicorn

from datetime import datetime, timedelta
from typing import Union, Any
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

class AuthorizationService:


    def __init__(self, db_connect: OrmConfig) -> None:
        self.dbConnect = db_connect
        super().__init__()

    def verify(self, username: str, password: str):
        if username == 'admin' and password == 'admin':
            return True
        return False

