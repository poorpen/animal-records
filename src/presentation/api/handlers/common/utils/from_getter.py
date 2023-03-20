from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel


def from_getter(request: Request, model: BaseModel):
    try:
        model.offset = int(request.query_params['from'])
    except KeyError:
        model.offset = model.offset
