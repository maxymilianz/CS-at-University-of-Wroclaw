#include <iostream>
#include <functional>
#include <unordered_map>

using namespace std;

void foo(const unordered_map<int, string> map) {
    map.at(1);      // [] not for const
}

int main() {
    size_t a = 1, b = 2;
    size_t h = hash<int>{}(1);

    pair<int, int> p = {1, 2};
    cout << p.first << '\n';

    //for (int a = 0, size_t b = 0; a < 10; a++, b++);
    cout << (a < p.first) << '\n';

    return 0;
}
