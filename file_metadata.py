# file_metadata.py

from __future__ import annotations

import json
import hashlib
from datetime import datetime, UTC
from pathlib import Path
from typing import Any


class FileMetadataStore:
    """
    Менеджер метаданих файлів.

    Структура:
        data/
            file1.dbf
            file2.dbf
            .metadata.json
    """

    META_FILENAME = ".metadata.json"

    def __init__(self, directory: str | Path):
        self.directory = Path(directory)
        self.meta_path = self.directory / self.META_FILENAME

    # =========================
    # Public API
    # =========================

    def get(self, filename: str) -> dict[str, Any] | None:
        data = self._load()
        return data.get(filename)

    def exists(self, filename: str) -> bool:
        data = self._load()
        return filename in data

    def set_status(
        self,
        filename: str,
        status: str,
        **extra: Any,
    ) -> None:
        data = self._load()

        entry = data.setdefault(filename, {})

        entry["status"] = status
        entry["updated_at"] = self._now()

        for key, value in extra.items():
            entry[key] = value

        self._save(data)

    def update_file_info(self, filename: str) -> None:
        """
        Оновлює базову інформацію про файл:
        - size
        - mtime
        - sha256
        """

        path = self.directory / filename

        if not path.exists():
            raise FileNotFoundError(path)

        data = self._load()

        entry = data.setdefault(filename, {})

        stat = path.stat()

        entry["size"] = stat.st_size
        entry["mtime"] = stat.st_mtime
        entry["sha256"] = self._sha256(path)
        entry["updated_at"] = self._now()

        self._save(data)

    def remove(self, filename: str) -> None:
        data = self._load()

        if filename in data:
            del data[filename]

        self._save(data)

    def list_all(self) -> dict[str, dict[str, Any]]:
        return self._load()

    def get_by_status(self, status: str) -> list[str]:
        data = self._load()

        return [
            filename
            for filename, meta in data.items()
            if meta.get("status") == status
        ]

    def is_file_changed(self, filename: str) -> bool:
        """
        Перевіряє чи змінився файл
        за size + mtime.
        """

        path = self.directory / filename

        if not path.exists():
            return True

        meta = self.get(filename)

        if not meta:
            return True

        stat = path.stat()

        return (
            meta.get("size") != stat.st_size
            or meta.get("mtime") != stat.st_mtime
        )

    # =========================
    # Internal
    # =========================

    def _load(self) -> dict[str, Any]:
        if not self.meta_path.exists():
            return {}

        with open(self.meta_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save(self, data: dict[str, Any]) -> None:
        self.directory.mkdir(parents=True, exist_ok=True)

        tmp_path = self.meta_path.with_suffix(".tmp")

        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(
                data,
                f,
                indent=2,
                ensure_ascii=False,
                sort_keys=True,
            )

        tmp_path.replace(self.meta_path)

    @staticmethod
    def _sha256(path: Path) -> str:
        h = hashlib.sha256()

        with open(path, "rb") as f:
            while chunk := f.read(1024 * 1024):
                h.update(chunk)

        return h.hexdigest()

    @staticmethod
    def _now() -> str:
        return datetime.now(UTC).isoformat()


if __name__ == "__main__":
    store = FileMetadataStore("data")

    store.set_status(
        "report1.dbf",
        "processing",
    )

    store.update_file_info("report1.dbf")

    store.set_status(
        "report1.dbf",
        "processed",
        rows=1523,
        errors=[],
    )

    print(store.get("report1.dbf"))

    print(store.get_by_status("processed"))