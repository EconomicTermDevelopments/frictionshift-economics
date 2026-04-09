"""Script to generate synthetic data for Frictionshift analysis."""
import sys
from pathlib import Path
import pandas as pd

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / 'scripts'
sys.path.insert(0, str(SCRIPTS_DIR))

from phase2_upgrade_selected import generate_data  # noqa: E402

df = generate_data('frictionshift', 20260322)
output = Path(__file__).resolve().parent / 'frictionshift_dataset.csv'
df.to_csv(output, index=False)
print('Generated', output.name, 'with', len(df), 'rows')
