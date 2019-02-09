def primes(n)
  (2..n).to_a.select { |a| (2..n).find_index { |d| (a % d).zero? } == a - 2 }
end

def proper_divisors(n)
  (1..n - 1).select { |d| (n % d).zero? }
end

def perfects(n)
  (1..n).to_a.select { |a| proper_divisors(a).sum == a }
end


puts(primes(100))

puts(perfects(500))
