
PHONE_BOOK_NAME      = 'phone_book.txt'
FIELDS_NAME = ('ID', 'Фамилия', 'Имя', 'Телефон', 'Описание')
SEPARATOR = ','

phone_book = []
__id = 0

class UserItem:

    def __init__(self, id: int, surname: str, name: str, phone: str, description: str = '') -> None:
        self.__id = id
        self.name = self.__normalize(name).capitalize()
        self.surname = self.__normalize(surname).capitalize()
        self.phone = self.__normalize(phone)
        self.description = self.__normalize(description)

    def __normalize(self, in_str: str) -> str:
        in_str = in_str.replace('/t','')
        in_str = in_str.replace('/n','')
        in_str = in_str.strip()
        return in_str

    def __str__(self) -> str:
        # return f'{ self.surname = } | { self.name = } | { self.phone = } | { self.description = }'
        # return f'{FIELDS_NAME[0]}: {self.__id} {self.__get_tabs(str(self.__id), 1)}| {FIELDS_NAME[1]}: {self.surname} {self.__get_tabs(self.surname)}| {FIELDS_NAME[2]}: {self.name} {self.__get_tabs(self.name)}| {FIELDS_NAME[3]}: {self.phone} {self.__get_tabs(self.phone, 1)}| {FIELDS_NAME[4]}: {self.description}'
        return f'{FIELDS_NAME[0]}: {self.__id} {self.__get_sps(str(self.__id), 6)}| {FIELDS_NAME[1]}: {self.surname} {self.__get_sps(self.surname, 20)}| {FIELDS_NAME[2]}: {self.name} {self.__get_sps(self.name)}| {FIELDS_NAME[3]}: {self.phone} {self.__get_sps(self.phone)}| {FIELDS_NAME[4]}: {self.description}'

    def __get_tabs(self, in_str: str, tabs_limit: int = 2) -> str:
        return '\t' * (tabs_limit - len(in_str) // 6)

    def __get_sps(self, in_str: str, spaces_amount: int = 10) -> str:
        return ' ' * (spaces_amount - len(in_str))

    def get_id(self) -> int:
        return self.__id

    def set_id(self, __id: int):
        self.__id = __id


def read_phone_book(filename): 
    ''' Читаем телефонный справочник из файла'''
    
    phone_book = []     # локальная
    global __id

    with open(filename, 'r', encoding='utf-8') as phb:

        for line in phb:

            record = line.split(SEPARATOR)

            for _ in range(len(record), len(FIELDS_NAME)-1):
                record.append('')
            
            print(record)

            person = UserItem(0, *record)

            if person.name or person.surname:
                __id += 1
                person.set_id(__id)
                phone_book.append(person)	

    return phone_book


def get_phone() -> str:
    ''' получаем номер телефона '''

    pattern = '0123456789()+-'
    digits_amount = 3

    is_phone_correct = True
    
    while is_phone_correct:
        
        phone = input('Введите номер абонента: ')
        digits = [digit for digit in phone if digit in pattern]
        
        if len(digits) >= digits_amount:
            is_phone_correct = False
        else:
            print(f'Номер телефона должен содержать символы {pattern} и быть не меньше {digits_amount} знаков!')
    
    return phone


def get_user_by_id(__id: int) -> UserItem | None:
    """ Возвращает абонента по ID """

    for person in phone_book:
        if __id == person.get_id():
            return person

    return

def output_phone_book(phone_book: list) -> None:
    ''' Вывод справочника'''
    
    print(*phone_book, sep='\n')    


#*******************************************************************
#********************* Реализация интерфейса ***********************
#*******************************************************************

def print_result():
    ''' Вывод телефонного справочника '''

    output_phone_book(phone_book)
#*******************************************************************

def find_by_surname(surname: str) -> None:
    ''' Поиск по фамилии '''

    find_items = [person for person in phone_book if surname.lower() in person.surname.lower()]
    output_phone_book(find_items)
#*******************************************************************

def find_by_phone(phone: str) -> None:
    ''' Поиск по номеру телефона '''

    find_items = [person for person in phone_book if phone in person.phone]
    output_phone_book(find_items)
#*******************************************************************

def add_user() -> None:
    ''' Добавление в справочник нового абонента '''

    global __id

    surname = input('Введите фамилию абонента: ')
    name = input('Введите имя абонента: ')
    
    phone = get_phone()

    description = input('Введите описание абонента: ')

    __id += 1
    person = UserItem(__id, surname, name, phone, description)
    phone_book.append(person)

    output_phone_book(phone_book)
#*******************************************************************

def change_user(__id: int) -> None:
    ''' Изменение абонента '''

    person = get_user_by_id(__id)
    if not person:
        print(f'Абонент с ID = {__id} не найден!')
        return

    print('Текущие данные абонента:')
    print(person, '\n')
    print('Новые данные абонента:')

    surname = input('Введите фамилию абонента: ')
    name = input('Введите имя абонента: ')
    
    phone = get_phone()

    description = input('Введите описание абонента: ')

    person.surname = surname if surname != '' else person.surname
    person.name = name if name != '' else person.name
    person.phone = phone if phone != '' else person.phone
    person.description = description if description != '' else person.description

    print('Данные успешно изменены!\n')

    output_phone_book(phone_book)
#*******************************************************************

def del_user(__id: int) -> None:
    ''' Удаление абонента '''

    person = get_user_by_id(__id)
    if not person:
        print(f'Абонент с ID = {__id} не найден!')
        return

    phone_book.remove(person)

    print('\nДанные успешно удалены!\n')

    output_phone_book(phone_book)
#*******************************************************************

def save_phone_book(file_name: str = '') -> None:
    ''' Сохранение в файл '''

    file_name = PHONE_BOOK_NAME if file_name == '' else file_name + '.txt'
    
    with open(file_name, 'w', encoding='utf-8') as phout:
        
        for person in phone_book:
            data = f'{person.surname}{SEPARATOR} {person.name}{SEPARATOR} {person.phone}{SEPARATOR} {person.description.replace(SEPARATOR, '')}\n'
            phout.write(data)

#*******************************************************************
#**************** Окончание реализации  интерфейса *****************
#*******************************************************************

def work_with_phonebook():
    ''' Вызов интерфейса '''

    choice = show_menu()

    while (choice != 9):
        
        match choice:
            case 1: 
                print_result()
            case 2: 
                surname_name = input('Введите фамилию Абонента: ')
                find_by_surname(surname_name)
            case 3: 
                phone = input('Введите номер телефона Абонента: ')
                find_by_phone(phone) 
            case 4: 
                add_user()                          
            case 5:
                user_id = int(input('Введите ID Абонента: '))
                change_user(user_id)
            case 6:
                user_id = int(input('Введите ID Абонента: '))
                del_user(user_id)
            case 7:
                save_phone_book()
            case 8:
                file_name = input('Введите имя файла телефонной книги: ')
                save_phone_book(file_name)                                        

        choice = show_menu()


def show_menu():
    ''' Вывод интерфейса '''

    print('\nВыберите необходимое действие:\n',
          '1. Отобразить весь справочник\n',
          '2. Найти абонента по фамилии\n',
          '3. Найти абонента по номеру телефона\n',
          '4. Добавить абонента в справочник\n',
		  '5. Изменить данные абонента\n',
          '6. Удалить абонента\n',
          '7. Сохранить справочник в текстовом формате\n',
          '8. Сохранить справочник в текстовом формате в другой файл\n',
          '9. Закончить работу (выход без сохранения)\n')

    choice = int(input('Сделайте Ваш выбор: '))
    
    return choice


phone_book = read_phone_book(PHONE_BOOK_NAME)

work_with_phonebook()
