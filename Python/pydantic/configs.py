from enum import Enum
import os
from pathlib import Path
import tomllib
from typing import Self, Tuple, Type
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
        # toml_file=os.getenv("PATH_TO_TOML", 'configs.toml'),  # it is okey for the file to not exist
        # NOTE: Removing toml_file from here since we'll load it manually
        # yaml_file='configs.yaml',  
        # NOTE:defining `yaml_file`/`toml_file` here are not that useful, since they need to be fixed paths
    )  # default priority: cli args > env > .env > ...
    
    data_loader_config: DataLoaderConfig = Field(default_factory=DataLoaderConfig)
    app_name: str = "deepsearch"
    api_key: SecretStr
    test_msg: str

    
    # inspect default params: `help(AppConfig.__init__)`


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
    
    @classmethod
    def from_toml(cls, toml_path: str, **kwargs) -> 'AppConfig':
        """
        Create an AppConfig instance, loading settings from a specified TOML file
        while preserving the correct priority order.

        Priority Order:
        1. CLI arguments
        2. Environment variables
        3. .env file
        4. Dynamically specified TOML file (via this method)
        5. Model's default values
        """
        
        # Create a new SettingsConfigDict that includes the dynamic toml_file path.
        # It inherits all other settings from the base class's model_config.
        dynamic_config = cls.model_config.copy()
        dynamic_config['toml_file'] = toml_path

        # 2. Generate a dynamic and descriptive name for the temporary class.
        # This is crucial for debugging and clarity.
        dynamic_class_name = f"Dynamic{cls.__name__}FromToml"
        
        # NOTE: More detailed explanation in `README.md`
        # Use Python's `type()` to create a new class on the fly.
        # This new class inherits from our original `AppConfig` but has the
        # modified `model_config`.
        DynamicConfig = type(
            dynamic_class_name,  # The name of the new class
            (cls,),              # A tuple of base classes (our AppConfig)
            {'model_config': dynamic_config} # A dict of class attributes
        )
        
        # Instantiate this new temporary class. Pydantic will now use its
        # built-in `toml_file` loader at the correct priority.
        return DynamicConfig(**kwargs)

if __name__ == "__main__":
    app_config = AppConfig()
    # app_config = AppConfig.from_toml("configs.toml")
    # print(yaml.dump(app_config.model_dump()))
    # import tomllib
    # with open("configs.toml", "rb") as f:
    #     v = tomllib.load(f)
    #     print(v)

    print(app_config.model_dump_json(indent=2))
    # breakpoint()

    # python configs.py --app_name="config-from-cli-args" --data_loader_config.data_config.s3_bucket="cli_bucket_name"

