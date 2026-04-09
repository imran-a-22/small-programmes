/**
 * loot_rarity_simulator.ts
 *
 * Simulates a loot table for a game and prints drop distributions by item and rarity.
 * Run with:
 *   ts-node loot_rarity_simulator.ts 10000
 * Or compile with:
 *   tsc loot_rarity_simulator.ts && node loot_rarity_simulator.js 10000
 */

type Rarity = "Common" | "Rare" | "Epic" | "Legendary";

interface LootItem {
  name: string;
  rarity: Rarity;
  dropRate: number; // percentage, total should equal 100
}

const lootTable: LootItem[] = [
  { name: "Old Boots", rarity: "Common", dropRate: 24.0 },
  { name: "Healing Herb", rarity: "Common", dropRate: 23.0 },
  { name: "Iron Dagger", rarity: "Rare", dropRate: 18.0 },
  { name: "Mana Crystal", rarity: "Rare", dropRate: 16.0 },
  { name: "Phoenix Feather", rarity: "Epic", dropRate: 11.0 },
  { name: "Shadow Cloak", rarity: "Epic", dropRate: 6.0 },
  { name: "Dragon Crown", rarity: "Legendary", dropRate: 2.0 },
];

function validateLootTable(items: LootItem[]): void {
  const total = items.reduce((sum, item) => sum + item.dropRate, 0);
  if (Math.abs(total - 100) > 0.0001) {
    throw new Error(`Loot table must add up to 100. Current total: ${total}`);
  }

  for (const item of items) {
    if (item.dropRate <= 0) {
      throw new Error(`Invalid drop rate for ${item.name}. Must be positive.`);
    }
  }
}

function rollOne(items: LootItem[]): LootItem {
  const roll = Math.random() * 100;
  let runningTotal = 0;

  for (const item of items) {
    runningTotal += item.dropRate;
    if (roll <= runningTotal) {
      return item;
    }
  }

  return items[items.length - 1];
}

function simulate(items: LootItem[], drops: number): void {
  const itemCounts = new Map<string, number>();
  const rarityCounts = new Map<Rarity, number>([
    ["Common", 0],
    ["Rare", 0],
    ["Epic", 0],
    ["Legendary", 0],
  ]);

  for (const item of items) {
    itemCounts.set(item.name, 0);
  }

  for (let i = 0; i < drops; i += 1) {
    const drop = rollOne(items);
    itemCounts.set(drop.name, (itemCounts.get(drop.name) ?? 0) + 1);
    rarityCounts.set(drop.rarity, (rarityCounts.get(drop.rarity) ?? 0) + 1);
  }

  console.log(`\nLoot Simulation Results`);
  console.log(`Drops simulated: ${drops}\n`);

  console.log(`By item:`);
  for (const item of items) {
    const count = itemCounts.get(item.name) ?? 0;
    const actualPct = (count / drops) * 100;
    console.log(
      `- ${item.name.padEnd(16)} | rarity=${item.rarity.padEnd(9)} | expected=${item.dropRate.toFixed(2)}% | actual=${actualPct.toFixed(2)}% | count=${count}`
    );
  }

  console.log(`\nBy rarity:`);
  for (const rarity of ["Common", "Rare", "Epic", "Legendary"] as Rarity[]) {
    const count = rarityCounts.get(rarity) ?? 0;
    const actualPct = (count / drops) * 100;
    console.log(`- ${rarity.padEnd(9)} | actual=${actualPct.toFixed(2)}% | count=${count}`);
  }
}

function getDropCountFromArgs(): number {
  const arg = process.argv[2];
  if (!arg) {
    return 1000;
  }

  const parsed = Number(arg);
  if (!Number.isInteger(parsed) || parsed <= 0) {
    throw new Error("Please provide a positive integer for the number of simulated drops.");
  }
  return parsed;
}

function main(): void {
  validateLootTable(lootTable);
  const dropCount = getDropCountFromArgs();
  simulate(lootTable, dropCount);
}

main();
