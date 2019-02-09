class Person
  def initialize(nick, phone_number, email_address)
    @nick = nick
    save_phone_number(phone_number)
    save_email_address(email_address)
  end

  def save_phone_number(phone_number)
    raise 'Wrong phone number, you fool!' unless phone_number =~ /^\d+$/

    @phone_number = phone_number
  end

  def save_email_address(email_address)
    raise 'Wrong email address, you fool!' unless email_address =~ /^[a-zA-Z\d_]+@[a-zA-Z\d_]+(.[a-zA-Z\d_]+)+$/

    @email_address = email_address
  end

  def to_s
    "#{@nick}, #{@phone_number}, #{@email_address}"
  end
end
