cat("=== Science Score Analyzer ===\n")
cat("This script summarises class scores and gives simple teaching insights.\n\n")

students <- data.frame(
  name = c("Amina", "Ben", "Chloe", "Dani", "Eli", "Farah"),
  score = c(88, 72, 91, 64, 79, 95)
)

average_score <- mean(students$score)
highest_score <- max(students$score)
lowest_score <- min(students$score)
pass_rate <- mean(students$score >= 70) * 100

cat("Student scores:\n")
print(students)
cat("\n")
cat("Average score:", round(average_score, 2), "\n")
cat("Highest score:", highest_score, "\n")
cat("Lowest score:", lowest_score, "\n")
cat("Pass rate (70 or above):", round(pass_rate, 2), "%\n\n")

cat("Teaching insight:\n")
if (average_score >= 85) {
  cat("The class is performing strongly overall. Introduce stretch questions.\n")
} else if (average_score >= 70) {
  cat("The class is doing reasonably well, but some targeted revision could help.\n")
} else {
  cat("The class needs reteaching on key concepts before moving on.\n")
}

low_performers <- students[students$score < 70, ]
if (nrow(low_performers) > 0) {
  cat("\nStudents who may need support:\n")
  print(low_performers)
}
