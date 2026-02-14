def lerp(t: float, min_val: float, max_val: float) -> float:
    return min_val + t * (max_val - min_val)


def inverse_lerp(value: float, min_val: float, max_val: float) -> float:
    return (value - min_val) / (max_val - min_val)
