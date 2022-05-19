#include "util.h"

int cmpf(double a, double b){
	if (fabs(a-b) < EPS) return 0;
	if (a < b) return -1;
	return 1;
}