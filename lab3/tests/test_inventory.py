
# tests/test_inventory.py
from library_manager.inventory import LibraryInventory
from library_manager.book import Book

def test_add_and_search(tmp_path):
    fp = tmp_path / "books.json"
    inv = LibraryInventory(file_path=str(fp))
    b = Book("My Book", "Me", "111")
    assert inv.add_book(b) is True
    assert inv.search_by_isbn("111").title == "My Book"
    # duplicate ISBN not added
    assert inv.add_book(Book("Other","You","111")) is False

def test_issue_and_return(tmp_path):
    fp = tmp_path / "books2.json"
    inv = LibraryInventory(file_path=str(fp))
    inv.add_book(Book("Test", "Author", "222"))
    assert inv.issue_book("222") is True
    assert inv.issue_book("222") is False  # already issued
    assert inv.return_book("222") is True
    assert inv.return_book("222") is False  # already returned