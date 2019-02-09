i = 0

with open('tests/pracownia1/parse_error.xi') as file:
    for test in file.read().split('\n\n'):
        with open('tests/pracownia1/parse_error_' + str(i) + '.xi', 'w') as new_file:
            new_file.write(test + '\n\n//@PRACOWNIA\n//@should_not_parse')
        i += 1
