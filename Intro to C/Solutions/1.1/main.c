#include "stdio.h"
#include <stdlib.h>
#include <math.h>

int main()
{
    double k = 0, k2;
    int n = 0;

    while (n < 100000000) {
        k += pow(-1, n) / pow(2 * n + 1, 2);
        printf("%d. %0.17f\n", n, k);
        n++;

        if (k == k2)
            break;

        k2 = k;
    }

    return 0;
}
