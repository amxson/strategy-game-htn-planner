# Python HTN Planner for Village Guard Game AI

## Group 10 - HTN Task Submission

## Project Overview

This project implements a Python-based HTN (Hierarchical Task Network) planner.

The planner decomposes a high-level goal into smaller compound tasks until it reaches executable primitive tasks.

Our custom domain is a simple strategy game called **Village Guard Game**, where an AI guard must protect a village from an enemy.

The planner uses recursive task decomposition and method preconditions to decide the best actions depending on the current game state.

---

# Domain Description

## Main Goal

```text
ProtectVillage

The AI guard must secure the village by:

Checking the village
Preparing for battle
Defeating the enemy
Finishing the mission

Compound Tasks

The following compound tasks are used:

ProtectVillage
CheckVillage
PrepareGuard
StopEnemy
FinishMission

Primitive Tasks

The following primitive tasks are executable actions:

PatrolArea
HealGuard
PickUpSword
MoveToEnemy
AttackEnemy
CelebrateVictory
Dynamic Planning Logic

The planner chooses methods based on the current world state.

Examples:

If village is unchecked → PatrolArea
If health is low → HealGuard
If no weapon → PickUpSword
If enemy is near and guard is ready → AttackEnemy
If enemy is defeated → CelebrateVictory
Initial State
{
    "village_checked": False,
    "has_weapon": False,
    "health": 30,
    "enemy_near": True,
    "at_enemy": False,
    "enemy_defeated": False,
    "village_safe": False,
    "mission_complete": False
}
Planning Trace / Walkthrough

The planner starts with:

ProtectVillage

It decomposes the task as follows:

ProtectVillage
├── CheckVillage
│   └── PatrolArea
├── PrepareGuard
│   ├── HealGuard
│   └── PickUpSword
├── StopEnemy
│   ├── MoveToEnemy
│   └── AttackEnemy
└── FinishMission
    └── CelebrateVictory
Final Primitive Plan
Step 1: PatrolArea
Step 2: HealGuard
Step 3: PickUpSword
Step 4: MoveToEnemy
Step 5: AttackEnemy
Step 6: CelebrateVictory
Final World State
{
    "village_checked": True,
    "has_weapon": True,
    "health": 100,
    "enemy_near": True,
    "at_enemy": True,
    "enemy_defeated": True,
    "village_safe": True,
    "mission_complete": True
}
Implementation Details

Files included in the repository:

main.py → Runs planner
htn_engine.py → Recursive HTN planner engine
domain.py → Village Guard domain tasks and methods
tree_visualizer.py → Decomposition trace output
README.md → Technical report

Failure Cases / Limitations
Total-order planning only (tasks executed in sequence)
No parallel actions
Single enemy scenario only
No random behavior or learning
World state is manually defined

Future Improvements
Add multiple enemies
Add shield / bow weapons
Add patrol map movement
Add graphical animation
Add partial replanning during combat

Conclusion

This project demonstrates how HTN planning can be used in games.

The AI guard reasons hierarchically, chooses actions based on conditions, and successfully protects the village through intelligent planning.
## Correctness checks

Run `python -m unittest -v test_planner.py`. Failed methods roll back their state, primitive steps, and tree edges before another method is tried. A failed plan leaves the caller state unchanged; a successful plan commits the final state. A depth limit prevents cyclic methods from recursing indefinitely.
