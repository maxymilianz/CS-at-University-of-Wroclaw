require_relative 'journal'

require 'date'


class EntryTests
  def self.append_to_file_test
    path = 'append_to_file_test.txt'

    file = File.open(path)
    content = file.read
    file.close

    entry = Entry.new(Date.today, 'foobar')
    entry.append_to_file(path)
    entry.append_to_file(path)

    file = File.open(path)

    raise 'Failure' if file.read != content + entry.to_s + entry.to_s
  end
end


class JournalTests
  def self.parameters_from_file_test
    raise 'Failure' if Journal.parameters_from_file('parameters_from_file_test.txt') != ['foo 0-10', 'bar 11-20']
  end

  def self.save_to_file_test
    journal = Journal.new(['foo', 'bar'], 'baz; qux')
    path = 'save_to_file_test.txt'
    journal.save_to_file(path)

    raise 'Failure' if journal.to_s != File.open(path).read
  end
end


def test_all
  EntryTests.append_to_file_test
  JournalTests.parameters_from_file_test
  JournalTests.save_to_file_test
end


test_all
