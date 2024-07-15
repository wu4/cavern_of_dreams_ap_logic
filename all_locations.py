from dataclasses import dataclass
from typing import Callable, TypeAlias
from collections.abc import Generator, Iterable

@dataclass
class Row:
  item: str
  location: str
  flag: str

class Category:
  rows: list[Row]

  def __init__(self, *rows: str):
    super().__init__()
    i: int = 0
    items_len = len(rows)
    self.rows = []
    while i < items_len:
      self.rows.append(Row(rows[i], rows[i+1], rows[i+2]))
      i += 3

@dataclass
class RowNoLocation:
  item: str
  flag: str

class CategoryNoLocation:
  rows: list[RowNoLocation]

  def __init__(self, *rows: str):
    super().__init__()
    i: int = 0
    items_len = len(rows)
    self.rows = []
    while i < items_len:
      self.rows.append(RowNoLocation(rows[i], rows[i+1]))
      i += 2

def items(c: Category | CategoryNoLocation):
  for i in c.rows:
    yield i.item

def locations(c: Category):
  for i in c.rows:
    yield i.location

others = set(dir())

ability = Category(
  "Tail",  "Sun Cavern - Sage's Blessing 1", "SKILL_ATTACK",
  "Horn",  "Sun Cavern - Sage's Blessing 2", "SKILL_DIVE",
  "Wings", "Sun Cavern - Sage's Blessing 3", "SKILL_HOVER",
  "Bubble","Sun Cavern - Sage's Blessing 4", "SKILL_PROJECTILE",
  "Flight","Sun Cavern - Sage's Blessing 5", "SKILL_FLIGHT",
)

nonVanillaAbility = CategoryNoLocation(
  "Grounded Tail", "SKILL_GROUNDATTACK",
  "Aerial Tail", "SKILL_AIRATTACK",
  "Double Jump", "SKILL_DOUBLEJUMP",
  "Roll", "SKILL_ROLL",
  "Swim", "SKILL_SWIM",
  "Carry", "SKILL_CARRY",
  "Climb", "SKILL_CLIMB",
  "High Jump", "SKILL_HIGHJUMP",
  "Sprint", "SKILL_SPRINT",
  "Super Bounce", "SKILL_SUPERBOUNCE",
  "Super Bubble Jump", "SKILL_SUPERBUBBLEJUMP",
  "Air Swim", "SKILL_AIRSWIM",
)

teleport = CategoryNoLocation(
  "Open Lake Lobby Teleport", "TELEPORT_LAKE",
  "Open Armada Lobby Teleport", "TELEPORT_MONSTER",
  "Open Palace Lobby Teleport", "TELEPORT_PALACE",
  "Open Gallery Lobby Teleport", "TELEPORT_GALLERY",
)

gratitude = Category(
  "Gratitude 1", "Fed Lostleaf Lake Fella", "GRATITUDE1",
  "Gratitude 2", "Fed Airborne Armada Fella", "GRATITUDE2",
  "Gratitude 3", "Fed Prismic Palace Fella", "GRATITUDE3",
  "Gratitude 4", "Fed Gallery of Nightmares Fella", "GRATITUDE4",
)

pickup = Category(
  "Fish Food", "Treehouse - Fish Food", "ITEM_FISH_FOOD",
  "Lady Opal's Egg 1", "Lady Opal's Egg: Castle", "ITEM_PRINCESS_1",
  "Lady Opal's Egg 2", "Lady Opal's Egg: Pool", "ITEM_PRINCESS_2",
  "Lady Opal's Egg 3", "Lady Opal's Egg: Poki-Poki", "ITEM_PRINCESS_3",
)

event = Category(
  "Topple Mighty Wall", "Whack Mighty Wall", "CAVE_NURIKABE_FALLEN",

  "Raise Armada Lobby Pipes", "Armada Lobby Purple Valve", "MONSTER_LOBBY_PIPES_RISEN",
  "Activate Armada Lobby Red Pipe Updraft", "Armada Lobby Green Valve", "MONSTER_LOBBY_STEAM",

  "Run Palace Lobby Faucet", "Palace Lobby Faucet Preston", "PALACE_LOBBY_FAUCET_ON",
  "Activate Palace Lobby Whirlpool", "Palace Lobby Whirlpool Preston", "PALACE_LOBBY_WHIRLPOOL_ON",

  "Open Gallery Lobby Hedge Maze", "Gallery Lobby - Extinguish Torches", "CAVE_GALLERY_LOBBY_TORCH_EXTINGUISH",
  "Open Gallery Lobby Door", "Gallery Lobby - Hedge Maze Preston", "CAVE_GALLERY_LOBBY_GALLERY_OPEN",

  "Raise Lake Swings", "Lostleaf Lake - Winky Tree Target", "LAKE_SWINGS_RAISED",
  "Open Deep Woods", "Lostleaf Lake - Help Shelnert", "LAKE_KAPPA_SUCCESS",
  "Open Crypt", "Lostleaf Lake - Back of the Headstone", "LAKE_CRYPT_GATE_OPEN",
  "Open Church", "Lostleaf Lake - Ring Bell", "LAKE_BELL_RANG",
  "Open Church Basement", "Church - Angel Statue Puzzle", "LAKE_CHURCH_SUCCESS",
  "Open Treehouse", "Lostleaf Lake - Treehouse Preston", "LAKE_BEDROOM_DOOR_OPEN",
  "Lower Deep Woods Egg", "Lostleaf Lake - Tree Puzzle", "LAKE_GROVE_HELPED",

  "Open Armada Cockpit", "Kerrington - Soothe Mr. Kerrington's Boils", "MONSTER_BOILS_REMOVED",
  "Free Armada Buddies", "Kerrington - Generators Puzzle", "MONSTER_TEST_CHUBES_OPENED",
  "Unclog Kerrington's Heart", "Heart - Generators Puzzle", "MONSTER_HEART_ROOM_SUCCESS",
  "Open Kerrington's Heart", "Kerrington - Race", "MONSTER_HEART_GATE_OPEN",
  "Open Medicine Pool", "Kerrington - Medicine Pool Preston", "MONSTER_TAIL_GATE_OPEN",

  "Open Prismic Palace Basement", "Prismic Palace - Basement Star Hoops", "PALACE_ABYSS_HOOP_SUCCESS",
  "Open Palace-Lostleaf Connector", "Palace-Lostleaf Connector - Preston", "PALACE_LAKE_GATE_OPEN",
  "Open Prismic Palace Gate", "Prismic Palace - Angel Statue Puzzle", "PALACE_GATE_RISEN",
  "Unfreeze Prismic Palace", "Prismic Palace - Help Lady Opal", "PALACE_MELTED_ICE",
  "Open Prismic Palace Snowcastle", "Prismic Palace - Snowcastle Preston", "PALACE_SNOW_CASTLE_GATE_OPEN",
  "Open Observatory Shortcut", "Prismic Palace - Observatory Preston", "PALACE_OBSERVATORY_SHORTCUT",
  "Open Bigstar Cave", "Prismic Palace - Bigstar Preston", "PALACE_ICE_WALL_STARFISH_REMOVED",
  "Open Gobbler Cave", "Prismic Palace - Gobbler Preston", "PALACE_ICE_WALL_MORAY_REMOVED",
  "Snooze Gobbler", "Prismic Palace - Feed Gobbler", "PALACE_MORAY_FED",

  "Disable Prismic Palace Seedragons", "Palace Interior - Sentry Control Preston", "PALACE_SENTRIES_DISABLED",
  "Open Bubble Conch Room", "Palace Interior - Seastar Puzzle", "PALACE_TORPEDO_DOOR_OPENED",

  "Open Heaven's Path Exit", "Heaven's Path - Finished Race", "PALACE_SANCTUM_RACE_FINISHED",
  "Open Heaven's Path Race Entrance", "Heaven's Path - Bottom Preston", "PALACE_SANCTUM_STOPPER_RAISED",

  "Raise Dining Room Platform", "Palace Dining Room - Preston", "PALACE_DINING_ROOM_RISEN",

  "Reveal Observatory Item", "Observatory - Telescope Puzzle", "OBSERVATORY_SUCCESS",

  "Open Gallery Doors", "Gallery of Nightmares - Sage's Painting", "GALLERY_SAGE_PAINTING_SUCCESS",
  "Open Mr. Kerrington Painting Gate", "Gallery of Nightmares - Mr. Kerrington's Painting", "GALLERY_MONSTER_PAINTING_SUCCESS",
  "Open Skull's Diamond Eye", "Gallery of Nightmares - Shelnert's Painting", "GALLERY_KAPPA_PAINTING_SUCCESS",
  "Open Gallery-Armada Connector", "Gallery-Armada Connector - Preston", "GALLERY_MONSTER_SHORTCUT_OPEN",
  "Open Gallery of Nightmares Swamp Door", "Gallery of Nightmares - Swamp Angel Statue Puzzle", "GALLERY_STATUE_PUZZLE_SUCCESS",
  "Open Gallery of Nightmares Sewer Chest #1", "Gallery of Nightmares - Sewer Angel Statue Puzzle", "GALLERY_ANGEL_STATUE_SHADOWS_SUCCESS",
  "Open Gallery of Nightmares Sewer Chest #2", "Gallery of Nightmares - Lady Opal's Painting", "GALLERY_PRINCESS_PAINTING_SUCCESS",
  "Open Luna's House", "Gallery of Nightmares - Helped Sniffles", "GALLERY_GIANT_HEALED",
  "Extend Fire Lobby Tongue Platform", "Gallery of Nightmares - Fire Lobby Preston", "GALLERY_FIRE_LOBBY_BRIDGE_EXTENDED",
  "Extend Fire Lobby Frying Pans", "Gallery of Nightmares - Fire Lobby Hoops", "GALLERY_HOOP_SUCCESS",
  "Coils of Agony - Open Shortcut", "Coils of Agony - Hidden Pillar", "CHALICE_BRIDGE_ACTIVE",
  "Wastes of Eternity - Wet", "Gallery of Nightmares - Moisten Wastes of Eternity Painting", "UNDEAD_WET",
)

