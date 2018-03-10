class Decrypted
    def initialize(string)
        @string = string
    end

    def encrypt(key)
        encrypted = ""
        @string.each_char { |ch| encrypted += key[ch] }
        Encrypted.new encrypted
    end

    def to_s
        @string
    end
end


class Encrypted
    def initialize(string)
        @string = string
    end

    def decrypt(key)
        decrypted = ""
        @string.each_char { |ch| decrypted += key.key ch }
        Decrypted.new decrypted
    end

    def to_s
        @string
    end
end

puts "Do You want to enter your key (k) or use the example from list (l)?"
ch = gets.chomp

if ch == 'k'
    dict = {}
    letters = "abcdefghijklmnopqrstuvwxyz"

    letters.each_char do |ch|
        puts "Enter value for '" + ch + "'"
        val = gets.chomp
        dict[ch] = val
    end

    puts "Enter string to encrypt:"
    string = gets.chomp
    dec = Decrypted.new string
    puts "Encrypted: " + dec.encrypt(dict)

    puts "Enter string to decrypt:"
    string = gets.chomp
    enc = Encrypted.new string
    puts "Decrypted: " + enc.decrypt(dict)
else
    dec = Decrypted.new 'ruby'
    puts "encrypted 'ruby': " + dec.encrypt({ 'a' => 'b', 'b' => 'r', 'r' => 'y', 'y' => 'u', 'u' => 'a' }).to_s
    enc = Encrypted.new 'ruby'
    puts "decrypted 'ruby': " + enc.decrypt({ 'a' => 'b', 'b' => 'r', 'r' => 'y', 'y' => 'u', 'u' => 'a' }).to_s
end
