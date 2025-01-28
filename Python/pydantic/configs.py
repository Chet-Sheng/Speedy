from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings


class DataConfig(BaseSettings):
    s3_bucket_name: str = "my-bucket"
    s3_prefix: str = "path-to-data"
    local_data_dir: str = "my-local-path"
    max_workers: int = 6

    class Config:
        env_prefix = "DATA_"
        case_sensitive = False


class DataLoaderConfig(BaseSettings):
    # this will be initialized whenever DataLoaderConfig is imported, making env vars not effective
    data_config: DataConfig = DataConfig()
    local_data_dir: str = str((Path(__file__).parents[0] / "artefacts").resolve())
    batch_size: int = 100

    class Config:
        env_prefix = "DATA_LOADER_"
        case_sensitive = False

class DataLoaderConfigV2(BaseSettings):
    data_config: DataConfig = Field(default_factory=DataConfig)  # use default_factory for dynamic initialization
    local_data_dir: str = str((Path(__file__).parents[0] / "artefacts").resolve())
    batch_size: int = 100
    
    class Config:
        env_prefix = "DATA_LOADER_"
        case_sensitive = False
