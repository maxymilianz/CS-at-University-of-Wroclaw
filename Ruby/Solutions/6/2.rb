class Track
  attr_reader :name, :artist

  def initialize(name, artist)
    @name = name
    @artist = artist
  end
end


class MusicCD
  def initialize(name, tracks)
    @name = name
    @tracks = tracks
  end

  def to_s
    result = "#{@name}: "
    @tracks.each do |track|
      result += "#{track.name} - #{track.artist}, "
    end
    result
  end
end


class Borrow
  attr_reader :return_date, :borrower

  def initialize(borrower, return_date)
    @borrower = borrower
    @return_date = return_date
  end

  def to_s
    "#{@borrower}, #{@return_date}"
  end
end
