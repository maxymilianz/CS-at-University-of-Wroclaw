class Task
  attr_reader :time

  def initialize(time, description)
    @time = time
    @description = description
  end

  def conflicts?(task)
    (@time - task.time).abs < 3600
  end

  def to_s
    "#{@description} at #{@time}"
  end
end

class Calendar
  def initialize
    @tasks = []
  end

  def find(task)
    # returns index to insert task at and array of conflicting tasks

    i = 0
    conflicts_list = []
    while i < @tasks.length && task.time < @tasks[i].time
      conflicts_list.push(@tasks[i]) if task.conflicts?(@tasks[i])
      i += 1
    end

    j = i
    while j < @tasks.length && task.conflicts?(@tasks[j])
      conflicts_list.push(@tasks[j])
      j += 1
    end

    [i, conflicts_list]
  end

  def insert(task)
    i, conflicts_list = find(task)
    @tasks.insert(i, task)
    puts("Conflict with #{conflicts_list.join(', ')}") unless conflicts_list
                                                              .empty?
  end

  def print
    puts(@tasks)
  end
end

def add_task(calendar)
  puts("Enter 'year month day hours minutes seconds' (You can omit as many arguments from the end as you want, if you don't enter any argument, the time will be current time).")
  time = gets.split.map(&:to_i)
  puts('Enter task description.')
  description = gets.chomp
  calendar.insert(Task.new(Time.new(*time), description))
end

def main
  calendar = Calendar.new

  loop do
    puts('To add new task, enter "a", to print all tasks, enter "p", to exit, enter "e".')
    command = gets.chomp

    case command
    when 'a'
      add_task(calendar)
    when 'p'
      calendar.print
    when 'e'
      break
    else
      puts('Wrong input!')
    end
  end
end

main
