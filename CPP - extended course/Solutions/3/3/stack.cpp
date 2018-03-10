#include "stack.h"

/*void stack::ensure_capacity(size_t c) {
	if (current_capacity < c) {
		// New capacity will be the greater of c and
		// 2 * current_capacity.
		if (c < 2 * current_capacity)
			c = 2 * current_capacity;

		double* newtab = new double[c];
		for (size_t i = 0; i < current_size; ++i)
			newtab[i] = tab[i];

		current_capacity = c;
		delete[] tab;
		tab = newtab;
	}
}

void stack::operator =(const stack &s) {
	current_capacity = s.current_capacity;
	tab = new double[current_capacity];

	for (current_size = 0; current_size < s.current_size; current_size++)
		tab[current_size] = s.tab[current_size];
}

void stack::pop() {
	if (current_size > 1)
		tab[--current_size] = 0;
	else
		throw runtime_error("Stack is empty!");
}*/