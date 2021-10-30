# По ТЗ требуется рандом, значит рандом
from random import randint

import heapq

# Класс узла
class Node:
    def __init__(self, char, freq):
        # Символ
        self.char = char
        # Частота, с которой он встречается
        self.frequency = freq
        # Ссылка на левую часть дерева
        self.left = None
        # Ссылка на правую часть дерева
        self.right = None

    # Методы сравнения (для кучи)
    def __cmp__(self, other):
        if other is None:
            return -1
        if not isinstance(other, Node):
            return -1
        return self.frequency >= other.frequency

    def __lt__(self, other):
        return self.frequency < other.frequency

# Класс, который реализует кодирование по Хаффману
class HuffmanCoding:
    def __init__(self, use_same_freq=False, use_block=False):
        self.heap = []
        self.codes = {}
        self.reverse_mapping = {}

        # Флаг, означающий, что кодирование Хаффмана нужно проводить
        # с равновероятной встрече букв
        self.use_same_freq = use_same_freq

        # Согласно задаче, также применить блочное кодирование
        # Данный флаг отвечает как раз за эту задачу
        self.use_block = use_block

    # Данная функция генерирует словарь частот
    def generate_frequency(self, text):
        # Словарь с нашими частотами
        frequency = {}
        for symbol in text:
            # В этом месте используем равновероятное кодирование
            if self.use_same_freq:
                frequency[symbol] = 50
            else:
                # Если символа в данном словаре нету, то тогда добавляем его
                if not symbol in frequency:
                    frequency[symbol] = 0
                frequency[symbol] += 1
        return frequency

    # Метод, который генерирует кучу на основе данных частот с текста
    def make_heap(self, frequency):
        # Проходимся по словарю
        for key in frequency:
            # Формируем объект узла
            node = Node(key, frequency[key])

            # Добавляем в кучу наши данные
            heapq.heappush(self.heap, node)

    # Метод, который объединяет наши словарь
    def merge_nodes(self):
        # Проходимся по циклу, пока имеются данные
        while len(self.heap) > 1:
            # Удаляем последние данные
            node1 = heapq.heappop(self.heap)
            node2 = heapq.heappop(self.heap)

            # Объединяем данные в класс Node
            merging_data = Node(None, node1.frequency + node2.frequency)

            # Вставляем ссылку на левую и правую части
            merging_data.left = node1
            merging_data.right = node2

            # Добавляем в кучу
            heapq.heappush(self.heap, merging_data)

    # Метод, который осуществляет вставку "0" и "1"
    def make_codes_helper(self, root, current_code):
        # Если дерево пусто, то делать нечего :(
        if root is None:
            return

        # В противном случае, для статистики запомиинаем для каждого символа(-ов) последовательность 0 и 1
        if root.char is not None:
            self.codes[root.char] = current_code
            # Записывааем в словарь ключ - код и значение - символ
            self.reverse_mapping[current_code] = root.char
            return

        # Рекурсивно проходимся по левой и правой части
        self.make_codes_helper(root.left, current_code + "0")
        self.make_codes_helper(root.right, current_code + "1")

    # Метод, который генерирует код из нашего текста
    def make_code(self):
        # Извлекаем последний текст
        root = heapq.heappop(self.heap)
        current_code = ""
        self.make_codes_helper(root, current_code)

    # Возвращает в удобном для пользователя виде текст
    def get_encoded_text(self, text):
        return ''.join([str(self.codes[symbol]) for symbol in text])

    # Мозг программы - кодирование по Хаффману
    def compress(self, data):
        # Удаляем лишние пробельные символы справа
        text = data.rstrip()

        if self.use_block:
            # По заданию дано 2 блока, поэтому делаем по 2 блока
            count_symbols_in_block = 2
            text = [text[i: i + count_symbols_in_block] for i in range(0, len(text), count_symbols_in_block)]

        # Генерируем словарь с нашими частотами
        frequency = self.generate_frequency(text)

        # Делаем на этой основе кучу
        self.make_heap(frequency)
        # Объединяем в одно целое
        self.merge_nodes()
        # Создаём коды
        self.make_code()

        # Возвращаем закодированный текст
        return self.get_encoded_text(text)

    # Обратная операция - осуществлятем декомпрессию данных
    def decompress(self, encoded_text):
        # Переменная, которая проверяет, есть ли код в данном тексте
        current_code = ""
        # Декодированный текст
        decoded_text = ""

        # Каждый бит записываем и проверяем в map-е
        for number in encoded_text:
            current_code += number
            if current_code in self.reverse_mapping:
                character = self.reverse_mapping[current_code]
                # Записываем в наш декомпрессивный текст
                decoded_text += character

                # Если символ по данному коду был найден, то мы сбрасываем текущий код для того чтобы
                # дальше найти символы по коду
                current_code = ""

        return decoded_text

# Функция, осуществляющая "порчу данных" - инверсия бинарных значений с определённой вероятностью
def make_worse_data(binary_data, probability):
    worse_binary_data = str()

    for bit in binary_data:
        if probability > randint(0, 100):
            worse_binary_data += "0" if bit == "1" else "1"
        else:
            worse_binary_data += bit

    return worse_binary_data


def main(use_worse_data=False):
    # Чтение данных осуществляется из файла (при необходимости заменить файл text_2 на text)
    with open('../files/2/text.txt', 'r') as f:
        data = f.read()

    print("Данные из файла получены")

    # Кодируем данные
    h = HuffmanCoding(use_same_freq=False, use_block=True)

    # Применяем метод компрессии данных
    binary_data = h.compress(data)

    # Записывааем данные в файл
    with open('../files/2/decode.txt', 'w') as f:
        f.write(binary_data)

    print("Закодированный текст по Хаффману успешно записан в файл")

    # Осуществляем "порчу данных". Инвертируем значения с определённой вероятностью (задаётся параметром)
    if use_worse_data:
        worse_binary_data = make_worse_data(binary_data, probability=8)
        # Записываем в файл испорченные данные
        with open('../files/2/decode_worse.txt', 'w') as f:
            f.write(worse_binary_data)

        # Наши данные теперь испорченные
        binary_data = worse_binary_data

    # Применяем метод декомпрессии данных
    decoded_text = h.decompress(binary_data)

    # Записываем декодированный текст в файл output
    with open('../files/2/output.txt', 'w') as f:
        f.write(decoded_text)

    print("Декодированный файл успешно записан")

    print(f"\nДлина бинарных символов: {len(binary_data)}")
    print(f"Количество символов '0': {binary_data.count('0')}, '1': {binary_data.count('1')}")

    length = 0
    for code in h.codes.values():
        length += len(code)

    print(f"Средняя длина символов: {length / len(h.codes)}\n")

if __name__ == "__main__":
    main(use_worse_data=False)