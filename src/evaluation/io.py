"""JSONL and artifact IO helpers for RAG evaluation."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


def ensure_parent(path: str | Path) -> Path:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    return target


def read_jsonl(path: str | Path, model: type[T] | None = None) -> list[T] | list[dict]:
    target = Path(path)
    if not target.exists():
        return []

    records = []
    with target.open("r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            data = json.loads(line)
            records.append(model.model_validate(data) if model else data)
    return records


def append_jsonl(path: str | Path, records: Iterable[BaseModel | dict]) -> None:
    target = ensure_parent(path)
    with target.open("a", encoding="utf-8") as file:
        for record in records:
            if isinstance(record, BaseModel):
                data = record.model_dump(mode="json")
            else:
                data = record
            file.write(json.dumps(data, ensure_ascii=False) + "\n")


def write_jsonl(path: str | Path, records: Iterable[BaseModel | dict]) -> None:
    target = ensure_parent(path)
    tmp = target.with_suffix(target.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8") as file:
        for record in records:
            if isinstance(record, BaseModel):
                data = record.model_dump(mode="json")
            else:
                data = record
            file.write(json.dumps(data, ensure_ascii=False) + "\n")
    tmp.replace(target)


def load_existing_ids(path: str | Path, id_field: str = "id") -> set[str]:
    ids = set()
    for record in read_jsonl(path):
        value = record.get(id_field)
        if value:
            ids.add(str(value))
    return ids


def write_failed_record(output_dir: str | Path, step: str, record: dict, error: str) -> None:
    failed_path = Path(output_dir) / "failed" / f"{step}.jsonl"
    append_jsonl(failed_path, [{"record": record, "error": error}])


def save_raw_response(raw_dir: str | Path, step: str, record_id: str, response: str) -> None:
    target = Path(raw_dir) / step / f"{record_id}.json"
    ensure_parent(target)
    with target.open("w", encoding="utf-8") as file:
        json.dump({"response": response}, file, ensure_ascii=False, indent=2)
