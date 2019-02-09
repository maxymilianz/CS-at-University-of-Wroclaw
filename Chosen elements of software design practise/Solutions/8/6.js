const pgp = require('pg-promise')();


const database = pgp({
    host: 'localhost',
    port: 5432,
    database: 'postgres',
    user: 'postgres',
    password: '568923bbb'
});


function generate_line(id){
    if (id == 213714)
        return 'nextval(\'seq\'), true, \'Mlody G\', \'z Gdyni\'';

    const name = Math.random().toString(36).substring(5);
    const address = Math.random().toString(36).substring(5);
    return `nextval('seq'), true, ${name}, ${address}`;
}


function insert(i){
    database.none(`INSERT INTO public."PERSON" (id1, sex, name1, surname) VALUES (${generate_line(i)})`);
}


function insert_all() {
    [...Array(1).keys()].forEach((i) => insert(i));
}


async function main(){
    await insert_all();

    console.time("select");
    let res = await database.query(`SELECT * FROM public."PERSON" WHERE name1='Mlody G'`);
    console.timeEnd("select");

    console.log(res.rows);

    await database.none('CREATE INDEX i ON public."PERSON" (name1)');

    console.time("select");
    res = await database.query(`SELECT * FROM public."PERSON" WHERE name1='Mlody G'`);
    console.timeEnd("select");

    console.log(res.rows);
}


main();


// bez indeksu ok. 56 ms, z - 0,79