# geography_capital_quiz.exs
# A tiny capital city quiz in Elixir.

questions = [
  {"France", "Paris"},
  {"Japan", "Tokyo"},
  {"Brazil", "Brasilia"},
  {"Egypt", "Cairo"}
]

IO.puts("Geography Capital Quiz")

score =
  Enum.reduce(questions, 0, fn {country, capital}, acc ->
    answer =
      IO.gets("What is the capital of #{country}? ")
      |> to_string()
      |> String.trim()

    if String.downcase(answer) == String.downcase(capital) do
      IO.puts("Correct!\n")
      acc + 1
    else
      IO.puts("Not quite. Correct answer: #{capital}\n")
      acc
    end
  end)

IO.puts("Final score: #{score}/#{length(questions)}")
