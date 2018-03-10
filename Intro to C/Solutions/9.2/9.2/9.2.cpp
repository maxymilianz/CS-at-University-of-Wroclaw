// 9.2.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"

short j;
char word[1000] = { 0 };
int palindroms = 0;

char same(char ch1, char ch2) {
	if (ch1 <= 'Z')
		ch1 += 'a' - 'A';

	if (ch2 <= 'Z')
		ch2 += 'a' - 'A';

	if (ch1 == 'd' || ch1 == 'p')
		ch1 = 'b';
	else if (ch1 == 's')
		ch1 = 'g';
	else if (ch1 == 'y')
		ch1 = 'c';
	
	if (ch2 == 'd' || ch2 == 'p')
		ch2 = 'b';
	else if (ch2 == 's')
		ch2 = 'g';
	else if (ch2 == 'y')
		ch2 = 'c';

	if (ch1 == ch2)
		return 1;

	return 0;
}

void palindrom(short b, short e) {
	if (b + 1 < e && e < j) {
		short s = (e - b) / 2;

		for (short i = 0; i <= s; i++) {
			if (!same(word[b + i], word[e - i])) {
				palindrom(b, e + 1);
				return;
			}
		}

		palindroms++;
	}
	else if (e == j)
		palindrom(b + 1, b + 3);
}

int main()
{
	int n;
	scanf_s("%d", &n);
	char ch;
	ch = getchar();

	for (int i = 0; i < n; i++) {
		ch = getchar();

		for (j = 0; ch != '\n' && ch != EOF; j++) {
			word[j] = ch;
			ch = getchar();
		}

		palindrom(0, 2);

		for (j = 0; word[j] != 0; j++)
			word[j] = 0;
	}

	printf_s("%d\n", palindroms);

    return 0;
}

