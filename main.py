from heapq import heappop, heappush, heapify


class Node:
    """Класс узла дерева для генерации кода Хаффмана"""
    def __init__(self, chars: str, count: int):
        # Символ(ы) входного алфавита
        self.chars = chars
        # Количество вхождений символа (символов) в исходной строке
        self.weight = count
        # Левое и правое поддерево
        self.left = None
        self.right = None

    def __eq__(self, other):
        """
        Сравнение объектов <Node> на равенство
        """
        return self.weight == other.weight

    def __ne__(self, other):
        """
        Сравнение объектов <Node> на неравенство
        """
        return self.weight != other.weight

    def __lt__(self, other):
        """
        Сравнение объектов <Node> на меньше
        """
        return self.weight < other.weight

    def __gt__(self, other):
        """
        Сравнение объектов <Node> на больше
        """
        return self.weight > other.weight


class HTree:
    """Класс Дерево для генерации кода Хаффмана"""
    def __init__(self):
        # Корень дерева
        self.root = None
        # Таблица кодировки (создается на основе дерева)
        self.encode_table = dict()

    def create_tree(self, freq: list[tuple[str, int]]):
        """
        Построение дерева кодирование (H-дерева)
        freq: таблица частотности
        """
        # Список свободных узлов.
        # Создается как приоритетная очередь
        # free_leaves = []
        free_leaves = [Node(v, w) for v, w in freq]
        heapify(free_leaves)
        # for it in freq:
        #     leaf = Node(it[0], it[1])
        #     heappush(free_leaves, leaf)
        # Итерационно заполняем дерево пока в списке свободных узлов не останется один узел (корень)
        while len(free_leaves) > 1:
            # Выбираются два свободных узла дерева с наименьшими весами
            l_leaf = heappop(free_leaves)
            r_leaf = heappop(free_leaves)
            # Создается их родитель с весом, равным их суммарному весу
            parent_str = l_leaf.chars + r_leaf.chars
            parent_weight = l_leaf.weight + r_leaf.weight
            parent = Node(parent_str, parent_weight)
            parent.left = l_leaf
            parent.right = r_leaf
            # Родитель добавляется в список свободных узлов, а два его потомка удаляются из этого списка
            heappush(free_leaves, parent)
        # Корень дерева
        self.root = free_leaves[0]
        # Создание таблицы кодировки
        self.__h_tree_to_table__(freq)

    # def __find_min_items_indexis__(self, nodes_list: list) -> tuple[int, int]:
    #     """
    #     Возвращает индексы двух минимальных элементов списка
    #     nodes_list: список вида list<Node>
    #     : результат кортеж значений индексов
    #     """
    #     weights = [it.weight for it in nodes_list]
    #     min_index = len(weights) - 1
    #     min_val = weights[-1]
    #     for i in range(len(weights) - 1, -1, -1):
    #         if weights[i] < min_val:
    #             min_val = weights[i]
    #             min_index = i
    #     min_1_index = min_index
    #
    #     min_index = len(weights) - 1
    #     if min_index == min_1_index:
    #         min_index = len(weights) - 2
    #     min_val = weights[min_index]
    #     for i in range(len(weights) - 1, -1, -1):
    #         if i == min_1_index:
    #             continue
    #         if weights[i] < min_val:
    #             min_val = weights[i]
    #             min_index = i
    #     min_2_index = min_index
    #     # res = tuple(sorted([min_2_index, min_1_index]))
    #     return min_2_index, min_1_index

    def __h_tree_to_table__(self, freq: list[tuple[str, int]]):
        """
        freq: таблица частотности.
        Создает на основе H-дерева таблицу кодировки.
        """
        for it in freq:
            c, _ = it
            c_code = self.__encode_char_by_tree__(c)
            self.encode_table[c] = c_code
        print(self.encode_table)

    def __encode_char_by_tree__(self, c: str) -> str:
        """
        Кодирование символа с помощью H-дерева
        c: кодируемый символ
        результат: код (двоичный)
        """
        current_leaf = self.root
        code = ""
        while current_leaf.chars != c:
            if c in current_leaf.left.chars:
                code += "0"
                current_leaf = current_leaf.left
            else:
                code += "1"
                current_leaf = current_leaf.right
        return code

    def encode_char(self, c: str) -> str:
        """
        Кодирование символа (через таблицу)
        c: кодируемый символ
        результат: код (двоичный)
        """
        return self.encode_table.get(c)


def frequencies(s: str) -> list[tuple[str, int]]:
    """
    Возвращает список с частотой вхождения символов в данной строке
    s: исходная строка (текст)
    результат: список в виде [(str, int) ...]
    где str - символ из исходного текста
    int - количество вхождений данного символа
    """
    freq = []
    # Список с символами, которые уже встречались
    symbols = []
    for c in s:
        if c not in symbols:
            symbols.append(c)
            # Кортеж вида (str, int)
            fr = c, s.count(c)
            freq.append(fr)
    return freq


def encode(freq: list[tuple[str, int]], s: str):
    """
    Функция кодировки строки в код Хаффмана
    freq: список частоты вхождения символов в тексте
    s: исходная строка текста
    результат: строка вида '1001011' как код Хаффмана
    """
    # Если в таблице частотности один или меньше символов, то выход
    if len(freq) <= 1:
        return None
    # Создаем H-дерево
    h_t = HTree()
    h_t.create_tree(freq)

    h_code = ""
    for ch in s:
        encoded_c = h_t.encode_char(ch)
        h_code += encoded_c
    return h_code


test = 'ааааааааааааааабббббббввввввггггггддддд'
# test = 'aaaabcc'
# test = 'aabacdab'
# test = 'Huffman coding is a data compression algorithm.'
fq = frequencies(test)
print(fq)
print(encode(fq, test))
