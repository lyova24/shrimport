from shrimport.config import get_config
from shrimport.service import ImportFormatter


def main():
    config = get_config()
    formatter = ImportFormatter(config=config)
    exit(formatter.convert_relative_imports())


if __name__ == "__main__":
    main()
