from datetime import datetime, timedelta

def calculate_expiry(start_date, duration):
    """Calculate expiry date based on duration ('monthly', '6 months', 'yearly', or custom days)."""
    
    if duration == "monthly":
        return start_date + timedelta(days=30)  # Approximate
    elif duration == "6 months":
        return start_date + timedelta(days=182)  # 6 months
    elif duration == "yearly":
        return start_date + timedelta(days=365)  # 1 year
    elif isinstance(duration, int):  # Manual entry (custom days)
        return start_date + timedelta(days=duration)
    else:
        raise ValueError("Invalid duration")

# Example Usage
if __name__ == "__main__":
    start_date = datetime.today()
    expiry = calculate_expiry(start_date, "6 months")
    print("Expiry Date:", expiry)
