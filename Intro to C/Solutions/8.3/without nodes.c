// 8.3.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"

int n, iter, exp = 0, startX, startY, endX, endY, var = 0;
short image[1024][1024];
char request[100];

void chooseFragment() {
	for (int i = 1; i <= exp; i++) {
		if (request[i] == 'A') {
			endX = (startX + endX) / 2;
			endY = (startY + endY) / 2;
		}
		else if (request[i] == 'B') {
			startX = (startX + endX) / 2 + 1;
			endY = (startY + endY) / 2;
		}
		else if (request[i] == 'C') {
			startX = (startX + endX) / 2 + 1;
			startY = (startY + endY) / 2 + 1;
		}
		else if (request[i] == 'D') {
			endX = (startX + endX) / 2;
			startY = (startY + endY) / 2 + 1;
		}
	}
}

void rotate() {
	int sup;

	for (int i = startX; i <= (startX + endX) / 2; i++) {
		for (int j = startY; j <= (startY + endY) / 2; j++) {
			sup = image[i][j];
			image[i][j] = image[j][endY - i];
			image[j][endY - i] = image[endX - i][endY - j];
			image[endX - i][endY - j] = image[endX - j][i];
			image[endX - j][i] = sup;
		}
	}
}

void negate() {
	for (int i = startX; i <= endX; i++) {
		for (int j = startY; j <= endY; j++) {
			if (image[startX][startY])
				image[startX][startY] = 0;
			else
				image[startX][startY] = 1;
		}
	}
}

void zeros() {
	for (int i = startX; i <= endX; i++) {
		for (int j = startY; j <= endY; j++) {
			image[startX][startY] = 0;
		}
	}
}

void ones() {
	for (int i = startX; i <= endX; i++) {
		for (int j = startY; j <= endY; j++) {
			image[startX][startY] = 1;
		}
	}
}

int round(int a) {
	while (a != 1 && a != 2 && a != 4 && a != 8 && a != 16 && a != 32 && a != 64 && a != 128 && a != 256 && a != 512)
		a--;

	return a;
}

void checkers() {
	
}

void variety(int xStart, int xEnd, int yStart, int yEnd) {
	var++;

	for (int i = xStart; i <= xEnd; i++) {
		for (int j = yStart; j <= yEnd; j++) {
			if (image[i][j] != image[xStart][yStart]) {
				i = round(i) - xStart;
				j = round(j) - yStart;
				variety(i, 2 * (i + xStart), j, 2 * (j + yStart));
			}
		}
	}
}

int main()
{
	int m, ch;
	
	getchar();
	getchar();

	scanf_s("%d", &n);
	m = n;

	for (int i = 0; i < n; i++) {
		for (int j = 0; j < n; j++) {
			image[i][j] = getchar();
		}

		ch = getchar();
	}

	while (m > 1) {
		exp++;
		m /= 2;
	}

	while (ch != EOF && ch != '.') {
		request[0] = ch;
		ch = getchar();
		iter = 1;

		while (ch != EOF && ch != '.' && ch != '\n') {
			request[iter] = ch;
			ch = getchar();
			iter++;
		}

		startX = 0, startY = 0, endX = n, endY = n;
		chooseFragment();

		if (request[0] == '*')
			rotate();
		else if (request[0] == '-')
			negate();
		else if (request[0] == '0')
			zeros();
		else if (request[0] == '1')
			ones();
		else if (request[0] == '=') {
			variety(startX, endX, startY, endY);
			printf("%d\n", var);
		}
		else if (request[0] == '#')
			checkers();
	}

    return 0;
}

