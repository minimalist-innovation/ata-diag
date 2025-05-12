def get_slider_format(units):
    """Determine the appropriate slider format based on the metric units"""
    if "Months" in units:
        return "%d"
    elif "Days" in units:
        return "%d"
    elif "Hours" in units:
        return "%d"
    elif "Milliseconds" in units:
        return "%d"
    elif "Percentage" in units:
        return "%.1f%%"
    else:
        return "%.2f"


def get_step_size(units):
    """Determine the appropriate step size based on the metric units"""
    if "Months" in units:
        return 1.0
    elif "Days" in units:
        return 5.0
    elif "Hours" in units:
        return 1.0
    elif "Percentage" in units:
        return 0.3
    else:
        return 0.5
