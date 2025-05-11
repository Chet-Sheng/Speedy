from .config import ModelConfig
from .registry import build_model
import .bindings  # Ensures all components are registered

cfg = ModelConfig(model_name="dense", embedder="openai", splitter="sentence")
model = build_model(cfg)
print(model.predict("This is a test. Another sentence here.")) 