const pgp = require('pg-promise')();


const database = pgp({
    host: 'localhost',
    port: 5432,
    database: 'postgres',
    user: 'postgres',
    password: '568923bbb'
});


async function main() {
    const workplace_id = await database.one('INSERT INTO public."WORKPLACE" (address) VALUES (\'some address\') RETURNING id');
    console.log(workplace_id);
    const person_id = await database.one(`INSERT INTO public."WORKING_PERSON" (name, id_workplace) VALUES (\'oooooo\', ${workplace_id.id}) RETURNING id`);
    console.log(person_id);
}


main();