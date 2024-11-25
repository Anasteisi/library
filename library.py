class Book:
    def __init__(self, book_id, title, author, year, status="в наличии"):  # книга
        self.id = book_id
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def __str__(self):  # строка библиотеки
        return f"ID: {self.id}, Title: {self.title}, Author: {self.author}, Year: {self.year}, Status: {self.status}"

class Library:
    def __init__(self, filename):  # библиотека
        self.filename = filename
        self.books = []
        self.load_books()

    def load_books(self):  # загрузка из файла
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                for line in file:
                    book_data = line.strip().split(';')
                    if len(book_data) == 5:
                        try:
                            book_id = int(book_data[0])
                            title = book_data[1]
                            author = book_data[2]
                            year = int(book_data[3])
                            status = book_data[4]
                            self.books.append(Book(book_id, title, author, year, status))
                        except ValueError:
                            print(f"Ошибка: данные некорректны: {line.strip()}")
        except FileNotFoundError:
            print(f"Файл '{self.filename}' не найден. Он будет создан при добавлении первой книги.")
        except Exception as e:  # другие ошибки
            print(f"Ошибка при загрузке из файла: {e}")

    def save_books(self): # запись в файл
        try:
            with open(self.filename, 'w', encoding='utf-8') as file:
                for book in self.books:
                    file.write(f"{book.id};{book.title};{book.author};{book.year};{book.status}\n")
        except Exception as e:
            print(f"Ошибка при записи в файл: {e}")

    def add_book(self, title, author, year): 
        new_id = max([book.id for book in self.books], default=0) + 1
        new_book = Book(new_id, title, author, year)
        self.books.append(new_book)
        self.save_books()
        print(f"Книга добавлена.")

    def remove_book(self, book_id):
        for book in self.books:
            if book.id == book_id:
                self.books.remove(book)
                self.save_books()
                print(f"Книга удалена.")
                return
        print(f"Ошибка: книга не найдена.")

    def search_books(self, request):
        results = []
        for book in self.books:
            if (request.lower() in book.title.lower() or 
                request.lower() in book.author.lower() or 
                (request.isdigit() and request == str(book.year))):
                results.append(book)
        return results

    def display_books(self):
        if not self.books:
            print("Библиотека пуста.")
            return
        for book in self.books:
            print(book)

    def change_status(self, book_id, new_status):
        if new_status not in ["в наличии", "выдана"]:
            print("Ошибка: неверный статус.")
            return
        for book in self.books:
            if book.id == book_id:
                book.status = new_status
                self.save_books()
                print(f"Статус книги изменен на '{new_status}'.")
                return

def input_int(number): # целое число
    while True:
        try:
            return int(input(number))
        except ValueError:
            print("Ошибка: введите целое число.")

def main():
    library = Library('library.txt')

    while True:
        print("\nДоступные команды:")
        print("1. Добавить книгу.")
        print("2. Удалить книгу по ID.")
        print("3. Найти книгу по названию, автору или году.")
        print("4. Отобразить все книги библиотеки.")
        print("5. Изменить статус книги по её ID.")
        print("6. Выход.\n")

        digit = input("Выберите команду: ")

        if digit == '1':
            title = input("Введите название: ")
            author = input("Введите автора: ")
            year = input_int("Введите год издания: ")
            if year > 2024:  # год не больше текущего
                print("Ошибка: неверный год")
                continue
            library.add_book(title, author, year)

        elif digit == '2':
            book_id = input_int("Введите ID: ")
            library.remove_book(book_id)

        elif digit == '3':
            request = input("Введите название, автора или год: ")
            results = library.search_books(request)
            if results:
                for book in results:
                    print(f"{book}")
            else:
                print("Книги не найдены.")

        elif digit == '4':
            library.display_books()

        elif digit == '5':
            book_id = input_int("Введите ID: ")
            for book in library.books:
                if book.id == book_id:
                    new_status = input("Введите новый статус: ")
                    library.change_status(book_id, new_status)
                    break
            else:
                print("Ошибка: книга не найдена.")

        elif digit == '6':
            print("Выход.")
            break

        else:
            print("Ошибка: неверная команда.")

if __name__ == "__main__":
    main()