#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include "f-protot.h"

int main() {
	bool sprawdz = 1;
	sprawdz = input_and_check_data();

	if (!sprawdz)
		return 0;

	C_S();
	output_data();
}
