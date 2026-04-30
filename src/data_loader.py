"""
Minimal Data Loader
===================
Only downloads Kaggle datasets defined in `DATASETS` to `data_dir`.
Requires `KAGGLE_USERNAME` and `KAGGLE_KEY` in environment (e.g. via .env).
"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


class DataLoader:
    """Minimal downloader: only handles authentication and dataset download."""

    DATASETS = {
        "fda_drug_labels": {
            "kaggle_id": "jefflin97/fda-guidelines-data",
            "local_path": "fda_drug_labels",
        },
        "fda_approved_drugs": {
            "kaggle_id": "thedevastator/fda-approved-drugs-therapeutics",
            "local_path": "fda_approved_drugs",
        },
    }

    def __init__(self, data_dir: str = "./data/raw"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self._validate_kaggle_credentials()

    def _validate_kaggle_credentials(self) -> bool:
        user = os.getenv("KAGGLE_USERNAME")
        key = os.getenv("KAGGLE_KEY")
        if not user or not key:
            raise EnvironmentError(
                "Kaggle credentials not found. Please set KAGGLE_USERNAME and KAGGLE_KEY in .env"
            )

        try:
            from kaggle.api.kaggle_api_extended import KaggleApi

            api = KaggleApi()
            api.authenticate()
            print("✓ Kaggle credentials validated")
            return True
        except Exception as e:
            print(f"Could not validate Kaggle credentials: {e}")
            return False

    def download_dataset(self, dataset_key: str, force: bool = False) -> Path:
        if dataset_key not in self.DATASETS:
            raise ValueError(f"Unknown dataset: {dataset_key}")

        info = self.DATASETS[dataset_key]
        local_path = self.data_dir / info["local_path"]

        if local_path.exists() and not force:
            print(f"✓ Dataset '{dataset_key}' already exists at {local_path}")
            return local_path

        local_path.mkdir(parents=True, exist_ok=True)
        print(f"Downloading '{dataset_key}' to {local_path}...")

        try:
            from kaggle.api.kaggle_api_extended import KaggleApi

            api = KaggleApi()
            api.authenticate()
            api.dataset_download_files(info["kaggle_id"], path=str(local_path), unzip=True)

            print(f"✓ Successfully downloaded {dataset_key} to {local_path}")
            return local_path
        except Exception as e:
            print(f"✗ Failed to download {dataset_key}: {e}")
            raise

    def download_all_datasets(self, force: bool = False) -> None:
        for key in self.DATASETS.keys():
            try:
                self.download_dataset(key, force=force)
            except Exception as e:
                print(f"Failed: {key}: {e}")


if __name__ == "__main__":
    import sys

    loader = DataLoader(data_dir="./data/raw")

    if len(sys.argv) > 1:
        # accept multiple dataset keys
        for arg in sys.argv[1:]:
            loader.download_dataset(arg)
    else:
        loader.download_all_datasets()