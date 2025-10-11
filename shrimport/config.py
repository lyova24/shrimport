import dataclasses
from dataclasses import dataclass, field, fields
from functools import lru_cache

from shrimport.utils import get_args


@dataclass
class Config:
    root_dir: str = "./"
    is_verbose: bool = False
    is_dry_run: bool = False
    file_paths: list[str] = field(default_factory=list)
    ignored_paths: list[str] = field(default_factory=list)

    @classmethod
    def get_from_arguments(cls) -> "Config":
        args = get_args()
        initial_values = {}
        for f in fields(cls):
            if value := getattr(args, f.name, None):
                initial_values[f.name] = value
            else:
                if f.default_factory is not dataclasses.MISSING:
                    initial_values[f.name] = f.default_factory()
                    continue
                initial_values[f.name] = f.default
        return cls(**initial_values)


@lru_cache(1)
def get_config() -> Config:
    return Config.get_from_arguments()
