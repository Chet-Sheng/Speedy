import dotenv

from configs import DataConfig, DataLoaderConfig, DataLoaderConfigV2

env_loaded: bool = dotenv.load_dotenv(override=True)
print(f"Environment variables loaded: {env_loaded}")

data_config = DataConfig()
print(data_config)

data_loader_config = DataLoaderConfig()
print(data_loader_config)  # env var DATA_S3_BUCKET_NAME not set here

data_loader_config = DataLoaderConfigV2()
print(data_loader_config)  # env var DATA_S3_BUCKET_NAME is properly set here