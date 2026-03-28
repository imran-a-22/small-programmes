print("=== History Timeline Builder ===")
print("Put the events in the correct order from earliest to latest.\n")

local events = {
    { year = 1776, text = "American Declaration of Independence" },
    { year = 1789, text = "French Revolution begins" },
    { year = 1865, text = "American Civil War ends" }
}

print("Events:")
for i, event in ipairs(events) do
    print(i .. ". " .. event.text)
end

print("\nType the correct order using numbers separated by spaces (example: 1 2 3):")
local answer = io.read()
local correct = "1 2 3"

if answer == correct then
    print("Correct. You placed the events in chronological order.")
else
    print("Not quite.")
    print("Correct order:")
    for _, event in ipairs(events) do
        print(event.year .. " - " .. event.text)
    end
end
