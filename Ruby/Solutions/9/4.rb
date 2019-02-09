require 'set'
require 'tk'


class TicTacToe
  def initialize
    @window = TkRoot.new { title('Tic-tac-toe') }
    initialize_menu
    @label = TkLabel.new(@window) do
      grid(row: 1, column: 3)
      width(16)
    end
    new_game(:o)
  end

  def new_game(player)
    initialize_fields
    @turn = player
    @filled = 0
    initialize_board
    @label.text('')
  end

  def initialize_menu
    menu = TkMenu.new
    new_menu = TkMenu.new(menu)
    menu.add(:cascade, menu: new_menu, label: 'New game')
    new_menu.add(:command, label: 'o starts', command: proc { new_game(:o) })
    new_menu.add(:command, label: 'x starts', command: proc { new_game(:x) })
    @window.menu(menu)
  end

  def initialize_fields
    @fields = []

    3.times do |y|
      row = []

      3.times do |x|
        button = TkButton.new(@window) do
          grid(row: y, column: x)
          width(4)
          height(2)
        end
        button.command { click(y, x) }
        row.push(button)
      end

      @fields.push(row)
    end
  end

  def initialize_board
    @board = []
    3.times { |y| @board[y] = [nil] * 3 }
  end

  def winner
    # rows
    @board.each do |row|
      return row[0] if Set.new(row).length == 1 && row[0]
    end

    # columns
    3.times do |x|
      column = @board.map { |row| row[x] }
      return column[0] if Set.new(column).length == 1 && column[0]
    end

    # diagonals
    return @board[0][0] if Set.new([@board[0][0], @board[1][1], @board[2][2]]).length == 1 && @board[0][0]
    return @board[0][2] if Set.new([@board[0][2], @board[1][1], @board[2][0]]).length == 1 && @board[0][2]

    return "No one" if @filled == 9
  end

  def end_game(winner)
    return if winner.nil?

    @label.text("#{winner} wins!")
  end

  def click(y, x)
    return unless @board[y][x].nil?

    @fields[y][x].text(@turn)
    @board[y][x] = @turn
    @filled += 1
    end_game(winner)
    next_turn
  end

  def next_turn
    @turn = if @turn == :o
              :x
            else
              :o
            end
  end
end


TicTacToe.new
Tk.mainloop
