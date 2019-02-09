def primes(n)
  (2..n).to_a.select { |a| (2..n).find_index { |d| (a % d).zero? } == a - 2 }
end

def decomposition(n)
  redundant = primes(n).map do |p|
    [p, (0..Math.log(n, p)).find_index { |e| (n % p ** e).nonzero? } - 1]
  end
  redundant.select { |a| a[1].nonzero? }
end

def proper_divisors(n)
  (1..n - 1).select { |d| (n % d).zero? }
end

def amicables(n)
  divisors = (0..n).map { |a| proper_divisors(a) }
  redundant = (1..n).map do |a|
    [a, (0..a - 1).find_index { |b| divisors[a].sum == b && divisors[b].sum == a }]
  end
  redundant.select { |pair| pair[1] }
end


decomposition(756).each { |a| print(a, "\n") }

amicables(1300).each { |a| print(a, "\n") }
