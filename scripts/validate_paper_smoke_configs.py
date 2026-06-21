"""Validate core paper China A-share smoke reproduction configs."""

from __future__ import annotations

import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "paper_id",
    "model",
    "task",
    "market",
    "universe_config",
    "split_config",
    "data",
    "upstream",
    "first_target",
    "blocked_by",
]
CONFIGS = [
    PROJECT_ROOT / "paper_projects" / "2021_tra_lin" / "configs" / "china_a_share_smoke.json",
    PROJECT_ROOT / "paper_projects" / "2024_master_li" / "configs" / "china_a_share_smoke.json",
    PROJECT_ROOT / "paper_projects" / "2023_doubleadapt_zhao" / "configs" / "china_a_share_smoke.json",
    PROJECT_ROOT / "paper_projects" / "2021_tcts_wu" / "configs" / "china_a_share_smoke.json",
]


def resolve_repo_path(path: str) -> Path:
    return PROJECT_ROOT.parent / path


def validate_config(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as file:
        config = json.load(file)
    missing = [field for field in REQUIRED if field not in config]
    if missing:
        raise RuntimeError(f"{path} missing fields: {missing}")
    for ref_field in ["universe_config", "split_config"]:
        ref_path = resolve_repo_path(config[ref_field])
        if not ref_path.exists():
            raise RuntimeError(f"{path} missing {ref_field}: {ref_path}")
    data = config["data"]
    for data_field in ["panel", "qlib_provider_uri"]:
        data_path = resolve_repo_path(data[data_field])
        if not data_path.exists():
            raise RuntimeError(f"{path} missing data.{data_field}: {data_path}")
    for label_name, label_path in data["labels"].items():
        resolved = resolve_repo_path(label_path)
        if not resolved.exists():
            raise RuntimeError(f"{path} missing label {label_name}: {resolved}")
    upstream_repo = resolve_repo_path(config["upstream"]["repo"])
    if not upstream_repo.exists():
        raise RuntimeError(f"{path} missing upstream repo: {upstream_repo}")
    return config


def main() -> int:
    for path in CONFIGS:
        config = validate_config(path)
        print(f"ok paper_id={config['paper_id']} model={config['model']} config={path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
