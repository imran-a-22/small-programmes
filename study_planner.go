// Study Planner (Go)
// A simple terminal program that creates a balanced study plan.
//
// Run:
//     go run study_planner.go
package main

import (
    "bufio"
    "fmt"
    "os"
    "strconv"
    "strings"
)

func main() {
    reader := bufio.NewReader(os.Stdin)

    fmt.Println("Study Planner")
    fmt.Println("Create a simple weekly study split for 3 subjects.")

    subjects := make([]string, 3)
    hours := make([]int, 3)

    for i := 0; i < 3; i++ {
        fmt.Printf("\nEnter subject %d name: ", i+1)
        subject, _ := reader.ReadString('\n')
        subjects[i] = strings.TrimSpace(subject)

        for {
            fmt.Printf("Enter hours to study %s this week: ", subjects[i])
            line, _ := reader.ReadString('\n')
            line = strings.TrimSpace(line)
            value, err := strconv.Atoi(line)
            if err == nil && value > 0 {
                hours[i] = value
                break
            }
            fmt.Println("Please enter a whole number greater than 0.")
        }
    }

    days := []string{"Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"}
    fmt.Println("\nSuggested Study Plan")
    fmt.Println("---------------------")

    dayIndex := 0
    for i := 0; i < len(subjects); i++ {
        remaining := hours[i]
        for remaining > 0 {
            fmt.Printf("%s: %s (1 hour)\n", days[dayIndex%len(days)], subjects[i])
            remaining--
            dayIndex++
        }
    }

    fmt.Println("\nTip: study the most difficult subject earlier in the day when your focus is strongest.")
}
