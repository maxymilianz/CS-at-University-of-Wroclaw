#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#define ROZMIAR 10000

int n, m;
int A[ROZMIAR];
int mniejsze[ROZMIAR];
int rowne[ROZMIAR];
int B[ROZMIAR];

void C_K_E();
void C_K_L();
void Reorg();
void C_S();
bool input_and_check_data();
void output_data();
