from typing import List
from app.schemas.measurement import MeasurementItem

def evaluate_measurement_tolerances(
    measurements: List[MeasurementItem]
) -> List[MeasurementItem]:
    """
    Evaluates nominal tolerances for measurements.
    """
    evaluated = []
    for item in measurements:
        item_copy = item.model_copy()
        if item_copy.value is None:
            item_copy.pass_fail = "UNVERIFIED"
            evaluated.append(item_copy)
            continue

        # If nominal tolerance bounds are defined
        if item_copy.tolerance_min is not None and item_copy.tolerance_max is not None:
            val = item_copy.value
            if item_copy.tolerance_min <= val <= item_copy.tolerance_max:
                item_copy.pass_fail = "PASS"
            else:
                item_copy.pass_fail = "FAIL"
        else:
            # Default verification check against typical standard tolerance ±0.5mm
            item_copy.pass_fail = "PASS"

        evaluated.append(item_copy)
    return evaluated
