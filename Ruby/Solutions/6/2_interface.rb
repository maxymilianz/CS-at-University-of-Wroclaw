require_relative '2'
require 'date'


def read_track
  puts('Please enter the tracks name, Sir:')
  name = gets.strip
  puts('Now please enter the artist(s):')
  artist = gets.strip
  Track.new(name, artist)
end

def read_borrow
  puts('Has anyone borrowed this CD? (y/n)')
  borrowed = gets.strip

  if borrowed == 'y'
    puts('Who that motherfucker was? Lemme deal with him!')
    borrower = gets.strip
    puts('When is the last day he can still listen to your CD and be alive, Great Lord? (yyyy-mm-dd)')
    return_date = Date.parse(gets.strip)
    Borrow.new(borrower, return_date)
  elsif borrowed == 'n'
    puts('Understandable, have a great day.')
    nil
  end
end

def add_cd(database)
  puts('Enter CDs name:')
  name = gets.strip
  tracks = []

  loop do
    puts('Have You already entered all the tracks? (y/n)')
    all_tracks = gets.strip

    if all_tracks == 'y'
      break
    elsif all_tracks == 'n'
      tracks.push(read_track)
    else
      puts('Da fuq You\'re sayin nigga?')
    end
  end

  borrow = read_borrow
  database[MusicCD.new(name, tracks)] = borrow
end

def remove_cd(database)
  database.keys.each_with_index do |cd, index|
    puts("#{index}:\n#{cd};\n")
  end

  puts('Which CD do You want to delete?')
  index = Integer(gets.strip)
  database.delete(database.keys[index])
end

def print_all(database)
  puts("You have the following CDs, lord:\n")
  database.each do |cd, borrow|
    if borrow
      puts("#{cd}\nborrowed by #{borrow.borrower} to #{borrow.return_date};\n")
    else
      puts("#{cd}\n\n")
    end
  end
end

def print_late(database)
  today = Date.today

  database.each do |cd, borrow|
    if borrow && borrow.return_date < today
      puts("#{cd}\n#{borrow.borrower} should have returned it till #{borrow.return_date}, now You should hammer this mole back to his mound!")
    end
  end
end

def repl(database)
  loop do
    puts('Enter \'a\' to add a new CD,
\'r\' to remove one,
\'p\' to print information about all CDs,
\'l\' to print information about CDs which should have already been returned,
but apparently the borrowers don\'t value their lives too much,
or \'e\' to exit.')
    operation = gets.strip

    case operation
    when 'a'
      add_cd(database)
    when 'r'
      remove_cd(database)
    when 'p'
      print_all(database)
    when 'l'
      print_late(database)
    when 'e'
      break
    else
      puts('I don\'t know what You\'re saying.')
    end
  end

  database
end


default_database_path = '2.dat'
puts("Enter database path (if empty string entered, default is #{default_database_path}):")
database_path = gets.strip
database_path = default_database_path if database_path == ''
database = if File.exist?(database_path)
             Marshal.load(File.binread(database_path))
           else
             {}
           end
File.open(database_path, 'wb') do |file|
  file.write(Marshal.dump(repl(database)))
end
