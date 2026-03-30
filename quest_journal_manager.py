from dataclasses import dataclass, field
from typing import List


@dataclass
class Quest:
    title: str
    description: str
    completed: bool = False
    rewards: List[str] = field(default_factory=list)

    def complete(self) -> None:
        self.completed = True


class QuestJournal:
    def __init__(self) -> None:
        self.quests: List[Quest] = []

    def add_quest(self, quest: Quest) -> None:
        self.quests.append(quest)

    def complete_quest(self, title: str) -> bool:
        for quest in self.quests:
            if quest.title.lower() == title.lower():
                quest.complete()
                return True
        return False

    def print_journal(self) -> None:
        print("QUEST JOURNAL")
        print("=" * 40)
        for quest in self.quests:
            status = "Completed" if quest.completed else "Active"
            print(f"{quest.title} [{status}]")
            print(f"  {quest.description}")
            if quest.rewards:
                print(f"  Rewards: {', '.join(quest.rewards)}")
            print()


def main() -> None:
    journal = QuestJournal()
    journal.add_quest(Quest("The Missing Scout", "Find the scout lost near the northern ruins.", rewards=["75 gold", "Scout's Compass"]))
    journal.add_quest(Quest("Herbal Remedy", "Collect 5 moonleaf herbs for the village healer.", rewards=["20 gold", "Healing Potion"]))
    journal.complete_quest("Herbal Remedy")
    journal.print_journal()


if __name__ == "__main__":
    main()
