class Collection
    class Elem
        def initialize(val)
            @val = val
            @next = nil
            @prev = nil
        end

        def next=(elem)
            @next = elem
        end

        def next
            @next
        end

        def prev=(elem)
            @prev = elem
        end

        def prev
            @prev
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
        elsif @first.val > val
            temp = @first
            @first.prev = @first
            @first = Elem.new val
            @first.next = temp
        else
            temp = @first
            temp = temp.next while temp.next != nil && temp.next.val < val
            temp2 = temp.next
            temp.next = Elem.new val
            temp.next.prev = temp
            temp.next.next = temp2
            temp2.prev = temp.next if temp2 != nil
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

    def printAll
        temp = @first

        while temp != nil
            print temp.val.to_s + " "
            temp = temp.next
        end

        print "\n"
    end
end

class Search
    def binary(coll, val)
        first = 0
        last = coll.length - 1

        while first != last
            if val <= coll.get((first + last) / 2)
                last = (first + last) / 2
            else
                first = (first + last) / 2 + 1
            end
        end

        if val == coll.get(first)
            first
        else
            nil
        end
    end

    def interpolation(coll, val)
        first = 0
        last = coll.length - 1

        while first != last && coll.get(first) != coll.get(last)
            middle = first + (val - coll.get(first)) / (coll.get(last) - coll.get(first)) * (last - first)

            if val <= coll.get(middle)
                last = middle
            else
                first = middle + 1
            end
        end

        if val == coll.get(first)
            first
        else
            nil
        end
    end
end

coll = Collection.new
puts "How many elements would You like to add to the collection?"
n = gets.chomp.to_i

n.times do |i|
    puts "Enter #{i}. value:"
    coll.add gets.chomp.to_i
end

coll.printAll

search = Search.new
puts "What value do You want to look for?"
val = gets.chomp.to_i
puts "#{search.binary coll, val}. element"
puts "#{search.interpolation coll, val}. element"
