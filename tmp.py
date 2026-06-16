from pathlib import Path

import sqladmin

print(Path(sqladmin.__file__).parent / "templates")

