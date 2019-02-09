require 'drb'


objects_server = DRbObject.new_with_uri('druby://localhost:9000')

objects_server.store_object('Nie przeżył JK', 0)
jfk = objects_server.restore_object(0)
puts(jfk)

objects_server.store_object('Znów mam katar, walę kwasa', 1)
objects_server.delete_object(1)

puts(objects_server.state)
puts(objects_server.search([]))
