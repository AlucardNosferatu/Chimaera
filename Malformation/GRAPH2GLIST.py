def get_all_symbol(results):
    symbols = []
    for sym_dict in results:
        if sym_dict['symbol'] not in symbols:
            symbols.append(sym_dict['symbol'])
    return symbols


def get_symbol_set(symbol):
    out_list = []
    for sym_dict in results:
        if sym_dict['symbol'] == symbol:
            out_list.append(sym_dict)
    return out_list


if __name__ == "__main__":
    results = [
        {'symbol': 'add1', 'param': 1, 'pcount': 4},
        {'symbol': 'add1', 'param': 2, 'pcount': 4},
        {'symbol': 'add1', 'param': 3, 'pcount': 4},
        {'symbol': 'add1', 'param': 4, 'pcount': 4},
        {'symbol': 'mul1', 'param': 5, 'pcount': 3},
        {'symbol': 'mul1', 'param': 6, 'pcount': 3},
        {'symbol': 'mul1', 'param': 'add1', 'pcount': 3},
        {'symbol': 'out1', 'param': 'mul1', 'pcount': 2},
        {'symbol': 'out1', 'param': 'add1', 'pcount': 2},
    ]
    symbols = get_all_symbol(results)
    sym_dicts = get_symbol_set('out1')
    print(symbols)
