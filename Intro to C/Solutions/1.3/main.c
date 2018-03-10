#include <stdio.h>
#include <stdlib.h>
#include <limits.h>

int main()
{
    int m, a = 1;
    long long int s;
    scanf("%d", &m);

    for (unsigned int i = m + 1; i < INT_MAX; i += a) {
        /*if (i < 0) {
            printf("BRAK");

            if (a == 1) {
                printf(" BRAK\n");
                return 0;
            }
        }*/

        if (a == 3)
            return 0;

        s = 0;

        for (unsigned int j = 1; j < i; j++) {
            if (i % j == 0)
                s += j;
        }

        if (s > i) {
            if (a == 3) {
                printf("%d\n", i);
                return 0;
            }

            printf("%d ", i);
            a++;
            i++;
        }
    }

    printf("BRAK");

    if (a == 1)
        printf(" BRAK");

    printf("\n");

    return 0;
}
