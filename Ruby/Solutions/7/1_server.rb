require 'drb'


class Log
  attr_reader :time, :program_identifier, :message

  def initialize(time, program_identifier, message)
    @time = time
    @program_identifier = program_identifier
    @message = message
  end

  def to_html
    "<div>\n#{@time}, #{@program_identifier} - #{@message}\n</div>"
  end
end


class LogServer
  def initialize(marshal_path = '1_marshal.dat')
    @marshal_path = marshal_path

    @logs_list = if File.exists?(marshal_path)
                   Marshal.load(File.binread(marshal_path))
                 else
                   []
                 end
  end

  def log_message(program_identifier, message)
    log = Log.new(Time.now, program_identifier, message)
    @logs_list.push(log)
    File.open(@marshal_path, 'wb') { |marshal| marshal.write(Marshal.dump(@logs_list)) }
  end

  def report(from_time, to_time, program_identifier, regular_expression)
    result = "<html>\n"

    @logs_list.each do |log|
      next unless from_time <= log.time && program_identifier == log.program_identifier && log.message =~ regular_expression
      break if to_time < log.time

      result += "#{log.to_html}\n"
    end

    "#{result}</html>"
  end
end


log_server = LogServer.new
DRb.start_service('druby://localhost:9000', log_server)
DRb.thread.join
