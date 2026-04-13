#include <iostream>
#include <limits>
#include <random>
#include <string>

struct Question {
    std::string prompt;
    int answer;
    std::string lesson;
};

int askInt(const std::string& message, int minValue, int maxValue) {
    while (true) {
        std::cout << message;
        int value;
        if (std::cin >> value && value >= minValue && value <= maxValue) {
            return value;
        }
        std::cout << "Invalid input. Enter a number from " << minValue << " to " << maxValue << ".\n";
        std::cin.clear();
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
    }
}

Question makeQuestion(std::mt19937& rng) {
    std::uniform_int_distribution<int> bitDist(0, 1);
    std::uniform_int_distribution<int> gateDist(0, 6);
    int a = bitDist(rng);
    int b = bitDist(rng);

    switch (gateDist(rng)) {
        case 0: return {"Gate: AND | Inputs: " + std::to_string(a) + ", " + std::to_string(b), a && b, "AND returns 1 only when both inputs are 1."};
        case 1: return {"Gate: OR  | Inputs: " + std::to_string(a) + ", " + std::to_string(b), a || b, "OR returns 1 when at least one input is 1."};
        case 2: return {"Gate: XOR | Inputs: " + std::to_string(a) + ", " + std::to_string(b), a ^ b, "XOR returns 1 when the inputs are different."};
        case 3: return {"Gate: NAND | Inputs: " + std::to_string(a) + ", " + std::to_string(b), !(a && b), "NAND is the opposite of AND."};
        case 4: return {"Gate: NOR | Inputs: " + std::to_string(a) + ", " + std::to_string(b), !(a || b), "NOR is the opposite of OR."};
        case 5: return {"Gate: XNOR | Inputs: " + std::to_string(a) + ", " + std::to_string(b), !(a ^ b), "XNOR returns 1 when the inputs match."};
        default: return {"Gate: NOT | Input: " + std::to_string(a), !a, "NOT flips a bit."};
    }
}

int main() {
    std::cout << "=== Logic Gate Defender ===\n";
    std::cout << "Protect the city core by answering digital logic questions.\n\n";

    std::random_device rd;
    std::mt19937 rng(rd());
    int shield = 3;
    int score = 0;
    int streak = 0;

    for (int round = 1; round <= 10 && shield > 0; ++round) {
        Question q = makeQuestion(rng);
        std::cout << "Round " << round << " | Shield: " << shield << " | Score: " << score << "\n";
        std::cout << q.prompt << "\n";
        int playerAnswer = askInt("Enter output (0 or 1): ", 0, 1);

        if (playerAnswer == q.answer) {
            ++streak;
            int points = 10 + (streak >= 3 ? 5 : 0);
            score += points;
            std::cout << "Correct. +" << points << " points. " << q.lesson << "\n\n";
        } else {
            --shield;
            streak = 0;
            std::cout << "Incorrect. Correct answer: " << q.answer << ". " << q.lesson << "\n\n";
        }
    }

    std::cout << "Final score: " << score << "\n";
    std::cout << (shield > 0 ? "You defended the city core.\n" : "The shields collapsed.\n");
    return 0;
}