card = Category(
  "Card: Shroom", "Card: Sun Cavern - Air Vent", "CARD_CAVE_MUSHROOM",
  "Card: Mighty Wall", "Card: Lostleaf Lobby - Branches", "CARD_CAVE_NURIKABE",
  "Card: Pale Carpy", "Card: Moon Cavern - Statue", "CARD_CAVE_KOI_CAVE",
  "Card: Preston", "Card: Armada Lobby - Jester Boots", "CARD_CAVE_SWITCH",
  "Card: Keehee", "Card: Moon Cavern - Dive", "CARD_CAVE_SHOOTING_STAR",
  "Card: Hunger", "Card: Gallery Lobby - Hedge Maze", "CARD_CAVE_HUNGER",

  "Card: Shelnert", "Card: Lostleaf Lake - Teepee", "CARD_LAKE_KAPPA",
  "Card: Shelwart", "Card: Lostleaf Lake - Apple Tree", "CARD_LAKE_CRYPT",
  "Card: Carpy", "Card: Lostleaf Lake - Lake Stump", "CARD_LAKE_KOI",
  "Card: Raay", "Card: Church - Top", "CARD_LAKE_SUN",
  "Card: Sappleing", "Card: Lostleaf Lake - Entry", "CARD_LAKE_SAPLING",
  "Card: Gabby Grove", "Card: Treehouse - Top", "CARD_LAKE_GROVE",

  "Card: Mr. Kerrington", "Card: Kerrington - Slide", "CARD_MONSTER_MONSTER",
  "Card: Skritch", "Card: Kerrington - Pipe", "CARD_MONSTER_SPIN_BLADE",
  "Card: Boiby", "Card: Airborne Armada - Broken Wing", "CARD_MONSTER_BOIL",
  "Card: Dumpling", "Card: Airborne Armada - Behind Entry Drone", "CARD_MONSTER_DUMPLING",
  "Card: F.I.S.H", "Card: Kerrington - Hammocks", "CARD_MONSTER_FISH",
  "Card: Reaper", "Card: Kerrington - Near Mr. Kerrington's Heart", "CARD_MONSTER_FF",

  "Card: Lady Opal", "Card: Observatory", "CARD_PALACE_PRINCESS",
  "Card: Poki-Poki", "Card: Prismic Palace - Top of Observatory", "CARD_PALACE_URCHIN",
  "Card: Pom", "Card: Prismic Palace - Snowcastle", "CARD_PALACE_PALM_TREE_FLOAT",
  "Card: Bigstar", "Card: Prismic Palace - Top of Palace", "CARD_PALACE_SEASTAR",
  "Card: The Gobbler!", "Card: Prismic Palace - Above Pool", "CARD_PALACE_MORAY",
  "Card: Seedragon", "Card: Prismic Palace - Inside Palace", "CARD_PALACE_SENTRY",

  "Card: Rattles", "Card: Gallery of Nightmares - Swamp Castle", "CARD_GALLERY_RATTLES",
  "Card: Sniffles", "Card: Gallery of Nightmares - Sewer Bottom", "CARD_GALLERY_GIANT",
  "Card: Starving Art", "Card: Gallery of Nightmares - Basement Entrance", "CARD_GALLERY_MIMIC_PAINTING",
  "Card: Eternal", "Card: Gallery of Nightmares - Swamp", "CARD_GALLERY_UNDEAD",
  "Card: Heartburn", "Card: Gallery of Nightmares - Frying Pans", "CARD_GALLERY_FIRE_SNAKE",
  "Card: Hawhaw", "Card: Gallery of Nightmares - Above Pits of Despair Painting", "CARD_GALLERY_CHOMP",

  "Card: Fynn", "Card: Sewer - Armada Lobby Side", "CARD_CAVE_DRAGON",
  "Card: Fynn's Siblings", "Card: Sewer - Gallery of Nightmares Side", "CARD_CAVE_FELLA",
  "Card: Sage", "Card: Dream", "CARD_CAVE_SAGE",
  "Card: Luna", "Card: Gallery Lobby - Behind the Gallery", "CARD_CAVE_VILLAIN",
  "Card: Boxed Nightmare", "Card: Palace Dining Room - Top", "CARD_CAVE_PANDORA",
  "Card: Frozen King", "Card: Palace Lobby - Top", "CARD_CAVE_KING",
)

