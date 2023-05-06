from pathlib import Path
import tomllib
from typing import Any
from pprint import pformat


class Config:
    _config = None
    _expected_config_file_locations = [
        Path('./config.toml'),
        Path('~/.config/worblehat/config.toml'),
        Path('/var/lib/worblehat/config.toml'),
    ]

    def __class_getitem__(cls, name: str) -> Any:
        __config = cls._config
        for attr in name.split('.'):
            __config = __config.get(attr)
            if __config is None:
                raise AttributeError(f'No such attribute: {name}')
        return __config


    @classmethod
    def _locate_configuration_file(cls) -> Path | None:
        for path in cls._expected_config_file_locations:
            if path.is_file():
                return path


    @classmethod
    def _load_configuration_from_file(cls, config_file_path: str | None) -> dict[str, any]:
        if config_file_path is None:
            config_file_path = cls._locate_configuration_file()

        if config_file_path is None:
            print('Error: could not locate configuration file.')
            exit(1)

        with open(config_file_path, 'rb') as config_file:
            args = tomllib.load(config_file)

        return args


    @classmethod
    def db_string(cls) -> str:
        db_type = cls._config.get('database').get('type')

        if db_type == 'sqlite':
            path = Path(cls._config.get('database').get('sqlite').get('path'))
            return f"sqlite:///{path.absolute()}"

        elif db_type == 'postgresql':
            db_config = cls._config.get('database').get('postgresql')
            hostname = db_config.get('hostname')
            port = db_config.get('port')
            username = db_config.get('username')
            password = db_config.get('password')
            database = db_config.get('database')
            return f"psycopg2+postgresql://{username}:{password}@{hostname}:{port}/{database}"
        else:
            print(f"Error: unknown database type '{db_config.get('type')}'")
            exit(1)


    @classmethod
    def debug(cls) -> str:
        return pformat(cls._config)


    @classmethod
    def load_configuration(cls, args: dict[str, any]) -> dict[str, any]:
        cls._config = cls._load_configuration_from_file(args.get('config_file'))