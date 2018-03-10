#include <stdio.h>
#include <stdlib.h>
#include <limits.h>
#include <math.h>

int main()
{
    int m, p = 0, n = 0, j = 1;
    double pie, s = 0;
    scanf("%d", &m);
    m++;

    while (m < INT_MAX && m > 0) {
        pie = sqrt(m);
        s = 1;

        for (int i = 2; i <= pie; i++) {
            if (m % i == 0)
                s += i + m / i;

            if (i == pie)
                s -= pie;
        }

        if (s > m && m % 2 == 0 && p == 0) {
            p = m;
        } else if (s > m && m % 2 == 1 && n == 0) {
            n = m;
        }

        if (p != 0 && n != 0) {
            printf("%d %d\n", p, n);
            return 0;
        }

        m += j;
    }

    if (p == 0 && n == 0)
        printf("BRAK BRAK\n");
    else if (n == 0)
        printf("%d BRAK\n", p);
    else
        printf("BRAK %d\n", n);

    return 0;
}

/*Wskazówka: Jeœli liczba n dzieli siê przez k,
to dzieli siê równie¿ przez n/k
i jedna z tych liczb jest mniejsza b¹dŸ równa pierwiastkowi z n.*/
