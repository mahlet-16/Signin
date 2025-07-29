from fastapi import APIRouter, Body

from controllers import login, single_cancelation, single_registration

router = APIRouter()


@router.get("/login")
def login_route():
    return login()


@router.post("/single-registration")
def single_registration_route(request_body: dict = Body(...)):
    return single_registration(request_body)


@router.post("/single-cancelation")
def single_cancelation_route(request_body: dict = Body(...)):
    return single_cancelation(request_body)
