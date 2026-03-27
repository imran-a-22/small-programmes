# vocabulary_builder.rb
# Simple terminal-based vocabulary quiz for ed-tech portfolio use.

words = [
  { word: "benevolent", definition: "kind and generous" },
  { word: "diligent", definition: "hard-working and careful" },
  { word: "curious", definition: "eager to learn or know" },
  { word: "ancient", definition: "very old" },
  { word: "rapid", definition: "very fast" }
]

score = 0
puts "Vocabulary Builder"
puts "Type the correct word for each definition."
puts "-" * 40

words.each_with_index do |item, index|
  puts "Question #{index + 1}: Which word means '#{item[:definition]}'?"
  print "> "
  answer = STDIN.gets&.chomp

  if answer.nil?
    puts "No input received. Exiting."
    exit
  end

  if answer.strip.downcase == item[:word]
    puts "Correct!"
    score += 1
  else
    puts "Incorrect. The correct word was '#{item[:word]}'."
  end

  puts
end

puts "Quiz complete."
puts "Your score: #{score}/#{words.length}"

if score == words.length
  puts "Excellent work!"
elsif score >= 3
  puts "Good job. Keep practising."
else
  puts "Keep studying and try again."
end
