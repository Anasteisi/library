import unittest
from io import StringIO
import sys
from library import Library, Book

class TestLibrary(unittest.TestCase):
    def setUp(self):
        self.library = Library('test_library.txt')
        self.library.books = []

    def tearDown(self):
        import os
        if os.path.exists('test_library.txt'):
            os.remove('test_library.txt')

    def test_add_book(self):
        self.library.add_book("Test Book", "Test Author", 2022)
        self.assertEqual(len(self.library.books), 1)
        self.assertEqual(self.library.books[0].title, "Test Book")
        self.assertEqual(self.library.books[0].author, "Test Author")
        self.assertEqual(self.library.books[0].year, 2022)

    def test_remove_book(self):
        self.library.add_book("Test Book", "Test Author", 2022)
        self.library.remove_book(1)
        self.assertEqual(len(self.library.books), 0)

    def test_remove_nonexistent_book(self):
        initial_length = len(self.library.books)
        self.library.remove_book(999)
        self.assertEqual(len(self.library.books), initial_length)

    def test_search_books(self):
        self.library.add_book("Test Book", "Test Author", 2022)
        results = self.library.search_books("Test")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Test Book")

    def test_search_nonexistent_book(self):
        self.library.add_book("Test Book", "Test Author", 2022)
        results = self.library.search_books("Nonexistent")
        self.assertEqual(len(results), 0)

    def test_change_status(self):
        self.library.add_book("Test Book", "Test Author", 2022)
        self.library.change_status(1, "выдана")
        self.assertEqual(self.library.books[0].status, "выдана")

    def test_invalid_status_change(self):
        self.library.add_book("Test Book", "Test Author", 2022)
        self.library.change_status(1, "недоступен")
        self.assertEqual(self.library.books[0].status, "в наличии")

    def test_load_books(self):
        with open('test_library.txt', 'w', encoding='utf-8') as f:
            f.write("1;Test Book;Test Author;2022;в наличии\n")
        self.library.load_books()
        self.assertEqual(len(self.library.books), 1)
        self.assertEqual(self.library.books[0].title, "Test Book")

    def test_save_books(self):
        self.library.add_book("Test Book", "Test Author", 2022)
        self.library.save_books()
        with open('test_library.txt', 'r', encoding='utf-8') as f:
            content = f.read()
        self.assertIn("Test Book", content)

if __name__ == '__main__':
    unittest.main()