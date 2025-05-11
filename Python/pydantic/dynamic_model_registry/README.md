# Dynamic Model Registry

A lightweight Python library that implements a dynamic registry pattern for managing and instantiating different types of models and their components using decorators.

## Overview

This project provides a flexible way to register and instantiate different types of models (dense, sparse) along with their components (embedders, splitters, rerankers, filters) using a decorator-based registry pattern. It's designed to be extensible and maintain a clean separation between infrastructure and business logic.

## Key Features

- Decorator-based registration system
- Type-safe model configuration
- Component-based architecture
- Clean separation of concerns

## Architecture

### Dynamic Registry Pattern

The registry system uses Python decorators to register different types of components. The decorators are applied to classes rather than methods, allowing for class-level registration:

```python
@register_model(ModelName.dense)
class DenseModel:
    pass
```

The decorator syntax above is equivalent to:
```python
class DenseModel:
    pass
DenseModel = register_model(ModelName.dense)(DenseModel)
```

This means:
1. First, `register_model(ModelName.dense)` is called, which returns a decorator function
2. Then, that decorator function is called with `DenseModel` as its argument
3. The decorator registers the class in `MODEL_REGISTRY` and returns the original class

Each component type has its own registry:
- Models (`MODEL_REGISTRY`)
- Embedders (`EMBEDDER_REGISTRY`)
- Splitters (`SPLITTER_REGISTRY`)
- Rerankers (`RERANKER_REGISTRY`)
- Filters (`FILTER_REGISTRY`)

### Type System and Decoupling

The `types.py` module plays a crucial role in decoupling infrastructure from business logic:

1. **Enum-based Type Definitions**: Each component type is defined as a string enum, providing type safety and validation:
   ```python
   class ModelName(str, Enum):
       dense = "dense"
       sparse = "sparse"
   ```

2. **Infrastructure Decoupling**: By using enums for component names:
   - Business logic can reference components by their enum values
   - Infrastructure layer can map these values to actual implementations
   - Changes to implementation details don't affect business logic
   - Easy to add new component types without modifying existing code

### Model Building

The `build_model` function demonstrates how the registry pattern works in practice:

1. Takes a `ModelConfig` with component specifications
2. Looks up registered classes for each component
3. Instantiates components with proper configuration
4. Assembles the final model with all components

## Usage Example

```python
config = ModelConfig(
    model_name=ModelName.dense,
    embedder=EmbedderName.openai,
    splitter=SplitterName.sentence,
    reranker=RerankerName.none,
    filter=FilterName.none
)

model = build_model(config)
```

## Project Structure

```
dynamic_model_registry/
├── registry.py      # Core registry implementation
├── types.py         # Type definitions and enums
├── config.py        # Configuration models
├── models/          # Model implementations
├── embedders/       # Embedder implementations
├── splitters/       # Splitter implementations
└── bindings.py      # External bindings
```
