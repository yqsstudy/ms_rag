import json
from pathlib import Path
from typing import Dict, Optional


class DocumentStore:
    def __init__(self, persist_directory: str = "./data/docstore"):
        self.persist_directory = Path(persist_directory)
        self.persist_directory.mkdir(parents=True, exist_ok=True)
        self.store_path = self.persist_directory / "doc_store.json"
        self.store: Dict[str, dict] = self._load()

    def _load(self) -> Dict[str, dict]:
        if self.store_path.exists():
            try:
                with open(self.store_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {}
        return {}

    def _save(self) -> None:
        with open(self.store_path, "w", encoding="utf-8") as f:
            json.dump(self.store, f, ensure_ascii=False, indent=2)

    def add_documents(self, docs: Dict[str, dict]) -> None:
        self.store.update(docs)
        self._save()

    def get_document(self, doc_id: str) -> Optional[dict]:
        return self.store.get(doc_id)

    def delete_documents(self, doc_ids: list[str]) -> None:
        changed = False
        for doc_id in doc_ids:
            if doc_id in self.store:
                del self.store[doc_id]
                changed = True
        if changed:
            self._save()

    def delete_all(self) -> None:
        self.store = {}
        self._save()

    def count(self) -> int:
        return len(self.store)
