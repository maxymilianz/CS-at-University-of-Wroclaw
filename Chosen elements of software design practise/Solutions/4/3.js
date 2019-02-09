function Foo() {
    this.bar = (function () {
        function qux() {
            console.log('qux');
        }

        return () => {
            qux();
            console.log('bar');
        }
    })();
}


const foo = new Foo();
foo.bar();