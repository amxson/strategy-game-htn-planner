def always(state, *args):
    return True



# Primitive preconditions


def enemy_near(state, *args):
    return state["enemy_near"] is True


def weapon_ready(state, *args):
    return state["has_weapon"] is True


def no_weapon(state, *args):
    return state["has_weapon"] is False


def health_low(state, *args):
    return state["health"] < 50


def health_ok(state, *args):
    return state["health"] >= 50


# Primitive effects


def patrol_area(state):
    state["village_checked"] = True


def pick_up_sword(state):
    state["has_weapon"] = True


def heal_guard(state):
    state["health"] = 100


def move_to_enemy(state):
    state["at_enemy"] = True


def attack_enemy(state):
    state["enemy_defeated"] = True
    state["village_safe"] = True


def celebrate_victory(state):
    state["mission_complete"] = True



# Compound preconditions


def village_not_checked(state, *args):
    return state["village_checked"] is False


def village_checked(state, *args):
    return state["village_checked"] is True


def enemy_defeated(state, *args):
    return state["enemy_defeated"] is True


# Methods


methods = {
    "ProtectVillage": [
        (
            "MainProtectionPlan",
            always,
            lambda state: [
                ("CheckVillage",),
                ("PrepareGuard",),
                ("StopEnemy",),
                ("FinishMission",)
            ],
        )
    ],

    "CheckVillage": [
        (
            "PatrolFirst",
            village_not_checked,
            lambda state: [
                ("PatrolArea",),
                ("CheckVillage",)
            ],
        ),
        (
            "VillageAlreadyChecked",
            village_checked,
            lambda state: []
        ),
    ],

    "PrepareGuard": [
        (
            "HealFirst",
            health_low,
            lambda state: [
                ("HealGuard",),
                ("PrepareGuard",)
            ],
        ),
        (
            "GetWeapon",
            no_weapon,
            lambda state: [
                ("PickUpSword",),
                ("PrepareGuard",)
            ],
        ),
        (
            "GuardReady",
            lambda state, *args: health_ok(state) and weapon_ready(state),
            lambda state: []
        ),
    ],

    "StopEnemy": [
        (
            "FightEnemy",
            lambda state, *args: enemy_near(state) and weapon_ready(state),
            lambda state: [
                ("MoveToEnemy",),
                ("AttackEnemy",)
            ],
        ),
    ],

    "FinishMission": [
        (
            "Celebrate",
            enemy_defeated,
            lambda state: [
                ("CelebrateVictory",)
            ],
        )
    ],
}


# Operators


operators = {
    "PatrolArea": (always, lambda state: patrol_area(state)),
    "PickUpSword": (always, lambda state: pick_up_sword(state)),
    "HealGuard": (always, lambda state: heal_guard(state)),
    "MoveToEnemy": (enemy_near, lambda state: move_to_enemy(state)),
    "AttackEnemy": (weapon_ready, lambda state: attack_enemy(state)),
    "CelebrateVictory": (enemy_defeated, lambda state: celebrate_victory(state)),
}


# Initial state


initial_state = {
    "village_checked": False,
    "has_weapon": False,
    "health": 30,
    "enemy_near": True,
    "at_enemy": False,
    "enemy_defeated": False,
    "village_safe": False,
    "mission_complete": False,
}