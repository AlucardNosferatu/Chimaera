import hy

if __name__ == "__main__":
    name = 'add1'
    placeholder = ['a', 'b']
    placeholder_str = ' '.join(placeholder)
    params = ['2029', '1224']
    params_str = ' '.join(params)

    exp_str0 = '(import FUNC_STORAGE)'
    expr = hy.read_str(exp_str0)
    res0 = hy.eval(expr)
    exp_str1 = "(defn {} [{}] (.{} FUNC_STORAGE {}))\n".format(name, placeholder_str, name, placeholder_str)
    expr = hy.read_str(exp_str1)
    res1 = hy.eval(expr)
    exp_str2 = "({} {})".format(name, params_str)
    expr = hy.read_str(exp_str2)
    res2 = hy.eval(expr)

    print('Fuck')
