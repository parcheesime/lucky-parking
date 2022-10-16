#!/usr/bin/env conda run -n citation-analysis python
import click
from pathlib import Path
import glob
import os
from make_dataset import clean, create_sample
# Load project directory
PROJECT_DIR = Path(__file__).resolve().parents[2]
NEW_PATH= PROJECT_DIR / "data" / "raw"
os.chdir(NEW_PATH)
@click.command()
@click.argument("frac", type=click.FLOAT)
def main(frac: float):
    """Creates sample from "frac" and outputs geojson file
    """
    try:
        # Load newest raw data file
        newest_file = max(list(Path().glob('*.csv')), key=os.path.getctime)
        print(type(newest_file))
        clean(
            create_sample(newest_file,"data/interim", frac),
            "data/processed",
            geojson=True,
        )
    except:
        print('No raw data. Try make data.')
if __name__ == "__main__":
    main()