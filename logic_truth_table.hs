-- logic_truth_table.hs
-- Prints truth tables for basic logical operations.

showBool :: Bool -> String
showBool True = "T"
showBool False = "F"

printRow :: Bool -> Bool -> IO ()
printRow a b = putStrLn (showBool a ++ "  " ++ showBool b ++ "  " ++ showBool (a && b) ++ "    " ++ showBool (a || b) ++ "   " ++ showBool (a /= b))

main :: IO ()
main = do
  putStrLn "Logic Truth Table"
  putStrLn "A  B  AND  OR  XOR"
  printRow True True
  printRow True False
  printRow False True
  printRow False False
  putStrLn "\nUse this to study how logical operators work."
