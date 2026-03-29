// algebra_step_checker.dart
// Solves equations of the form ax + b = c and prints the steps.

import 'dart:io';

void main() {
  print('Algebra Step Checker');
  stdout.write('Enter coefficient a: ');
  final a = double.tryParse(stdin.readLineSync() ?? '');

  stdout.write('Enter coefficient b: ');
  final b = double.tryParse(stdin.readLineSync() ?? '');

  stdout.write('Enter value c: ');
  final c = double.tryParse(stdin.readLineSync() ?? '');

  if (a == null || b == null || c == null) {
    print('Invalid input. Please enter numbers only.');
    return;
  }

  if (a == 0) {
    print('a cannot be 0 in a linear equation of this form.');
    return;
  }

  print('\nEquation: ${a}x + ${b} = ${c}');
  final afterSubtract = c - b;
  print('Step 1: Subtract ${b} from both sides -> ${a}x = ${afterSubtract}');

  final x = afterSubtract / a;
  print('Step 2: Divide both sides by ${a} -> x = ${x}');
  print('Check: ${a} * ${x} + ${b} = ${a * x + b}');
}
