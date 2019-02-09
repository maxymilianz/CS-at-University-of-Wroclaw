require_relative '3'


def add_person(database)
  puts('Enter persons nick:')
  nick = gets.strip
  puts('Enter their phone number:')
  phone_number = gets.strip
  puts('Enter their email address:')
  email_address = gets.strip
  database.push(Person.new(nick, phone_number, email_address))
end

def remove_person(database)
  database.each_with_index { |person, index| puts("#{index}: #{person}\n") }
  puts('Which person do You want to erase from the history?')
  index = Integer(gets.strip)
  database.delete_at(index)
end

def print_all(database)
  database.each { |person| puts(person) }
  puts
end

def repl(database)
  loop do
    puts('Enter \'a\' to add a person,
\'r\' to remove one,
\'p\' to print information about all persons,
or \'e\' to exit.')
    operation = gets.strip

    case operation
    when 'a'
      add_person(database)
    when 'r'
      remove_person(database)
    when 'p'
      print_all(database)
    when 'e'
      return database
    else
      puts('I don\'t know what You\'re saying.')
    end
  end
end


default_database_path = '3.dat'
puts("Enter database path (if empty string entered, default is #{default_database_path}):")
database_path = gets.strip
database_path = default_database_path if database_path == ''
database = if File.exist?(database_path)
             Marshal.load(File.binread(database_path))
           else
             []
           end
File.open(database_path, 'wb') do |file|
  file.write(Marshal.dump(repl(database)))
end
