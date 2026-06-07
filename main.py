from app.ui import run
from app.config import asset

path = asset("config.toml")
print(path)

run()
