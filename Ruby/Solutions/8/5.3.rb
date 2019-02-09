# Modification of task 5.3 so it includes unit tests and documentation


require 'httparty'
require 'nokogiri'
require 'set'
require 'test/unit'


# Function computing distance between two pages (how many times you have to click a link to get from one to the other)
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


# Class for unit tests for distance function
class DistanceTests < Test::Unit::TestCase
  # Very standard test, which tests the most common case
  def test_success
    assert_equal(distance('https://www.ii.uni.wroc.pl/~marcinm/',
                          'https://tracker-zapisy.ii.uni.wroc.pl/', 3), 2)
  end

  # This method tests the case which should not 'work' but raise an exception
  def test_fail
    assert_raise do
      distance('https://www.ii.uni.wroc.pl/~marcinm/',
               'https://tracker-zapisy.ii.uni.wroc.pl/', 0)
    end
  end

  # Method testing the not-so-common case of destination url being same as the source url
  def test_same_url
    assert_equal(distance('thethirdwave.co', 'thethirdwave.co', 0), 0)
  end
end
