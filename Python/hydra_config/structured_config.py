from dataclasses import dataclass, field
import os

import hydra
from hydra.core.config_store import ConfigStore
from omegaconf import OmegaConf


@dataclass
class SpringerNatureDataConfig:
    s3_bucket_name: str = os.getenv("S3_BUCKET_NAME", "datalake")
    s3_prefix: str = os.getenv("S3_PREFIX", "springer-nature")
    local_data_dir: str = os.getenv("LOCAL_DATA_DIR", "default/local/dir")
    max_workers: int = int(os.getenv("MAX_WORKERS", "6"))

@dataclass
class SpringerNatureDataLoaderConfig:
    data_config: SpringerNatureDataConfig = field(default_factory=SpringerNatureDataConfig)
    local_data_dir: str = os.getenv("LOADER_LOCAL_DATA_DIR", "default/loader/dir")
    batch_size: int = int(os.getenv("BATCH_SIZE", "100"))

@dataclass
class DataLoaderConfig:
    springer_nature: SpringerNatureDataLoaderConfig = field(default_factory=SpringerNatureDataLoaderConfig)

@dataclass
class ChunkingConfig:
    chunk_size: int = int(os.getenv("CHUNK_SIZE", "1000"))
    chunk_overlap: int = int(os.getenv("CHUNK_OVERLAP", "200"))

@dataclass
class EmbeddingModelConfig:
    model: str = os.getenv("MODEL", "openai_text_embedding_ada")
    openai_api_base: str = os.getenv("OPENAI_API_BASE", "https://www.openai.com")

@dataclass
class VectorStoreConfig:
    # define fields if any
    pass

@dataclass
class AppConfig:
    data_loader: DataLoaderConfig = field(default_factory=DataLoaderConfig)
    chunking: ChunkingConfig = field(default_factory=ChunkingConfig)
    embedding: EmbeddingModelConfig = field(default_factory=EmbeddingModelConfig)
    vector_store: VectorStoreConfig = field(default_factory=VectorStoreConfig)


cs = ConfigStore.instance()
# AppConfig is a top-level config
cs.store(name="all_config", node=AppConfig)
# Below are modular configs and can be used seperately on demand
cs.store(name="embedding_model_config", node=EmbeddingModelConfig)
cs.store(name="chunking_config", node=ChunkingConfig)


# Initialize Hydra and print the configuration
@hydra.main(config_name="all_config", version_base="1.3")
def main(cfg: AppConfig) :
    print(OmegaConf.to_yaml(cfg))

# @hydra.main(config_name="embedding_model_config", version_base="1.3")
# def main(cfg: EmbeddingModelConfig) :
#     print(OmegaConf.to_yaml(cfg))


if __name__ == "__main__":
    main()