import sqladmin
from pathlib import Path

print(Path(sqladmin.__file__).parent / "templates")

