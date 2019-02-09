const pgp = require('pg-promise')();


const database = pgp({
    host: 'localhost',
    port: 5432,
    database: 'postgres',
    user: 'postgres',
    password: '568923bbb'
});


function select() {
    return database.any('SELECT * FROM public."PERSON"');
}


function insert() {
    return database.one('INSERT INTO public."PERSON" (id1, sex, name1, surname) VALUES (nextval(\'seq\'), true, \'belmondo\', \'gnocchi\') RETURNING id1');
}


function update() {
    database.none('UPDATE public."PERSON" SET sex = false where name1 = \'belmondo\'');
}


function delete_from_database() {
    return database.result('DELETE FROM public."PERSON" where name1 = \'belmondo\'')
}


async function main() {
    const deleted = await delete_from_database();
    console.log(deleted);
    const id = await insert();
    console.log(id);
    update();
    const persons = await select();
    console.log(persons);
}


main();