const object = {
    foo: 'bar',
    baz: function (tuzza) {
        return tuzza + 'globale'
    },
    get outbreak() {
        return 'tt'
    },
    set tc(value) {
        object.foo = value
    }
};

console.log(object.baz('hc'), object.outbreak);
object.tc = '1337';
console.log(object.foo);

object.new_foo = '7312';
object.new_baz = function (tuzza) {
    return 'swizzy'
};
Object.defineProperty(object, 'br', {
    get : () => object.foo + 'rab',
    set : v => object.foo += v
});

console.log(object.new_foo, object.new_baz('p406'), object.br);
object.br = 'o co chodzi cale te';
console.log(object.foo);

// za pomocą Object.defineProperty można dodać do obiektu dowolną składową, a trzeba akcesory