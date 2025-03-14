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
uvsh() {
    local venv_name=${1:-'.venv'}
    venv_name=${venv_name//\//} # remove trailing slashes (Linux)
    venv_name=${venv_name//\\/} # remove trailing slashes (Windows)

    local venv_bin=
    if [[ -d ${WINDIR} ]]; then
        venv_bin='Scripts/activate'
    else
        venv_bin='bin/activate'
    fi

    local activator="${venv_name}/${venv_bin}"
    echo "[INFO] Activate Python venv: ${venv_name} (via ${activator})"

    if [[ ! -f ${activator} ]]; then
        echo "[ERROR] Python venv not found: ${venv_name}"
        return
    fi

    # shellcheck disable=SC1090
    . "${activator}"
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