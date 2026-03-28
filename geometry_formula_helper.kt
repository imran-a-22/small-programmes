import kotlin.math.PI

fun readPositiveDouble(prompt: String): Double {
    while (true) {
        print(prompt)
        val input = readLine()?.trim()
        val value = input?.toDoubleOrNull()
        if (value != null && value > 0) return value
        println("Please enter a positive number.")
    }
}

fun round2(value: Double): String = String.format("%.2f", value)

fun main() {
    println("=== Geometry Formula Helper ===")
    println("This tool helps students calculate shapes and understand the formula used.")
    println()
    println("Choose a topic:")
    println("1. Rectangle")
    println("2. Triangle")
    println("3. Circle")
    println("4. Cube")
    print("Enter choice: ")

    when (readLine()?.trim()) {
        "1" -> {
            val length = readPositiveDouble("Length: ")
            val width = readPositiveDouble("Width: ")
            val area = length * width
            val perimeter = 2 * (length + width)
            println("\nFormula used:")
            println("Area = length x width")
            println("Perimeter = 2 x (length + width)")
            println("Area = ${round2(area)}")
            println("Perimeter = ${round2(perimeter)}")
        }
        "2" -> {
            val base = readPositiveDouble("Base: ")
            val height = readPositiveDouble("Height: ")
            val area = 0.5 * base * height
            println("\nFormula used:")
            println("Area = 1/2 x base x height")
            println("Area = ${round2(area)}")
        }
        "3" -> {
            val radius = readPositiveDouble("Radius: ")
            val area = PI * radius * radius
            val circumference = 2 * PI * radius
            println("\nFormula used:")
            println("Area = pi x r^2")
            println("Circumference = 2 x pi x r")
            println("Area = ${round2(area)}")
            println("Circumference = ${round2(circumference)}")
        }
        "4" -> {
            val side = readPositiveDouble("Side length: ")
            val surfaceArea = 6 * side * side
            val volume = side * side * side
            println("\nFormula used:")
            println("Surface Area = 6 x s^2")
            println("Volume = s^3")
            println("Surface Area = ${round2(surfaceArea)}")
            println("Volume = ${round2(volume)}")
        }
        else -> println("Invalid option.")
    }

    println("\nTip: try changing the numbers to see how each formula responds.")
}
