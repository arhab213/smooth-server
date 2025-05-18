from fastapi.responses import JSONResponse


def build_json_response(status: int, context: str) -> dict:
    return JSONResponse(
        status_code=400,
        content={
            "status": True,
            "status_code": status,
            "message": context,
        },
    )
