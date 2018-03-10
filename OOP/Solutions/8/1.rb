class Fixnum
    def factors
        fac = []
        root = Math.sqrt self

        1.upto(root) do |i|
            if self % i == 0
                fac << i
                fac << self / i if (i != self / i)
            end
        end

        fac
    end

    def ack(n)
        if self == 0
            n + 1
        elsif n == 0
            (self - 1).ack 1
        else
            (self - 1).ack(ack(n - 1))
        end
    end

    def perfect
        sum = -self
        factors.each { |a| sum += a }
        sum == self
    end

    def verbose
        dict = { 0 => 'zero ',
                1 => 'one ',
                2 => 'two ',
                3 => 'three ',
                4 => 'four ',
                5 => 'five ',
                6 => 'six ',
                7 => 'seven ',
                8 => 'eight ',
                9 => 'nine ' }
        digits = []
        nr = self
        words = ''

        if nr < 0
            words += 'minus '
            nr *= -1
        end

        while nr != 0 do
            digits << nr % 10
            nr /= 10
        end

        digits.reverse.each { |n| words += dict[n] }
        words
    end
end

print "What number's factors would You like to see?\n"
n = gets
print n.to_i.factors, "\n"

print "What numbers would You like to calculate the Ackerman function on?\n"
n = gets
print "And what is the argument?\n"
m = gets
puts n.to_i.ack(m.to_i)

print "What number would You like to check if it is perfect?\n"
n = gets
puts n.to_i.perfect

print "What number would You like to verbose?\n"
n = gets
puts n.to_i.verbose
