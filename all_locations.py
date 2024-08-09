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
  "Wings", "Sun Cavern - Sage's Blessing 2", "SKILL_HOVER",
  "Horn",  "Sun Cavern - Sage's Blessing 3", "SKILL_DIVE",
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

carryable = Category(
  "Apple", "Lostleaf Lake - Lake Apple", "LAKE_CARRYABLE_APPLE_LAKE",
  "Apple", "Lostleaf Lake - Entry Apple", "LAKE_CARRYABLE_APPLE_ENTRY",
  "Apple", "Lostleaf Lake - Deep Woods Entryway Apple", "LAKE_CARRYABLE_APPLE_DEEPENTRY",
  "Apple", "Lostleaf Lake - Winky Tree Ledge Apple", "LAKE_CARRYABLE_APPLE_WINKYLEDGE",

  "Apple", "Lostleaf Lake - Deep Woods Apple", "LAKE_CARRYABLE_APPLE_DEEPWOODS",
  "Apple", "Lostleaf Lake - Crypt Apple", "LAKE_CARRYABLE_APPLE_CRYPT",
  "Jester Boots", "Lostleaf Lake - Deep Woods Jester Boots", "LAKE_CARRYABLE_BOOTS_DEEPWOODS",

  "Bubble Conch", "Pits of Despair - Bubble Conch", "DROWN_CARRYABLE_BUBBLECONCH",

  "Jester Boots", "Armada Lobby - Jester Boots", "CAVE_CARRYABLE_BOOTS_MONSTERLOBBY",

  "Mr. Kerrington's Wings", "Earth Lobby - Mr. Kerrington's Wings", "GALLERY_CARRYABLE_WINGS_EARTHLOBBY",

  "Shelnert's Fish", "Fire Lobby - Shelnert's Fish", "GALLERY_CARRYABLE_FISH_FIRELOBBY",

  "Sage's Gloves", "Water Lobby - Sage's Gloves", "GALLERY_CARRYABLE_GLOVES_WATERLOBBY",
  "Lady Opal's Head", "Water Lobby - Lady Opal's Head", "GALLERY_CARRYABLE_HEAD_WATERLOBBY",
  "Jester Boots", "Water Lobby - Jester Boots", "GALLERY_CARRYABLE_BOOTS_WATERLOBBY",

  "Medicine", "Kerrington - Main Medicine", "MONSTER_CARRYABLE_MEDICINE_MAIN",
  "Medicine", "Kerrington - Lab Medicine", "MONSTER_CARRYABLE_MEDICINE_LAB",
  "Medicine", "Kerrington - Rain Medicine", "MONSTER_CARRYABLE_MEDICINE_GREEN",
  "Medicine", "Kerrington - Bedroom Medicine", "MONSTER_CARRYABLE_MEDICINE_BEDROOM",
  "Medicine", "Kerrington - Medicine Pool Medicine", "MONSTER_CARRYABLE_MEDICINE_POOL",

  "Mr. Kerrington's Wings", "Airborne Armada - Mr. Kerrington's Wings", "MONSTER_CARRYABLE_WINGS",

  "Jester Boots", "Valley - Jester Boots", "PALACE_CARRYABLE_BOOTS",
  "Bubble Conch", "Palace Interior - Bubble Conch", "PALACE_CARRYABLE_BUBBLECONCH_PALACE",
  "Bubble Conch", "Heaven's Path - Bubble Conch", "PALACE_CARRYABLE_BUBBLECONCH_SANCTUM",
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
  "Open Kerrington's Medicine Pool", "Kerrington - Medicine Pool Preston", "MONSTER_TAIL_GATE_OPEN",

  "Open Prismic Palace Basement", "Valley - Depths Star Hoops", "PALACE_ABYSS_HOOP_SUCCESS",
  "Open Palace-Lostleaf Connector", "Valley - Lostleaf Connector Preston", "PALACE_LAKE_GATE_OPEN",
  "Open Prismic Palace Gate", "Valley - Angel Statue Puzzle", "PALACE_GATE_RISEN",
  "Unfreeze Prismic Palace", "Valley - Help Lady Opal", "PALACE_MELTED_ICE",
  "Open Valley Snowcastle", "Valley - Snowcastle Preston", "PALACE_SNOW_CASTLE_GATE_OPEN",
  "Open Observatory Shortcut", "Valley - Observatory Preston", "PALACE_OBSERVATORY_SHORTCUT",
  "Open Bigstar Cave", "Valley - Bigstar Preston", "PALACE_ICE_WALL_STARFISH_REMOVED",
  "Open Gobbler Cave", "Valley - Gobbler Preston", "PALACE_ICE_WALL_MORAY_REMOVED",
  "Snooze Gobbler", "Valley - Feed Gobbler", "PALACE_MORAY_FED",

  "Disable Prismic Palace Seedragons", "Palace Interior - Sentry Control Preston", "PALACE_SENTRIES_DISABLED",
  "Open Bubble Conch Room", "Palace Interior - Seastar Puzzle", "PALACE_TORPEDO_DOOR_OPENED",

  "Open Heaven's Path Exit", "Heaven's Path - Finished Race", "PALACE_SANCTUM_RACE_FINISHED",
  "Open Heaven's Path Race Entrance", "Heaven's Path - Bottom Preston", "PALACE_SANCTUM_STOPPER_RAISED",

  "Raise Dining Room Platform", "Palace Dining Room - Preston", "PALACE_DINING_ROOM_RISEN",

  "Reveal Observatory Item", "Observatory - Telescope Puzzle", "OBSERVATORY_SUCCESS",

  "Open Foyer Doors", "Foyer - Sage's Painting", "GALLERY_SAGE_PAINTING_SUCCESS",
  "Open Mr. Kerrington Painting Gate", "Fire Lobby - Mr. Kerrington's Painting", "GALLERY_MONSTER_PAINTING_SUCCESS",
  "Open Skull's Diamond Eye", "Earth Lobby - Shelnert's Painting", "GALLERY_KAPPA_PAINTING_SUCCESS",
  "Open Gallery-Armada Connector", "Earth Lobby - Armada Connector Preston", "GALLERY_MONSTER_SHORTCUT_OPEN",
  "Open Earth Lobby Castle Door", "Earth Lobby - Angel Statue Puzzle", "GALLERY_STATUE_PUZZLE_SUCCESS",
  "Open Water Lobby Chest #1", "Water Lobby - Angel Statue Puzzle", "GALLERY_ANGEL_STATUE_SHADOWS_SUCCESS",
  "Open Water Lobby Chest #2", "Water Lobby - Lady Opal's Painting", "GALLERY_PRINCESS_PAINTING_SUCCESS",
  "Open Luna's House", "Water Lobby - Helped Sniffles", "GALLERY_GIANT_HEALED",
  "Extend Fire Lobby Tongue Platform", "Fire Lobby Preston", "GALLERY_FIRE_LOBBY_BRIDGE_EXTENDED",
  "Extend Fire Lobby Frying Pans", "Fire Lobby Hoops", "GALLERY_HOOP_SUCCESS",
  "Coils of Agony - Open Shortcut", "Coils of Agony - Hidden Pillar", "CHALICE_BRIDGE_ACTIVE",
  "Water Wastes of Eternity Plants", "Earth Lobby - Moisten Wastes of Eternity Painting", "UNDEAD_WET",
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
  "Card: Poki-Poki", "Card: Valley - Top of Observatory", "CARD_PALACE_URCHIN",
  "Card: Pom", "Card: Valley - Snowcastle", "CARD_PALACE_PALM_TREE_FLOAT",
  "Card: Bigstar", "Card: Valley - Top of Palace", "CARD_PALACE_SEASTAR",
  "Card: The Gobbler!", "Card: Valley - Above Pool", "CARD_PALACE_MORAY",
  "Card: Seedragon", "Card: Palace", "CARD_PALACE_SENTRY",

  "Card: Rattles", "Card: Earth Lobby - Swamp Castle", "CARD_GALLERY_RATTLES",
  "Card: Sniffles", "Card: Water Lobby - Sewer Bottom", "CARD_GALLERY_GIANT",
  "Card: Starving Art", "Card: Foyer - Water Lobby Entrance", "CARD_GALLERY_MIMIC_PAINTING",
  "Card: Eternal", "Card: Earth Lobby - Swamp", "CARD_GALLERY_UNDEAD",
  "Card: Heartburn", "Card: Fire Lobby - Frying Pans", "CARD_GALLERY_FIRE_SNAKE",
  "Card: Hawhaw", "Card: Water Lobby - Above Pits of Despair Painting", "CARD_GALLERY_CHOMP",

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
  "Heart Egg", "Egg: Heart", "FELLA_MONSTER7",
  "Dumpling Egg", "Egg: Kerrington - Dumpling", "FELLA_MONSTER8",

  "Hatchable Egg: Prismic Palace", "Egg: Valley - Snowcastle", "FELLA_PALACE1",
  "Ornate Egg", "Egg: Palace Dining Room", "FELLA_PALACE2",
  "Starlit Egg", "Egg: Observatory", "FELLA_PALACE3",
  "Checkered Egg", "Egg: Valley - Observatory Slide", "FELLA_PALACE4",
  "Flower Egg", "Egg: Valley - Bigstar", "FELLA_PALACE5",
  "Snowstorm Egg", "Egg: Valley - Top of the Palace", "FELLA_PALACE6",
  "Zig-zag Egg", "Egg: Palace Interior - Basement", "FELLA_PALACE7",
  "Happy Egg", "Egg: Valley - Gobbler", "FELLA_PALACE8",

  "Red Eyes Egg", "Egg: Coils of Agony", "FELLA_CHALICE1",
  "Seaweed Egg", "Egg: Pits of Despair", "FELLA_DROWN1",
  "Moonlight Egg", "Egg: Wastes of Eternity", "FELLA_UNDEAD1",

  "Hatchable Egg: Gallery of Nightmares", "Egg: Foyer - Matryoshka Egg", "FELLA_GALLERY1",
  "Ripped Egg", "Egg: Earth Lobby - Skull's Eye", "FELLA_GALLERY2",
  "Robot Egg", "Egg: Fire Lobby - Mr. Kerrington Painting", "FELLA_GALLERY3",
  "Bricked Egg", "Egg: Water Lobby - Sewer", "FELLA_GALLERY4",
  "Specter Egg", "Egg: Water Lobby - Deepest Darkness", "FELLA_GALLERY5",
)

