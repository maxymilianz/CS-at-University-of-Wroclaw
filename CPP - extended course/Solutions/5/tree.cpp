
#include "tree.h"

/*void recSubst(tree &t, const string &var, const tree &val) {
	if (!t.nrsubtrees() && t.functor() == var)
		t = val;
	
	for (size_t i = 0; i < t.nrsubtrees(); i++)
		recSubst(t[i], var, val);
}

tree subst(const tree &t, const string &var, const tree &val) {
	if (!t.nrsubtrees() && t.functor() == var)
		return tree(val);
	
	tree t2 = t;
	for (size_t i = 0; i < t.nrsubtrees(); i++)
		recSubst(t2[i], var, val);
	return t2;
}*/

void recSubst(tree &t, const string &var, const tree &val) {
	if (!t.nrsubtrees() && t.functor() == var)
		t = val;
	
	for (size_t i = 0; i < t.nrsubtrees(); i++) {
		tree t2 = t[i];
		recSubst(t2, var, val);
		t.replacesubtree(i, t2);
	}
}

tree subst(const tree &t, const string &var, const tree &val) {
	if (!t.nrsubtrees() && t.functor() == var)
		return tree(val);
	
	tree t2 = t;
	for (size_t i = 0; i < t.nrsubtrees(); i++)
		recSubst(t2[i], var, val);
	return t2;
}