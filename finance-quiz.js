const readline = require("readline");

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

const quizQuestions = [
  {
    questionText: "What is profit?",
    possibleAnswers: {
      A: "Revenue - Costs",
      B: "Assets - Liabilities",
      C: "Cash inflow only",
      D: "Sales tax collected"
    },
    correctAnswer: "A"
  },
  {
    questionText: "What does break-even mean?",
    possibleAnswers: {
      A: "The business makes a large profit",
      B: "Revenue equals total costs",
      C: "Variable costs are zero",
      D: "The business has no fixed costs"
    },
    correctAnswer: "B"
  },
  {
    questionText: "Which of these is a fixed cost?",
    possibleAnswers: {
      A: "Raw materials per unit",
      B: "Sales commission per sale",
      C: "Monthly rent",
      D: "Packaging per product"
    },
    correctAnswer: "C"
  },
  {
    questionText: "What is revenue?",
    possibleAnswers: {
      A: "Money left after all costs",
      B: "Money earned from sales before costs",
      C: "Only the cash in the bank",
      D: "Tax paid by the business"
    },
    correctAnswer: "B"
  },
  {
    questionText: "What is profit margin?",
    possibleAnswers: {
      A: "Profit as a percentage of revenue",
      B: "Revenue as a percentage of assets",
      C: "Costs divided by units sold",
      D: "Fixed costs divided by revenue"
    },
    correctAnswer: "A"
  }
];

function ask(question) {
  return new Promise((resolve) => {
    rl.question(question, (answer) => resolve(answer.trim()));
  });
}

async function askYesNo(promptText) {
  while (true) {
    const input = (await ask(promptText)).toLowerCase();

    if (input === "yes" || input === "y") {
      return true;
    }

    if (input === "no" || input === "n") {
      return false;
    }

    console.log('Please respond with "yes" or "no".\n');
  }
}

async function askValidAnswer(promptText) {
  while (true) {
    const input = (await ask(promptText)).toUpperCase();

    if (["A", "B", "C", "D"].includes(input)) {
      return input;
    }

    console.log("Input is not valid. Please enter A, B, C, or D.\n");
  }
}

function showQuestion(questionObject, questionNumber, totalQuestions) {
  console.log(`\nQuestion ${questionNumber} of ${totalQuestions}`);
  console.log(questionObject.questionText);
  console.log(`A: ${questionObject.possibleAnswers.A}`);
  console.log(`B: ${questionObject.possibleAnswers.B}`);
  console.log(`C: ${questionObject.possibleAnswers.C}`);
  console.log(`D: ${questionObject.possibleAnswers.D}`);
}

async function runQuiz() {
  let score = 0;
  let currentQuestionIndex = 0;

  while (currentQuestionIndex < quizQuestions.length) {
    const currentQuestion = quizQuestions[currentQuestionIndex];

    showQuestion(
      currentQuestion,
      currentQuestionIndex + 1,
      quizQuestions.length
    );

    const userAnswer = await askValidAnswer("Enter your answer (A/B/C/D): ");

    if (userAnswer === currentQuestion.correctAnswer) {
      console.log("Correct!\n");
      score += 1;
    } else {
      const correctLetter = currentQuestion.correctAnswer;
      const correctText = currentQuestion.possibleAnswers[correctLetter];
      console.log(`Incorrect. The correct answer was ${correctLetter}: ${correctText}\n`);
    }

    currentQuestionIndex += 1;
  }

  const percentage = ((score / quizQuestions.length) * 100).toFixed(2);

  console.log("Quiz complete.");
  console.log(`You scored ${score} out of ${quizQuestions.length}.`);
  console.log(`Percentage: ${percentage}%\n`);
}

async function main() {
  console.log('Welcome to "Finance Quiz"\n');

  while (true) {
    const startQuiz = await askYesNo("Do you want to start the quiz? (yes/no): ");

    if (!startQuiz) {
      console.log("Ok, next time then.");
      break;
    }

    await runQuiz();

    const restartQuiz = await askYesNo("Do you want to restart the quiz? (yes/no): ");

    if (!restartQuiz) {
      console.log("Goodbye, until next time.");
      break;
    }

    console.log("");
  }

  rl.close();
}

main();