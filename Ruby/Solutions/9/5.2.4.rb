require 'tk'


class WordsStatistics
  def initialize
    @window = TkRoot.new { title("Words Statistics") }
    @entry = TkEntry.new(@window) do
      text("Filename")
      pack
    end
    @button = TkButton.new(@window) do
      text("Go!")
      pack
    end
    @button.command { words_statistics(@entry.value) }
    initialize_list(5)
  end

  def initialize_list(length)
    @list = []

    length.times do
      label = TkLabel.new(@window) { pack }
      @list.push(label)
    end
  end

  def words_statistics(filename)
    word_to_frequency = Hash.new(0)
    File.read(filename).gsub(/[^0-9A-Za-z]/, ' ').split
        .each { |word| word_to_frequency[word] += 1 }
    word_and_frequency = word_to_frequency.sort_by { |key_value| -key_value[1] }.to_a

    puts(word_and_frequency)

    @list.each_with_index do |label, index|
      label.text(word_and_frequency[index])
    end
  end
end


WordsStatistics.new
Tk.mainloop
