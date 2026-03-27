/*
Multiplication Trainer (C)
A small terminal maths practice program.

Compile:
    gcc multiplication_trainer.c -o multiplication_trainer
Run:
    ./multiplication_trainer
*/

#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main(void) {
    int rounds = 5;
    int score = 0;

    srand((unsigned int)time(NULL));

    printf("Multiplication Trainer\n");
    printf("Answer %d multiplication questions.\n\n", rounds);

    for (int i = 1; i <= rounds; i++) {
        int a = (rand() % 11) + 2;
        int b = (rand() % 11) + 2;
        int userAnswer = 0;
        int correct = a * b;

        printf("Question %d: %d x %d = ", i, a, b);
        if (scanf("%d", &userAnswer) != 1) {
            printf("Invalid input. Exiting.\n");
            return 1;
        }

        if (userAnswer == correct) {
            printf("Correct!\n\n");
            score++;
        } else {
            printf("Incorrect. The correct answer is %d.\n\n", correct);
        }
    }

    printf("You scored %d out of %d.\n", score, rounds);

    if (score == rounds) {
        printf("Excellent maths work!\n");
    } else if (score >= 3) {
        printf("Good effort. Keep practising to improve speed and accuracy.\n");
    } else {
        printf("Keep practising. Repetition builds confidence.\n");
    }

    return 0;
}
