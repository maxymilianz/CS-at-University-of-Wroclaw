require 'httparty'
require 'nokogiri'
require 'set'


class SearchEngine
  def index(start_url, depth)
    indexed = {}
    queue = [start_url]

    (depth + 1).times do
      new_queue = []

      queue.each do |url|
        next if indexed.include?(url)

        indexed[url] = Set.new

        begin
          page = Nokogiri::HTML(HTTParty.get(url))
          puts("Checking #{url}.")
          page.to_s.split(/[^a-z0-9]/).each do |word|
            indexed[url].add(word)
          end

          links = page.css('a[href]')
          links.map { |link| link['href'] }.each do |new_url|
            new_queue.push(new_url) unless indexed.include?(new_url)
          end
        rescue
          # could not open a page
        end
      end

      queue = new_queue
    end

    @indexed = indexed
  end

  def search_on_page(url, regular_expression)
    @indexed[url].any? { |word| !!(word =~ regular_expression) }
  end

  def search(regular_expression)
    @indexed.keys.select { |url| search_on_page(url, regular_expression) }
  end
end


time_before = Time.now

search_engine = SearchEngine.new
search_engine.index('http://spidersweb.pl', 1)
puts('notaword', search_engine.search(/notaword/))
puts('play', search_engine.search(/play/))

puts(Time.now - time_before)


# ~130 s
