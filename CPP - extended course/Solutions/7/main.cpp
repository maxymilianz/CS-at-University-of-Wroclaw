#include <iostream>

#include "tasks.h"
#include "vectortest.h"

int main() {
    map<string, unsigned int, case_insensitive_cmp> m =
        frequencytable<case_insensitive_cmp>(vector<string>({"t1", "t2", "t3", "t2", "t3", "t2", "t4", "a", "B"}));
    cout << m << '\n';

    case_insensitive_cmp cmp;
    cout << cmp("a", "B") << ' ' << ('a' < 'B') << '\n';

    case_insensitive_hash hash;
    cout << hash("a") << ' ' << hash("A") << ' ' << hash("B") << '\n';

    case_insensitive_equality e;
    cout << e("A", "a") << ' ' << e("A", "B") << '\n';

    unordered_map<string, unsigned int, case_insensitive_hash, case_insensitive_equality> um =
        hashed_frequencytable <case_insensitive_hash, case_insensitive_equality>(vector<string>({"t1", "t2", "t3", "t2", "t3", "t2", "t4", "a", "B"}));
    cout << um << '\n';

    ifstream s("book.html");
    vector<string> v = vectortest::readfile(s);
    map<string, unsigned int, case_insensitive_cmp> book = frequencytable<case_insensitive_cmp>(v);
    map<string, unsigned int, case_insensitive_cmp>::const_iterator i;

    for (string s : {"magnus", "hominum", "memoria"}) {
        i = book.find(s);

        if (i == book.end())
            cout << "There's no such element!" << '\n';
        else
            cout << i->first << ", " << i->second << '\n';
    }

    map<string, unsigned int, case_insensitive_cmp>::const_iterator most = book.begin();

    for (i = book.begin(); i != book.end(); i++)
        if (i->second > most->second)
            most = i;

    cout << most->first << ", " << most->second << '\n';

    return 0;
}
