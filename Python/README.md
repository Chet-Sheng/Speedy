# Create environment
```bash
# install uv:
curl -LsSf https://astral.sh/uv/install.sh | sh
# or 
brew install uv

# setting up uv for the first time
uv init

# create venv and sync dependencies
uv sync --all-extras

uv venv

uv add <pkg>
uv add --dev <pkg>

source .venv/bin/activate
deactivate


# python kernel path:
./Python/.venv/bin/python

# creating ipykernel:
uv run ipython kernel install --user --env VIRTUAL_ENV $(pwd)/.venv --name=speedy_python
```

## Misc
Suggests adding below functons to `~/.zshrc`
```bash
# Function definition - takes an optional argument
uvsh() {
    # Set venv_name to the first argument ($1) if provided, otherwise use '.venv'
    # ${1:-'.venv'} means "use $1 if it exists, otherwise use '.venv'"
    local venv_name=${1:-'.venv'}
    
    # Construct the full path to the activate script
    # On Mac, virtual environments always use bin/activate
    local activator="${venv_name}/bin/activate"
    
    # Check if the activate script exists
    # [[ ! -f ${activator} ]] tests if the file does NOT exist
    if [[ ! -f ${activator} ]]; then
        # If file doesn't exist, print error and exit function
        echo "[ERROR] Python venv not found: ${venv_name}"
        return
    fi
    
    # Print informative message about which venv is being activated
    echo "[INFO] Activating Python venv: ${venv_name}"
    
    # Source (activate) the virtual environment
    # source is equivalent to . (dot) in shell scripts
    source "${activator}"
}
```

### VSCode trick to select all keys
You can use VS Code’s regex Find feature to select all keys. For example:
1. Open the `.env` file.
2. Press Cmd+F to open the search bar.
3. Enable regex search by clicking the .* icon.
4. Enter this regex pattern to match keys (assuming keys are at the start of a line before the equals sign):
    ```bash
    ^\s*([A-Za-z0-9_]+)\s*=
    ```
5. Click the "Select All Matches" button (or press `Cmd+Shift+L`) to create multi-cursors on all matched keys.
Now you can modify them as needed.