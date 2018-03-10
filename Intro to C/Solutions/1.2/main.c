#include <stdio.h>
#include <stdlib.h>

int main()
{
    int m, n, p = 2;
    printf("Podaj liczbe >= 3: ");
    scanf("%d", &m);

    while (m < 3) {
        printf("Podaj liczbe >= 3: ");
        scanf("%d", &m);
    }

    printf("Podaj liczbe wieksza od poprzedniej: ");
    scanf("%d", &n);

    while (n <= m) {
        printf("Podaj liczbe wieksza od poprzedniej: ");
        scanf("%d", &n);
    }

    while (m%p == n%p) {
        p++;
    }

    printf("p = %d jest najmniejsza liczba taka, ze reszty z dzielenia m i n przez p sa rozne.", p);

    return 0;
}
