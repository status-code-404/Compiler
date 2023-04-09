from lexical_analysis import sort_all_symbol, paras


class Syntax_Node:
    def __init__(self):
        self.data = "Sequence"
        self.left = None
        self.right = None

    def init_son(self):
        self.left = Syntax_Node()
        self.right = Syntax_Node()

    def __str__(self):
        return "\n{data:%s, left:%s, right:%s}" % (
            self.data, str(self.left), str(self.right))

    def __repr__(self):
        return self.__str__()


def get_same_level_expression(representation: list):
    p = 1
    while p < len(representation):
        if representation[p][3] > representation[0][3]:
            break
        p += 1
    return p if p < len(representation) else -1


def find_next_same_level(representation):
    now_level = representation[0][3]
    n = 1
    while n < len(representation):
        if representation[n][3] <= now_level:
            break
        n += 1

    return n


def paras_to_syntax_node(node: Syntax_Node, representation: list):
    # todo: 暂未支持def 函数解析，后面补上
    while len(representation) > 0 and representation[0][1] == "SPLIT":
        representation = representation[1:]

    if len(representation) == 0:
        return

    if len(representation) == 1:
        if representation[0][1] == "KEYWORD" and representation[0][2] in "and or while if else switch elif ":
            raise Exception("syntax_parse Error, cant parse this")
        node.data = representation[0][2]

    elif representation[0][1] == "KEYWORD" and representation[0][2] in "if elif while for":
        same_level_index = get_same_level_expression(representation)
        if same_level_index == -1:
            raise Exception("syntax_parser Error, keyword logical is not correct")
        left_representation = representation[1:same_level_index]
        right_representation = representation[same_level_index:]

        node.data = representation[0][2].upper()
        node.init_son()
        paras_to_syntax_node(node.left, left_representation)

        if representation[0][2] in "while for":
            paras_to_syntax_node(node.right, right_representation)

        elif representation[0][2] in "if elif":
            node = node.right
            node.data = representation[0][2] + "_statement"
            node.left = Syntax_Node()
            next_level_index = abs(find_next_same_level([left_representation[-1]] + right_representation)) - 1

            paras_to_syntax_node(node.left, right_representation[:next_level_index])
            if next_level_index >= len(right_representation):
                return
            node.right = Syntax_Node()
            paras_to_syntax_node(node.right, right_representation[next_level_index:])

    elif representation[0][1] == "KEYWORD" and representation[0][2] == "else":
        if representation[1][2] != ":" and representation[2][1] != "SPLIT":
            raise Exception("syntax_paras else wrong")
        node.data = "else".upper()
        node.left = Syntax_Node()
        next_level_index = abs(find_next_same_level(representation[2:]))
        left_representation = representation[3:next_level_index + 2]
        paras_to_syntax_node(node.left, left_representation)
        right_representation = representation[next_level_index + 2:]
        if len(right_representation) > 0:
            node.right = Syntax_Node()
            paras_to_syntax_node(node.right, right_representation)


    else:
        node.left = Syntax_Node()
        node.left.data = representation[0][2]
        if representation[1][1] != "OPERATOR":
            node.right = Syntax_Node()
            paras_to_syntax_node(node.right, representation[1:])
        else:
            node.data = representation[1][2]
            if len(representation) >= 2:
                node.right = Syntax_Node()
                paras_to_syntax_node(node.right, representation[2:])


if __name__ == '__main__':
    m = Syntax_Node()

    paras('''
    while a<=10:
        if a == 5:
            b += 1
        elif a== 20:
            c += 1
        else:
            d+=1
    ''')
    paras_to_syntax_node(m, sort_all_symbol())
    print(m)