egg = Category(
  "Sun Egg", "Egg: Sun Cavern - Mighty Wall", "FELLA_CAVE1",
  "Green Starry Egg", "Egg: Sun Cavern - Waterfall", "FELLA_CAVE2",
  "Blue Moon Egg", "Egg: Moon Cavern - Dive Puzzle", "FELLA_CAVE3",
  "Blorange Striped Egg", "Egg: Moon Cavern - Keehee Climb", "FELLA_CAVE4",
  "Blue Dotted Egg", "Egg: Lostleaf Lobby - Branches", "FELLA_CAVE5",
  "American Egg", "Egg: Armada Lobby - Cannon", "FELLA_CAVE6",
  "Red Swirly Egg", "Egg: Palace Lobby - Submerged", "FELLA_CAVE7",
  "Ghost Egg", "Egg: Gallery Lobby - Lostleaf Lobby Entryway", "FELLA_CAVE8",

  "Hatchable Egg: Lostleaf Lake", "Egg: Lostleaf Lake - Entry Stump", "FELLA_LAKE1",
  "Easter Zig-zag Egg", "Egg: Lostleaf Lake - Jester Boots", "FELLA_LAKE2",
  "Apple Egg", "Egg: Lostleaf Lake - Lake Log", "FELLA_LAKE3",
  "Snowfall Egg", "Egg: Lostleaf Lake - Waterfall", "FELLA_LAKE4",
  "Fishbones Egg", "Egg: Crypt - Shelwart's Gravestone", "FELLA_LAKE5",
  "Sunshine Egg", "Egg: Lostleaf Lake - Deep Woods Puzzle", "FELLA_LAKE6",
  "Birds Egg", "Egg: Lostleaf Lake - Near the Treehouse", "FELLA_LAKE7",
  "Stained Glass Egg", "Egg: Church - Below the Angel Statues", "FELLA_LAKE8",

  "Hatchable Egg: Airborne Armada", "Egg: Airborne Armada - Mr. Kerrington's Tail", "FELLA_MONSTER1",
  "Burning Egg", "Egg: Fire Drone", "FELLA_MONSTER2",
  "Bat Egg", "Egg: Kerrington - Slide", "FELLA_MONSTER3",
  "Doggy Egg", "Egg: Kerrington - Dog Food", "FELLA_MONSTER4",
  "Spooky Egg", "Egg: Kerrington - Boiler", "FELLA_MONSTER5",
  "Smiley Egg", "Egg: Kerrington - Pipe", "FELLA_MONSTER6",
  "Heart Egg", "Egg: Mr. Kerrington's Heart", "FELLA_MONSTER7",
  "Dumpling Egg", "Egg: Kerrington - Dumpling", "FELLA_MONSTER8",

  "Hatchable Egg: Prismic Palace", "Egg: Prismic Palace - Snowcastle", "FELLA_PALACE1",
  "Ornate Egg", "Egg: Palace Dining Room", "FELLA_PALACE2",
  "Starlit Egg", "Egg: Observatory", "FELLA_PALACE3",
  "Checkered Egg", "Egg: Prismic Palace - Observatory Slide", "FELLA_PALACE4",
  "Flower Egg", "Egg: Prismic Palace - Bigstar", "FELLA_PALACE5",
  "Snowstorm Egg", "Egg: Prismic Palace - Top of the Palace", "FELLA_PALACE6",
  "Zig-zag Egg", "Egg: Palace Interior - Basement", "FELLA_PALACE7",
  "Happy Egg", "Egg: Prismic Palace - Gobbler", "FELLA_PALACE8",

  "Red Eyes Egg", "Egg: Coils of Agony", "FELLA_CHALICE1",
  "Seaweed Egg", "Egg: Pits of Despair", "FELLA_DROWN1",
  "Moonlight Egg", "Egg: Wastes of Eternity", "FELLA_UNDEAD1",

  "Hatchable Egg: Gallery of Nightmares", "Egg: Gallery of Nightmares - Matryoshka Egg", "FELLA_GALLERY1",
  "Ripped Egg", "Egg: Gallery of Nightmares - Skull's Eye", "FELLA_GALLERY2",
  "Robot Egg", "Egg: Gallery of Nightmares - Mr. Kerrington Painting", "FELLA_GALLERY3",
  "Bricked Egg", "Egg: Gallery of Nightmares - Sewer", "FELLA_GALLERY4",
  "Specter Egg", "Egg: Gallery of Nightmares - Deepest Darkness", "FELLA_GALLERY5",
)

