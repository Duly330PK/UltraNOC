def generate_event(type, device_id, message, severity):
    return {
        "type": type,
        "device_id": device_id,
        "message": message,
        "severity": severity
    }