shroom = Category(
  "Shroom", "Shroom: Sun Cavern - Mighty Wall Ground 1", "NOTE_CAVE2",
  "Shroom", "Shroom: Sun Cavern - Mighty Wall Ground 2", "NOTE_CAVE3",
  "Shroom", "Shroom: Sun Cavern - Mighty Wall Ground 3", "NOTE_CAVE4",
  "Shroom", "Shroom: Sun Cavern - Mighty Wall Ground 4", "NOTE_CAVE5",
  "Shroom", "Shroom: Sun Cavern - Mighty Wall Egg Ledge 1", "NOTE_CAVE1",
  "Shroom", "Shroom: Sun Cavern - Mighty Wall Egg Ledge 2", "NOTE_CAVE6",
  "Shroom", "Shroom: Sun Cavern - Mighty Wall Egg Ledge 3", "NOTE_CAVE7",
  "Shroom", "Shroom: Sun Cavern - High Jump Ledge 1", "NOTE_CAVE8",
  "Shroom", "Shroom: Sun Cavern - High Jump Ledge 2", "NOTE_CAVE9",
  "Shroom", "Shroom: Sun Cavern - Tail Spin Ledge 1", "NOTE_CAVE10",
  "Shroom", "Shroom: Sun Cavern - Tail Spin Ledge 2", "NOTE_CAVE11",
  "Shroom", "Shroom: Sun Cavern - Ducklings Ledge 1", "NOTE_CAVE12",
  "Shroom", "Shroom: Sun Cavern - Ducklings Ledge 2", "NOTE_CAVE13",
  "Shroom", "Shroom: Sun Cavern - Armada Entrance 1", "NOTE_CAVE14",
  "Shroom", "Shroom: Sun Cavern - Armada Entrance 2", "NOTE_CAVE15",
  "Shroom", "Shroom: Sun Cavern - Armada Entrance 3", "NOTE_CAVE16",
  "Shroom", "Shroom: Sun Cavern - Vine Ledge 1", "NOTE_CAVE17",
  "Shroom", "Shroom: Sun Cavern - Vine Ledge 2", "NOTE_CAVE18",
  "Shroom", "Shroom: Moon Cavern - Dive Holes 1", "NOTE_CAVE19",
  "Shroom", "Shroom: Moon Cavern - Dive Holes 2", "NOTE_CAVE20",
  "Shroom", "Shroom: Moon Cavern - Dive Holes 3", "NOTE_CAVE21",
  "Shroom", "Shroom: Moon Cavern - Dive Holes 4", "NOTE_CAVE22",
  "Shroom", "Shroom: Moon Cavern - Dive Holes 5", "NOTE_CAVE23",
  "Shroom", "Shroom: Moon Cavern - Dive Holes 6", "NOTE_CAVE24",
  "Shroom", "Shroom: Moon Cavern - Dive Puzzle 1", "NOTE_CAVE25",
  "Shroom", "Shroom: Moon Cavern - Dive Puzzle 2", "NOTE_CAVE26",
  "Shroom", "Shroom: Moon Cavern - Dive Puzzle 3", "NOTE_CAVE27",
  "Shroom", "Shroom: Moon Cavern - Potionfall", "NOTE_CAVE28",
  "Shroom", "Shroom: Moon Cavern - Lonely Shroom", "NOTE_CAVE29",
  "Shroom", "Shroom: Moon Cavern - Palace Lobby Pathway 2", "NOTE_CAVE30",
  "Shroom", "Shroom: Moon Cavern - Palace Lobby Pathway 1", "NOTE_CAVE31",
  "Shroom", "Shroom: Moon Cavern - Palace Lobby Pathway 3", "NOTE_CAVE32",
  "Shroom", "Shroom: Moon Cavern - Palace Lobby Statue 1", "NOTE_CAVE33",
  "Shroom", "Shroom: Moon Cavern - Palace Lobby Statue 2", "NOTE_CAVE34",
  "Shroom", "Shroom: Moon Cavern - Palace Lobby Entryway 1", "NOTE_CAVE35",
  "Shroom", "Shroom: Moon Cavern - Palace Lobby Entryway 2", "NOTE_CAVE36",
  "Shroom", "Shroom: Moon Cavern - Palace Lobby Entryway 3", "NOTE_CAVE37",
  "Shroom", "Shroom: Moon Cavern - Lava Platforms 1", "NOTE_CAVE38",
  "Shroom", "Shroom: Moon Cavern - Lava Platforms 2", "NOTE_CAVE39",
  "Shroom", "Shroom: Moon Cavern - Lava Platforms 3", "NOTE_CAVE40",
  "Shroom", "Shroom: Moon Cavern - Lava Platforms 4", "NOTE_CAVE41",
  "Shroom", "Shroom: Moon Cavern - Lava Mushroom Platform 1", "NOTE_CAVE42",
  "Shroom", "Shroom: Moon Cavern - Lava Mushroom Platform 2", "NOTE_CAVE43",
  "Shroom", "Shroom: Lostleaf Lobby - Bridge 2", "NOTE_CAVE44",
  "Shroom", "Shroom: Lostleaf Lobby - Bridge 3", "NOTE_CAVE45",
  "Shroom", "Shroom: Lostleaf Lobby - Bridge 1", "NOTE_CAVE46",
  "Shroom", "Shroom: Lostleaf Lobby - Trees 1", "NOTE_CAVE47",
  "Shroom", "Shroom: Lostleaf Lobby - Trees 2", "NOTE_CAVE48",
  "Shroom", "Shroom: Lostleaf Lobby - Trees 3", "NOTE_CAVE49",
  "Shroom", "Shroom: Armada Lobby - Cliffside 1", "NOTE_CAVE50",
  "Shroom", "Shroom: Armada Lobby - Cliffside 2", "NOTE_CAVE51",
  "Shroom", "Shroom: Armada Lobby - Cliffside 4", "NOTE_CAVE52",
  "Shroom", "Shroom: Armada Lobby - Cliffside 5", "NOTE_CAVE53",
  "Shroom", "Shroom: Armada Lobby - Cliffside 3", "NOTE_CAVE54",
  "Shroom", "Shroom: Palace Lobby - Ledges 1", "NOTE_CAVE55",
  "Shroom", "Shroom: Palace Lobby - Ledges 6", "NOTE_CAVE56",
  "Shroom", "Shroom: Palace Lobby - Ledges 5", "NOTE_CAVE57",
  "Shroom", "Shroom: Palace Lobby - Ledges 3", "NOTE_CAVE58",
  "Shroom", "Shroom: Palace Lobby - Ledges 2", "NOTE_CAVE59",
  "Shroom", "Shroom: Palace Lobby - Ledges 4", "NOTE_CAVE60",
  "Shroom", "Shroom: Palace Lobby - Underwater 1", "NOTE_CAVE61",
  "Shroom", "Shroom: Palace Lobby - Underwater 2", "NOTE_CAVE62",
  "Shroom", "Shroom: Palace Lobby - Underwater 3", "NOTE_CAVE63",
  "Shroom", "Shroom: Palace Lobby - Underwater 5", "NOTE_CAVE64",
  "Shroom", "Shroom: Palace Lobby - Underwater 6", "NOTE_CAVE65",
  "Shroom", "Shroom: Palace Lobby - Underwater 4", "NOTE_CAVE66",
  "Shroom", "Shroom: Gallery Lobby - Fountain 1", "NOTE_CAVE67",
  "Shroom", "Shroom: Gallery Lobby - Fountain 2", "NOTE_CAVE68",
  "Shroom", "Shroom: Gallery Lobby - Fountain 3", "NOTE_CAVE69",
  "Shroom", "Shroom: Gallery Lobby - Fountain 4", "NOTE_CAVE70",
  "Shroom", "Shroom: Gallery Lobby - Castle Hill 3", "NOTE_CAVE71",
  "Shroom", "Shroom: Gallery Lobby - Castle Hill 5", "NOTE_CAVE72",
  "Shroom", "Shroom: Gallery Lobby - Castle Hill 4", "NOTE_CAVE73",
  "Shroom", "Shroom: Gallery Lobby - Castle Hill 1", "NOTE_CAVE74",
  "Shroom", "Shroom: Gallery Lobby - Castle Hill 2", "NOTE_CAVE75",
  "Shroom", "Shroom: Gallery Lobby - Entryway 1", "NOTE_CAVE76",
  "Shroom", "Shroom: Gallery Lobby - Entryway 4", "NOTE_CAVE77",
  "Shroom", "Shroom: Gallery Lobby - Entryway 5", "NOTE_CAVE78",
  "Shroom", "Shroom: Gallery Lobby - Entryway 3", "NOTE_CAVE79",
  "Shroom", "Shroom: Gallery Lobby - Entryway 2", "NOTE_CAVE80",

  "Shroom", "Shroom: Lostleaf Lake - Treehouse Branches 4", "NOTE_LAKE1",
  "Shroom", "Shroom: Lostleaf Lake - Treehouse Branches 3", "NOTE_LAKE2",
  "Shroom", "Shroom: Lostleaf Lake - Treehouse Branches 1", "NOTE_LAKE3",
  "Shroom", "Shroom: Lostleaf Lake - Treehouse Branches 2", "NOTE_LAKE4",
  "Shroom", "Shroom: Lostleaf Lake - Treehouse Branches 6", "NOTE_LAKE5",
  "Shroom", "Shroom: Lostleaf Lake - Treehouse Branches 5", "NOTE_LAKE6",
  "Shroom", "Shroom: Lostleaf Lake - Deep Woods 2", "NOTE_LAKE7",
  "Shroom", "Shroom: Lostleaf Lake - Deep Woods 1", "NOTE_LAKE8",
  "Shroom", "Shroom: Lostleaf Lake - Deep Woods 3", "NOTE_LAKE9",
  "Shroom", "Shroom: Lostleaf Lake - Deep Woods 6", "NOTE_LAKE10",
  "Shroom", "Shroom: Lostleaf Lake - Deep Woods 4", "NOTE_LAKE11",
  "Shroom", "Shroom: Lostleaf Lake - Deep Woods 5", "NOTE_LAKE12",
  "Shroom", "Shroom: Lostleaf Lake - Behind Church 3", "NOTE_LAKE13",
  "Shroom", "Shroom: Lostleaf Lake - Behind Church 1", "NOTE_LAKE14",
  "Shroom", "Shroom: Lostleaf Lake - Behind Church 2", "NOTE_LAKE15",
  "Shroom", "Shroom: Lostleaf Lake - Teepee 1", "NOTE_LAKE16",
  "Shroom", "Shroom: Lostleaf Lake - Teepee 3", "NOTE_LAKE17",
  "Shroom", "Shroom: Lostleaf Lake - Teepee 2", "NOTE_LAKE18",
  "Shroom", "Shroom: Lostleaf Lake - Waterfall Logs 2", "NOTE_LAKE19",
  "Shroom", "Shroom: Lostleaf Lake - Waterfall Logs 3", "NOTE_LAKE20",
  "Shroom", "Shroom: Lostleaf Lake - Waterfall Logs 4", "NOTE_LAKE21",
  "Shroom", "Shroom: Lostleaf Lake - Waterfall Logs 1", "NOTE_LAKE22",
  "Shroom", "Shroom: Lostleaf Lake - Lake Logs 2", "NOTE_LAKE23",
  "Shroom", "Shroom: Lostleaf Lake - Lake Logs 1", "NOTE_LAKE24",
  "Shroom", "Shroom: Lostleaf Lake - Lake Logs 3", "NOTE_LAKE25",
  "Shroom", "Shroom: Lostleaf Lake - Lake Logs 4", "NOTE_LAKE26",
  "Shroom", "Shroom: Lostleaf Lake - Winky Bouncy Mushroom 1", "NOTE_LAKE27",
  "Shroom", "Shroom: Lostleaf Lake - Winky Bouncy Mushroom 2", "NOTE_LAKE28",
  "Shroom", "Shroom: Lostleaf Lake - Winky Bouncy Mushroom 3", "NOTE_LAKE29",
  "Shroom", "Shroom: Lostleaf Lake - Ramp to Winky Tree 1", "NOTE_LAKE30",
  "Shroom", "Shroom: Lostleaf Lake - Ramp to Winky Tree 3", "NOTE_LAKE31",
  "Shroom", "Shroom: Lostleaf Lake - Ramp to Winky Tree 5", "NOTE_LAKE32",
  "Shroom", "Shroom: Lostleaf Lake - Ramp to Winky Tree 2", "NOTE_LAKE33",
  "Shroom", "Shroom: Lostleaf Lake - Ramp to Winky Tree 4", "NOTE_LAKE34",
  "Shroom", "Shroom: Lostleaf Lake - Deep Woods Entryway 1", "NOTE_LAKE35",
  "Shroom", "Shroom: Lostleaf Lake - Deep Woods Entryway 2", "NOTE_LAKE36",
  "Shroom", "Shroom: Lostleaf Lake - Deep Woods Entryway 3", "NOTE_LAKE37",
  "Shroom", "Shroom: Lostleaf Lake - Lake Gravestone 1", "NOTE_LAKE38",
  "Shroom", "Shroom: Lostleaf Lake - Lake Gravestone 2", "NOTE_LAKE39",
  "Shroom", "Shroom: Lostleaf Lake - Lake Gravestone 3", "NOTE_LAKE40",
  "Shroom", "Shroom: Lostleaf Lake - Bridge 2", "NOTE_LAKE41",
  "Shroom", "Shroom: Lostleaf Lake - Bridge 1", "NOTE_LAKE42",
  "Shroom", "Shroom: Lostleaf Lake - Bridge 3", "NOTE_LAKE43",
  "Shroom", "Shroom: Lostleaf Lake - Winky Apple Tree 4", "NOTE_LAKE44",
  "Shroom", "Shroom: Lostleaf Lake - Winky Apple Tree 3", "NOTE_LAKE45",
  "Shroom", "Shroom: Lostleaf Lake - Winky Apple Tree 1", "NOTE_LAKE46",
  "Shroom", "Shroom: Lostleaf Lake - Winky Apple Tree 2", "NOTE_LAKE47",
  "Shroom", "Shroom: Lostleaf Lake - Church Entryway 3", "NOTE_LAKE48",
  "Shroom", "Shroom: Lostleaf Lake - Church Entryway 2", "NOTE_LAKE49",
  "Shroom", "Shroom: Lostleaf Lake - Church Entryway 1", "NOTE_LAKE50",
  "Shroom", "Shroom: Church - Pews 4", "NOTE_LAKE51",
  "Shroom", "Shroom: Church - Pews 2", "NOTE_LAKE52",
  "Shroom", "Shroom: Church - Pews 1", "NOTE_LAKE53",
  "Shroom", "Shroom: Church - Pews 3", "NOTE_LAKE54",
  "Shroom", "Shroom: Treehouse - Corners 4", "NOTE_LAKE55",
  "Shroom", "Shroom: Treehouse - Corners 3", "NOTE_LAKE56",
  "Shroom", "Shroom: Treehouse - Corners 2", "NOTE_LAKE57",
  "Shroom", "Shroom: Treehouse - Corners 1", "NOTE_LAKE58",
  "Shroom", "Shroom: Treehouse - Corners 5", "NOTE_LAKE59",
  "Shroom", "Shroom: Treehouse - Corners 6", "NOTE_LAKE60",

  "Shroom", "Shroom: Airborne Armada - Bouncy Shroom 1", "NOTE_MONSTER1",
  "Shroom", "Shroom: Airborne Armada - Bouncy Shroom 3", "NOTE_MONSTER2",
  "Shroom", "Shroom: Airborne Armada - Bouncy Shroom 2", "NOTE_MONSTER3",
  "Shroom", "Shroom: Airborne Armada - Bouncy Shroom 4", "NOTE_MONSTER4",
  "Shroom", "Shroom: Airborne Armada - Entry Pathway 5", "NOTE_MONSTER5",
  "Shroom", "Shroom: Airborne Armada - Front Entrance 1", "NOTE_MONSTER6",
  "Shroom", "Shroom: Airborne Armada - Front Entrance 2", "NOTE_MONSTER7",
  "Shroom", "Shroom: Airborne Armada - Front Entrance 3", "NOTE_MONSTER8",
  "Shroom", "Shroom: Airborne Armada - Side 1", "NOTE_MONSTER9",
  "Shroom", "Shroom: Airborne Armada - Side 2", "NOTE_MONSTER10",
  "Shroom", "Shroom: Airborne Armada - Side Yellow Ledge", "NOTE_MONSTER11",
  "Shroom", "Shroom: Airborne Armada - Back Entrance 1", "NOTE_MONSTER12",
  "Shroom", "Shroom: Airborne Armada - Back Entrance 2", "NOTE_MONSTER13",
  "Shroom", "Shroom: Airborne Armada - Back Entrance 3", "NOTE_MONSTER14",
  "Shroom", "Shroom: Airborne Armada - Back Entrance 4", "NOTE_MONSTER15",
  "Shroom", "Shroom: Airborne Armada - Back Entrance 6", "NOTE_MONSTER16",
  "Shroom", "Shroom: Airborne Armada - Back Entrance 5", "NOTE_MONSTER17",
  "Shroom", "Shroom: Airborne Armada - Topside 1", "NOTE_MONSTER18",
  "Shroom", "Shroom: Airborne Armada - Topside 2", "NOTE_MONSTER19",
  "Shroom", "Shroom: Airborne Armada - Topside 3", "NOTE_MONSTER20",
  "Shroom", "Shroom: Airborne Armada - Entry Pathway 1", "NOTE_MONSTER21",
  "Shroom", "Shroom: Airborne Armada - Entry Pathway 2", "NOTE_MONSTER22",
  "Shroom", "Shroom: Airborne Armada - Entry Pathway 3", "NOTE_MONSTER23",
  "Shroom", "Shroom: Airborne Armada - Entry Pathway 4", "NOTE_MONSTER24",
  "Shroom", "Shroom: Kerrington - Rain Entryway 4", "NOTE_MONSTER25",
  "Shroom", "Shroom: Kerrington - Rain Entryway 3", "NOTE_MONSTER26",
  "Shroom", "Shroom: Kerrington - Rain Entryway 2", "NOTE_MONSTER27",
  "Shroom", "Shroom: Kerrington - Hammocks Entryway 2", "NOTE_MONSTER28",
  "Shroom", "Shroom: Kerrington - Hammocks Entryway 1", "NOTE_MONSTER29",
  "Shroom", "Shroom: Kerrington - Cockpit Entry 3", "NOTE_MONSTER30",
  "Shroom", "Shroom: Kerrington - Cockpit Entry 2", "NOTE_MONSTER31",
  "Shroom", "Shroom: Kerrington - Cockpit Entry 1", "NOTE_MONSTER32",
  "Shroom", "Shroom: Kerrington - Cockpit Entry 6", "NOTE_MONSTER33",
  "Shroom", "Shroom: Kerrington - Cockpit Entry 5", "NOTE_MONSTER34",
  "Shroom", "Shroom: Kerrington - Cockpit Entry 4", "NOTE_MONSTER35",
  "Shroom", "Shroom: Kerrington - Rain Below Medicine 3", "NOTE_MONSTER36",
  "Shroom", "Shroom: Kerrington - Rain Below Medicine 2", "NOTE_MONSTER37",
  "Shroom", "Shroom: Kerrington - Rain Below Boiler 1", "NOTE_MONSTER38",
  "Shroom", "Shroom: Kerrington - Rain Below Boiler 2", "NOTE_MONSTER39",
  "Shroom", "Shroom: Kerrington - Rain Below Boiler 3", "NOTE_MONSTER40",
  "Shroom", "Shroom: Kerrington - Rain Below Medicine 1", "NOTE_MONSTER41",
  "Shroom", "Shroom: Kerrington - Rain Plant Base", "NOTE_MONSTER42",
  "Shroom", "Shroom: Kerrington - Rain Plant 1", "NOTE_MONSTER43",
  "Shroom", "Shroom: Kerrington - Lab Rain Connector 5", "NOTE_MONSTER44",
  "Shroom", "Shroom: Kerrington - Lab Rain Connector 6", "NOTE_MONSTER45",
  "Shroom", "Shroom: Kerrington - Lab Rain Connector 4", "NOTE_MONSTER46",
  "Shroom", "Shroom: Kerrington - Lab Rain Connector 3", "NOTE_MONSTER47",
  "Shroom", "Shroom: Kerrington - Lab Rain Connector 2", "NOTE_MONSTER48",
  "Shroom", "Shroom: Kerrington - Lab Rain Connector 1", "NOTE_MONSTER49",
  "Shroom", "Shroom: Kerrington - Lab Entryway 4", "NOTE_MONSTER50",
  "Shroom", "Shroom: Kerrington - Lab Entryway 3", "NOTE_MONSTER51",
  "Shroom", "Shroom: Kerrington - Lab Entryway 2", "NOTE_MONSTER52",
  "Shroom", "Shroom: Kerrington - Lab Entryway 1", "NOTE_MONSTER53",
  "Shroom", "Shroom: Kerrington - Pipe 5", "NOTE_MONSTER54",
  "Shroom", "Shroom: Kerrington - Pipe 4", "NOTE_MONSTER55",
  "Shroom", "Shroom: Kerrington - Pipe 3", "NOTE_MONSTER56",
  "Shroom", "Shroom: Kerrington - Pipe 2", "NOTE_MONSTER57",
  "Shroom", "Shroom: Kerrington - Pipe 1", "NOTE_MONSTER58",
  "Shroom", "Shroom: Kerrington - Pipe Ramp 3", "NOTE_MONSTER59",
  "Shroom", "Shroom: Kerrington - Pipe Ramp 2", "NOTE_MONSTER60",
  "Shroom", "Shroom: Kerrington - Pipe Ramp 1", "NOTE_MONSTER61",
  "Shroom", "Shroom: Kerrington - Rain Entryway 1", "NOTE_MONSTER62",
  "Shroom", "Shroom: Kerrington - Slide Entryway 1", "NOTE_MONSTER63",
  "Shroom", "Shroom: Kerrington - Slide Entryway 2", "NOTE_MONSTER64",
  "Shroom", "Shroom: Kerrington - Slide Entryway 3", "NOTE_MONSTER65",
  "Shroom", "Shroom: Kerrington - Rain Plant 2", "NOTE_MONSTER66",
  "Shroom", "Shroom: Kerrington - Rain Plant 3", "NOTE_MONSTER67",
  "Shroom", "Shroom: Kerrington - Rain Plant 4", "NOTE_MONSTER68",
  "Shroom", "Shroom: Kerrington - Rain Above Boiler 4", "NOTE_MONSTER69",
  "Shroom", "Shroom: Kerrington - Rain Above Boiler 2", "NOTE_MONSTER70",
  "Shroom", "Shroom: Kerrington - Rain Above Boiler 1", "NOTE_MONSTER71",
  "Shroom", "Shroom: Kerrington - Rain Above Boiler 3", "NOTE_MONSTER72",
  "Shroom", "Shroom: Armada Entry Drone - Ledges 6", "NOTE_MONSTER73",
  "Shroom", "Shroom: Armada Entry Drone - Ledges 5", "NOTE_MONSTER74",
  "Shroom", "Shroom: Armada Entry Drone - Ledges 4", "NOTE_MONSTER75",
  "Shroom", "Shroom: Armada Entry Drone - Ledges 3", "NOTE_MONSTER76",
  "Shroom", "Shroom: Armada Entry Drone - Ledges 7", "NOTE_MONSTER77",
  "Shroom", "Shroom: Armada Entry Drone - Ledges 8", "NOTE_MONSTER78",
  "Shroom", "Shroom: Armada Entry Drone - Ledges 1", "NOTE_MONSTER79",
  "Shroom", "Shroom: Armada Entry Drone - Ledges 2", "NOTE_MONSTER80",

  "Shroom", "Shroom: Valley - Poms 5", "NOTE_PALACE1",
  "Shroom", "Shroom: Valley - Poms 3", "NOTE_PALACE2",
  "Shroom", "Shroom: Valley - Poms 4", "NOTE_PALACE3",
  "Shroom", "Shroom: Valley - Poms 2", "NOTE_PALACE4",
  "Shroom", "Shroom: Valley - Poms 1", "NOTE_PALACE5",
  "Shroom", "Shroom: Valley - Entry Tree 2", "NOTE_PALACE6",
  "Shroom", "Shroom: Valley - Entry Tree 1", "NOTE_PALACE7",
  "Shroom", "Shroom: Valley - Entry Tree 3", "NOTE_PALACE8",
  "Shroom", "Shroom: Valley - Entry 1", "NOTE_PALACE9",
  "Shroom", "Shroom: Valley - Entry 2", "NOTE_PALACE10",
  "Shroom", "Shroom: Valley - Entry 3", "NOTE_PALACE11",
  "Shroom", "Shroom: Valley - Jester Boots 1", "NOTE_PALACE12",
  "Shroom", "Shroom: Valley - Jester Boots 2", "NOTE_PALACE13",
  "Shroom", "Shroom: Valley - Jester Boots 3", "NOTE_PALACE14",
  "Shroom", "Shroom: Valley - Jester Boots 4", "NOTE_PALACE15",
  "Shroom", "Shroom: Valley - Jester Boots 5", "NOTE_PALACE16",
  "Shroom", "Shroom: Valley - Pom Spire 1", "NOTE_PALACE17",
  "Shroom", "Shroom: Valley - Pom Spire 2", "NOTE_PALACE18",
  "Shroom", "Shroom: Valley - Pom Spire 3", "NOTE_PALACE19",
  "Shroom", "Shroom: Valley - Pom Spire 4", "NOTE_PALACE20",
  "Shroom", "Shroom: Valley - Pom Spire 5", "NOTE_PALACE21",
  "Shroom", "Shroom: Valley - Observatory Spire 1", "NOTE_PALACE22",
  "Shroom", "Shroom: Valley - Observatory Spire 2", "NOTE_PALACE23",
  "Shroom", "Shroom: Valley - Observatory Spire 3", "NOTE_PALACE24",
  "Shroom", "Shroom: Valley - Observatory Spire 4", "NOTE_PALACE25",
  "Shroom", "Shroom: Valley - Observatory Spire 5", "NOTE_PALACE26",
  "Shroom", "Shroom: Valley - Lake Gobbler 2", "NOTE_PALACE27",
  "Shroom", "Shroom: Valley - Lake Gobbler 3", "NOTE_PALACE28",
  "Shroom", "Shroom: Valley - Lake Gobbler 1", "NOTE_PALACE29",
  "Shroom", "Shroom: Valley - Lake Plants 2", "NOTE_PALACE30",
  "Shroom", "Shroom: Valley - Lake Plants 3", "NOTE_PALACE31",
  "Shroom", "Shroom: Valley - Lake Plants 1", "NOTE_PALACE32",
  "Shroom", "Shroom: Valley - Lake Plants 5", "NOTE_PALACE33",
  "Shroom", "Shroom: Valley - Lake Plants 6", "NOTE_PALACE34",
  "Shroom", "Shroom: Valley - Lake Plants 4", "NOTE_PALACE35",
  "Shroom", "Shroom: Valley - Lake Depths Overpass 3", "NOTE_PALACE36",
  "Shroom", "Shroom: Valley - Lake Depths Overpass 4", "NOTE_PALACE37",
  "Shroom", "Shroom: Valley - Lake Depths Overpass 5", "NOTE_PALACE38",
  "Shroom", "Shroom: Valley - Lake Depths Overpass 2", "NOTE_PALACE39",
  "Shroom", "Shroom: Valley - Lake Depths Overpass 1", "NOTE_PALACE40",
  "Shroom", "Shroom: Valley - Lake Mushroom Cave 3", "NOTE_PALACE41",
  "Shroom", "Shroom: Valley - Lake Mushroom Cave 4", "NOTE_PALACE42",
  "Shroom", "Shroom: Valley - Lake Mushroom Cave 5", "NOTE_PALACE43",
  "Shroom", "Shroom: Valley - Lake Mushroom Cave 2", "NOTE_PALACE44",
  "Shroom", "Shroom: Valley - Lake Mushroom Cave 1", "NOTE_PALACE45",
  "Shroom", "Shroom: Valley - Observatory Slide 5", "NOTE_PALACE46",
  "Shroom", "Shroom: Valley - Observatory Slide 4", "NOTE_PALACE47",
  "Shroom", "Shroom: Valley - Observatory Slide 3", "NOTE_PALACE48",
  "Shroom", "Shroom: Valley - Observatory Slide 2", "NOTE_PALACE49",
  "Shroom", "Shroom: Valley - Observatory Slide 1", "NOTE_PALACE50",
  "Shroom", "Shroom: Valley - Poki-Poki Cave 1", "NOTE_PALACE51",
  "Shroom", "Shroom: Valley - Poki-Poki Cave 2", "NOTE_PALACE52",
  "Shroom", "Shroom: Valley - Poki-Poki Cave 3", "NOTE_PALACE53",
  "Shroom", "Shroom: Valley - Poki-Poki Cave 4", "NOTE_PALACE54",
  "Shroom", "Shroom: Valley - Poki-Poki Cave 5", "NOTE_PALACE55",
  "Shroom", "Shroom: Valley - Pool 1", "NOTE_PALACE56",
  "Shroom", "Shroom: Valley - Pool 2", "NOTE_PALACE57",
  "Shroom", "Shroom: Valley - Pool 3", "NOTE_PALACE58",
  "Shroom", "Shroom: Valley - Pool 4", "NOTE_PALACE59",
  "Shroom", "Shroom: Valley - Pool 5", "NOTE_PALACE60",
  "Shroom", "Shroom: Valley - Lake Depths Entry 3", "NOTE_PALACE61",
  "Shroom", "Shroom: Valley - Lake Depths Entry 4", "NOTE_PALACE62",
  "Shroom", "Shroom: Valley - Lake Depths Entry 5", "NOTE_PALACE63",
  "Shroom", "Shroom: Valley - Lake Depths Entry 6", "NOTE_PALACE64",
  "Shroom", "Shroom: Valley - Lake Depths Entry 8", "NOTE_PALACE65",
  "Shroom", "Shroom: Valley - Lake Depths Entry 7", "NOTE_PALACE66",
  "Shroom", "Shroom: Valley - Lake Depths Entry 2", "NOTE_PALACE67",
  "Shroom", "Shroom: Valley - Lake Depths Entry 1", "NOTE_PALACE68",
  "Shroom", "Shroom: Valley - Lake Corner 1", "NOTE_PALACE69",
  "Shroom", "Shroom: Valley - Lake Corner 2", "NOTE_PALACE70",
  "Shroom", "Shroom: Valley - Lake Corner 3", "NOTE_PALACE71",
  "Shroom", "Shroom: Valley - Lake Behind 3", "NOTE_PALACE72",
  "Shroom", "Shroom: Valley - Lake Behind 1", "NOTE_PALACE73",
  "Shroom", "Shroom: Valley - Lake Behind 2", "NOTE_PALACE74",
  "Shroom", "Shroom: Valley - Pool Bridges 2", "NOTE_PALACE75",
  "Shroom", "Shroom: Valley - Pool Bridges 3", "NOTE_PALACE76",
  "Shroom", "Shroom: Valley - Pool Bridges 1", "NOTE_PALACE77",
  "Shroom", "Shroom: Valley - Pool Bridges 5", "NOTE_PALACE78",
  "Shroom", "Shroom: Valley - Pool Bridges 4", "NOTE_PALACE79",
  "Shroom", "Shroom: Valley - Pool Bridges 6", "NOTE_PALACE80",
  "Shroom", "Shroom: Palace Interior - Star Puzzle 3", "NOTE_PALACE81",
  "Shroom", "Shroom: Palace Interior - Star Puzzle 1", "NOTE_PALACE82",
  "Shroom", "Shroom: Palace Interior - Star Puzzle 2", "NOTE_PALACE83",
  "Shroom", "Shroom: Palace Interior - Heaven's Path Entry 3", "NOTE_PALACE84",
  "Shroom", "Shroom: Palace Interior - Heaven's Path Entry 1", "NOTE_PALACE85",
  "Shroom", "Shroom: Palace Interior - Heaven's Path Entry 2", "NOTE_PALACE86",
  "Shroom", "Shroom: Palace Interior - Bubble Conch Room 3", "NOTE_PALACE87",
  "Shroom", "Shroom: Palace Interior - Bubble Conch Room 1", "NOTE_PALACE88",
  "Shroom", "Shroom: Palace Interior - Bubble Conch Room 2", "NOTE_PALACE89",
  "Shroom", "Shroom: Palace Interior - Sentry Control Chamber 3", "NOTE_PALACE90",
  "Shroom", "Shroom: Palace Interior - Sentry Control Chamber 1", "NOTE_PALACE91",
  "Shroom", "Shroom: Palace Interior - Sentry Control Chamber 2", "NOTE_PALACE92",
  "Shroom", "Shroom: Palace Interior - Palace Back 1", "NOTE_PALACE93",
  "Shroom", "Shroom: Palace Interior - Palace Back 2", "NOTE_PALACE94",
  "Shroom", "Shroom: Palace Interior - Palace Back 3", "NOTE_PALACE95",
  "Shroom", "Shroom: Palace Interior - Palace Back 4", "NOTE_PALACE96",
  "Shroom", "Shroom: Palace Interior - Palace Back 5", "NOTE_PALACE97",
  "Shroom", "Shroom: Palace Interior - Palace Back 6", "NOTE_PALACE98",
  "Shroom", "Shroom: Palace Interior - Bubble Conch Room 4", "NOTE_PALACE99",
  "Shroom", "Shroom: Palace Interior - Bubble Conch Room 5", "NOTE_PALACE100",
)

categories = list(set(dir()) - others)

carryables_blacklist: set[str] = {
  "Card: Armada Lobby - Jester Boots",
  "Shroom: Lostleaf Lake - Deep Woods 1",
  "Shroom: Lostleaf Lake - Deep Woods 2",
  "Shroom: Lostleaf Lake - Deep Woods 3",
  "Shroom: Lostleaf Lake - Deep Woods 4",
  "Shroom: Lostleaf Lake - Deep Woods 5",
  "Shroom: Lostleaf Lake - Deep Woods 6",
}

CategoryGenerator: TypeAlias = Generator[tuple[str, Category | CategoryNoLocation], None, None]

def all_categories() -> CategoryGenerator:
  for k in categories:
    v: Category | CategoryNoLocation | None = eval(k)
    if not (isinstance(v, Category) or isinstance(v, CategoryNoLocation)): continue
    yield k, v

def items_by_category():
  for k, v in all_categories():
    yield k, list(i.item for i in v.rows)

def all_items():
  for _k, v in all_categories():
    for i in v.rows:
      yield i.item

def locations_by_category():
  for k, v in all_categories():
    if not isinstance(v, Category): continue
    yield k, list(i.location for i in v.rows)

def all_locations():
  for _k, v in all_categories():
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
