#include "fifteen.h"

fifteen::fifteen( ) {
    for (size_t i = 0; i < dimension; i++) {
        for (size_t j = 0; j < dimension; j++) {
            table[i][j] = i * dimension + j + 1;
        }
    }

    table[dimension - 1][dimension - 1] = 0;
    open_i = dimension - 1;
    open_j = dimension - 1;
}

fifteen::fifteen( std::initializer_list< std::initializer_list< size_t >> init ) {
    size_t iUInt = 0;

    for (std::initializer_list<std::initializer_list<size_t>>::iterator i = init.begin(); i != init.end(); i++, iUInt++) {
        size_t jUInt = 0;

        for (std::initializer_list<size_t>::iterator j = (*i).begin(); j != (*i).end(); j++, jUInt++) {
            table[iUInt][jUInt] = *j;

            if (!table[iUInt][jUInt]) {
                open_i = iUInt;
                open_j = jUInt;
            }
        }
    }
}

void fifteen::makemove(move m) {
    if (m == move::up && open_i != dimension - 1) {
        table[open_i][open_j] = table[open_i + 1][open_j];
        ++open_i;
        table[open_i][open_j] = 0;
    }
    else if (m == move::down && open_i != 0) {
        table[open_i][open_j] = table[open_i - 1][open_j];
        --open_i;
        table[open_i][open_j] = 0;
    }
    else if (m == move::left && open_j != dimension - 1) {
        table[open_i][open_j] = table[open_i][open_j + 1];
        ++open_j;
        table[open_i][open_j] = 0;
    }
    else if (m == move::right && open_j != 0) {
        table[open_i][open_j] = table[open_i][open_j - 1];
        --open_j;
        table[open_i][open_j] = 0;
    }
    else
        throw illegalmove(m);
}

size_t fifteen::distance( ) const {
    size_t dist = 0;

    for (size_t i = 0; i < dimension; i++) {
        for (size_t j = 0; j < dimension; j++) {
            position solved = solvedposition(table[i][j]);
            dist += size_tAbsDiff(i, solved.first) + size_tAbsDiff(j, solved.second);
        }
    }

    return dist;
}

bool fifteen::issolved( ) const {
    for (size_t i = 0; i < dimension; i++)
        for (size_t j = 0; j < dimension; j++)
            if (table[i][j] != i * dimension + j + 1 && !(i == dimension - 1 && j == i && !table[i][j]))
                return false;

    return true;
}

size_t fifteen::hashvalue( ) const {
    unsigned long long h = 1;

    for (size_t i = 0; i < dimension; i++) {
        for (size_t j = 0; j < dimension; j++) {
            h *= std::hash<size_t>{}(table[i][j]);
        }
    }

    return h;
}

bool fifteen::equals( const fifteen& other ) const {
    for (size_t i = 0; i < dimension; i++)
        for (size_t j = 0; j < dimension; j++)
            if (table[i][j] != other.table[i][j])
                return false;

    return true;
}
