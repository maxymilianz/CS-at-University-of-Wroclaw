// 8.3.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <stdlib.h>

struct node {
	node *A = NULL, *B = NULL, *C = NULL, *D = NULL;		// upper left, right, lower left, right
	short val;
};

int n, iter, exp = 0, startX, startY, endX, endY, var = 0;
short image[1024][1024];
char request[100];
node *root;

void chooseFragment() {
	for (int i = 1; i <= exp; i++) {
		if (request[i] == 'A')
			root = root->A;
		else if (request[i] == 'B')
			root = root->B;
		else if (request[i] == 'C')
			root = root->C;
		else if (request[i] == 'D')
			root = root->D;
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

void negate(node *checked) {
	if (checked->A != NULL) {
		negate(checked->A);
		negate(checked->B);
		negate(checked->C);
		negate(checked->D);
	}
	else if (checked->val)
		checked->val = 0;
	else
		checked->val = 1;
}

void zeros(node *checked) {
	if (checked->A != NULL) {
		negate(checked->A);
		negate(checked->B);
		negate(checked->C);
		negate(checked->D);
	}
	else
		checked->val = 0;
}

void ones(node *checked) {
	if (checked->A != NULL) {
		negate(checked->A);
		negate(checked->B);
		negate(checked->C);
		negate(checked->D);
	}
	else
		checked->val = 1;
}

void checkers(node *checked) {
	
}

int variety(node *checked) {
	
}

int howManyToMalloc(int field) {
	int res = 1, pow = 1;

	while (pow <= field) {
		res += pow;
		pow *= 4;
	}

	return res;
}

int main()
{
	char ch;
	
	getchar();
	getchar();

	scanf_s("%d", &n);
	int m = n;
	int field = n * n;
	int amount = howManyToMalloc(field);
	node *nodes = (node *)malloc(sizeof node * amount);

	int i;

	for (i = 0; i < field; i++) {
		for (int j = 0; j < n; j++) {
			nodes[i].val = getchar();
		}

		ch = getchar();
	}

	field /= 4;

	// ASSIGN MASTER NODES TO THEIR CHILDREN AND OPTIONALLY GIVE THEM VALUE (IF ALL THE CHILDREN ARE THE SAME)

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

		*root = nodes[amount - 1];
		chooseFragment();

		if (request[0] == '*')
			rotate();
		else if (request[0] == '-')
			negate(root);
		else if (request[0] == '0')
			zeros(root);
		else if (request[0] == '1')
			ones(root);
		else if (request[0] == '=')
			printf("%d\n", variety(root));
		else if (request[0] == '#')
			checkers(root);
	}

    return 0;
}

