use std::io;

fn read_number(prompt: &str) -> u32 {
    loop {
        println!("{}", prompt);
        let mut input = String::new();
        io::stdin().read_line(&mut input).expect("Failed to read line");
        match input.trim().parse::<u32>() {
            Ok(value) if value > 0 => return value,
            _ => println!("Please enter a positive whole number."),
        }
    }
}

fn main() {
    println!("=== Reading Timer Tutor ===");
    println!("Estimate how long a student may need to read a passage and answer a quick check question.\n");

    let words = read_number("How many words are in the passage?");
    let wpm = read_number("What is the student's reading speed in words per minute?");

    let minutes = words as f64 / wpm as f64;
    println!("\nEstimated reading time: {:.2} minutes", minutes);

    println!("\nMini comprehension check:");
    println!("Why is reading speed useful to know?");
    println!("A) It helps plan study time");
    println!("B) It changes the meaning of every word");
    println!("C) It removes the need to understand the text");

    let mut answer = String::new();
    io::stdin().read_line(&mut answer).expect("Failed to read line");

    match answer.trim().to_uppercase().as_str() {
        "A" => println!("Correct. Reading speed helps students plan realistic study time."),
        _ => println!("Not quite. The best answer is A, because reading speed helps with time planning."),
    }
}
