import pathlib
import sys

# Add project root to sys.path so "from app.main import app" works in tests
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
