from typing import Dict, Type, Any

from fastapi import HTTPException, APIRouter
from fastapi.openapi.models import Response
from fastapi.params import Depends

from beans.login_request import LoginRequest
import security.security as security
from beans.login_response import LoginResponse

router = APIRouter()


@router.post('/login', response_model=LoginResponse)
def login(request_data: LoginRequest) -> Any:
    print(f'[x] request_data: {request_data.__dict__}')
    token = security.generate_token(request_data.username)
    # if security.verify_password(username=request_data.username, password=request_data.password):
    #     token = security.generate_token(request_data.username)
    res = LoginResponse()
    res.token = token
    res.username = request_data.username

    # return {"token": token, "username": request_data.username, "email": "mail@xml.vn"}
    return res
    # else:
    #     raise HTTPException(status_code=404, detail="User not found")


@router.get('/books', dependencies=[Depends(security.validate_token)])
def list_books():
    return {'data': ['Sherlock Homes', 'Harry Potter', 'Rich Dad Poor Dad']}
