class Expression

end


class Constant < Expression
  def initialize(value)
    @value = value
  end

  def compute(_environment)
    @value
  end

  def simplify
    self
  end

  def to_s
    @value.to_s
  end
end


class Variable < Expression
  def initialize(name)
    @name = name
  end

  def compute(environment)
    environment[@name]
  end

  def simplify
    self
  end

  def to_s
    @name
  end
end


class Negation < Expression
  def initialize(expression)
    @expression = expression
  end

  def compute(environment)
    -@expression.compute(environment)
  end

  def simplify
    simplified = @expression.simplify

    if simplified.instance_of?(Constant)
      value = simplified.compute({})

      if value < 0
        Constant.new(-value)
      else
        self
      end
    else
      self
    end
  end
end


class BinaryExpression < Expression
  def initialize(expression0, expression1)
    @expression0 = expression0
    @expression1 = expression1
  end
end


class Addition < BinaryExpression
  def compute(environment)
    @expression0.compute(environment) + @expression1.compute(environment)
  end

  def simplify
    simplified0 = @expression0.simplify
    simplified1 = @expression1.simplify

    if simplified0.instance_of?(Constant)
      if simplified1.instance_of?(Constant)
        Constant.new(simplified0.compute({}) + simplified1.compute({}))
      elsif simplified0.compute({}).zero?
        simplified1
      else
        Addition.new(simplified0, simplified1)
      end
    elsif simplified1.instance_of?(Constant) && simplified1.compute({}).zero?
      simplified0
    else
      Addition.new(simplified0, simplified1)
    end
  end

  def to_s
    "#{@expression0} + #{@expression1}"
  end
end


class Subtraction < BinaryExpression
  def compute(environment)
    @expression0.compute(environment) - @expression1.compute(environment)
  end

  def simplify
    simplified0 = @expression0.simplify
    simplified1 = @expression1.simplify

    if simplified0.instance_of?(Constant)
      if simplified1.instance_of?(Constant)
        Constant.new(simplified0.compute({}) - simplified1.compute({}))
      elsif simplified0.compute({}).zero?
        Negation.new(simplified1).simplify
      else
        Subtraction.new(simplified0, simplified1)
      end
    elsif simplified1.instance_of?(Constant) && simplified1.compute({}).zero?
      simplified0
    else
      Subtraction.new(simplified0, simplified1)
    end
  end

  def to_s
    "#{@expression0} - #{@expression1}"
  end
end


class Multiplication < BinaryExpression
  def compute(environment)
    @expression0.compute(environment) * @expression1.compute(environment)
  end

  def simplify
    simplified0 = @expression0.simplify
    simplified1 = @expression1.simplify

    if simplified0.instance_of?(Constant)
      if simplified1.instance_of?(Constant)
        Constant.new(simplified0.compute({}) * simplified1.compute({}))
      elsif simplified0.compute({}).zero?
        Constant.new(0)
      elsif simplified0.compute({}) == 1
        simplified1
      else
        Multiplication.new(simplified0, simplified1)
      end
    elsif simplified1.instance_of?(Constant)
      if simplified1.compute({}).zero?
        Constant.new(0)
      elsif simplified1.compute({}) == 1
        simplified0
      else
        Multiplication.new(simplified0, simplified1)
      end
    else
      Multiplication.new(simplified0, simplified1)
    end
  end

  def to_s
    "#{@expression0} * #{@expression1}"
  end
end


class Division < BinaryExpression
  def compute(environment)
    @expression0.compute(environment) / @expression1.compute(environment)
  end

  def simplify
    simplified0 = @expression0.simplify
    simplified1 = @expression1.simplify

    if simplified0.instance_of?(Constant)
      if simplified1.instance_of?(Constant)
        Constant.new(simplified0.compute({}) / simplified1.compute({}))
      elsif simplified0.compute({}).zero?
        Constant.new(0)
      else
        Division.new(simplified0, simplified1)
      end
    elsif simplified1.instance_of?(Constant) && simplified1.compute({}) == 1
      simplified0
    else
      Division.new(simplified0, simplified1)
    end
  end

  def to_s
    "#{@expression0} / #{@expression1}"
  end
end


a = Addition.new(Constant.new(21), Constant.new(37))
puts(a.simplify)

b = Subtraction.new(a, Multiplication.new(Constant.new(14), Variable.new('x')))
puts(b)

c = Multiplication.new(Constant.new(1998), Negation.new(Variable.new('ex')))
puts(c.compute('ex' => 1997))
