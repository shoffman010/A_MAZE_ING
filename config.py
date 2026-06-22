from dataclasses import dataclass
import re


@dataclass
class Config:
    width: int
    height: int
    entry: tuple[int, int]
    exit: tuple[int, int]
    perfect: bool
    output_file: str
    pattern: str
    seed: int | None
    wall_color: str
    path_color: str
    pattern_color: str


CONFIG_KEYS = (
    "WIDTH",
    "HEIGHT",
    "ENTRY",
    "EXIT",
    "OUTPUT_FILE",
    "PERFECT",
    "PATTERN",
    "SEED",
    "WALL_COLOR",
    "PATH_COLOR",
    "PATTERN_COLOR",
)

KEY_VALUE_PATTERN = re.compile(
    rf"^\s*(?P<key>{'|'.join(CONFIG_KEYS)})\s*=\s*(?P<value>.*?)\s*$"
)
COORDINATE_PATTERN = re.compile(
    r"^\s*(?P<x>-?\d+)\s*,\s*(?P<y>-?\d+)\s*$"
)
BOOLEAN_PATTERN = re.compile(r"^(?P<value>True|False)$")

REQUIRED_KEYS = set(CONFIG_KEYS) - {"PATTERN"}

COLOR_NAMES = {
    "BLACK",
    "RED",
    "GREEN",
    "YELLOW",
    "BLUE",
    "MAGENTA",
    "CYAN",
    "WHITE",
    "DEFAULT",
}


def load_config(path: str) -> Config:
    """Parse and validate a maze configuration file."""
    values: dict[str, str] = {}

    with open(path, "r") as config_file:
        for line_number, line in enumerate(config_file, start=1):
            stripped_line = line.strip()
            if not stripped_line or stripped_line.startswith("#"):
                continue

            key_value_match = KEY_VALUE_PATTERN.fullmatch(line)
            if key_value_match is None:
                valid_keys = ", ".join(CONFIG_KEYS)
                raise ValueError(
                    f"invalid config syntax on line {line_number}: "
                    f"expected one of {valid_keys}=VALUE"
                )

            key = key_value_match.group("key")
            value = key_value_match.group("value").strip()

            if key in values:
                raise ValueError(f"duplicate config key: {key}")

            values[key] = value

    missing_keys = REQUIRED_KEYS - values.keys()
    if missing_keys:
        missing = ", ".join(missing_keys)
        raise ValueError(f"missing required config key(s): {missing}")

    width = _parse_positive_int(values["WIDTH"], "WIDTH")
    height = _parse_positive_int(values["HEIGHT"], "HEIGHT")
    entry = _parse_maze_position(values["ENTRY"], width, height, "ENTRY")
    exit = _parse_maze_position(values["EXIT"], width, height, "EXIT")
    perfect = _parse_bool(values["PERFECT"], "PERFECT")
    output_file = values["OUTPUT_FILE"]
    pattern = values.get("PATTERN") or "42"
    seed = _parse_seed(values["SEED"])
    wall_color = _parse_color(values.get("WALL_COLOR", "DEFAULT"), "WALL_COLOR")
    path_color = _parse_color(values.get("PATH_COLOR", "RED"), "PATH_COLOR")
    pattern_color = _parse_color(values.get("PATTERN_COLOR", "CYAN"), "PATTERN_COLOR")

    if not output_file:
        raise ValueError("OUTPUT_FILE cannot be empty")

    if entry == exit:
        raise ValueError("ENTRY and EXIT must be different coordinates")

    return Config(
        width=width,
        height=height,
        entry=entry,
        exit=exit,
        perfect=perfect,
        output_file=output_file,
        pattern=pattern,
        seed=seed,
        wall_color=wall_color,
        path_color=path_color,
        pattern_color=pattern_color,
    )


def _parse_positive_int(value: str, key: str) -> int:
    try:
        number = int(value)
    except ValueError:
        raise ValueError(f"{key} must be an integer")

    if number <= 0:
        raise ValueError(f"{key} must be greater than 0")

    return number


def _parse_maze_position(
    value: str,
    width: int,
    height: int,
    key: str,
) -> tuple[int, int]:
    coordinate_match = COORDINATE_PATTERN.fullmatch(value)
    if coordinate_match is None:
        raise ValueError(f"{key} must use x,y coordinates")

    x = int(coordinate_match.group("x"))
    y = int(coordinate_match.group("y"))

    if not (0 <= x < width and 0 <= y < height):
        raise ValueError(f"{key} must be inside the maze bounds")

    return y, x


def _parse_bool(value: str, key: str) -> bool:
    boolean_match = BOOLEAN_PATTERN.fullmatch(value)
    if boolean_match is None:
        raise ValueError(f"{key} must be True or False")

    return boolean_match.group("value") == "True"


def _parse_seed(value: str) -> int | None:
    if not value:
        return None

    try:
        return int(value)
    except ValueError:
        raise ValueError("SEED must be an integer")


def _parse_color(value: str, key: str) -> str:
    color = value.upper()
    if color not in COLOR_NAMES:
        available_colors = ", ".join(sorted(COLOR_NAMES))
        raise ValueError(f"{key} must be one of: {available_colors}")

    return color
