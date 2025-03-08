# Create environment
```bash
# install uv:
curl -LsSf https://astral.sh/uv/install.sh | sh
# or 
brew install uv

# setting up uv for the first time
uv init

# create venv and sync dependencies
uv sync

uv venv

uv add <pkg>
uv add --dev <pkg>

source .venv/bin/activate
deactivate
```

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