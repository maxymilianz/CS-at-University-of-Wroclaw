class Collection
    class Elem
        def initialize(val)
            @val = val
            @next = nil
        end

        def next=(elem)
            @next = elem
        end

        def next
            @next
        end

        def val=(val)
            @val = val
        end

        def val
            @val
        end
    end

    def initialize
        @first = nil
        @last = nil
        @length = 0
    end

    def add(val)
        @length += 1

        if @first == nil
            @first = Elem.new val
            @last = @first
        else
            @last.next = Elem.new val
            @last = @last.next
        end
    end

    def get(i)
        if i < length
            temp = @first
            i.times { temp = temp.next }
            temp.val
        else
            nil
        end
    end

    def length
        @length
    end

    def swap(i, j)
        if i > j
            temp = i
            i = j
            j = temp
        end

        if i < j && j < @length
            tempI = @first
            i.times { tempI = tempI.next }
            tempJ = tempI
            i.upto(j - 1) { tempJ = tempJ.next }

            temp = tempI.val
            tempI.val = tempJ.val
            tempJ.val = temp
        end
    end

    def printAll
        temp = @first

        while temp != nil
            print temp.val.to_s + " "
            temp = temp.next
        end

        print "\n"
    end
end

class Sort
    def selection(coll)
        0.upto(coll.length - 1) do |i|
            temp = i
            i.upto(coll.length - 1) { |j| temp = j if coll.get(temp) > coll.get(j) }
            coll.swap i, temp
        end
    end

    def bubble(coll)
        sorted = false

        while !sorted
            sorted = true

            0.upto(coll.length - 2) do |i|
                if coll.get(i) > coll.get(i + 1)
                    sorted = false
                    coll.swap i, i + 1
                end
            end
        end
    end
end

# design pattern strategy

coll = Collection.new
puts "How many elements would You like to add to the collection?"
n = gets.chomp.to_i

n.times do |i|
    puts "Enter #{i}. value:"
    coll.add gets.chomp.to_i
end

coll.printAll
puts "Collection length: #{coll.length}"

puts "Which elements would You like to swap?"
n = gets.chomp.to_i
m = gets.chomp.to_i
coll.swap n, m
coll.printAll

puts "Which element would You like to display?"
puts coll.get gets.chomp.to_i

sort = Sort.new
puts "Would You like to sort the collection with selection sort (s) or bubble sort (b)?"
ch = gets.chomp

if ch == 's'
    sort.selection coll
else
    sort.bubble coll
end

coll.printAll

# selection sort is almost 2 times faster than bubble sort

sort = Sort.new
big = Collection.new
0.upto(500) { big.add rand(200) }

time = Time.new
sort.selection big
time2 = Time.new
puts "Selection sort took #{time2 - time} s"

big = Collection.new
0.upto(500) { big.add rand(200) }

time = Time.new
sort.bubble big
time2 = Time.new
puts "Bubble sort took #{time2 - time} s"
