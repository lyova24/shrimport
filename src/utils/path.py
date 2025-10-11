from pathlib import Path


def get_path_from_str(path: str) -> Path:
    return Path(path).expanduser().resolve()


def get_paths_from_list(paths: list[str]) -> list[Path]:
    return [Path(path).expanduser().resolve() for path in paths]


def get_module_path(file_path: Path, root_dir: Path) -> str | None:
    try:
        relative_path = (
            file_path.resolve().relative_to(root_dir.resolve()).with_suffix("")
        )
    except ValueError:
        print(f"skip: {file_path} not in root_dir {root_dir}")
        return None
    return ".".join(relative_path.parts)


def exit_if_path_is_not_a_dir(path: Path) -> None:
    if not path.is_dir():
        exit(f"path {path} is not a directory.")
