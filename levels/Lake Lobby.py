from ..shared import *

hidden_passage_reqs: ConnectionRuleFactory = lambda c: lambda s: (
  s.has("Open Lake Lobby Gallery Exit", c.player)
  or c.can_clear_whackable(s, attack_works = True, roll_works = True, throw_works = True)
)

data = {
  "Lobby": Area(
    area_connections = {
      "Hidden Passage Connector": hidden_passage_reqs,
      "Trees": lambda c: lambda s: (
        c.options.movement >= 2
        or c.can_clear_high_jump_obstacle(s)
      )
    },
    entrances = {
      "Sun Cavern Door": Entrance(to=("Sun Cavern", "Lostleaf Lobby Door")),
      # "Lostleaf Door": Entrance(to=("Lostleaf Lake", "Lostleaf Lobby Door"))
    },
    locations = Locations(
      shrooms = {
        **shrooms("Bridge", 3),
      },
    )
  ),

  "Trees": Area(
    area_connections = {
      "Lobby": None
    },
    locations = Locations(
      eggs = {
        # Fella Cave5 (Lake Lobby)
        "Blue Spots": None
      },
      shrooms = {
        **shrooms("Trees", 3)
      },
      cards = {
        # CardPack NURIKABE

        "Mighty Wall": None
      }
    )
  ),

  "Hidden Passage Connector": Area(
    area_connections = {
      "Lobby": None,
      "Hidden Wall": None
    },
    locations = Locations(
      events = {
        "Lake Lobby Breakable Wall": None
      }
    )
  ),

  "Hidden Wall": Area(
    area_connections = {
      "Hidden Passage Connector": hidden_passage_reqs
    },
    entrances = {
      # "Gallery Lobby Door": Entrance(to=("Gallery Lobby", "Lostleaf Lobby Door"))
    }
  )
}