# library_manager/inventory.py
import json
import logging
from pathlib import Path
from typing import List, Optional

from .book import Book

logger = logging.getLogger(__name__)

class LibraryInventory:
    def __init__(self, file_path: str = "data/books.json"):
        self.file_path = Path(file_path)
        self.books: List[Book] = []
        self._ensure_data_dir()
        self.load_data()

    def _ensure_data_dir(self):
        if not self.file_path.parent.exists():
            self.file_path.parent.mkdir(parents=True, exist_ok=True)

    def load_data(self):
        """Load books from JSON. If missing create empty file. If corrupted rename and start fresh."""
        try:
            if not self.file_path.exists():
                # Create an empty JSON file
                self.save_data()
                return

            with self.file_path.open("r", encoding="utf-8") as f:
                data = json.load(f)

            # Expecting a list of dicts
            self.books = [Book.from_dict(item) for item in data if isinstance(item, dict)]
            logger.info("Loaded %d books from %s", len(self.books), self.file_path)
        except json.JSONDecodeError:
            logger.error("books.json is corrupted. Renaming and starting fresh.")
            corrupted = self.file_path.with_suffix(".corrupted.json")
            try:
                self.file_path.replace(corrupted)
                logger.info("Renamed corrupted file to %s", corrupted)
            except Exception:
                logger.exception("Failed to rename corrupted file.")
            self.books = []
            self.save_data()
        except Exception as exc:
            logger.exception("Unexpected error while loading data: %s", exc)
            self.books = []

    def save_data(self):
        """Write current catalog to JSON."""
        try:
            with self.file_path.open("w", encoding="utf-8") as f:
                json.dump([b.to_dict() for b in self.books], f, indent=4, ensure_ascii=False)
            logger.info("Saved %d books to %s", len(self.books), self.file_path)
        except Exception as exc:
            logger.exception("Failed to save data: %s", exc)
            raise

    def add_book(self, book: Book) -> bool:
        """Add book if ISBN not already present. Returns True if added."""
        if self.search_by_isbn(book.isbn) is not None:
            logger.info("Cannot add book; ISBN %s already exists.", book.isbn)
            return False
        self.books.append(book)
        self.save_data()
        return True

    def search_by_title(self, query: str) -> List[Book]:
        q = query.strip().lower()
        return [b for b in self.books if q in b.title.lower()]

    def search_by_isbn(self, isbn: str) -> Optional[Book]:
        isbn = isbn.strip()
        for b in self.books:
            if b.isbn == isbn:
                return b
        return None

    def display_all(self) -> List[Book]:
        return list(self.books)

    def issue_book(self, isbn: str) -> bool:
        book = self.search_by_isbn(isbn)
        if book and book.issue():
            self.save_data()
            return True
        return False

    def return_book(self, isbn: str) -> bool:
        book = self.search_by_isbn(isbn)
        if book and book.return_book():
            self.save_data()
            return True
        return False