const pgp = require('pg-promise')();


const database = pgp({
    host: 'localhost',
    port: 5432,
    database: 'postgres',
    user: 'postgres',
    password: '568923bbb'
});


async function main() {
    const workplace_id = await database.one('INSERT INTO public."WORKPLACE_1" (address) VALUES (\'some address\') RETURNING id');
    console.log(workplace_id);
    const person_id = await database.one(`INSERT INTO public."WORKING_PERSON_1" (name) VALUES (\'oooooo\') RETURNING id`);
    console.log(person_id);
    const working_relation_id = await database.one(`INSERT INTO public."WORKING_RELATION" (id_person, id_workplace) VALUES (${person_id.id}, ${workplace_id.id}) RETURNING id`);
    console.log(working_relation_id);
}


main();