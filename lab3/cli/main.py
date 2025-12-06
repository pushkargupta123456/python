# cli/main.py
#!/usr/bin/env python3
"""
Command-line interface for Library Inventory Manager.
"""

import logging
import sys

from librarymanager.inventory import LibraryInventory
from librarymanager.book import Book

# Configure root logger to show messages in console
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("library_cli")

def print_menu():
    print("\n=== Library Inventory Manager ===")
    print("1. Add Book")
    print("2. Issue Book")
    print("3. Return Book")
    print("4. View All Books")
    print("5. Search by Title")
    print("6. Search by ISBN")
    print("7. Exit")

def read_non_empty(prompt: str) -> str:
    while True:
        try:
            v = input(prompt).strip()
        except EOFError:
            # In some editors terminal may send EOF — treat as empty and re-prompt
            v = ""
        if v:
            return v
        print("Input cannot be empty. Please try again.")

def main():
    inv = LibraryInventory()
    while True:
        try:
            print_menu()
            choice = input("Enter choice: ").strip()
            if choice == "1":
                title = read_non_empty("Title: ")
                author = read_non_empty("Author: ")
                isbn = read_non_empty("ISBN: ")
                ok = inv.add_book(Book(title=title, author=author, isbn=isbn))
                print("Book added successfully." if ok else "Book with that ISBN already exists.")
            elif choice == "2":
                isbn = read_non_empty("ISBN to issue: ")
                print("Book issued." if inv.issue_book(isbn) else "Cannot issue (not found or already issued).")
            elif choice == "3":
                isbn = read_non_empty("ISBN to return: ")
                print("Book returned." if inv.return_book(isbn) else "Cannot return (not found or not issued).")
            elif choice == "4":
                books = inv.display_all()
                if not books:
                    print("No books in the catalog.")
                else:
                    for b in books:
                        print(b)
            elif choice == "5":
                q = read_non_empty("Search title: ")
                results = inv.search_by_title(q)
                if not results:
                    print("No books matched that title.")
                else:
                    for r in results:
                        print(r)
            elif choice == "6":
                isbn = read_non_empty("Search ISBN: ")
                b = inv.search_by_isbn(isbn)
                print(b if b else "No book found with that ISBN.")
            elif choice == "7":
                print("Exiting. Goodbye!")
                break
            else:
                print("Invalid choice. Enter a number between 1 and 7.")
        except KeyboardInterrupt:
            print("\nInterrupted. Exiting.")
            break
        except Exception as exc:
            logger.exception("An unexpected error occurred: %s", exc)
            print("An unexpected error occurred. Check logs for details.")

if __name__ == "__main__":
    main()