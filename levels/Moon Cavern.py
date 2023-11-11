from ..shared import *

data = {
  "Start": Area(
    area_connections = {
      "Lower": lambda c: lambda s: c.can_clear_whackable(s, attack_works = True, dive_works = True, throw_works = True),

      "Upper Connector": lambda c: c.can_clear_high_jump_obstacle,

      "Lava Mushroom Platform": None
    },

    entrances = {
      "Sun Cavern Door": Entrance(to=("Sun Cavern", "Moon Cavern Heart Door")),
    },
    locations = Locations(
      cards = {
        # CardPack SHOOTING_STAR
        "Dive": lambda c: lambda s: (
          c.has_swim(s)
          and c.can_clear_whackable(s, dive_works = True)
        )
      },
      shrooms = {
        **shrooms("Dive Holes", 6, lambda c: lambda s: c.can_clear_whackable(s, dive_works = True)),
        **shrooms("Lava Platforms", 4),
        **shrooms("Dive Puzzle", 3, lambda c: lambda s: (
          c.can_bubble_jump(s)
          or c.has_dive(s)
          or c.can_super_bounce(s)
          or c.has_flight(s)
        )),
        "Potionfall": None
      }
    )
  ),

  "Upper Connector": Area(
    area_connections = {
      "Upper": lambda c: c.can_clear_high_jump_obstacle,
      "Start": None
    },
    locations = Locations(
      shrooms = {
        "Lonely Shroom": None
      }
    )
  ),

  "Upper": Area(
    area_connections = {
      "Upper Connector": None
    },
    entrances = {
      # "Prismic Lobby Door": Entrance(to=("Prismic Lobby", "Moon Cavern Door")),
    },
    locations = Locations(
      eggs = {
        # Fella4 (Depths Shot)
        "Keehee Climb": lambda c: lambda s: (
          c.can_bubble_jump(s)
          or (
            c.has_wings(s)
            and (
              c.has_high_jump(s)
              or c.has_dive(s)
            )
          )
          or c.has_flight(s)
        )
      },
      cards = {
        # CardPack KOI_CAVE
        "Before Prismic Lobby": None
      },
      shrooms = {
        **shrooms("Prismic Pathway", 3),
        **shrooms("Prismic Statue", 2),
        **shrooms("Prismic Entrance", 3)
      }
    )
  ),

  "Lava Mushroom Platform": Area(
    area_connections = {
      "Start": lambda c: c.can_clear_high_jump_obstacle,
      "Nightmare Lobby Door Platform": lambda c: lambda s: (
        c.can_clear_high_jump_obstacle(s)
        or c.can_smuggle_jester_boots(s)
      )
    },
    locations = Locations(
      shrooms = {
        **shrooms("Lava Mushroom Platform", 2)
      }
    )
  ),

  "Nightmare Lobby Door Platform": Area(
    entrances = {
      # "Nightmare Lobby Door": Entrance(
      #   to = ("Nightmare Lobby", "Moon Cavern Door"),
      #   rule = lambda c: lambda s: (
      #     s.has("Doused Nightmare Lobby Entrance", c.player)
      #     or c.can_hitlaunch_cancel(s)
      #   )
      # )
    },
    locations = Locations(
      events = {
        "Doused Nightmare Lobby Entrance": lambda c: c.can_douse_flames
      }
    )
  ),

  "Lower": Area(
    area_connections = {
      "Start": lambda c: lambda s: c.can_clear_whackable(s, attack_works = True, throw_works = True)
    },
    locations = Locations(
      eggs = {
        # Fella3 (Depths Dive)
        "Dive Puzzle": lambda c: lambda s: c.can_clear_whackable(s, dive_works = True)
      }
    )
  )
}