shroom = Category(
  "Cavern Shroom 1", "Shroom: Sun Cavern - Mighty Wall Ground 1", "NOTE_CAVE2",
  "Cavern Shroom 2", "Shroom: Sun Cavern - Mighty Wall Ground 2", "NOTE_CAVE3",
  "Cavern Shroom 3", "Shroom: Sun Cavern - Mighty Wall Ground 3", "NOTE_CAVE4",
  "Cavern Shroom 4", "Shroom: Sun Cavern - Mighty Wall Ground 4", "NOTE_CAVE5",
  "Cavern Shroom 5", "Shroom: Sun Cavern - Mighty Wall Egg Ledge 1", "NOTE_CAVE1",
  "Cavern Shroom 6", "Shroom: Sun Cavern - Mighty Wall Egg Ledge 2", "NOTE_CAVE6",
  "Cavern Shroom 7", "Shroom: Sun Cavern - Mighty Wall Egg Ledge 3", "NOTE_CAVE7",
  "Cavern Shroom 8", "Shroom: Sun Cavern - High Jump Ledge 1", "NOTE_CAVE8",
  "Cavern Shroom 9", "Shroom: Sun Cavern - High Jump Ledge 2", "NOTE_CAVE9",
  "Cavern Shroom 10", "Shroom: Sun Cavern - Tail Spin Ledge 1", "NOTE_CAVE10",
  "Cavern Shroom 11", "Shroom: Sun Cavern - Tail Spin Ledge 2", "NOTE_CAVE11",
  "Cavern Shroom 12", "Shroom: Sun Cavern - Ducklings Ledge 1", "NOTE_CAVE12",
  "Cavern Shroom 13", "Shroom: Sun Cavern - Ducklings Ledge 2", "NOTE_CAVE13",
  "Cavern Shroom 14", "Shroom: Sun Cavern - Armada Entrance 1", "NOTE_CAVE14",
  "Cavern Shroom 15", "Shroom: Sun Cavern - Armada Entrance 2", "NOTE_CAVE15",
  "Cavern Shroom 16", "Shroom: Sun Cavern - Armada Entrance 3", "NOTE_CAVE16",
  "Cavern Shroom 17", "Shroom: Sun Cavern - Vine Ledge 1", "NOTE_CAVE17",
  "Cavern Shroom 18", "Shroom: Sun Cavern - Vine Ledge 2", "NOTE_CAVE18",
  "Cavern Shroom 19", "Shroom: Moon Cavern - Dive Holes 1", "NOTE_CAVE19",
  "Cavern Shroom 20", "Shroom: Moon Cavern - Dive Holes 2", "NOTE_CAVE20",
  "Cavern Shroom 21", "Shroom: Moon Cavern - Dive Holes 3", "NOTE_CAVE21",
  "Cavern Shroom 22", "Shroom: Moon Cavern - Dive Holes 4", "NOTE_CAVE22",
  "Cavern Shroom 23", "Shroom: Moon Cavern - Dive Holes 5", "NOTE_CAVE23",
  "Cavern Shroom 24", "Shroom: Moon Cavern - Dive Holes 6", "NOTE_CAVE24",
  "Cavern Shroom 25", "Shroom: Moon Cavern - Dive Puzzle 1", "NOTE_CAVE25",
  "Cavern Shroom 26", "Shroom: Moon Cavern - Dive Puzzle 2", "NOTE_CAVE26",
  "Cavern Shroom 27", "Shroom: Moon Cavern - Dive Puzzle 3", "NOTE_CAVE27",
  "Cavern Shroom 28", "Shroom: Moon Cavern - Potionfall", "NOTE_CAVE28",
  "Cavern Shroom 29", "Shroom: Moon Cavern - Lonely Shroom", "NOTE_CAVE29",
  "Cavern Shroom 30", "Shroom: Moon Cavern - Palace Lobby Pathway 2", "NOTE_CAVE30",
  "Cavern Shroom 31", "Shroom: Moon Cavern - Palace Lobby Pathway 1", "NOTE_CAVE31",
  "Cavern Shroom 32", "Shroom: Moon Cavern - Palace Lobby Pathway 3", "NOTE_CAVE32",
  "Cavern Shroom 33", "Shroom: Moon Cavern - Palace Lobby Statue 1", "NOTE_CAVE33",
  "Cavern Shroom 34", "Shroom: Moon Cavern - Palace Lobby Statue 2", "NOTE_CAVE34",
  "Cavern Shroom 35", "Shroom: Moon Cavern - Palace Lobby Entryway 1", "NOTE_CAVE35",
  "Cavern Shroom 36", "Shroom: Moon Cavern - Palace Lobby Entryway 2", "NOTE_CAVE36",
  "Cavern Shroom 37", "Shroom: Moon Cavern - Palace Lobby Entryway 3", "NOTE_CAVE37",
  "Cavern Shroom 38", "Shroom: Moon Cavern - Lava Platforms 1", "NOTE_CAVE38",
  "Cavern Shroom 39", "Shroom: Moon Cavern - Lava Platforms 2", "NOTE_CAVE39",
  "Cavern Shroom 40", "Shroom: Moon Cavern - Lava Platforms 3", "NOTE_CAVE40",
  "Cavern Shroom 41", "Shroom: Moon Cavern - Lava Platforms 4", "NOTE_CAVE41",
  "Cavern Shroom 42", "Shroom: Moon Cavern - Lava Mushroom Platform 1", "NOTE_CAVE42",
  "Cavern Shroom 43", "Shroom: Moon Cavern - Lava Mushroom Platform 2", "NOTE_CAVE43",
  "Cavern Shroom 44", "Shroom: Lostleaf Lobby - Bridge 2", "NOTE_CAVE44",
  "Cavern Shroom 45", "Shroom: Lostleaf Lobby - Bridge 3", "NOTE_CAVE45",
  "Cavern Shroom 46", "Shroom: Lostleaf Lobby - Bridge 1", "NOTE_CAVE46",
  "Cavern Shroom 47", "Shroom: Lostleaf Lobby - Trees 1", "NOTE_CAVE47",
  "Cavern Shroom 48", "Shroom: Lostleaf Lobby - Trees 2", "NOTE_CAVE48",
  "Cavern Shroom 49", "Shroom: Lostleaf Lobby - Trees 3", "NOTE_CAVE49",
  "Cavern Shroom 50", "Shroom: Armada Lobby - Cliffside 1", "NOTE_CAVE50",
  "Cavern Shroom 51", "Shroom: Armada Lobby - Cliffside 2", "NOTE_CAVE51",
  "Cavern Shroom 52", "Shroom: Armada Lobby - Cliffside 4", "NOTE_CAVE52",
  "Cavern Shroom 53", "Shroom: Armada Lobby - Cliffside 5", "NOTE_CAVE53",
  "Cavern Shroom 54", "Shroom: Armada Lobby - Cliffside 3", "NOTE_CAVE54",
  "Cavern Shroom 55", "Shroom: Palace Lobby - Ledges 1", "NOTE_CAVE55",
  "Cavern Shroom 56", "Shroom: Palace Lobby - Ledges 6", "NOTE_CAVE56",
  "Cavern Shroom 57", "Shroom: Palace Lobby - Ledges 5", "NOTE_CAVE57",
  "Cavern Shroom 58", "Shroom: Palace Lobby - Ledges 3", "NOTE_CAVE58",
  "Cavern Shroom 59", "Shroom: Palace Lobby - Ledges 2", "NOTE_CAVE59",
  "Cavern Shroom 60", "Shroom: Palace Lobby - Ledges 4", "NOTE_CAVE60",
  "Cavern Shroom 61", "Shroom: Palace Lobby - Underwater 1", "NOTE_CAVE61",
  "Cavern Shroom 62", "Shroom: Palace Lobby - Underwater 2", "NOTE_CAVE62",
  "Cavern Shroom 63", "Shroom: Palace Lobby - Underwater 3", "NOTE_CAVE63",
  "Cavern Shroom 64", "Shroom: Palace Lobby - Underwater 5", "NOTE_CAVE64",
  "Cavern Shroom 65", "Shroom: Palace Lobby - Underwater 6", "NOTE_CAVE65",
  "Cavern Shroom 66", "Shroom: Palace Lobby - Underwater 4", "NOTE_CAVE66",
  "Cavern Shroom 67", "Shroom: Gallery Lobby - Fountain 1", "NOTE_CAVE67",
  "Cavern Shroom 68", "Shroom: Gallery Lobby - Fountain 2", "NOTE_CAVE68",
  "Cavern Shroom 69", "Shroom: Gallery Lobby - Fountain 3", "NOTE_CAVE69",
  "Cavern Shroom 70", "Shroom: Gallery Lobby - Fountain 4", "NOTE_CAVE70",
  "Cavern Shroom 71", "Shroom: Gallery Lobby - Castle Hill 3", "NOTE_CAVE71",
  "Cavern Shroom 72", "Shroom: Gallery Lobby - Castle Hill 5", "NOTE_CAVE72",
  "Cavern Shroom 73", "Shroom: Gallery Lobby - Castle Hill 4", "NOTE_CAVE73",
  "Cavern Shroom 74", "Shroom: Gallery Lobby - Castle Hill 1", "NOTE_CAVE74",
  "Cavern Shroom 75", "Shroom: Gallery Lobby - Castle Hill 2", "NOTE_CAVE75",
  "Cavern Shroom 76", "Shroom: Gallery Lobby - Entryway 1", "NOTE_CAVE76",
  "Cavern Shroom 77", "Shroom: Gallery Lobby - Entryway 4", "NOTE_CAVE77",
  "Cavern Shroom 78", "Shroom: Gallery Lobby - Entryway 5", "NOTE_CAVE78",
  "Cavern Shroom 79", "Shroom: Gallery Lobby - Entryway 3", "NOTE_CAVE79",
  "Cavern Shroom 80", "Shroom: Gallery Lobby - Entryway 2", "NOTE_CAVE80",

  "Lostleaf Shroom 1", "Shroom: Lostleaf Lake - Treehouse Branches 4", "NOTE_LAKE1",
  "Lostleaf Shroom 2", "Shroom: Lostleaf Lake - Treehouse Branches 3", "NOTE_LAKE2",
  "Lostleaf Shroom 3", "Shroom: Lostleaf Lake - Treehouse Branches 1", "NOTE_LAKE3",
  "Lostleaf Shroom 4", "Shroom: Lostleaf Lake - Treehouse Branches 2", "NOTE_LAKE4",
  "Lostleaf Shroom 5", "Shroom: Lostleaf Lake - Treehouse Branches 6", "NOTE_LAKE5",
  "Lostleaf Shroom 6", "Shroom: Lostleaf Lake - Treehouse Branches 5", "NOTE_LAKE6",
  "Lostleaf Shroom 7", "Shroom: Lostleaf Lake - Deep Woods 2", "NOTE_LAKE7",
  "Lostleaf Shroom 8", "Shroom: Lostleaf Lake - Deep Woods 1", "NOTE_LAKE8",
  "Lostleaf Shroom 9", "Shroom: Lostleaf Lake - Deep Woods 3", "NOTE_LAKE9",
  "Lostleaf Shroom 10", "Shroom: Lostleaf Lake - Deep Woods 6", "NOTE_LAKE10",
  "Lostleaf Shroom 11", "Shroom: Lostleaf Lake - Deep Woods 4", "NOTE_LAKE11",
  "Lostleaf Shroom 12", "Shroom: Lostleaf Lake - Deep Woods 5", "NOTE_LAKE12",
  "Lostleaf Shroom 13", "Shroom: Lostleaf Lake - Behind Church 3", "NOTE_LAKE13",
  "Lostleaf Shroom 14", "Shroom: Lostleaf Lake - Behind Church 1", "NOTE_LAKE14",
  "Lostleaf Shroom 15", "Shroom: Lostleaf Lake - Behind Church 2", "NOTE_LAKE15",
  "Lostleaf Shroom 16", "Shroom: Lostleaf Lake - Teepee 1", "NOTE_LAKE16",
  "Lostleaf Shroom 17", "Shroom: Lostleaf Lake - Teepee 3", "NOTE_LAKE17",
  "Lostleaf Shroom 18", "Shroom: Lostleaf Lake - Teepee 2", "NOTE_LAKE18",
  "Lostleaf Shroom 19", "Shroom: Lostleaf Lake - Waterfall Logs 2", "NOTE_LAKE19",
  "Lostleaf Shroom 20", "Shroom: Lostleaf Lake - Waterfall Logs 3", "NOTE_LAKE20",
  "Lostleaf Shroom 21", "Shroom: Lostleaf Lake - Waterfall Logs 4", "NOTE_LAKE21",
  "Lostleaf Shroom 22", "Shroom: Lostleaf Lake - Waterfall Logs 1", "NOTE_LAKE22",
  "Lostleaf Shroom 23", "Shroom: Lostleaf Lake - Lake Logs 2", "NOTE_LAKE23",
  "Lostleaf Shroom 24", "Shroom: Lostleaf Lake - Lake Logs 1", "NOTE_LAKE24",
  "Lostleaf Shroom 25", "Shroom: Lostleaf Lake - Lake Logs 3", "NOTE_LAKE25",
  "Lostleaf Shroom 26", "Shroom: Lostleaf Lake - Lake Logs 4", "NOTE_LAKE26",
  "Lostleaf Shroom 27", "Shroom: Lostleaf Lake - Winky Bouncy Mushroom 1", "NOTE_LAKE27",
  "Lostleaf Shroom 28", "Shroom: Lostleaf Lake - Winky Bouncy Mushroom 2", "NOTE_LAKE28",
  "Lostleaf Shroom 29", "Shroom: Lostleaf Lake - Winky Bouncy Mushroom 3", "NOTE_LAKE29",
  "Lostleaf Shroom 30", "Shroom: Lostleaf Lake - Ramp to Winky Tree 1", "NOTE_LAKE30",
  "Lostleaf Shroom 31", "Shroom: Lostleaf Lake - Ramp to Winky Tree 3", "NOTE_LAKE31",
  "Lostleaf Shroom 32", "Shroom: Lostleaf Lake - Ramp to Winky Tree 5", "NOTE_LAKE32",
  "Lostleaf Shroom 33", "Shroom: Lostleaf Lake - Ramp to Winky Tree 2", "NOTE_LAKE33",
  "Lostleaf Shroom 34", "Shroom: Lostleaf Lake - Ramp to Winky Tree 4", "NOTE_LAKE34",
  "Lostleaf Shroom 35", "Shroom: Lostleaf Lake - Deep Woods Entryway 1", "NOTE_LAKE35",
  "Lostleaf Shroom 36", "Shroom: Lostleaf Lake - Deep Woods Entryway 2", "NOTE_LAKE36",
  "Lostleaf Shroom 37", "Shroom: Lostleaf Lake - Deep Woods Entryway 3", "NOTE_LAKE37",
  "Lostleaf Shroom 38", "Shroom: Lostleaf Lake - Lake Gravestone 1", "NOTE_LAKE38",
  "Lostleaf Shroom 39", "Shroom: Lostleaf Lake - Lake Gravestone 2", "NOTE_LAKE39",
  "Lostleaf Shroom 40", "Shroom: Lostleaf Lake - Lake Gravestone 3", "NOTE_LAKE40",
  "Lostleaf Shroom 41", "Shroom: Lostleaf Lake - Bridge 2", "NOTE_LAKE41",
  "Lostleaf Shroom 42", "Shroom: Lostleaf Lake - Bridge 1", "NOTE_LAKE42",
  "Lostleaf Shroom 43", "Shroom: Lostleaf Lake - Bridge 3", "NOTE_LAKE43",
  "Lostleaf Shroom 44", "Shroom: Lostleaf Lake - Winky Apple Tree 4", "NOTE_LAKE44",
  "Lostleaf Shroom 45", "Shroom: Lostleaf Lake - Winky Apple Tree 3", "NOTE_LAKE45",
  "Lostleaf Shroom 46", "Shroom: Lostleaf Lake - Winky Apple Tree 1", "NOTE_LAKE46",
  "Lostleaf Shroom 47", "Shroom: Lostleaf Lake - Winky Apple Tree 2", "NOTE_LAKE47",
  "Lostleaf Shroom 48", "Shroom: Lostleaf Lake - Church Entryway 3", "NOTE_LAKE48",
  "Lostleaf Shroom 49", "Shroom: Lostleaf Lake - Church Entryway 2", "NOTE_LAKE49",
  "Lostleaf Shroom 50", "Shroom: Lostleaf Lake - Church Entryway 1", "NOTE_LAKE50",
  "Lostleaf Shroom 51", "Shroom: Church - Pews 4", "NOTE_LAKE51",
  "Lostleaf Shroom 52", "Shroom: Church - Pews 2", "NOTE_LAKE52",
  "Lostleaf Shroom 53", "Shroom: Church - Pews 1", "NOTE_LAKE53",
  "Lostleaf Shroom 54", "Shroom: Church - Pews 3", "NOTE_LAKE54",
  "Lostleaf Shroom 55", "Shroom: Treehouse - Corners 4", "NOTE_LAKE55",
  "Lostleaf Shroom 56", "Shroom: Treehouse - Corners 3", "NOTE_LAKE56",
  "Lostleaf Shroom 57", "Shroom: Treehouse - Corners 2", "NOTE_LAKE57",
  "Lostleaf Shroom 58", "Shroom: Treehouse - Corners 1", "NOTE_LAKE58",
  "Lostleaf Shroom 59", "Shroom: Treehouse - Corners 5", "NOTE_LAKE59",
  "Lostleaf Shroom 60", "Shroom: Treehouse - Corners 6", "NOTE_LAKE60",

  "Armada Shroom 1", "Shroom: Airborne Armada - Bouncy Shroom 1", "NOTE_MONSTER1",
  "Armada Shroom 2", "Shroom: Airborne Armada - Bouncy Shroom 3", "NOTE_MONSTER2",
  "Armada Shroom 3", "Shroom: Airborne Armada - Bouncy Shroom 2", "NOTE_MONSTER3",
  "Armada Shroom 4", "Shroom: Airborne Armada - Bouncy Shroom 4", "NOTE_MONSTER4",
  "Armada Shroom 5", "Shroom: Airborne Armada - Entry Pathway 5", "NOTE_MONSTER5",
  "Armada Shroom 6", "Shroom: Airborne Armada - Front Entrance 1", "NOTE_MONSTER6",
  "Armada Shroom 7", "Shroom: Airborne Armada - Front Entrance 2", "NOTE_MONSTER7",
  "Armada Shroom 8", "Shroom: Airborne Armada - Front Entrance 3", "NOTE_MONSTER8",
  "Armada Shroom 9", "Shroom: Airborne Armada - Side 1", "NOTE_MONSTER9",
  "Armada Shroom 10", "Shroom: Airborne Armada - Side 2", "NOTE_MONSTER10",
  "Armada Shroom 11", "Shroom: Airborne Armada - Side Yellow Ledge", "NOTE_MONSTER11",
  "Armada Shroom 12", "Shroom: Airborne Armada - Back Entrance 1", "NOTE_MONSTER12",
  "Armada Shroom 13", "Shroom: Airborne Armada - Back Entrance 2", "NOTE_MONSTER13",
  "Armada Shroom 14", "Shroom: Airborne Armada - Back Entrance 3", "NOTE_MONSTER14",
  "Armada Shroom 15", "Shroom: Airborne Armada - Back Entrance 4", "NOTE_MONSTER15",
  "Armada Shroom 16", "Shroom: Airborne Armada - Back Entrance 6", "NOTE_MONSTER16",
  "Armada Shroom 17", "Shroom: Airborne Armada - Back Entrance 5", "NOTE_MONSTER17",
  "Armada Shroom 18", "Shroom: Airborne Armada - Topside 1", "NOTE_MONSTER18",
  "Armada Shroom 19", "Shroom: Airborne Armada - Topside 2", "NOTE_MONSTER19",
  "Armada Shroom 20", "Shroom: Airborne Armada - Topside 3", "NOTE_MONSTER20",
  "Armada Shroom 21", "Shroom: Airborne Armada - Entry Pathway 1", "NOTE_MONSTER21",
  "Armada Shroom 22", "Shroom: Airborne Armada - Entry Pathway 2", "NOTE_MONSTER22",
  "Armada Shroom 23", "Shroom: Airborne Armada - Entry Pathway 3", "NOTE_MONSTER23",
  "Armada Shroom 24", "Shroom: Airborne Armada - Entry Pathway 4", "NOTE_MONSTER24",
  "Armada Shroom 25", "Shroom: Kerrington - Rain Entryway 4", "NOTE_MONSTER25",
  "Armada Shroom 26", "Shroom: Kerrington - Rain Entryway 3", "NOTE_MONSTER26",
  "Armada Shroom 27", "Shroom: Kerrington - Rain Entryway 2", "NOTE_MONSTER27",
  "Armada Shroom 28", "Shroom: Kerrington - Hammocks Entryway 2", "NOTE_MONSTER28",
  "Armada Shroom 29", "Shroom: Kerrington - Hammocks Entryway 1", "NOTE_MONSTER29",
  "Armada Shroom 30", "Shroom: Kerrington - Cockpit Entry 3", "NOTE_MONSTER30",
  "Armada Shroom 31", "Shroom: Kerrington - Cockpit Entry 2", "NOTE_MONSTER31",
  "Armada Shroom 32", "Shroom: Kerrington - Cockpit Entry 1", "NOTE_MONSTER32",
  "Armada Shroom 33", "Shroom: Kerrington - Cockpit Entry 6", "NOTE_MONSTER33",
  "Armada Shroom 34", "Shroom: Kerrington - Cockpit Entry 5", "NOTE_MONSTER34",
  "Armada Shroom 35", "Shroom: Kerrington - Cockpit Entry 4", "NOTE_MONSTER35",
  "Armada Shroom 36", "Shroom: Kerrington - Rain Below Medicine 3", "NOTE_MONSTER36",
  "Armada Shroom 37", "Shroom: Kerrington - Rain Below Medicine 2", "NOTE_MONSTER37",
  "Armada Shroom 38", "Shroom: Kerrington - Rain Below Boiler 1", "NOTE_MONSTER38",
  "Armada Shroom 39", "Shroom: Kerrington - Rain Below Boiler 2", "NOTE_MONSTER39",
  "Armada Shroom 40", "Shroom: Kerrington - Rain Below Boiler 3", "NOTE_MONSTER40",
  "Armada Shroom 41", "Shroom: Kerrington - Rain Below Medicine 1", "NOTE_MONSTER41",
  "Armada Shroom 42", "Shroom: Kerrington - Rain Plant Base", "NOTE_MONSTER42",
  "Armada Shroom 43", "Shroom: Kerrington - Rain Plant 1", "NOTE_MONSTER43",
  "Armada Shroom 44", "Shroom: Kerrington - Lab Rain Connector 5", "NOTE_MONSTER44",
  "Armada Shroom 45", "Shroom: Kerrington - Lab Rain Connector 6", "NOTE_MONSTER45",
  "Armada Shroom 46", "Shroom: Kerrington - Lab Rain Connector 4", "NOTE_MONSTER46",
  "Armada Shroom 47", "Shroom: Kerrington - Lab Rain Connector 3", "NOTE_MONSTER47",
  "Armada Shroom 48", "Shroom: Kerrington - Lab Rain Connector 2", "NOTE_MONSTER48",
  "Armada Shroom 49", "Shroom: Kerrington - Lab Rain Connector 1", "NOTE_MONSTER49",
  "Armada Shroom 50", "Shroom: Kerrington - Lab Entryway 4", "NOTE_MONSTER50",
  "Armada Shroom 51", "Shroom: Kerrington - Lab Entryway 3", "NOTE_MONSTER51",
  "Armada Shroom 52", "Shroom: Kerrington - Lab Entryway 2", "NOTE_MONSTER52",
  "Armada Shroom 53", "Shroom: Kerrington - Lab Entryway 1", "NOTE_MONSTER53",
  "Armada Shroom 54", "Shroom: Kerrington - Pipe 5", "NOTE_MONSTER54",
  "Armada Shroom 55", "Shroom: Kerrington - Pipe 4", "NOTE_MONSTER55",
  "Armada Shroom 56", "Shroom: Kerrington - Pipe 3", "NOTE_MONSTER56",
  "Armada Shroom 57", "Shroom: Kerrington - Pipe 2", "NOTE_MONSTER57",
  "Armada Shroom 58", "Shroom: Kerrington - Pipe 1", "NOTE_MONSTER58",
  "Armada Shroom 59", "Shroom: Kerrington - Pipe Ramp 3", "NOTE_MONSTER59",
  "Armada Shroom 60", "Shroom: Kerrington - Pipe Ramp 2", "NOTE_MONSTER60",
  "Armada Shroom 61", "Shroom: Kerrington - Pipe Ramp 1", "NOTE_MONSTER61",
  "Armada Shroom 62", "Shroom: Kerrington - Rain Entryway 1", "NOTE_MONSTER62",
  "Armada Shroom 63", "Shroom: Kerrington - Slide Entryway 1", "NOTE_MONSTER63",
  "Armada Shroom 64", "Shroom: Kerrington - Slide Entryway 2", "NOTE_MONSTER64",
  "Armada Shroom 65", "Shroom: Kerrington - Slide Entryway 3", "NOTE_MONSTER65",
  "Armada Shroom 66", "Shroom: Kerrington - Rain Plant 2", "NOTE_MONSTER66",
  "Armada Shroom 67", "Shroom: Kerrington - Rain Plant 3", "NOTE_MONSTER67",
  "Armada Shroom 68", "Shroom: Kerrington - Rain Plant 4", "NOTE_MONSTER68",
  "Armada Shroom 69", "Shroom: Kerrington - Rain Above Boiler 4", "NOTE_MONSTER69",
  "Armada Shroom 70", "Shroom: Kerrington - Rain Above Boiler 2", "NOTE_MONSTER70",
  "Armada Shroom 71", "Shroom: Kerrington - Rain Above Boiler 1", "NOTE_MONSTER71",
  "Armada Shroom 72", "Shroom: Kerrington - Rain Above Boiler 3", "NOTE_MONSTER72",
  "Armada Shroom 73", "Shroom: Armada Entry Drone - Ledges 6", "NOTE_MONSTER73",
  "Armada Shroom 74", "Shroom: Armada Entry Drone - Ledges 5", "NOTE_MONSTER74",
  "Armada Shroom 75", "Shroom: Armada Entry Drone - Ledges 4", "NOTE_MONSTER75",
  "Armada Shroom 76", "Shroom: Armada Entry Drone - Ledges 3", "NOTE_MONSTER76",
  "Armada Shroom 77", "Shroom: Armada Entry Drone - Ledges 7", "NOTE_MONSTER77",
  "Armada Shroom 78", "Shroom: Armada Entry Drone - Ledges 8", "NOTE_MONSTER78",
  "Armada Shroom 79", "Shroom: Armada Entry Drone - Ledges 1", "NOTE_MONSTER79",
  "Armada Shroom 80", "Shroom: Armada Entry Drone - Ledges 2", "NOTE_MONSTER80",

  "Palace Shroom 1", "Shroom: Prismic Palace - Poms 5", "NOTE_PALACE1",
  "Palace Shroom 2", "Shroom: Prismic Palace - Poms 3", "NOTE_PALACE2",
  "Palace Shroom 3", "Shroom: Prismic Palace - Poms 4", "NOTE_PALACE3",
  "Palace Shroom 4", "Shroom: Prismic Palace - Poms 2", "NOTE_PALACE4",
  "Palace Shroom 5", "Shroom: Prismic Palace - Poms 1", "NOTE_PALACE5",
  "Palace Shroom 6", "Shroom: Prismic Palace - Entry Tree 2", "NOTE_PALACE6",
  "Palace Shroom 7", "Shroom: Prismic Palace - Entry Tree 1", "NOTE_PALACE7",
  "Palace Shroom 8", "Shroom: Prismic Palace - Entry Tree 3", "NOTE_PALACE8",
  "Palace Shroom 9", "Shroom: Prismic Palace - Entry 1", "NOTE_PALACE9",
  "Palace Shroom 10", "Shroom: Prismic Palace - Entry 2", "NOTE_PALACE10",
  "Palace Shroom 11", "Shroom: Prismic Palace - Entry 3", "NOTE_PALACE11",
  "Palace Shroom 12", "Shroom: Prismic Palace - Jester Boots 1", "NOTE_PALACE12",
  "Palace Shroom 13", "Shroom: Prismic Palace - Jester Boots 2", "NOTE_PALACE13",
  "Palace Shroom 14", "Shroom: Prismic Palace - Jester Boots 3", "NOTE_PALACE14",
  "Palace Shroom 15", "Shroom: Prismic Palace - Jester Boots 4", "NOTE_PALACE15",
  "Palace Shroom 16", "Shroom: Prismic Palace - Jester Boots 5", "NOTE_PALACE16",
  "Palace Shroom 17", "Shroom: Prismic Palace - Pom Spire 1", "NOTE_PALACE17",
  "Palace Shroom 18", "Shroom: Prismic Palace - Pom Spire 2", "NOTE_PALACE18",
  "Palace Shroom 19", "Shroom: Prismic Palace - Pom Spire 3", "NOTE_PALACE19",
  "Palace Shroom 20", "Shroom: Prismic Palace - Pom Spire 4", "NOTE_PALACE20",
  "Palace Shroom 21", "Shroom: Prismic Palace - Pom Spire 5", "NOTE_PALACE21",
  "Palace Shroom 22", "Shroom: Prismic Palace - Observatory Spire 1", "NOTE_PALACE22",
  "Palace Shroom 23", "Shroom: Prismic Palace - Observatory Spire 2", "NOTE_PALACE23",
  "Palace Shroom 24", "Shroom: Prismic Palace - Observatory Spire 3", "NOTE_PALACE24",
  "Palace Shroom 25", "Shroom: Prismic Palace - Observatory Spire 4", "NOTE_PALACE25",
  "Palace Shroom 26", "Shroom: Prismic Palace - Observatory Spire 5", "NOTE_PALACE26",
  "Palace Shroom 27", "Shroom: Prismic Palace - Lake Gobbler 2", "NOTE_PALACE27",
  "Palace Shroom 28", "Shroom: Prismic Palace - Lake Gobbler 3", "NOTE_PALACE28",
  "Palace Shroom 29", "Shroom: Prismic Palace - Lake Gobbler 1", "NOTE_PALACE29",
  "Palace Shroom 30", "Shroom: Prismic Palace - Lake Plants 2", "NOTE_PALACE30",
  "Palace Shroom 31", "Shroom: Prismic Palace - Lake Plants 3", "NOTE_PALACE31",
  "Palace Shroom 32", "Shroom: Prismic Palace - Lake Plants 1", "NOTE_PALACE32",
  "Palace Shroom 33", "Shroom: Prismic Palace - Lake Plants 5", "NOTE_PALACE33",
  "Palace Shroom 34", "Shroom: Prismic Palace - Lake Plants 6", "NOTE_PALACE34",
  "Palace Shroom 35", "Shroom: Prismic Palace - Lake Plants 4", "NOTE_PALACE35",
  "Palace Shroom 36", "Shroom: Prismic Palace - Lake Basement Overpass 3", "NOTE_PALACE36",
  "Palace Shroom 37", "Shroom: Prismic Palace - Lake Basement Overpass 4", "NOTE_PALACE37",
  "Palace Shroom 38", "Shroom: Prismic Palace - Lake Basement Overpass 5", "NOTE_PALACE38",
  "Palace Shroom 39", "Shroom: Prismic Palace - Lake Basement Overpass 2", "NOTE_PALACE39",
  "Palace Shroom 40", "Shroom: Prismic Palace - Lake Basement Overpass 1", "NOTE_PALACE40",
  "Palace Shroom 41", "Shroom: Prismic Palace - Lake Mushroom Cave 3", "NOTE_PALACE41",
  "Palace Shroom 42", "Shroom: Prismic Palace - Lake Mushroom Cave 4", "NOTE_PALACE42",
  "Palace Shroom 43", "Shroom: Prismic Palace - Lake Mushroom Cave 5", "NOTE_PALACE43",
  "Palace Shroom 44", "Shroom: Prismic Palace - Lake Mushroom Cave 2", "NOTE_PALACE44",
  "Palace Shroom 45", "Shroom: Prismic Palace - Lake Mushroom Cave 1", "NOTE_PALACE45",
  "Palace Shroom 46", "Shroom: Prismic Palace - Observatory Slide 5", "NOTE_PALACE46",
  "Palace Shroom 47", "Shroom: Prismic Palace - Observatory Slide 4", "NOTE_PALACE47",
  "Palace Shroom 48", "Shroom: Prismic Palace - Observatory Slide 3", "NOTE_PALACE48",
  "Palace Shroom 49", "Shroom: Prismic Palace - Observatory Slide 2", "NOTE_PALACE49",
  "Palace Shroom 50", "Shroom: Prismic Palace - Observatory Slide 1", "NOTE_PALACE50",
  "Palace Shroom 51", "Shroom: Prismic Palace - Poki-Poki Cave 1", "NOTE_PALACE51",
  "Palace Shroom 52", "Shroom: Prismic Palace - Poki-Poki Cave 2", "NOTE_PALACE52",
  "Palace Shroom 53", "Shroom: Prismic Palace - Poki-Poki Cave 3", "NOTE_PALACE53",
  "Palace Shroom 54", "Shroom: Prismic Palace - Poki-Poki Cave 4", "NOTE_PALACE54",
  "Palace Shroom 55", "Shroom: Prismic Palace - Poki-Poki Cave 5", "NOTE_PALACE55",
  "Palace Shroom 56", "Shroom: Prismic Palace - Pool 1", "NOTE_PALACE56",
  "Palace Shroom 57", "Shroom: Prismic Palace - Pool 2", "NOTE_PALACE57",
  "Palace Shroom 58", "Shroom: Prismic Palace - Pool 3", "NOTE_PALACE58",
  "Palace Shroom 59", "Shroom: Prismic Palace - Pool 4", "NOTE_PALACE59",
  "Palace Shroom 60", "Shroom: Prismic Palace - Pool 5", "NOTE_PALACE60",
  "Palace Shroom 61", "Shroom: Prismic Palace - Lake Basement Entry 3", "NOTE_PALACE61",
  "Palace Shroom 62", "Shroom: Prismic Palace - Lake Basement Entry 4", "NOTE_PALACE62",
  "Palace Shroom 63", "Shroom: Prismic Palace - Lake Basement Entry 5", "NOTE_PALACE63",
  "Palace Shroom 64", "Shroom: Prismic Palace - Lake Basement Entry 6", "NOTE_PALACE64",
  "Palace Shroom 65", "Shroom: Prismic Palace - Lake Basement Entry 8", "NOTE_PALACE65",
  "Palace Shroom 66", "Shroom: Prismic Palace - Lake Basement Entry 7", "NOTE_PALACE66",
  "Palace Shroom 67", "Shroom: Prismic Palace - Lake Basement Entry 2", "NOTE_PALACE67",
  "Palace Shroom 68", "Shroom: Prismic Palace - Lake Basement Entry 1", "NOTE_PALACE68",
  "Palace Shroom 69", "Shroom: Prismic Palace - Lake Corner 1", "NOTE_PALACE69",
  "Palace Shroom 70", "Shroom: Prismic Palace - Lake Corner 2", "NOTE_PALACE70",
  "Palace Shroom 71", "Shroom: Prismic Palace - Lake Corner 3", "NOTE_PALACE71",
  "Palace Shroom 72", "Shroom: Prismic Palace - Lake Behind 3", "NOTE_PALACE72",
  "Palace Shroom 73", "Shroom: Prismic Palace - Lake Behind 1", "NOTE_PALACE73",
  "Palace Shroom 74", "Shroom: Prismic Palace - Lake Behind 2", "NOTE_PALACE74",
  "Palace Shroom 75", "Shroom: Prismic Palace - Pool Bridges 2", "NOTE_PALACE75",
  "Palace Shroom 76", "Shroom: Prismic Palace - Pool Bridges 3", "NOTE_PALACE76",
  "Palace Shroom 77", "Shroom: Prismic Palace - Pool Bridges 1", "NOTE_PALACE77",
  "Palace Shroom 78", "Shroom: Prismic Palace - Pool Bridges 5", "NOTE_PALACE78",
  "Palace Shroom 79", "Shroom: Prismic Palace - Pool Bridges 4", "NOTE_PALACE79",
  "Palace Shroom 80", "Shroom: Prismic Palace - Pool Bridges 6", "NOTE_PALACE80",
  "Palace Shroom 81", "Shroom: Palace Interior - Star Puzzle 3", "NOTE_PALACE81",
  "Palace Shroom 82", "Shroom: Palace Interior - Star Puzzle 1", "NOTE_PALACE82",
  "Palace Shroom 83", "Shroom: Palace Interior - Star Puzzle 2", "NOTE_PALACE83",
  "Palace Shroom 84", "Shroom: Palace Interior - Heaven's Path Entry 3", "NOTE_PALACE84",
  "Palace Shroom 85", "Shroom: Palace Interior - Heaven's Path Entry 1", "NOTE_PALACE85",
  "Palace Shroom 86", "Shroom: Palace Interior - Heaven's Path Entry 2", "NOTE_PALACE86",
  "Palace Shroom 87", "Shroom: Palace Interior - Bubble Conch Room 3", "NOTE_PALACE87",
  "Palace Shroom 88", "Shroom: Palace Interior - Bubble Conch Room 1", "NOTE_PALACE88",
  "Palace Shroom 89", "Shroom: Palace Interior - Bubble Conch Room 2", "NOTE_PALACE89",
  "Palace Shroom 90", "Shroom: Palace Interior - Sentry Control Chamber 3", "NOTE_PALACE90",
  "Palace Shroom 91", "Shroom: Palace Interior - Sentry Control Chamber 1", "NOTE_PALACE91",
  "Palace Shroom 92", "Shroom: Palace Interior - Sentry Control Chamber 2", "NOTE_PALACE92",
  "Palace Shroom 93", "Shroom: Palace Interior - Palace Back 1", "NOTE_PALACE93",
  "Palace Shroom 94", "Shroom: Palace Interior - Palace Back 2", "NOTE_PALACE94",
  "Palace Shroom 95", "Shroom: Palace Interior - Palace Back 3", "NOTE_PALACE95",
  "Palace Shroom 96", "Shroom: Palace Interior - Palace Back 4", "NOTE_PALACE96",
  "Palace Shroom 97", "Shroom: Palace Interior - Palace Back 5", "NOTE_PALACE97",
  "Palace Shroom 98", "Shroom: Palace Interior - Palace Back 6", "NOTE_PALACE98",
  "Palace Shroom 99", "Shroom: Palace Interior - Bubble Conch Room 4", "NOTE_PALACE99",
  "Palace Shroom 100", "Shroom: Palace Interior - Bubble Conch Room 5", "NOTE_PALACE100",
)

