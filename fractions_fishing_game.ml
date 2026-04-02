(*
  fractions_fishing_game.ml

  Ed-tech + gaming console program in OCaml.
  The player catches fish by simplifying fractions correctly.

  Compile:
    ocamlc -o fractions_fishing_game fractions_fishing_game.ml

  Run:
    ./fractions_fishing_game
*)

type player = {
  name : string;
  mutable score : int;
  mutable lives : int;
  mutable streak : int;
}

type fish = {
  species : string;
  points : int;
}

let fish_types = [|
  { species = "Silver Minnow"; points = 10 };
  { species = "River Trout"; points = 15 };
  { species = "Golden Carp"; points = 20 };
  { species = "Crystal Pike"; points = 25 };
  { species = "Legendary Koi"; points = 30 };
|]

let gcd a b =
  let rec aux x y =
    if y = 0 then abs x else aux y (x mod y)
  in
  aux a b

let random_between a b =
  a + Random.int (b - a + 1)

let generate_fraction () =
  let base = random_between 2 12 in
  let factor = random_between 2 6 in
  let numerator = base * factor in
  let denominator = (random_between 2 12) * factor in
  (numerator, denominator)

let simplify_fraction n d =
  let g = gcd n d in
  (n / g, d / g)

let trim s =
  String.trim s

let parse_fraction input =
  try
    match String.split_on_char '/' (trim input) with
    | [n; d] ->
        let num = int_of_string (trim n) in
        let den = int_of_string (trim d) in
        if den = 0 then None else Some (num, den)
    | _ -> None
  with _ -> None

let print_divider () =
  print_endline "----------------------------------------"

let random_fish round =
  let max_index = min (Array.length fish_types - 1) (round / 2) in
  fish_types.(Random.int (max_index + 1))

let ask prompt =
  print_string prompt;
  read_line ()

let play_round player round =
  let fish = random_fish round in
  let n, d = generate_fraction () in
  let sn, sd = simplify_fraction n d in

  print_divider ();
  Printf.printf "Round %d\n" round;
  Printf.printf "A %s is near the hook.\n" fish.species;
  Printf.printf "Simplify this fraction to catch it: %d/%d\n" n d;
  print_endline "Type your answer in the form a/b";
  let answer = ask "> " in

  match parse_fraction answer with
  | Some (user_n, user_d) ->
      if user_n = sn && user_d = sd then begin
        player.score <- player.score + fish.points + (player.streak * 2);
        player.streak <- player.streak + 1;
        Printf.printf "Correct. You caught the %s.\n" fish.species;
        Printf.printf "You earned %d points.\n" (fish.points + ((player.streak - 1) * 2));
      end else begin
        player.lives <- player.lives - 1;
        player.streak <- 0;
        Printf.printf "Wrong. Correct answer: %d/%d\n" sn sd;
        print_endline "The fish escaped.";
      end
  | None ->
      player.lives <- player.lives - 1;
      player.streak <- 0;
      Printf.printf "Invalid format. Correct answer was %d/%d\n" sn sd;
      print_endline "The fish escaped.";

  Printf.printf "Score: %d | Lives: %d | Streak: %d\n"
    player.score player.lives player.streak

let boss_round player =
  print_divider ();
  print_endline "BOSS ROUND: Leviathan of Fractions";
  print_endline "Solve 3 fraction challenges in a row to win the boss treasure.";

  let rec loop count =
    if count = 3 then begin
      player.score <- player.score + 100;
      print_endline "Boss defeated. You earned 100 bonus points."
    end else if player.lives <= 0 then
      ()
    else
      let n, d = generate_fraction () in
      let sn, sd = simplify_fraction n d in
      Printf.printf "Challenge %d: Simplify %d/%d\n" (count + 1) n d;
      let answer = ask "> " in
      match parse_fraction answer with
      | Some (user_n, user_d) when user_n = sn && user_d = sd ->
          print_endline "Correct.";
          loop (count + 1)
      | _ ->
          player.lives <- player.lives - 1;
          print_endline "Wrong. The Leviathan strikes back.";
          Printf.printf "Correct answer: %d/%d\n" sn sd;
          Printf.printf "Lives left: %d\n" player.lives
  in
  loop 0

let () =
  Random.self_init ();
  print_endline "=== FRACTIONS FISHING GAME ===";
  print_endline "Catch fish by simplifying fractions.";
  let name =
    let n = ask "Enter your player name: " in
    if trim n = "" then "Player" else n
  in

  let player = {
    name;
    score = 0;
    lives = 3;
    streak = 0;
  } in

  Printf.printf "Welcome, %s.\n" player.name;

  let rec main_loop round =
    if player.lives <= 0 then begin
      print_divider ();
      print_endline "Game Over.";
      Printf.printf "Final score: %d\n" player.score
    end else if round = 6 then begin
      boss_round player;
      print_divider ();
      if player.lives > 0 then begin
        print_endline "You finished the adventure.";
        Printf.printf "Final score: %d\n" player.score
      end else begin
        print_endline "The boss defeated you.";
        Printf.printf "Final score: %d\n" player.score
      end
    end else begin
      play_round player round;
      main_loop (round + 1)
    end
  in

  main_loop 1
