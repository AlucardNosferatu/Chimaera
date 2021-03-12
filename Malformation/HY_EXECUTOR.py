import importlib
import hy
import FUNC_TEMP as ft


def reg_func(name='add1', placeholder=None):
    if placeholder is None:
        placeholder = ['a', 'b']
    placeholder_str = ' '.join(placeholder)
    with open('FUNC_TEMP.hy', 'r') as f:
        lines = f.readlines()
    for i in range(len(lines)):
        if not lines[i].endswith('\n'):
            lines[i] += '\n'
    exp_str = "(defn {} [{}] (.{} FUNC_STORAGE {}))\n".format(name, placeholder_str, name, placeholder_str)
    lines.append(exp_str)
    with open('FUNC_TEMP.hy', 'w') as f:
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
    eval_str = 'ft.{}({})'.format(name, params_str)
    res = eval(eval_str)
    return res


if __name__ == "__main__":
    reg_func()
    exe_func()
    print('Fuck')
