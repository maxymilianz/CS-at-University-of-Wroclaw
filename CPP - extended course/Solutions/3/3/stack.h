#ifndef _STACK
#define _STACK 1

#include <iostream>
#include <initializer_list>

using namespace std;

class stack {
	size_t current_size, current_capacity;

	double *tab;

	//void ensure_capacity(size_t c);

public:
	stack() : tab(nullptr), current_size(0), current_capacity(0) { }

	stack(initializer_list<double> d) : current_size(d.size()), current_capacity(d.size()), tab(new double[current_capacity]) {
		copy(d.begin(), d.end(), tab);
	}

	stack(const stack &s) : current_size(s.current_capacity), current_capacity(s.current_capacity), tab(new double[current_capacity]) {
		for (int i = 0; i < current_capacity; i++)
			tab[i] = s.tab[i];
	}

	~stack() {
		delete [] tab;
	}

	//void operator =(const stack &s);

	void push(double d) {		// MEM LEAKS
		ensure_capacity(++current_size);
		tab[current_size - 1] = d;
	}

	//void pop();

	void reset(size_t s) {
		while (current_size > s)
			pop();
	}

	double & top() {		// NOT WORKING
		double &ref = tab[current_size - 1];
		return ref;
	}

	double top() const {
		return tab[current_size];
	}

	size_t size() const {
		return current_size;
	}
	
	bool empty() const {
		return current_size == 0;
	}

	void ensure_capacity(size_t c) {
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

	void operator =(const stack &s) {
		current_capacity = s.current_capacity;
		tab = new double[current_capacity];

		for (current_size = 0; current_size < s.current_size; current_size++)
			tab[current_size] = s.tab[current_size];
	}

	void pop() {
		if (current_size > 1)
			tab[--current_size] = 0;
		else
			throw runtime_error("Stack is empty!");
	}

	friend ostream & operator <<(ostream &stream, const stack &s) {
		return stream << "size = " << s.current_size << endl << "capacity = " << s.current_capacity << endl << "top = " << s.top() << endl;
	}
};

#endif