// 6.3.cpp : Defines the entry point for the console application.
//

#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>

long n = 0;
char *start, *actual;

void Clear_Buffer(char* b) {
	for (int i = 0; i < n; i++)
		*(start + i) = 0;
}

char* Assign_Block(long l) {
	if (l <= 0 || l > n) {
		printf("\nAssign_Block: wrong input data\n");
		exit(1);
	}
	else {
		int amount = 0;
		char *ptr = actual;

		for (int i = actual - start; i < n; i++) {
			if (*(start + i) == 0)
				amount++;
			else {
				amount = 0;

				if (i < n - 1)
					ptr = start + i + 1;
				else
					ptr = start;
			}

			if (amount >= l)
				return ptr;
		}

		for (int i = 0; i < n; i++) {
			if (*(start + i) == 0)
				amount++;
			else {
				amount = 0;
				ptr = start + i + 1;
			}

			if (amount >= l)
				return ptr;
		}

		return NULL;
	}
}

char* Find_Block(char c, long l) {
	if (l <= 0 || l > n) {
		printf("\nFind_Block: wrong input data\n");
		exit(1);
	}
	else {
		int amount = 0;
		char *ptr = actual;

		for (int i = actual - start; i < n; i++) {
			if (*(start + i) == c)
				amount++;
			else {
				amount = 0;

				if (i < n - 1)
					ptr = start + i + 1;
				else
					ptr = start;
			}

			if (amount >= l)
				return ptr;
		}

		for (int i = 0; i < n; i++) {
			if (*(start + i) == c)
				amount++;
			else {
				amount = 0;
				ptr = start + i + 1;
			}

			if (amount >= l)
				return ptr;
		}

		return NULL;
	}
}

void Set_Block(char *b, long l, char c) {
	if (l <= 0 || l > n || b == NULL) {
		printf("\nSet_Block: wrong input data\n");
		exit(1);
	}
	else {
		if (c >= 'a' && c <= 'z')
			c -= ('a' - 'A');
		else if (c < 'A' || c > 'Z') {
			printf("\nSet_Block: wrong input data\n");
			exit(1);
		}

		int i = b - start, i2 = 0;

		while (i < n && i2 < l) {
			*(start + i) = c;
			i++;
			i2++;
		}

		if (i < l) {
			for (int i2 = 0; i2 < n && i < l; i2++, i++)
				*(start + i2) = c;
		}
	}
}

void Release_Block(char *b, long l) {
	if (l <= 0 || l > n || b == NULL) {
		printf("\nRelease_Block: wrong input data\n");
		exit(1);
	}
	else {
		int i = b - start, i2 = 0;

		while (i < n && i2 < l) {
			*(start + i) = 0;
			i++;
			i2++;
		}

		if (i < l) {
			for (int i2 = 0; i2 < n && i < l; i2++, i++)
				*(start + i2) = 0;
		}
	}
}

char* Relocate(void) {
	for (int i = 0; i < n; i++) {
		if (*(start + i) == 0) {
			for (int j = i; j < n - 1; j++) {
				*(start + j) = *(start + j + 1);
				*(start + j + 1) = 0;
			}
		}
	}

	for (int i = 0; i < n; i++) {
		if (*(start + i) == 0)
			return start + i;
	}

	return NULL;
}

void Process_Request(void) {
	int ch = getchar(), sign;
	long request;

	while (ch >= '0' && ch <= '9') {
		n *= 10;
		n += ch - '0';
		ch = getchar();
	}

	start = (char *)calloc(n, sizeof *start);
	actual = start;

	while (ch != EOF) {
		request = 0;
		sign = 1;
		ch = getchar();

		while (isspace(ch))
			ch = getchar();

		if (ch == EOF)
			return;

		if (ch == '-') {
			sign = -1;
			ch = getchar();
		}

		while (ch >= '0' && ch <= '9') {
			request *= 10;
			request += ch - '0';
			ch = getchar();
		}

		if (!request) {
			printf("\nProcess_Request: zero length blocks not allowed\n");
			exit(1);
		}
		else if (sign > 0) {
			actual = Assign_Block(request);

			if (actual == NULL) {
				actual = Relocate();
				actual = Assign_Block(request);
			}

			Set_Block(actual, request, ch);
		}
		else {
			actual = Find_Block(ch, request);
			
			if (actual == NULL) {
				actual = Relocate();
				actual = Find_Block(ch, request);
			}

			Release_Block(actual, request);
		}
	}
}

void Output_Buffer_State(void) {
	int amount;

	for (int i = 0; i < n; i++) {
		amount = 1;

		while (*(start + i) == *(start + i + 1)) {
			amount++;
			i++;
		}

		printf("%d%c ", amount, *(start + i) == 0 ? '*' : *(start + i));
	}
}

int main()
{
	Process_Request();
	Output_Buffer_State();

    return 0;
}

