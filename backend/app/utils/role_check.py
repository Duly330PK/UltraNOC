from fastapi import Request, HTTPException

def check_permission(request: Request, required_role: str):
    user_role = request.headers.get("X-User-Role", "guest")
    if user_role != required_role:
        raise HTTPException(status_code=403, detail="Insufficient privileges")
