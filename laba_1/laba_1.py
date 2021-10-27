# Вспомогательный класс, который содержит описание узла
class Node:
    def __init__(self, prob, symbol, left=None, right=None):
        # Частота встречи данного символа
        self.prob = prob

        # Наш символ
        self.symbol = symbol

        # Ссылка на левую часть
        self.left = left

        # Ссылка на правую часть
        self.right = right

        # Числовое описание (0/1)
        self.code = ''

# Класс Хаффмана
class Haffman_Algorithm:
    def __init__(self):
        # Словарь, где будем хранить наши ноды
        self.codes = dict()


    def calc_code(self, node, val=''):
        # Для каждой конкретного узла мы считаем его код Хаффмана
        newVal = val + str(node.code)

        # Действуем по принципу рекурсии
        if node.left:
            self.calc_code(node.left, newVal)
        if node.right:
            self.calc_code(node.right, newVal)

        # Если ноды слева и справа не существует, то мы дошли до конца и записываем значение
        if not node.left and not node.right:
            self.codes[node.symbol] = newVal
            
        return self.codes        

    # Вспомогательная ф-ция, высчитывающая частоту встречи (возвратит 1 если узел создаётся впервые)
    def calc_prob(self, data):
        # Словарь, в котором мы будем хранить данные
        self.symbols = dict()

        for element in data:
            if self.symbols.get(element) == None:
                self.symbols[element] = 1
            else: 
                self.symbols[element] += 1     
        return self.symbols


    # Вспомогательная функция для получения закодированного сообщения из переданного массива
    def string_encoding(self, data, coding):
        encoding_output = []
        for c in data:
            encoding_output.append(coding[c])
            
        string = ''.join([str(item) for item in encoding_output])    
        return string

    # Мозг программы - кодировка в Хаффмана
    def encode(self, data):
        # Символы с частотами их встречи
        symbol_with_probs = self.calc_prob(data)

        # В качестве ключей выступают символы
        symbols = symbol_with_probs.keys()
        
        nodes = []
        
        # converting symbols and probabilities into huffman tree nodes
        for symbol in symbols:
            nodes.append(Node(symbol_with_probs.get(symbol), symbol))
        
        while len(nodes) > 1:
            # Сортируем все узлы встроенной функцией
            nodes = sorted(nodes, key=lambda x: x.prob)

            # Берём 2 самых маленьких узла (в отсортированном массиве это 0 и 1)
            right = nodes[0]
            left = nodes[1]
        
            left.code = 0
            right.code = 1
        
            # Объединяем 2 наименьших элемента
            newNode = Node(left.prob+right.prob, left.symbol+right.symbol, left, right)

            # Удаляем два наименьших элемента
            nodes.remove(left)
            nodes.remove(right)

            # Добавляем в конец объединение двух файлов
            nodes.append(newNode)

        # Считаем в массив        
        huffman_encoding = self.calc_code(nodes[0])

        # Преобразуем в красивый вид для нас
        encoded_output = self.string_encoding(data, huffman_encoding)

        return encoded_output, nodes[0]
        
    
    # Выполняет обратную задачу - декодирует из Хаффмана в обычный вид
    def decode(self, encoded_data, huffman_tree):
        # Ссылка на голову
        tree_head = huffman_tree
        # Массив, в котром мы будем хранить наши декодированные данные
        decoded_output = []

        for x in encoded_data:
            # Если встречаем 1, то движемся вправо, иначе - влево
            if x == '1':
                huffman_tree = huffman_tree.right   
            else:
                huffman_tree = huffman_tree.left
            
            try:
                if huffman_tree.left.symbol == None and huffman_tree.right.symbol == None:
                    pass
            except AttributeError:
                decoded_output.append(huffman_tree.symbol)
                huffman_tree = tree_head
            
        string = ''.join([str(item) for item in decoded_output])
    
        return string        


def main():
    # Тестирование программы на примере текста
    data = "Выпей чаю да съешь еще этих мягких французских булок"
    print("Исходный текст:", data)

    h = Haffman_Algorithm()
    encoding, tree = h.encode(data)

    print("Закодированный по Хаффману: ", encoding)
    print("Декодированный по Хаффману: ", h.decode(encoding,tree))

    # Также был проведён тест с огромным файлом длинной 2000 слов
    f = open("text.txt", "r")

    data = f.read()
    print("Исходный текст: ", data)

    encoding, tree = h.encode(data)

    print("Закодированный по Хаффману: ", encoding)
    print("Декодированный по Хаффману: ", h.decode(encoding,tree))


if __name__ == "__main__":
    main()