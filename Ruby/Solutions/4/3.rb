class BinarySearchTree
  def initialize
    @root = nil
  end

  def insert(element)
    if @root.nil?
      @root = Node.new(element)
    else
      @root.insert(element)
    end
  end

  def exists?(element)
    if @root.nil?
      false
    else
      @root.exists?(element)
    end
  end

  def remove(element)
    return if @root.nil?

    if @root.value == element && @root.leaf?
      @root = nil
    else
      @root.remove(element)
    end
  end

  def to_s
    @root.to_s
  end
end


class Node
  attr_reader :value, :right, :left

  def initialize(element)
    @value = element
    @left = nil
    @right = nil
  end

  def insert(element)
    if element < @value
      if @left.nil?
        @left = Node.new(element)
      else
        @left.insert(element)
      end
    elsif @value < element
      if @right.nil?
        @right = Node.new(element)
      else
        @right.insert(element)
      end
    end
  end

  def exists?(element)
    !!(@value == element || (@left && @left.exists?(element)) || (@right && @right.exists?(element)))
  end

  def remove(element)
    if element < @value
      @left.remove(element) if @left
    elsif @value < element
      @right.remove(element) if @right
    else
      if @left.nil?
        @value = @right.value
        @left = @right.left
        @right = @right.right
      elsif @right.nil?
        @value = @left.value
        @left = @left.left
        @right = @left.right
      else
        if @left.right
          @value = @left.remove_and_return_rightmost
        else
          @value = @left.value
          @left = @left.left
        end
      end
    end
  end

  def remove_and_return_rightmost
    if @right && @right.right
      @right.remove_and_return_rightmost
    else
      element = @right.value

      if @right.left
        @right.value = @right.left.value
        @right.right = @right.left.right
        @right.left = @right.left.left
      else
        @right = nil
      end

      element
    end
  end

  def leaf?
    @left.nil? && @right.nil?
  end

  def to_s
    "(#{@left}, #{@value}, #{@right})"
  end
end


class Element
  attr_reader :value
  include(Comparable)

  def initialize(value)
    @value = value
  end

  def <=>(other)
    @value <=> other.value
  end
end


class StringBinarySearchTree < BinarySearchTree
  def insert(element)
    raise 'Wrong argument' unless element.instance_of?(String)

    super.insert(element)
  end

  def exists?(element)
    raise 'Wrong argument' unless element.instance_of?(String)

    super.exists?(element)
  end

  def remove(element)
    raise 'Wrong argument' unless element.instance_of?(String)

    super.remove(element)
  end
end


t = BinarySearchTree.new
puts(t)
t.insert(1)
puts(t)
t.insert(2)
puts(t)
t.insert(3)
puts(t)
t.insert(0)
puts(t)
t.remove(1)
puts(t)
puts(t.exists?(1))
puts(t.exists?(3))
puts(t.exists?(5))

st = StringBinarySearchTree.new
st.insert('a')
puts(st)
st.insert(1)
