import argparse


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-R",
        "--root-dir",
        default=".",
        help="path to root directory (e.g., ./shrimport)",
    )
    parser.add_argument(
        "-i",
        "--ignore",
        action="append",
        default=[],
        dest="ignored_paths",
        help="regex pattern to ignore file paths",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        default=False,
        dest="is_verbose",
        help="output extra information",
    )
    parser.add_argument(
        "-d",
        "--dry-run",
        action="store_true",
        default=False,
        dest="is_dry_run",
        help="run without changes",
    )
    parser.add_argument(
        "file_paths",
        nargs="+",
        help="files to be processed",
    )
    return parser.parse_args()
