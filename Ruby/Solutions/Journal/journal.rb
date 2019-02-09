require 'date'


# Journal entry
class Entry
  def initialize(date, text)
    @date = date
    @text = text
  end

  # assumes the file under the provided path is a journal and doesn't check for correctness
  def append_to_file(path)
    file = File.open(path, 'a')
    file << to_s
    file.close
  end

  def to_s
    "#{@date}\n#{@text}"
  end
end


class Journal
  def initialize(parameters, entries = '')
    @parameters = parameters
    @entries = entries
  end

  # parameters are things user keeps track of, like their productivity or mood
  def self.parameters_from_file(path)
    File.open(path, 'r').each do |line|
      return line.strip.split(', ')
    end
  end

  def save_to_file(path)
    file = File.open(path, 'w')
    file.write(to_s)
    file.close
  end

  def to_s
    result = ''
    result += "#{@parameters.join(', ')}\n\n"
    result += @entries
    result
  end
end


def create_journal(path)
  separator = ','
  end_token = 'end'
  puts("Enter arbitrarily many lines of form 'parameter#{separator} scale' (e.g. 'productivity, 0-10'; at the end, type '#{end_token}' in a separate line):")
  parameters = []

  loop do
    line = gets.chomp
    break if line == end_token

    parameters += [line.split(separator).map { |parameter| parameter.strip }.join(' ')]
  end

  journal = Journal.new(parameters)
  journal.save_to_file(path)
end


# add entry to journal
def add_entry(path)
  puts('Enter the date in yyyy-mm-dd format (if not entered, defaults to today):')
  maybe_date = gets.chomp

  date = if maybe_date != ''
           Date.parse(maybe_date)
         else
           Date.today
         end

  end_token = 'end'
  puts("Enter your note line by line. Write '#{end_token}' in the last line.")
  text = ''

  loop do
    line = gets
    break if line.chomp == end_token

    text += line
  end

  puts('Enter the values of the given parameters on the given scales:')

  Journal.parameters_from_file(path).each do |parameter|
    puts(parameter)
    value = gets.chomp
    text += "#{parameter} - #{value}\n"
  end

  text += "\n"

  entry = Entry.new(date, text)
  entry.append_to_file(path)
end


# prompts user to write a note and create a journal if it a file at given path doesn't exist
def main
  default_path = 'journal.txt'
  puts("Enter the path of the journal file (if not entered, defaults to '#{default_path}'):")
  maybe_path = gets.chomp

  path = if maybe_path != ''
           maybe_path
         else
           default_path
         end

  create_journal(path) unless File.exist?(path)
  raise 'You provided a directory path!' unless File.file?(path)

  add_entry(path)
end


main
