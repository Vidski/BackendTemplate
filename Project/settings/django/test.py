import os
import sys
from pathlib import Path


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR: str = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, os.path.join(BASE_DIR, "Apps"))

print(BASE_DIR)
print(os.path.join(BASE_DIR, "Apps"))
print(os.path.join(BASE_DIR, "Apps/Static"))
print(sys.path)
