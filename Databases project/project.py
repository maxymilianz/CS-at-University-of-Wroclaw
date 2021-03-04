import ast
import json
import psycopg2
import sys


connection = None
cursor = None


def open_database(data):
    connection = psycopg2.connect(user = data['login'], password = data['password'], host = '127.0.0.1', port = '5432', database = data['database'])

    return connection


def tuple_to_json(data):
    result = '[' + \
             ', '.join(['"true"' if element == 't' else
                        '"false"' if element == 'f' else str(element)
                        for element in data]) + ']'
    return result


def list_to_json(data):
    if len(data) == 1 and type(data[0][0]) == str:
        if data[0][0] == 'OK':
            return '{"status": "OK"}'
        elif 'ERROR' in data[0][0]:
            return '{"status": "ERROR"}'

    result = '{"status": "OK", "data": [' + \
             ', '.join(tuple_to_json(ast.literal_eval(element[0].replace('t', '"t"').
                                                      replace('f', '"f"'))) \
                                     for element in data) + ']}'
    return result

def create_leader(data):
    cursor.execute('SELECT leader(%s, %s, %s);', (data['timestamp'], data['password'], data['member']))
    result = cursor.fetchall()
    print(list_to_json(result))


def support(data):
    if 'authority' in data:
        cursor.execute('SELECT support(%s, %s, %s, %s, %s, %s);',
                       (data['timestamp'], data['member'], data['password'],
                        data['action'], data['project'], data['authority']))
    else:
        cursor.execute('SELECT support(%s, %s, %s, %s, %s);',
                       (data['timestamp'], data['member'], data['password'],
                        data['action'], data['project']))
    result = cursor.fetchall()
    print(list_to_json(result))


def protest(data):
    if 'authority' in data:
        cursor.execute('SELECT protest(%s, %s, %s, %s, %s, %s);',
                       (data['timestamp'], data['member'], data['password'],
                        data['action'], data['project'], data['authority']))
    else:
        cursor.execute('SELECT protest(%s, %s, %s, %s, %s);',
                       (data['timestamp'], data['member'], data['password'],
                        data['action'], data['project']))
    result = cursor.fetchall()
    print(list_to_json(result))


def upvote(data):
    cursor.execute('SELECT upvote(%s, %s, %s, %s);',
                   (data['timestamp'], data['member'], data['password'],
                    data['action']))
    result = cursor.fetchall()
    print(list_to_json(result))


def downvote(data):
    cursor.execute('SELECT downvote(%s, %s, %s, %s);',
                   (data['timestamp'], data['member'], data['password'],
                    data['action']))
    result = cursor.fetchall()
    print(list_to_json(result))


def extract_id(data):
    return data['project'] if 'project' in data else data['authority']


def type_to_bool(data):
    return 'TRUE' if data == 'support' else 'FALSE'


def print_actions(data):
    if 'type' in data:
        if 'project' in data or 'authority' in data:
            some_id = extract_id(data)
            cursor.execute('SELECT get_actions(%s, %s, %s, %s, %s);',
                           (data['timestamp'], data['member'], data['password'],
                            type_to_bool(data['type']), some_id))
        else:
            cursor.execute('SELECT get_actions(%s, %s, %s, %s);',
                           (data['timestamp'], data['member'], data['password'],
                            type_to_bool(data['type'])))
    else:
        if 'project' in data or 'authority' in data:
            some_id = extract_id(data)
            cursor.execute('SELECT get_actions(%s, %s, %s, %s, %s);',
                           (data['timestamp'], data['member'], data['password'],
                            None, some_id))
        else:
            cursor.execute('SELECT get_actions(%s, %s, %s);',
                           (data['timestamp'], data['member'], data['password']))
    result = cursor.fetchall()
    print(list_to_json(result))


def print_projects(data):
    if 'authority' in data:
        cursor.execute('SELECT get_projects(%s, %s, %s, %s);',
                       (data['timestamp'], data['member'], data['password'],
                        data['authority']))
    else:
        cursor.execute('SELECT get_projects(%s, %s, %s);',
                       (data['timestamp'], data['member'], data['password']))

    result = cursor.fetchall()
    print(list_to_json(result))


def extract_id_1(data):
    return data['project'] if 'project' in data else data['action']


def print_votes(data):
    if 'project' in data or 'action' in data:
        some_id = extract_id_1(data)
        cursor.execute('SELECT get_votes(%s, %s, %s, %s);',
                       (data['timestamp'], data['member'], data['password'], some_id))
    else:
        cursor.execute('SELECT get_votes(%s, %s, %s);',
                       (data['timestamp'], data['member'], data['password']))
    result = cursor.fetchall()
    print(list_to_json(result))


def print_trolls(data):
    cursor.execute('SELECT trolls(%s);', (data['timestamp'],))
    result = cursor.fetchall()
    print(list_to_json(result))


string_to_function = {'open': open_database, 'leader': create_leader, 'support': support, 'protest': protest, 'upvote': upvote, 'downvote': downvote, 'actions': print_actions,
                      'projects': print_projects, 'votes': print_votes, 'trolls': print_trolls}


def interpret_json(connection, data):
    for function_name in string_to_function:
        if function_name in data:
            string_to_function[function_name](data[function_name])
            return


def interpret_input():
    for line in sys.stdin:
        interpret_json(connection, json.loads(line))
        connection.commit()


def initialize():
    cursor.execute(''.join(open('physical model.sql', 'r').readlines()))
        

try:
    connection = open_database(json.loads(sys.stdin.readline())['open'])
    print('{"status": "OK"}')
    cursor = connection.cursor()
    if len(sys.argv) > 1 and sys.argv[1] == '--init':
        initialize()
    interpret_input()
except (Exception, psycopg2.Error) as error:
    print('{"status": "ERROR"}')
finally:
    if cursor:
        cursor.close()
    if connection:
        connection.close()