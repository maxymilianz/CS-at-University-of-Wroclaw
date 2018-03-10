// 10.2.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <math.h>

char n, j, word = 0, letter = 0;		// j - sumLength
char t[100][50] = { 0 };
char sum[50];
char length[100];
char attribution[10] = { 0 };

int solutions = 0;

void input() {
	scanf_s("%d", &n);
	char ch = getchar();

	while (ch == ' ')
		ch = getchar();

	for (char i = 0; i < n; i++) {
		j = 0;

		while (ch != ' ') {
			t[i][j] = ch;
			ch = getchar();
		}

		length[i] = j;

		while (ch == ' ')
			ch = getchar();
	}

	j = 0;

	while (ch != ' ' && ch != EOF) {
		sum[j] = ch;
		ch = getchar();
	}
}

char checkDigit(char letter) {
	for (char i = 0; i < 10; i++) {
		if (attribution[i] == letter)
			return i;
	}
}

void printResults() {
	if (solutions == 1) {
		for (char i = 0; i < 10; i++)
			printf_s("%d-%c ", i, attribution[i]);
	}
	else
		printf_s("%d\n", solutions);
}

char nextLetter() {
	char previousLetter = t[word][letter];
	letter++;

	if (t[word][letter]) {
		if (previousLetter != t[word][letter])
			return t[word][letter];
		else
			return nextLetter();
	}
	else {
		word++, letter = 0;
		if (t[word][letter]) {
			if (previousLetter != t[word][letter])
				return t[word][letter];
			else
				return nextLetter();
		}
		else
			printResults();
	}
}

char prevLetter() {
	char previousLetter = t[word][letter];
	letter--;

	if (t[word][letter]) {
		if (previousLetter != t[word][letter])
			return t[word][letter];
		else
			return prevLetter();
	}
	else {
		word--, letter = 49;

		while (!t[word][letter])
			letter--;

		if (t[word][letter]) {
			if (previousLetter != t[word][letter])
				return t[word][letter];
			else
				return prevLetter();
		}
		else
			printResults();
	}
}

void attributeAndCheck(char digit, char letter) {
	attribution[digit] = letter;

	int tempSum = 0;
	for (char i = 0; i < n; i++) {
		for (char j = 0; t[i][j] != 0; j++)
			tempSum += checkDigit(t[i][j]) * pow(10, length[i] - i);
	}

	int tempControlSum = 0;
	for (char i = 0; i < j; i++)
		tempControlSum += checkDigit(sum[i]) * pow(10, j - i);

	if (tempSum < tempControlSum) {
		if (digit < 9)
			attributeAndCheck(digit + 1, letter);
		else
			attributeAndCheck(1, nextLetter());
	}
	else if (tempSum > tempControlSum) {
		if (digit > 0)
			attributeAndCheck(digit - 1, letter);
		else
			attributeAndCheck(checkDigit(prevLetter()), prevLetter());
	}
	else {
		solutions++;

		if (checkDigit(t[0][0]) == 9)
			printResults();
	}
}

int main()
{
	input();
	attributeAndCheck(0, t[word][letter]);

    return 0;
}

