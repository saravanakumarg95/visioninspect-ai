from typing import List, Dict, Any
from .database import ISO_METRIC_FASTENERS

def search_fasteners_database(query: str = "") -> List[Dict[str, Any]]:
    """
    Searches ISO standards database by query term.
    """
    if not query:
        return ISO_METRIC_FASTENERS

    q = query.strip().lower()
    results = []
    for item in ISO_METRIC_FASTENERS:
        if (q in item["designation"].lower() or
            q in item["nominal_size"].lower() or
            q in item["type"].lower() or
            q in item["standard"].lower()):
            results.append(item)
    return results
