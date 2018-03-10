class Function
    def initialize(proc)
        @proc = proc
    end

    def value(x)
        @proc.call x
    end

    def zeros(a, b, e)
        sign = lambda { |x| x <=> 0 }
        list = []
        s = sign.call(value a)

        (a..b).step e do |x|
            if value(x) == 0 || s == -sign.call(value x)
                list.push x
            end

            s = sign.call(value x)
        end

        if (list != [])
            list
        else
            nil
        end
    end

    def field(a, b)
        field = 0
        precision = (b - a) / 1000.0

        (a...b).step precision do |x|
            field += (value(x) + value(x + precision)) / 2 * precision
        end

        field
    end

    def derivative(x)
        precision = 0.000000001
        (value(x + precision) - value(x)) / precision
    end

    def draw(width = 4, height = 4, x = -2, y = 2, precision = 2, freq = 0.01)     # left x, upper y, precision is nr of digits after comma, freq is the distance between 2 points
        text = "P1\n#{(width / freq).to_i} #{(height / freq).to_i}\n"

        (0...height).step freq do |v|
            (x...(x + width)).step freq do |a|
                if (y - v).round(precision) == (value a).round(precision)
                    text += '1 '
                else
                    text += '0 '
                end
            end

            text += "\n"
        end

        File.write('graph.pbm', text)
    end

    def gnuplot(width, x, freq)
        text = ''

        (x...(x + width)).step freq do |a|
            text += "#{a}\t\t#{value a}\n"
        end

        File.write('graph.gp', text)
    end
end

puts "Enter the code for the formula (the variable must be x):"
f = Function.new (eval "proc { |x| " + gets + " }")

puts "At what point would You like to see the value of the function?"
a = gets.chomp.to_f
puts f.value a

puts "What is the starting point for looking for 0s?"
a = gets.chomp.to_f
puts "What is the ending point for looking for 0s?"
b = gets.chomp.to_f
puts "What is the desired accuracy?"
e = gets.chomp.to_f
puts f.zeros a, b, e

puts "What is the starting point for calculating the field?"
a = gets.chomp.to_f
puts "What is the ending point for calculating the field?"
b = gets.chomp.to_f
puts f.field a, b

puts "At what point would You like to see the value of the derivative?"
a = gets.chomp.to_f
puts f.derivative a

puts "Do You want to give directions for drawing chart (d) or draw the default one (any other char)?"

if (gets.chomp == 'd')
    puts "How wide do You want the graph to be?"
    w = gets.chomp.to_f
    puts "How high do You want the graph to be?"
    h = gets.chomp.to_f
    puts "What is the starting x for drawing the graph?"
    x = gets.chomp.to_f
    puts "What is the starting y for drawing the graph?"
    y = gets.chomp.to_f
    puts "Enter the precision (nr of digits after comma, RECOMMENDED IS 2):"
    p = gets.chomp.to_f
    puts "Enter the frequency of generating new points (distance, RECOMMENDED IS 0.01):"
    freq = gets.chomp.to_f

    f.draw w, h, x, y, p, freq
    f.gnuplot w, x, freq
else
    puts f.draw
end
