import numpy as np
# Helper function to convert numpy types to Python native types
def convert_numpy_type(obj):
    if isinstance(obj, (np.int8, np.int16, np.int32, np.int64,
                        np.uint8, np.uint16, np.uint32, np.uint64)):
        return int(obj)
    elif isinstance(obj, (np.float16, np.float32, np.float64)):
        return float(obj)
    elif isinstance(obj, np.bool_):
        return bool(obj)
    elif isinstance(obj, np.datetime64):
        return str(obj)
    return obj