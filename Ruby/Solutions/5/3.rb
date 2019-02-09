require 'httparty'
require 'nokogiri'
require 'set'


def distance(source, destination, max_depth)
  raise "Distance greater than max depth (#{max_depth})." if max_depth < 0

  if source == destination
    0
  else
    checked = Set[source]
    queue = [[source, 0]]

    while queue.any?
      url, depth = queue[0]
      queue = queue[1, queue.length]

      next if max_depth <= depth

      new_depth = depth + 1

      begin
        page = Nokogiri::HTML(HTTParty.get(url))
        links = page.css('a[href]')
        puts("Checking #{url}.")

        links.map { |link| link['href'] }.each do |new_url|
          return new_depth if new_url == destination
          next if checked.include?(new_url)

          checked.add(new_url)
          queue.push([new_url, new_depth])
        end
      rescue
        # could not open a page
      end
    end

    raise "Distance greater than max depth (#{max_depth})."
  end
end


# puts(distance('http://spidersweb.pl',
#               'https://www.spidersweb.pl/2018/11/skladany-ekran-samsunga-rozczarowanie.html', 10))

puts(distance('https://www.ii.uni.wroc.pl/~marcinm/',
              'https://tracker-zapisy.ii.uni.wroc.pl/', 3))
