import random
import itertools
from app import app

styles = [
    "modern minimalist",
    "contemporary and transitional",
    "traditional and classic",
    "rustic farmhouse",
    "children’s / playful",
    "elegant and romantic"
]

color_schemes = [
    "neutral earthy tones",
    "white and light teal / pastel",
    "warm browns and cream",
    "bright and colorful accents",
    "blue and natural wood",
    "soft peach, lavender, or muted tones"
]

layouts = [
    "central bed with symmetry",
    "open-plan with balcony or sitting area",
    "compact or shared room",
    "two beds side-by-side",
    "standard hotel arrangement",
    "canopy or ornate centerpiece setup"
]

materials = [
    "painted or dark wood",
    "fabric and textiles",
    "glass and metal accents",
    "sheer or soft fabrics",
    "patterned or textured finishes",
    "natural surfaces (plaster, tile, woven, mirror)"
]

lighting = [
    "abundant natural light",
    "warm ambient lamps",
    "overhead lighting",
    "table or bedside lamps",
    "decorative lighting",
    "bright general lighting"
]

decor = [
    "minimal wall art",
    "mirrors (ornate or large)",
    "cecorative vases and plants",
    "catterned rugs or curtains",
    "child-friendly or playful décor",
    "canopies, drapes, or antique accents"
]


def generate_description():
    return (
        f"A {random.choice(styles)} room with {random.choice(color_schemes)}, "
        f"featuring {random.choice(layouts)}, {random.choice(materials)}, "
        f"{random.choice(lighting)}, and {random.choice(decor)}."
    )

print(generate_description())

