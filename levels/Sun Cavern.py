from ..shared import *

expected_shrooms = 18
expected_eggs = 2

data = {
  "Lower": Area(
    area_connections = {
      "Upper": lambda c: lambda s: (
        (
          # movement
          c.has_high_jump(s)
          and c.has_fast_roll(s)
        )

        or c.has_dive(s)
        or c.has_wings(s)
        or c.has_flight(s)

        or c.can_bubble_jump(s)
        or (
          c.has_bubble(s)
          and c.has_high_jump(s)
        )
        or c.can_super_bounce(s)
        or c.can_smuggle_jester_boots(s)
      ),

      "Waterfall Ledge": lambda c: lambda s: (
        c.has_flight(s)

        or c.can_super_bounce(s)
        or c.can_smuggle_jester_boots(s)
      ),

      "Ducklings Ledge": lambda c: lambda s: (
        c.has_dive(s)
        or c.has_fast_roll(s)
        or c.has_wings(s)

        or c.can_bubble_jump(s)
      ),

      "Ducklings Doorway": lambda c: lambda s: (
        c.options.movement >= 2
        and c.has_wings(s)
      ),

      "Moon Cavern Heart Door": lambda c: lambda s: (
        c.has_swim(s)
      )
    },
    entrances = {
      "Lostleaf Lobby Door": Entrance(
        to = ("Lake Lobby", "Sun Cavern Door"),
        rule = lambda c: lambda s: s.has("Mighty Wall Knocked Down", c.player)
      ),

    },
    locations = Locations(
      abilities = {
        "Attack": lambda c: lambda s: c.has_eggs(s, 1),
        "Wings":  lambda c: lambda s: c.has_eggs(s, 6),
        "Dive":   lambda c: lambda s: c.has_eggs(s, 12),
        "Bubble": lambda c: lambda s: c.has_eggs(s, 24),
        "Flight": lambda c: lambda s: c.has_eggs(s, 40),
      },
      cards = {
        "Shroom": None
      },
      shrooms = {
        **shrooms("Vine Ledge", 2),
        **shrooms("High Jump", 2, lambda c: lambda s: (
          c.can_bubble_jump(s)
          or c.has_high_jump(s)
          or c.has_flight(s)
          or c.can_smuggle_jester_boots(s)
        )),
        **shrooms("Tail Spin Launch", 2, lambda c: lambda s: (
          c.has_high_jump(s)
          or c.has_roll(s)
          or c.has_bubble(s)
          or c.has_wings(s)
          or c.can_smuggle_jester_boots(s)
        )),
        **shrooms("Mighty Wall", 7)
      }
    )
  ),

  "Mighty Wall Ledge": Area(
    locations = Locations(
      events = {
        "Beat Mighty Wall": lambda c: lambda s: c.can_clear_whackable(s, attack_works=True)
      },

      eggs = {
        # Fella1 (First)
        "Sunny": None
      },

      shrooms = {
        **shrooms("Mighty Wall Egg Ledge", 3)
      }
    )
  ),

  "Upper": Area(
    area_connections = {
      "Lower": None,
    },
    entrances = {
      "Airborne Armada Lobby Door": Entrance(to=("Airborne Armada Lobby", "Sun Cavern Door"))
    },
    locations = Locations(
      shrooms = {
        **shrooms("Stump", 3)
      }
    )
  ),

  "Waterfall Ledge": Area(
    area_connections = {
      "Lower": None,
      "Ducklings Ledge": lambda c: lambda s: (
        # floating down from the ledge is valid
        c.has_bubble(s)
        or c.has_wings(s)
      )
    },
    entrances = {
      "Lostleaf Ducklings Door - Upper": Entrance(to=("Lostleaf Lake", "Ducklings Door - Upper")),
    },
    locations = Locations(
      eggs = {
        # Fella2 (Waterfall)
        "Starry": None
      }
    )
  ),

  "Ducklings Ledge": Area(
    area_connections = {
      "Lower": None,
      "Ducklings Doorway": lambda c: lambda s: (
        c.can_clear_high_jump_obstacle(s)
      )
    },
    locations = Locations(
      shrooms = {
        **shrooms("Ducklings Ledge", 2)
      }
    )
  ),

  "Ducklings Doorway": Area(
    area_connections = {
      "Waterfall Lower Platform": None,
    },
    entrances = {
      "Lostleaf Ducklings Door - Lower": Entrance(to=("Lostleaf Lake", "Ducklings Door - Lower")),
    }
  ),

  "Moon Cavern Heart Door": Area(
    area_connections = {
      "Lower": lambda c: lambda s: c.has_swim(s)
    },
    entrances = {
      "Moon Cavern Heart Door": Entrance(
        to = ("Moon Cavern", "Sun Cavern Door"),
        rule = lambda c: lambda s: s.has("Open Moon Cavern Heart Door", c.player)
      )
    },
    locations = Locations(
      events = {
        "Moon Cavern Heart Door": lambda c: lambda s: (
          c.has_hearts(s, 1)
          and c.can_clear_whackable(s, attack_works = True)
        )
      }
    )
  )

}