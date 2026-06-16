from dataclasses import dataclass


@dataclass
class Config:
    width: int
    height: int
    entry_x: int
    entry_y: int
    exit_x: int
    exit_y: int
    perfect: bool
    output_file: str