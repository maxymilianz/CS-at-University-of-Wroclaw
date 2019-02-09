def words_statistics(filename)
  word_to_frequency = Hash.new(0)
  File.read(filename).gsub(/[^0-9A-Za-z]/, ' ').split
      .each { |word| word_to_frequency[word] += 1 }
  word_to_frequency
end


# print(words_statistics('test').sort_by { |key_value| -key_value[1] })


%w[burza dwaj-panowie-z-werony hamlet jak-wam-sie-podoba juliusz-cezar
   komedia-omylek krol-lear shakespeare-koriolan]
  .map { |title| "Szekspir/#{title}.txt" }
  .each do |filename|
  print(words_statistics(filename).sort_by { |key_value| -key_value[1] }
            .take(10), "\n\n")
end
