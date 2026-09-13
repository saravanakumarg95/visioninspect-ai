from typing import List, Dict, Any, Optional

ISO_METRIC_FASTENERS: List[Dict[str, Any]] = [
    {
        "standard": "ISO 4014 / DIN 931",
        "type": "hex_bolt",
        "designation": "M3 x 0.5",
        "nominal_size": "M3",
        "nominal_diameter_mm": 3.0,
        "pitch_mm": 0.5,
        "head_width_af_mm": 5.5,  # Across flats
        "head_height_mm": 2.0,
        "standard_lengths_mm": [6, 8, 10, 12, 16, 20, 25]
    },
    {
        "standard": "ISO 4014 / DIN 931",
        "type": "hex_bolt",
        "designation": "M4 x 0.7",
        "nominal_size": "M4",
        "nominal_diameter_mm": 4.0,
        "pitch_mm": 0.7,
        "head_width_af_mm": 7.0,
        "head_height_mm": 2.8,
        "standard_lengths_mm": [8, 10, 12, 16, 20, 25, 30]
    },
    {
        "standard": "ISO 4014 / DIN 931",
        "type": "hex_bolt",
        "designation": "M5 x 0.8",
        "nominal_size": "M5",
        "nominal_diameter_mm": 5.0,
        "pitch_mm": 0.8,
        "head_width_af_mm": 8.0,
        "head_height_mm": 3.5,
        "standard_lengths_mm": [10, 12, 16, 20, 25, 30, 40]
    },
    {
        "standard": "ISO 4014 / DIN 931",
        "type": "hex_bolt",
        "designation": "M6 x 1.0",
        "nominal_size": "M6",
        "nominal_diameter_mm": 6.0,
        "pitch_mm": 1.0,
        "head_width_af_mm": 10.0,
        "head_height_mm": 4.0,
        "standard_lengths_mm": [12, 16, 20, 25, 30, 40, 50]
    },
    {
        "standard": "ISO 4014 / DIN 931",
        "type": "hex_bolt",
        "designation": "M8 x 1.25",
        "nominal_size": "M8",
        "nominal_diameter_mm": 8.0,
        "pitch_mm": 1.25,
        "head_width_af_mm": 13.0,
        "head_height_mm": 5.3,
        "standard_lengths_mm": [16, 20, 25, 30, 40, 50, 60]
    },
    {
        "standard": "ISO 4014 / DIN 931",
        "type": "hex_bolt",
        "designation": "M10 x 1.5",
        "nominal_size": "M10",
        "nominal_diameter_mm": 10.0,
        "pitch_mm": 1.5,
        "head_width_af_mm": 16.0,
        "head_height_mm": 6.4,
        "standard_lengths_mm": [20, 25, 30, 40, 50, 60, 80]
    },
    {
        "standard": "ISO 4014 / DIN 931",
        "type": "hex_bolt",
        "designation": "M12 x 1.75",
        "nominal_size": "M12",
        "nominal_diameter_mm": 12.0,
        "pitch_mm": 1.75,
        "head_width_af_mm": 18.0,
        "head_height_mm": 7.5,
        "standard_lengths_mm": [25, 30, 40, 50, 60, 80, 100]
    },
    {
        "standard": "ISO 4014 / DIN 931",
        "type": "hex_bolt",
        "designation": "M16 x 2.0",
        "nominal_size": "M16",
        "nominal_diameter_mm": 16.0,
        "pitch_mm": 2.0,
        "head_width_af_mm": 24.0,
        "head_height_mm": 10.0,
        "standard_lengths_mm": [30, 40, 50, 60, 80, 100, 120]
    },
    {
        "standard": "ISO 7089 / DIN 125",
        "type": "washer",
        "designation": "Washer M10 Form A",
        "nominal_size": "M10",
        "inner_diameter_mm": 10.5,
        "outer_diameter_mm": 20.0,
        "thickness_mm": 2.0
    },
    {
        "standard": "ISO 7089 / DIN 125",
        "type": "washer",
        "designation": "Washer M8 Form A",
        "nominal_size": "M8",
        "inner_diameter_mm": 8.4,
        "outer_diameter_mm": 16.0,
        "thickness_mm": 1.6
    },
    {
        "standard": "ISO 7089 / DIN 125",
        "type": "washer",
        "designation": "Washer M12 Form A",
        "nominal_size": "M12",
        "inner_diameter_mm": 13.0,
        "outer_diameter_mm": 24.0,
        "thickness_mm": 2.5
    }
]
