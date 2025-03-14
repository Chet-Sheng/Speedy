from enum import Enum
from pathlib import Path
from typing import Tuple, Type
from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, PydanticBaseSettingsSource, SettingsConfigDict, TomlConfigSettingsSource
import yaml


class DataLoaderEnum(Enum):
    nature = "nature"
    pubmed = "pubmed"


class DataConfig(BaseSettings):
    s3_bucket: str = "my-bucket"
    s3_prefix: str = "path-to-data"
    local_data_dir: str = "my-local-path"
    max_workers: int = 6


class DataLoaderConfig(BaseSettings):
    # this will be initialized whenever DataLoaderConfig is imported, making env vars not effective
    data_config: DataConfig = DataConfig()
    data_loader: DataLoaderEnum = Field(description="Data loader type")
    local_data_dir: str = str((Path(__file__).parents[0] / "artefacts").resolve())
    batch_size: int = 100


class AppConfig(BaseSettings):
    # ref: https://docs.pydantic.dev/2.10/concepts/pydantic_settings/#field-value-priority
    model_config = SettingsConfigDict(
        cli_parse_args=True,
    env_file='.env', 
        env_file_encoding='utf-8',
        env_nested_delimiter='__',
        env_prefix='APP_CONFIG_',
        extra="ignore",  # ignore extra keys not defined in the model
        toml_file='configs.toml',  # it is okey for the file to not exist
        # yaml_file='configs.yaml',
    )  # default priority: cli args > env > .env > ...
    
    data_loader_config: DataLoaderConfig = Field(default_factory=DataLoaderConfig)
    app_name: str = "deepsearch"
    api_key: SecretStr


    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        # init_settings: for CLI input
        # below sequence reflects the priority of settings: CLI > env > .env > toml
        return (init_settings, env_settings, dotenv_settings, TomlConfigSettingsSource(settings_cls),)


if __name__ == "__main__":
    app_config = AppConfig()
    # print(yaml.dump(app_config.model_dump()))
    # import tomllib
    # with open("configs.toml", "rb") as f:
    #     v = tomllib.load(f)
    #     print(v)

    print(app_config.model_dump_json(indent=2))
    # breakpoint()

    # python configs.py --app_name="hello world" --data_loader_config.data_config.s3_bucket="cli_bucket_name"

