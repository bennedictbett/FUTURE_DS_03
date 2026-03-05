import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s')

project_name = "funnel_analysis"

list_of_files = [

    # GitHub Actions
    ".github/workflows/.gitkeep",

    # Source package
    f"src/{project_name}/__init__.py",
    "src/__init__.py",

    # Core scripts (run in order)
    "src/load_clean.py",
    "src/funnel_metrics.py",
    "src/channel_analysis.py",
    "src/export_for_powerbi.py",

    
    "notebooks/01_data_exploration.ipynb",

    
    "data/raw/.gitkeep",
    "data/processed/.gitkeep",

    
    "powerbi/.gitkeep",

    
    "reports/figures/.gitkeep",
    "reports/summary.md",

    
    "config.yaml",
    "requirements.txt",
    "setup.py",
    "README.md",
    ".gitignore",
]

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)

    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory: {filedir} for the file: {filename}")

    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass
        logging.info(f"Creating empty file: {filepath}")
    else:
        logging.info(f"{filename} already exists")

logging.info("Funnel Analysis project structure created successfully!")