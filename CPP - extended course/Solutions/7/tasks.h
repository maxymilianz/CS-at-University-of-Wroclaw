#include <map>
#include <string>
#include <vector>
#include <unordered_map>

using namespace std;

struct case_insensitive_cmp {
    bool operator()(const string &s1, const string &s2) {
        for (unsigned int i = 0; i < s1.length() && i < s2.length(); i++) {
            if (toupper(s1[i]) == toupper(s2[i]))
                continue;
            else
                return toupper(s1[i]) < toupper(s2[i]);
        }

        return s1.length() < s2.length();
    }
};

struct case_insensitive_hash {
    size_t operator ()(const string &s) const {
        size_t hash = 1;

        for (size_t i = 0; i < s.length(); i++) {
            hash *= 101;
            hash += toupper(s[i]);
        }

        return hash;
    }
};

struct case_insensitive_equality {
    bool operator()(const string &s1, const string &s2) const {
        case_insensitive_cmp cmp;
        return !(cmp(s1, s2) || cmp(s2, s1));

        /*if (s1.length() != s2.length())
            return false;

        for (size_t i = 0; i < s1.length(); i++)
            if (toupper(s1[i]) != toupper(s2[i]))
                return false;

        return true;*/
    }
};

template<typename C = less<string>> map<string, unsigned int, C> frequencytable(const vector<string> &text) {
    map<string, unsigned int, C> m = map<string, unsigned int, C>();

    for (string i : text) {
        if (m.find(i) == m.end())
            m.insert(pair<string, unsigned int>(i, 1));
        else {
            unsigned int freq = ++m[i];
            m.erase(i);
            m.insert(pair<string, unsigned int>(i, freq));
        }
    }

    return m;
}

template<typename C> ostream & operator <<(ostream &stream, const map<string, unsigned int, C> &m) {
    for (auto i : m)
        stream << i.first << ", " << i.second << '\n';

    return stream;
}

template<typename H, typename E> ostream & operator <<(ostream &stream, const unordered_map<string, unsigned int, H, E> &m) {
    for (auto i : m)
        stream << i.first << ", " << i.second << '\n';

    return stream;
}

template<typename H = hash<string>, typename E = equal_to<string>> unordered_map<string, unsigned int, H, E>
    hashed_frequencytable(const vector<string> &text) {
        unordered_map<string, unsigned int, H, E> m = unordered_map<string, unsigned int, H, E>();

        for (string i : text) {
            if (m.find(i) == m.end())
                m.insert(pair<string, unsigned int>(i, 1));
            else {
                unsigned int freq = ++m[i];
                m.erase(i);
                m.insert(pair<string, unsigned int>(i, freq));
            }
        }

        return m;
    }
