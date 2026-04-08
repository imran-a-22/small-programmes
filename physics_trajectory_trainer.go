package main

import (
    "bufio"
    "fmt"
    "math"
    "math/rand"
    "os"
    "strconv"
    "strings"
    "time"
)

type Round struct {
    targetDistance float64
}

const gravity = 9.8

func readFloat(reader *bufio.Reader, prompt string) float64 {
    for {
        fmt.Print(prompt)
        text, _ := reader.ReadString('\n')
        text = strings.TrimSpace(text)
        value, err := strconv.ParseFloat(text, 64)
        if err == nil {
            return value
        }
        fmt.Println("Enter a valid number.")
    }
}

func projectileRange(speed float64, angleDegrees float64) float64 {
    radians := angleDegrees * math.Pi / 180
    return (speed * speed * math.Sin(2*radians)) / gravity
}

func main() {
    rand.Seed(time.Now().UnixNano())
    reader := bufio.NewReader(os.Stdin)

    fmt.Println("================================================")
    fmt.Println("PHYSICS TRAJECTORY TRAINER")
    fmt.Println("Hit the target by choosing a launch speed and angle.")
    fmt.Println("You will learn how projectile range changes with both.")
    fmt.Println("Formula used: range = v^2 * sin(2θ) / g")
    fmt.Println("================================================")

    rounds := []Round{}
    for i := 0; i < 5; i++ {
        rounds = append(rounds, Round{targetDistance: float64(rand.Intn(56) + 25)})
    }

    totalStars := 0

    for index, round := range rounds {
        fmt.Printf("\nRound %d of %d\n", index+1, len(rounds))
        fmt.Printf("Target distance: %.1f metres\n", round.targetDistance)

        speed := readFloat(reader, "Choose launch speed (m/s): ")
        angle := readFloat(reader, "Choose launch angle (degrees): ")

        distance := projectileRange(speed, angle)
        errorAmount := math.Abs(distance - round.targetDistance)

        fmt.Printf("Projectile landed at: %.2f metres\n", distance)
        fmt.Printf("Distance from target: %.2f metres\n", errorAmount)

        stars := 0
        if errorAmount <= 2 {
            stars = 3
        } else if errorAmount <= 5 {
            stars = 2
        } else if errorAmount <= 10 {
            stars = 1
        }
        totalStars += stars

        switch stars {
        case 3:
            fmt.Println("Excellent hit. 3 stars.")
        case 2:
            fmt.Println("Strong attempt. 2 stars.")
        case 1:
            fmt.Println("Close enough to score. 1 star.")
        default:
            fmt.Println("Missed badly. 0 stars.")
        }

        if distance < round.targetDistance {
            fmt.Println("Feedback: increase speed, angle, or both.")
        } else if distance > round.targetDistance {
            fmt.Println("Feedback: reduce speed or use an angle closer to 45° depending on your choice.")
        } else {
            fmt.Println("Perfect shot.")
        }

        fmt.Println("Learning note: for a fixed speed, angles like 30° and 60° can create similar ranges because sin(2θ) mirrors.")
    }

    fmt.Println("\n================================================")
    fmt.Printf("Final stars: %d out of %d\n", totalStars, len(rounds)*3)
    if totalStars >= 12 {
        fmt.Println("You have strong intuition for projectile motion.")
    } else if totalStars >= 7 {
        fmt.Println("Good progress. Keep experimenting with speed-angle trade-offs.")
    } else {
        fmt.Println("Review how angle and speed affect range, then try again.")
    }
    fmt.Println("================================================")
}
