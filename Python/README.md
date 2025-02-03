# Create environment
```bash
python -m venv "$(basename $PWD)"
source venv/bin/activate

pip install -r requirements.txt
pip freeze
```