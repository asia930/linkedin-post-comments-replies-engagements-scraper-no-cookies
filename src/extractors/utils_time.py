from datetime import datetime, timedelta

def parse_relative_time(timestamp: int) -> str:
    now = datetime.utcnow()
    dt = datetime.utcfromtimestamp(timestamp)
    delta = now - dt

    if delta < timedelta(minutes=1):
        return "just now"
    elif delta < timedelta(hours=1):
        mins = int(delta.total_seconds() / 60)
        return f"{mins}m ago"
    elif delta < timedelta(days=1):
        hrs = int(delta.total_seconds() / 3600)
        return f"{hrs}h ago"
    elif delta < timedelta(days=7):
        days = delta.days
        return f"{days}d ago"
    else:
        return dt.strftime("%b %d, %Y")