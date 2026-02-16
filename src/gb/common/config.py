from pathlib import Path
import os

ROOT_DIR = Path(__file__).resolve().parents[3]
SCRIPTS_DIR = ROOT_DIR / 'scripts'
REPORTS_DIR = ROOT_DIR / 'reports'
DOCS_DIR = ROOT_DIR / 'docs'
DATA_DIR = ROOT_DIR / 'data'
BACKUPS_DIR = DATA_DIR / 'backups'
DEFAULT_DB_PATH = ROOT_DIR / os.environ.get('BRUETER_DB', 'brueter.sqlite')
