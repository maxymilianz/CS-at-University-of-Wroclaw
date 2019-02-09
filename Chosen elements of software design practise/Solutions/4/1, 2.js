function Tree(value, left, right) {
    this.value = value;
    this.left = left;
    this.right = right;

    this.iterate = function* () {
        if (left)
            for (let value of left.iterate())
                yield value;

        yield value;

        if (right)
            for (let value of right.iterate())
                yield value;
    };

    this[Symbol.iterator] = this.iterate;

    this.toString = function () {
        return '(' + this.left + ' ' + this.value + ' ' + this.right + ')'
    };
}


const tree0 = new Tree(0, new Tree(-1));
const tree1 = new Tree(10, undefined, new Tree(11));
const tree2 = new Tree(20, new Tree(5, tree0, tree1), new Tree(21));

console.log(tree2.toString());

for (let value of tree2)
    console.log(value);