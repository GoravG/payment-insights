import numpy as np


# Helper function to convert numpy types to Python native types
def to_native(obj):
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.bool_):
        return bool(obj)
    elif isinstance(obj, np.datetime64):
        return str(obj)
    return obj
