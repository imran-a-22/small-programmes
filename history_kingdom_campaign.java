import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Scanner;

class Question {
    String era;
    String prompt;
    String[] options;
    int answerIndex;
    String explanation;

    Question(String era, String prompt, String[] options, int answerIndex, String explanation) {
        this.era = era;
        this.prompt = prompt;
        this.options = options;
        this.answerIndex = answerIndex;
        this.explanation = explanation;
    }
}

class Kingdom {
    int food = 5;
    int knowledge = 5;
    int morale = 5;

    void rewardCorrect() {
        food += 2;
        knowledge += 2;
        morale += 1;
    }

    void punishWrong() {
        food -= 1;
        morale -= 2;
    }

    void invest(int choice) {
        switch (choice) {
            case 1 -> food += 2;
            case 2 -> knowledge += 2;
            case 3 -> morale += 2;
            default -> {
            }
        }
    }

    boolean isAlive() {
        return food > 0 && knowledge > 0 && morale > 0;
    }
}

public class history_kingdom_campaign {
    private static int readChoice(Scanner scanner, int min, int max) {
        while (true) {
            String input = scanner.nextLine().trim();
            try {
                int value = Integer.parseInt(input);
                if (value >= min && value <= max) {
                    return value;
                }
            } catch (NumberFormatException ignored) {
            }
            System.out.println("Enter a valid number.");
        }
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        Kingdom kingdom = new Kingdom();
        List<Question> questions = new ArrayList<>();

        questions.add(new Question(
            "Ancient Era",
            "Which civilisation built the pyramids at Giza?",
            new String[]{"Romans", "Egyptians", "Persians", "Vikings"},
            1,
            "The pyramids at Giza were built in ancient Egypt."
        ));

        questions.add(new Question(
            "Classical Era",
            "Which city is closely associated with democracy in ancient Greece?",
            new String[]{"Sparta", "Athens", "Troy", "Corinth"},
            1,
            "Athens is the most famous early example of direct democracy."
        ));

        questions.add(new Question(
            "Medieval Era",
            "In 1215, which document limited the English king's power?",
            new String[]{"Domesday Book", "Magna Carta", "Code of Hammurabi", "Bill of Rights"},
            1,
            "Magna Carta was a major step in limiting monarchical power."
        ));

        questions.add(new Question(
            "Early Modern Era",
            "Who sailed to the Americas in 1492 under the Spanish crown?",
            new String[]{"Ferdinand Magellan", "Marco Polo", "Christopher Columbus", "James Cook"},
            2,
            "Columbus reached the Americas in 1492."
        ));

        questions.add(new Question(
            "Industrial Era",
            "Which invention is most associated with James Watt improving industry?",
            new String[]{"Steam engine", "Telegraph", "Printing press", "Compass"},
            0,
            "James Watt is strongly linked to major improvements in the steam engine."
        ));

        questions.add(new Question(
            "Modern Era",
            "Which international organisation was founded in 1945 after World War II?",
            new String[]{"United Nations", "NATO", "European Union", "League of Nations"},
            0,
            "The United Nations was founded in 1945."
        ));

        Collections.shuffle(questions);

        System.out.println("=================================================");
        System.out.println("HISTORY KINGDOM CAMPAIGN");
        System.out.println("Answer history questions to keep your kingdom alive.");
        System.out.println("You manage food, knowledge, and morale.");
        System.out.println("=================================================");

        int rounds = 5;
        for (int i = 0; i < rounds; i++) {
            Question q = questions.get(i);
            System.out.println("\nRound " + (i + 1) + " of " + rounds + " - " + q.era);
            System.out.println("Food: " + kingdom.food + " | Knowledge: " + kingdom.knowledge + " | Morale: " + kingdom.morale);
            System.out.println(q.prompt);
            for (int j = 0; j < q.options.length; j++) {
                System.out.println((j + 1) + ". " + q.options[j]);
            }

            int answer = readChoice(scanner, 1, q.options.length) - 1;
            if (answer == q.answerIndex) {
                kingdom.rewardCorrect();
                System.out.println("Correct. " + q.explanation);
            } else {
                kingdom.punishWrong();
                System.out.println("Incorrect. Correct answer: " + q.options[q.answerIndex]);
                System.out.println(q.explanation);
            }

            System.out.println("Choose one investment:");
            System.out.println("1. Farms (+2 food)");
            System.out.println("2. Library (+2 knowledge)");
            System.out.println("3. Festival (+2 morale)");
            int investment = readChoice(scanner, 1, 3);
            kingdom.invest(investment);

            if (!kingdom.isAlive()) {
                System.out.println("\nYour kingdom collapsed before the campaign ended.");
                System.out.println("Final resources -> Food: " + kingdom.food + ", Knowledge: " + kingdom.knowledge + ", Morale: " + kingdom.morale);
                scanner.close();
                return;
            }
        }

        System.out.println("\n=================================================");
        System.out.println("Campaign complete.");
        System.out.println("Final resources -> Food: " + kingdom.food + ", Knowledge: " + kingdom.knowledge + ", Morale: " + kingdom.morale);
        if (kingdom.food >= 8 && kingdom.knowledge >= 8 && kingdom.morale >= 8) {
            System.out.println("Your kingdom enters a golden age.");
        } else {
            System.out.println("Your kingdom survives and is ready for another era.");
        }
        System.out.println("=================================================");
        scanner.close();
    }
}
