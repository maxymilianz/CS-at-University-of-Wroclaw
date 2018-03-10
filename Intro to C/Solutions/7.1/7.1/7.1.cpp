// 7.1.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <stdlib.h>

typedef struct wezel
{
	int x;
	struct wezel *lewy, *prawy;
} WEZEL;

int iter = 0, steps;
WEZEL *temp;
WEZEL *nodes;

int szukaj(int a) {
	if (a == temp->x)
		return steps;
	else if (a < temp->x && temp->lewy != NULL) {
		temp = temp->lewy;
		steps++;
		return szukaj(a);
	}
	else if (a > temp->x && temp->prawy != NULL) {
		temp = temp->prawy;
		steps++;
		return szukaj(a);
	}
	else
		return -1;
}

void addToTree(int val, WEZEL *masterNode) {
	if (val < masterNode->x) {
		if (masterNode->lewy == NULL) {
			masterNode->lewy = &nodes[iter + 1];
			nodes[iter + 1].x = val;
			nodes[iter + 1].lewy = NULL;
			nodes[iter + 1].prawy = NULL;
			iter++;
		}
		else
			addToTree(val, masterNode->lewy);
	}
	else {
		if (masterNode->prawy == NULL) {
			masterNode->prawy = &nodes[iter + 1];
			nodes[iter + 1].x = val;
			nodes[iter + 1].lewy = NULL;
			nodes[iter + 1].prawy = NULL;
			iter++;
		}
		else
			addToTree(val, masterNode->prawy);
	}
}

int main()
{
	int n, val, q, question;
	printf("Podaj liczbe wezlow: ");
	scanf_s("%d", &n);
	nodes = (WEZEL*)malloc(sizeof *nodes * n);

	if (n > 0) {
		printf("Podaj wartosc 1 wezla: ");
		scanf_s("%d", &nodes[0].x);
		nodes[0].lewy = NULL;
		nodes[0].prawy = NULL;
		
		for (int i = 1; i < n; i++) {
			printf("Podaj wartosc %d wezla: ", i + 1);
			scanf_s("%d", &val);
			addToTree(val, &nodes[0]);
		}
	}

	printf("Podaj liczbe zapytan: ");
	scanf_s("%d", &q);

	for (int i = 0; i < q; i++) {
		printf("Podaj %d zapytanie: ", i + 1);
		scanf_s("%d", &question);
		temp = &nodes[0];
		steps = 0;
		printf("%d\n", szukaj(question));
	}

	free(nodes);

    return 0;
}

