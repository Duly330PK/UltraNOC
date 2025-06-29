from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.forensics_schema import ForensicsQuery, ForensicsResult
from app.models.cgnat_log import CGNATLog
from app.models.user import User
from datetime import timedelta, timezone
from app.auth.auth_bearer import require_role

router = APIRouter(dependencies=[Depends(require_role("admin"))])

@router.post("/trace", response_model=ForensicsResult)
def trace_connection(query: ForensicsQuery, db: Session = Depends(get_db)):
    # Ensure timestamp from frontend is timezone-aware (UTC) for correct comparison
    if query.timestamp.tzinfo is None:
        query.timestamp = query.timestamp.replace(tzinfo=timezone.utc)

    time_window_start = query.timestamp - timedelta(minutes=5)
    time_window_end = query.timestamp + timedelta(minutes=5)

    log_entry = db.query(CGNATLog).filter(
        CGNATLog.external_ip == query.ip_address,
        CGNATLog.external_port == query.port,
        CGNATLog.timestamp.between(time_window_start, time_window_end)
    ).order_by(CGNATLog.timestamp.desc()).first()

    if not log_entry:
        raise HTTPException(status_code=404, detail="No matching log entry found for the given time window.")

    # In a real system, this would involve a lookup in a provisioning database.
    # Here, we simulate it based on the customer ID format.
    simulated_device_id = f"ONT-{log_entry.customer_id[-4:]}"

    return ForensicsResult(
        found=True,
        customer_id=log_entry.customer_id,
        internal_ip=log_entry.internal_ip,
        segment=log_entry.segment,
        device_id=simulated_device_id
    )