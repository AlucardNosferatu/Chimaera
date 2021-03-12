import importlib
import os

import FUNC_TEMP as ft


def reg_func(name='add1', placeholder=None):
    if placeholder is None:
        placeholder = ['a', 'b']
    placeholder_str = ' '.join(placeholder)
    path=os.getcwd()
    if path.endswith('Chimaera'):
        path=os.path.join(path,'Malformation')
    fthy=os.path.join(path,'FUNC_TEMP.hy')
    with open(fthy, 'r') as f:
        lines = f.readlines()
    for i in range(len(lines)):
        if not lines[i].endswith('\n'):
            lines[i] += '\n'
    exp_str = "(defn {} [{}] (.{} FUNC_STORAGE {}))\n".format(name, placeholder_str, name, placeholder_str)
    lines.append(exp_str)
    with open(fthy, 'w') as f:
        f.writelines(lines)


def exe_func(name='add1', params=None):
    if params is None:
        params = [2029, 1224]
    for i in range(len(params)):
        if type(params[i]) is str:
            params[i] = "'{}'".format(params[i])
        else:
            params[i] = "{}".format(params[i])
    params_str = ', '.join(params)
    importlib.reload(ft)
    importlib.reload(ft.FUNC_STORAGE)
    eval_str = 'ft.{}({})'.format(name, params_str)
    res = eval(eval_str)
    return res


if __name__ == "__main__":
    print('Fuck')