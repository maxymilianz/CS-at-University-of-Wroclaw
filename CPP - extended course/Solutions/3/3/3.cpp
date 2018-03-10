// 3.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include "stack.h"

int main()
{
	stack s1 = stack();
	stack s2 = stack({ 21.37, 14.88 });
	s1 = s2;

	cout << s1.top() << endl;
	s1.pop();

	stack s3 = stack(s1);

	s3.push(2.09);
	cout << s3.top() << endl;

	const stack s4 = { 1.2, 2.3 };
	cout << s4.top() << endl;

	// from list:

	{
		stack s1 = { 1, 2, 3, 4, 5 };
		stack s2 = s1; // Copy constructor.
					   // j is not size_t, because multiplying size_t with itself is
					   // unnatural:
		for (unsigned int j = 0; j < 20; ++j)
			s2.push(j * j);
		s1 = s2;
		// Assignment.
		s1 = s1;
		// Always check for self assignment.
		s1 = { 100,101,102,103 };
		// Works because the compiler inserts constructor and
		// calls assignment with the result

#if 1
		stack& sconst = s1;
		sconst.top() = 20;
		sconst.push(15);
#endif
	}

	// 5:

	{
		cout << s1;
		cout << s2;
		cout << s3;
		cout << s4;
	}

    return 0;
}

