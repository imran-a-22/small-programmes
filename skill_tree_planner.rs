use std::collections::{HashMap, HashSet};

#[derive(Debug, Clone)]
struct Skill {
    name: String,
    cost: u32,
    prerequisites: Vec<String>,
}

fn can_unlock(
    skill_name: &str,
    unlocked: &HashSet<String>,
    skills: &HashMap<String, Skill>,
) -> bool {
    if let Some(skill) = skills.get(skill_name) {
        skill.prerequisites.iter().all(|req| unlocked.contains(req))
    } else {
        false
    }
}

fn unlock_path(
    target: &str,
    skills: &HashMap<String, Skill>,
    visited: &mut HashSet<String>,
    order: &mut Vec<String>,
) {
    if visited.contains(target) {
        return;
    }

    visited.insert(target.to_string());

    if let Some(skill) = skills.get(target) {
        for prereq in &skill.prerequisites {
            unlock_path(prereq, skills, visited, order);
        }
        order.push(target.to_string());
    }
}

fn total_cost(path: &[String], skills: &HashMap<String, Skill>) -> u32 {
    path.iter()
        .filter_map(|name| skills.get(name))
        .map(|skill| skill.cost)
        .sum()
}

fn main() {
    let mut skills: HashMap<String, Skill> = HashMap::new();

    let data = vec![
        Skill {
            name: "Basic Attack".to_string(),
            cost: 1,
            prerequisites: vec![],
        },
        Skill {
            name: "Shield Training".to_string(),
            cost: 2,
            prerequisites: vec!["Basic Attack".to_string()],
        },
        Skill {
            name: "Power Strike".to_string(),
            cost: 3,
            prerequisites: vec!["Basic Attack".to_string()],
        },
        Skill {
            name: "Whirlwind".to_string(),
            cost: 4,
            prerequisites: vec!["Power Strike".to_string()],
        },
        Skill {
            name: "Guardian Aura".to_string(),
            cost: 5,
            prerequisites: vec!["Shield Training".to_string()],
        },
        Skill {
            name: "Dragon Slash".to_string(),
            cost: 7,
            prerequisites: vec!["Whirlwind".to_string(), "Guardian Aura".to_string()],
        },
    ];

    for skill in data {
        skills.insert(skill.name.clone(), skill);
    }

    let target = "Dragon Slash";
    let mut visited = HashSet::new();
    let mut order = Vec::new();

    unlock_path(target, &skills, &mut visited, &mut order);

    println!("Skill Tree Planner");
    println!("------------------");
    println!("Target skill: {}", target);
    println!("\nRequired unlock order:");

    let mut unlocked = HashSet::new();
    for step in &order {
        let status = can_unlock(step, &unlocked, &skills);
        if let Some(skill) = skills.get(step) {
            println!(
                "- {} | cost: {} | can unlock now: {}",
                skill.name, skill.cost, status
            );
        }
        unlocked.insert(step.clone());
    }

    println!("\nTotal skill point cost: {}", total_cost(&order, &skills));
}
