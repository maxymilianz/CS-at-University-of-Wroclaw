require 'date'
require 'open-uri'
require 'tk'
require 'zip'


# works only for 2018, because the earlier years URIs are stupid
class WeatherApp
  def initialize
    @filenames_prefix = 'data/'

    @base_url = 'https://dane.imgw.pl/data/dane_pomiarowo_obserwacyjne/dane_meteorologiczne/dobowe/synop/'
    @moths_back = 10

    @window = TkRoot.new
    @window.title('Weather App')

    from_label = TkLabel.new(@window)
    from_label.text("From or plot this day on last #{@moths_back} months: (yyyy-mm-dd)")
    from_label.grid(column: 0, row: 0)

    @from_entry = TkEntry.new(@window)
    @from_entry.grid(column: 1, row: 0)

    to_label = TkLabel.new(@window)
    to_label.text('To: (yyyy-mm-dd)')
    to_label.grid(column: 2, row: 0)

    @to_entry = TkEntry.new(@window)
    @to_entry.grid(column: 3, row: 0)

    @plot_button = TkButton.new(@window)
    @plot_button.text('Plot')
    @plot_button.command { plot }
    @plot_button.grid(column: 4, row: 0)

    @plot_1_day_button = TkButton.new(@window)
    @plot_1_day_button.text('Plot 1 day')
    @plot_1_day_button.command { plot_1_day }
    @plot_1_day_button.grid(column: 5, row: 0)
  end

  def plot
    from = Date.parse(@from_entry.value)
    to = Date.parse(@to_entry.value)

    return if to < from

    ensure_data_available(from, to)

    `python plot.py #{from} #{to}`
  end

  def plot_1_day
    date = Date.parse(@from_entry.value)
    current_date = date
    puts(date)

    10.times do
      ensure_day_available(current_date)
      current_date = current_date.prev_month
    end

    `python plot.py #{date}`
  end

  def ensure_data_available(from, to)
    from.upto(to) { |date| ensure_day_available(date) }
  end

  def ensure_day_available(date)
    return if File.file?(date_to_filename(date))

    zip_filename = date_to_zip_filename(date)
    open(zip_filename, 'wb') { |file| file << open(date_to_url(date)).read }

    Zip::File.open(zip_filename) do |zip_file|
      zip_file.each do |file|
        filename = date_to_filename(date)
        zip_file.extract(file, filename) if file.name == filename
      end
    end
  end

  def date_to_filename(date)
    "s_d_t_#{date.month >= 10 ? date.month : "0#{date.month}"}_#{date.year}.csv"
  end

  def date_to_url(date)
    "#{@base_url}#{date.year}/#{date.year}_#{date.month >= 10 ? date.month : "0#{date.month}"}_s.zip"
  end

  def date_to_zip_filename(date)
    "#{date.year}_#{date.month >= 10 ? date.month : "0#{date.month}"}_s.zip"
  end
end


WeatherApp.new
Tk.mainloop
