using System;
using System.Collections.Generic;

class PeriodicTableTrainer
{
    static void Main()
    {
        var elements = new Dictionary<string, string>(StringComparer.OrdinalIgnoreCase)
        {
            {"H", "Hydrogen"},
            {"O", "Oxygen"},
            {"Na", "Sodium"},
            {"Fe", "Iron"},
            {"Au", "Gold"}
        };

        Console.WriteLine("=== Periodic Table Trainer ===");
        Console.WriteLine("Type the full name of the element for each symbol.\n");

        int score = 0;

        foreach (var item in elements)
        {
            Console.Write($"What element has the symbol {item.Key}? ");
            string answer = Console.ReadLine() ?? "";

            if (answer.Trim().Equals(item.Value, StringComparison.OrdinalIgnoreCase))
            {
                Console.WriteLine("Correct!\n");
                score++;
            }
            else
            {
                Console.WriteLine($"Not quite. The correct answer is {item.Value}.\n");
            }
        }

        Console.WriteLine($"Final score: {score}/{elements.Count}");
        Console.WriteLine("Review the symbols you missed and try again.");
    }
}
