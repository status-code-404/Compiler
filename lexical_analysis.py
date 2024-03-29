IDENTIFIER_TABLE = {
    "BINARY": '01',
    'NUMBER': '0123456789',
    'HEXNUMBER': '0123456789abcdefABCDEF',
    'NUM_OPERATOR': '+-',
    'LETTER': 'abcdefghijklmnopqrstuvwxyzABCDEFGHIGKLMNOPQRSTUVWXYZ_',
    'OPERATOR': '''[];,./><:"'{}||()*&&^%#!~==+=-=*=''',
    'STRING_OPERATOR': "'" + '"',
    'SPLIT': '\n ',
}

TOKEN_TABLE = {
    "NUM": [],
    "STRING": [],
    "KEYWORD": [],
    "OPERATOR": [],
    "SPLIT": [],
}


class Token:
    def __init__(self, name, location, type):
        self.name = name
        self.location = location
        self.type = type

    def get_type(self):
        return self.type

    def __str__(self):
        return "{name:%s, location:%d, type:%s}" % (self.name, self.location, self.type)

    def __repr__(self):
        return self.__str__()


def operator_paras(s: str, loca):
    global TOKEN_TABLE
    now_loca = loca
    if s[loca] in IDENTIFIER_TABLE["OPERATOR"]:
        if len(s[loca:loca + 2] )== 2 and s[loca:loca + 2] in IDENTIFIER_TABLE["OPERATOR"]:
            TOKEN_TABLE["OPERATOR"].append(Token(s[loca:loca + 2], loca, "OPERATOR"))
            return loca + 2
        else:
            TOKEN_TABLE["OPERATOR"].append(Token(s[loca], loca, "OPERATOR"))
            return loca + 1
    else:
        raise Exception("operator_paras wrong")


def paras_template(s: str, loca, identifier_type: str, paras_type: str, *args):
    global TOKEN_TABLE
    start_loca = loca
    while loca < len(s):
        if s[loca] in IDENTIFIER_TABLE[identifier_type]:
            loca += 1
        elif s[loca] in IDENTIFIER_TABLE["OPERATOR"] or s[loca] in IDENTIFIER_TABLE["SPLIT"]:
            if loca == start_loca:
                raise Exception("%s_paras wrong" % paras_type)
            # 这里为了保证代码不重复所以下层封装了paras_template专门用来封装keyword_paras何num_paras抽象出来的相同逻辑
            # todo:然而这里的设计耦合num_paras的特殊逻辑，后续考虑如何解耦啊
            if paras_type == "NUM":
                start_loca = args[0]
            TOKEN_TABLE[paras_type].append(Token(s[start_loca:loca], start_loca, paras_type))
            return loca
        else:
            raise Exception("%s_paras wrong" % paras_type)

    if paras_type == "NUM":
        start_loca = args[0]
    TOKEN_TABLE[paras_type].append(Token(s[start_loca:loca], start_loca, paras_type))
    return loca


def keyword_paras(s: str, loca):
    return paras_template(s, loca, "LETTER", "KEYWORD")


def num_paras(s: str, loca):
    global TOKEN_TABLE
    start_loca = loca
    if s[loca] in IDENTIFIER_TABLE['NUM_OPERATOR']:
        loca += 1
    if s[loca:loca + 2] == '0x':
        loca += 2
    return paras_template(s, loca, "NUMBER", 'NUM', start_loca)


def string_paras(s: str, loca):
    global TOKEN_TABLE
    if s[loca] not in IDENTIFIER_TABLE["STRING_OPERATOR"]:
        raise Exception("string_paras wrong")
    # 暂不支持'''
    start_identifier = s[loca]
    start_loca = loca = loca + 1
    while loca < len(s):
        if s[loca] != start_identifier:
            loca += 1
        elif s[loca] == start_identifier:
            TOKEN_TABLE["STRING"].append(Token(s[start_loca:loca], start_loca, 'STRING'))
            return loca + 1
    raise Exception("string_paras wrong")


def split_paras(s: str, loca):
    start_loca = loca
    while loca < len(s):
        if s[loca] not in IDENTIFIER_TABLE["SPLIT"] and loca == start_loca:
            raise Exception("split_paras wrong")
        elif s[loca] not in IDENTIFIER_TABLE["SPLIT"]:
            break
        elif s[loca] == "\n":
            TOKEN_TABLE["SPLIT"].append(Token(None, start_loca, 'SPLIT'))
        loca += 1
    return loca


def paras(s: str):
    loca = 0
    paras_func = [num_paras, operator_paras, split_paras, keyword_paras, string_paras]
    while loca < len(s):
        paras_fail = True
        for func in paras_func:
            try:
                loca = func(s, loca)
                paras_fail = False
                break
            except:
                continue
        if paras_fail:
            raise Exception("paras wrong")


def sort_all_symbol():
    global TOKEN_TABLE
    paras_item = []
    for type_ in TOKEN_TABLE:
        for item in TOKEN_TABLE[type_]:
            paras_item.append([item.location, item.type, item.name])
    paras_item.sort()
    last_level = 0
    last_split_location = 0
    last_is_split = True
    for item in paras_item:
        if last_is_split:
            last_level = item[0] - last_split_location
        if item[1] == "SPLIT":
            last_split_location = item[0]
            last_is_split = True
        else:
            last_is_split = False
        item.append(last_level)

    return paras_item


# paras('''
#     def paras(s: str):
    #     loca = 0
    #     paras_func = [num_paras, operator_paras, split_paras, keyword_paras, string_paras]
    #     while loca < len(s):
    #         p = -1
    #         for func in paras_func:
    #             try:
    #                 loca = func(s, loca)
    #                 p = loca
    #                 break
    #             except:
    #                 continue
    #         if p == -1:
    #             raise Exception("paras wrong")
# ''')

if __name__ == '__main__':
    # 暂不支持注释， 暂时会将int这种解读成何变量一样的key word类型
    paras('''
        def paras(s: str):
            loca = 0
            paras_func = [num_paras, operator_paras, split_paras, keyword_paras, string_paras]
            while loca < len(s):
                p = -1
                for func in paras_func:
                    try:
                        loca = func(s, loca)
                        p = loca
                        break
                    except:
                        continue
                if p == -1:
                    raise Exception("paras wrong")
    ''')
    print(TOKEN_TABLE)
    print(sort_all_symbol())
