class Puzzle
  attr_reader :cipher_text, :options, :answer_index, :hint

  def initialize(cipher_text, options, answer_index, hint)
    @cipher_text = cipher_text
    @options = options
    @answer_index = answer_index
    @hint = hint
  end
end

PUZZLES = [
  Puzzle.new("KHOOR", ["HELLO", "HOUSE", "HONEY", "HELIX"], 0, "A Caesar shift moved each letter three places forward."),
  Puzzle.new("VFKRRO", ["SPORT", "SCHOOL", "SCIENCE", "SUMMER"], 1, "Think about a shift of three again."),
  Puzzle.new("JDPH", ["GAME", "GATE", "GLOW", "GEAR"], 0, "Short word. Reverse a +3 shift."),
  Puzzle.new("FRGH", ["MATH", "BOOK", "CODE", "PLAY"], 2, "This word is common in programming."),
  Puzzle.new("OHDUQ", ["LEVEL", "LEARN", "LASER", "LUNCH"], 1, "It matches the theme of education."),
  Puzzle.new("SX]]OH", ["PUZZLE", "PLAYER", "POCKET", "PLANET"], 0, "Double letters stay double after shifting."),
]

def ask_choice(max)
  loop do
    print "Your choice: "
    input = gets&.strip
    next puts("Enter a number.") if input.nil? || input.empty?

    value = input.to_i
    return value - 1 if value.between?(1, max)

    puts "Choose a number between 1 and #{max}."
  end
end

puts "================================================"
puts "CODEBREAKER CIPHER ARENA"
puts "Decode Caesar-shift words to defeat the arena locks."
puts "================================================"

score = 0
streak = 0
mistakes = 0

PUZZLES.shuffle.each_with_index do |puzzle, index|
  puts "\nRound #{index + 1}"
  puts "Encrypted word: #{puzzle.cipher_text}"
  puzzle.options.each_with_index do |option, i|
    puts "#{i + 1}. #{option}"
  end
  puts "Hint: #{puzzle.hint}"

  choice = ask_choice(puzzle.options.length)

  if choice == puzzle.answer_index
    streak += 1
    gained = 10 + streak * 2
    score += gained
    puts "Correct. Combo streak: #{streak}. You gain #{gained} points."
  else
    mistakes += 1
    streak = 0
    puts "Incorrect. Correct answer: #{puzzle.options[puzzle.answer_index]}"
    puts "A Caesar cipher shifts letters by a fixed amount each time."
  end
end

puts "\n================================================"
puts "ARENA SUMMARY"
puts "Score: #{score}"
puts "Mistakes: #{mistakes}"
if score >= 70
  puts "Excellent pattern recognition."
elsif score >= 45
  puts "Strong work. Your cipher intuition is improving."
else
  puts "Good start. Try again and look for repeated letter movement."
end
puts "================================================"
