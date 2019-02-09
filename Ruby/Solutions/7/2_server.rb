require 'drb'
require 'set'


class ObjectsServer
  def initialize(marshal_path = '2_marshal.dat')
    @marshal_path = marshal_path

    @identifier_to_object = if File.exists?(marshal_path)
                              Marshal.load(File.binread(marshal_path))
                            else
                              {}
                            end
  end

  def store_object(object, id)
    @identifier_to_object[id] = object
    File.open(@marshal_path, 'wb') { |marshal| marshal.write(Marshal.dump(@identifier_to_object)) }
  end

  def restore_object(id)
    @identifier_to_object[id]
  end

  def delete_object(id)
    @identifier_to_object.delete(id)
    File.open(@marshal_path, 'wb') { |marshal| marshal.write(Marshal.dump(@identifier_to_object)) }
  end

  def state
    result = "<html>\n"

    @identifier_to_object.each do |identifier, object|
      result += "#{identifier}: #{object.class}\n<br>\n"

      object.instance_variables.each do |name|
        result += "#{name}: #{object.instance_variable_get(name)}\n<br>\n"
      end

      result += "<br>\n"
    end

    "#{result}</html>"
  end

  def search(methods)
    methods = Set.new(methods)
    result = Set.new

    @identifier_to_object.each_value do |object|
      result.add(object) if (methods - Set.new(object.methods)).empty?
    end

    result
  end
end


objects_server = ObjectsServer.new
DRb.start_service('druby://localhost:9000', objects_server)
DRb.thread.join