categories = list(set(dir()) - others)

CategoryGenerator: TypeAlias = Generator[tuple[str, Category | CategoryNoLocation], None, None]

def all_categories() -> CategoryGenerator:
  for k in categories:
    v = eval(k)
    if not (isinstance(v, Category) or isinstance(v, CategoryNoLocation)): continue
    yield k, v

def items_by_category():
  for k, v in all_categories():
    yield k, list(i.item for i in v.rows)

def all_items():
  for k, v in all_categories():
    for i in v.rows:
      yield i.item

def locations_by_category():
  for k, v in all_categories():
    if not isinstance(v, Category): continue
    yield k, list(i.location for i in v.rows)

def all_locations():
  for k, v in all_categories():
    if not isinstance(v, Category): continue
    for i in v.rows:
      yield i.location

def generate_lines_from(category_func: Callable[[str], str], item_func: Callable[[str], str], end: str, things: Iterable[tuple[str, Iterable[str]]]):
  accum: list[str] = []
  all: list[str] = []
  all.append(category_func("Any"))
  for category, items in things:
    item_names = list(item_func(item) for item in items)
    accum.append(category_func(category))
    accum.extend(item_names)
    accum.append(end)
    all.extend(item_names)
  all.append(end)
  accum.extend(all)
  return accum

def generate_item_lines(category_func: Callable[[str], str], item_func: Callable[[str], str], end: str) -> list[str]:
  return generate_lines_from(category_func, item_func, end, items_by_category())

def generate_location_lines(category_func: Callable[[str], str], location_func: Callable[[str], str], end: str) -> list[str]:
  return generate_lines_from(category_func, location_func, end, locations_by_category())

def by_flag(thing: Iterable[tuple[str, Iterable[tuple[str, str]]]]):
  for category, gen in thing:
    yield category, ((b, a) for a, b in gen)

def all_items_with_flags():
  for k, v in all_categories():
    yield k, ((i.item, i.flag) for i in v.rows)

def all_locations_with_flags():
  for k, v in all_categories():
    if not isinstance(v, Category): continue
    yield k, ((i.location, f"LOCATION_{i.flag}") for i in v.rows)
