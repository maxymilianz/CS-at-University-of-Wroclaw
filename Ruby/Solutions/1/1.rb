def pascal(n)
  return if n.zero?

  puts(1)
  last_line = [1]

  (n - 1).times do
    new_line = last_line + [1]

    (1..(new_line.length - 2)).each do |i|
      new_line[i] += last_line[i - 1]
    end

    new_line.each do |x|
      print(x, ' ')
    end

    puts()
    last_line = new_line
  end
end

def dividers(n)
  result = []
  d = 2

  while n != 1
    if (n % d).zero?
      result += [d]

      n /= d while (n % d).zero?
    end

    d += 1
  end

  return result
end


pascal(5)

puts(dividers(1025))
