import dotenv
path_to_env_file = ".env"
env_var_loaded: bool = dotenv.load_dotenv(path_to_env_file, override=True)


import hydra
from omegaconf import OmegaConf
from pathlib import Path
import logging
from typing import List

from structured_config import AppConfig

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@hydra.main(config_name="all_config", version_base="1.3")
def main(cfg: AppConfig) :
    print(OmegaConf.to_yaml(cfg))

if __name__ == "__main__":
    main()