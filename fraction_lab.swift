import Foundation

func gcd(_ a: Int, _ b: Int) -> Int {
    var x = abs(a)
    var y = abs(b)
    while y != 0 {
        let temp = y
        y = x % y
        x = temp
    }
    return x == 0 ? 1 : x
}

func simplify(_ numerator: Int, _ denominator: Int) -> (Int, Int) {
    let divisor = gcd(numerator, denominator)
    var n = numerator / divisor
    var d = denominator / divisor
    if d < 0 {
        n *= -1
        d *= -1
    }
    return (n, d)
}

func readInt(_ prompt: String) -> Int {
    while true {
        print(prompt, terminator: "")
        if let line = readLine(), let value = Int(line.trimmingCharacters(in: .whitespacesAndNewlines)) {
            return value
        }
        print("Please enter a whole number.")
    }
}

print("=== Fraction Lab ===")
print("Practice fraction addition and subtraction with step-by-step output.\n")

let n1 = readInt("First fraction numerator: ")
let d1 = readInt("First fraction denominator: ")
let n2 = readInt("Second fraction numerator: ")
let d2 = readInt("Second fraction denominator: ")

if d1 == 0 || d2 == 0 {
    print("A denominator cannot be zero.")
    exit(0)
}

print("Choose operation: + or -")
let operation = readLine()?.trimmingCharacters(in: .whitespacesAndNewlines) ?? "+"

let commonDenominator = d1 * d2
let scaledN1 = n1 * d2
let scaledN2 = n2 * d1

print("\nStep 1: Find a common denominator.")
print("Common denominator = \(d1) × \(d2) = \(commonDenominator)")
print("\nStep 2: Rewrite both fractions.")
print("\(n1)/\(d1) becomes \(scaledN1)/\(commonDenominator)")
print("\(n2)/\(d2) becomes \(scaledN2)/\(commonDenominator)")

let rawNumerator: Int
if operation == "-" {
    rawNumerator = scaledN1 - scaledN2
    print("\nStep 3: Subtract numerators: \(scaledN1) - \(scaledN2) = \(rawNumerator)")
} else {
    rawNumerator = scaledN1 + scaledN2
    print("\nStep 3: Add numerators: \(scaledN1) + \(scaledN2) = \(rawNumerator)")
}

let result = simplify(rawNumerator, commonDenominator)
print("\nStep 4: Simplify the result.")
print("Final answer = \(result.0)/\(result.1)")
