from prev1 import perfect_numbers_list, perfect_numbers_fun
from new1 import perfect_numbers_iter
from timeit import timeit
import matplotlib.pyplot as plt

fst_col_len = 6
column_len = 24
list_str = 'list'
fun_str = 'fun'
iter_str = 'iter'

def test(n):
    return {list_str: timeit('perfect_numbers_list(' + str(n) + ')', 'from prev1 import perfect_numbers_list', number = 1),
            fun_str: timeit('perfect_numbers_fun(' + str(n) + ')', 'from prev1 import perfect_numbers_fun', number = 1),
            iter_str: timeit('list(perfect_numbers_iter(' + str(n) + '))', 'from new1 import perfect_numbers_iter', number = 1)}

def print_results(vals):
    line = ' ' * fst_col_len + '|' + ' ' * (column_len - len(list_str)) + list_str +\
           '|' + ' ' * (column_len - len(fun_str)) + fun_str +\
           '|' + ' ' * (column_len - len(iter_str)) + iter_str
    print(line)

    for val in vals:
        results = test(val)
        val_str = str(val)
        list_res_str = str(results[list_str])[:column_len]
        fun_res_str = str(results[fun_str])[:column_len]
        iter_res_str = str(results[iter_str])[:column_len]
        line = val_str + ' ' * (fst_col_len - len(val_str)) +\
            '|' + ' ' * (column_len - len(list_res_str)) + list_res_str + \
            '|' + ' ' * (column_len - len(fun_res_str)) + fun_res_str + \
            '|' + ' ' * (column_len - len(iter_res_str)) + iter_res_str
        print(line)

# print_results([10, 100, 1000])

def gen_gnuplot(filename, vals):
    with open(filename, 'w') as file:
        file.write('# n\t\t' + list_str + '\t\t' + fun_str + '\t\t' + iter_str + '\n')

        for val in vals:
            res = test(val)
            file.write(str(val) + '\t\t' + str(res[list_str]) + '\t\t' + str(res[fun_str]) + '\t\t' + str(res[iter_str]) + '\n')

def pyplot(vals):
    res = [[], [], []]

    for n in vals:
        part_res = test(n)
        res[0] += [part_res[list_str]]
        res[1] += [part_res[fun_str]]
        res[2] += [part_res[iter_str]]

    plot_list, = plt.plot(vals, res[0], 'o')
    plot_fun, = plt.plot(vals, res[1], 'ro')
    plot_iter, = plt.plot(vals, res[2], 'go')
    plt.xscale('log')
    plt.yscale('log')
    plt.ylabel('Time (seconds)')
    plt.legend([plot_list, plot_fun, plot_iter], ['List compr.', 'Functional', 'Iterators'])

    plt.show()

pyplot([10, 100, 1000])