def get_slider_format(metric_name):
    """Determine the appropriate slider format based on the metric name"""
    if "CAC Payback Period" in metric_name:
        return "%d months"
    elif "Decision turnaround time" in metric_name:
        return "%d hours"
    elif "CAC trend" in metric_name:
        return "%.2f"
    else:
        return "%.1f%%"


def get_slider_range(metric_name):
    """Determine the appropriate slider range based on the metric name"""
    if "CAC Payback Period" in metric_name:
        return (0, 36)  # 0 to 36 months
    elif "Decision turnaround time" in metric_name:
        return (0, 168)  # 0 to 168 hours (1 week)
    elif "CAC trend" in metric_name:
        return (-1.0, 1.0)  # -1 to 1
    else:
        return (0.0, 100.0)  # 0% to 100%


def get_step_size(metric_name):
    """Determine the appropriate step size based on the metric name"""
    if "CAC Payback Period" in metric_name:
        return 1.0  # Months as decimal
    elif "Decision turnaround time" in metric_name:
        return 1.0  # Hours as decimal
    elif "CAC trend" in metric_name:
        return 0.1  # 0.1 increments
    else:
        return 0.1  # 0.1% increments
