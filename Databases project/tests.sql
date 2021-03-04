{"leader": {"timestamp": 1557473000, "password": "abc", "member": 1}}
{"leader": {"timestamp": 1557473004, "password": "kot", "member": 2}}
{"leader": {"timestamp": 1557473008, "password": "123", "member": 3}}

-- poprawne dodanie akcji
{"protest": {"timestamp": 1557475700, "password": "123", "member": 3, "action": 500, "project": 5000, "authority": 10000}}
{"support": {"timestamp": 1557475701, "password": "123", "member": 3, "action": 600, "project": 5000}}
-- tworzymy tylko nowy projekt, authority to samo
{"support": {"timestamp": 1557475701, "password": "abc", "member": 1, "action": 601, "project": 5001, "authority": 10000}}
{"support": {"timestamp": 1557475701, "password": "abc", "member": 1, "action": 602, "project": 5002, "authority": 10001}}
-- uzytkownik nie istnieje, wiec dodany nowy
{"support": {"timestamp": 1557475701, "password": "cztery", "member": 4, "action": 700, "project": 5000}}
{"protest": {"timestamp": 1557475721, "password": "piec", "member": 5, "action": 701, "project": 5000}}


-- złe hasło
{"support": {"timestamp": 1557475701, "password": "456", "member": 3, "action": 700, "project": 5000}}
-- id akcji zajete
{"support": {"timestamp": 1557475701, "password": "cztery", "member": 4, "action": 600, "project": 5000}}
-- wymagane authority, bo trzba stworzyć projekt
{"support": {"timestamp": 1557475701, "password": "cztery", "member": 4, "action": 600, "project": 6000}}

-- nie ma takiego authority -> []
{"projects": {"timestamp": 1557475795, "password": "abc", "member": 1, "authority": 2}}
-- poprawne, zwróci 2 projekty
{"projects": {"timestamp": 1557475795, "password": "abc", "member": 1, "authority": 10000}}
-- zwróci 3 projekty
{"projects": {"timestamp": 1557475795, "password": "abc", "member": 1}}
-------------------------------
-- testy zaliczone
-------------------------------
-- poprawne dodawane głosy
{ "upvote": { "timestamp": 1557475712, "password": "kot", "member": 2, "action":500}}
{ "downvote": { "timestamp": 1557475713, "password": "abc", "member": 1, "action":500}}
{ "downvote": { "timestamp": 1557475713, "password": "123", "member": 3, "action":500}}
{ "downvote": { "timestamp": 1557475713, "password": "cztery", "member": 4, "action":500}}
{ "upvote": { "timestamp": 1557475713, "password": "cztery", "member": 4, "action":601}}
{ "downvote": { "timestamp": 1557475714, "password": "abc", "member": 1, "action":600}}

-- member juz oddał inny głos na tę akcję
{ "upvote": { "timestamp": 1557475714, "password": "abc", "member": 1, "action":600}}
-- taka akcja nie istnieje
{ "upvote": { "timestamp": 1557475715, "password": "123", "member": 3, "action":699}}
-------------------------------
-- testy zaliczone
-------------------------------
-- wszystkie akcje(6)
{"actions": {"timestamp": 1557475796, "password": "abc", "member": 1}}
-- akcje typu support(4)
{"actions": {"timestamp": 1557475796, "password": "abc", "member": 1, "type": "support"}}
-- akcje dla danego projektu(4)
{"actions": {"timestamp": 1557475796, "password": "abc", "member": 1, "project": 5000}}
-- akcje typy support dla danego projektu(2)
{"actions": {"timestamp": 1557475796, "password": "abc", "member": 1, "type": "support", "project": 5000}}
-- akcje dla danego authority(5)
{"actions": {"timestamp": 1557475796, "password": "abc", "member": 1, "authority": 10000}}

-- za dużo argumentów
{"actions": {"timestamp": 1557475796, "password": "abc", "member": 1, "project": 5000, "authority": 10000}}
-- authorityId nie nalezy do authority
{"actions": {"timestamp": 1557475796, "password": "abc", "member": 1, "authority": 2}}
-------------------------------
-- testy zaliczone
-------------------------------
-- wszytskie głosy
{ "votes": { "timestamp": 1557475715, "password": "abc", "member": 1}} 
-- głosy filtrowane po akcji
{ "votes": { "timestamp": 1557475715, "password": "abc", "member": 1, "action":500}}
-- głosy filtrowane po projekcie
{ "votes": { "timestamp": 1557475715, "password": "abc", "member": 1, "project": 5001}}

-- próba filtrowania głosów po id member jako id projektu
{ "votes": { "timestamp": 1557475715, "password": "abc", "member": 1, "project": 2}}
-------------------------------
-- testy zaliczone
-------------------------------
{ "trolls": { "timestamp": 1557477055 }}