# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from dataclasses import dataclass, field
import logging
from pathlib import Path

from omegaconf import MISSING, OmegaConf
import hydra
from hydra.core.config_store import ConfigStore


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class DataConfig:
    s3_bucket_name: str = MISSING
    s3_prefix: str = MISSING
    local_data_dir: str = MISSING
    max_workers: int = MISSING


@dataclass
class DataLoaderConfig:
    data_config: DataConfig=MISSING
    local_data_dir: str = MISSING
    batch_size: int = MISSING


@dataclass
class SpringerNatureDataConfig(DataConfig):
    s3_bucket_name: str = "datalake-anansi"
    s3_prefix: str = MISSING
    local_data_dir: str = str(Path(__file__).parents[1] / "artefacts/data/datalake-anasi").resolve()
    max_workers: int = 6


@dataclass
class SpringerNatureDataLoaderConfig(DataLoaderConfig):
    data_config: SpringerNatureDataConfig = field(default_factory=SpringerNatureDataConfig)
    local_data_dir: str = MISSING
    batch_size: int = 100


@dataclass
class DBConfig:
    driver: str = MISSING
    host: str = "localhost"
    port: int = MISSING


@dataclass
class MySQLConfig(DBConfig):
    driver: str = "mysql"
    port: int = 3306
    user: str = MISSING
    password: str = MISSING


@dataclass
class PostGreSQLConfig(DBConfig):
    driver: str = "postgresql"
    user: str = MISSING
    port: int = 5432
    password: str = MISSING
    timeout: int = 10


@dataclass
class Config:
    data_loader: DataLoaderConfig= MISSING
    db: DBConfig = MISSING
    debug: bool = False


cs = ConfigStore.instance()
cs.store(name="base_config", node=Config)
cs.store(group="db", name="base_mysql", node=MySQLConfig)
cs.store(group="db", name="base_postgresql", node=PostGreSQLConfig)


@hydra.main(version_base=None, config_path="conf", config_name="config")
def my_app(cfg: Config) -> None:
    logger.info(f"Configs:\n{OmegaConf.to_yaml(cfg)}")


if __name__ == "__main__":
    my_app()