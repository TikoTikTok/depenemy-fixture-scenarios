import sys
from pathlib import Path

# Make depenemy importable from the installed package or the local dev install
sys.path.insert(0, str(Path(__file__).parent.parent))
