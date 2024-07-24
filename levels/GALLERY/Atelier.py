# from ...logic import lazy_region, Region, Entrance, InternalEvent, Any, CarryableLocation
# from ...logic import item, carrying, difficulty, tech, event, templates
# 
# area_path = f"GALLERY/Atelier"
# 
# class FoyerDoor(Entrance):
#   warp_path = f"{area_path}/Warps/WarpFromAtelierToFoyer"
#   dest_path = f"{area_path}/Warps/DestFromFoyerToAtelier"
# 
# class EndgameDoor(Entrance):
#   randomize = False
#   warp_path = f"{area_path}/Warps/WarpFromAtelierWindowToGalleryLobby"
#   dest_path = f"{area_path}/Warps/DestFromGalleryLobbyToAtelier"
# 
# class EndgameOtherSideDoor(Entrance):
#   randomize = False
#   warp_path = f"{area_path}/Warps/WarpFromAtelierWindowToGalleryLobby"
#   dest_path = f"{area_path}/Warps/DestFromGalleryLobbyToAtelier"
# 
# @lazy_region
# def Main(r: Region):
#   from . import Foyer
#   r.entrances = [
#     FoyerDoor.define(Foyer.AtelierDoor),
#     EndgameDoor.define()
#   ]
# 
# @lazy_region
# def Endgame(r: Region):
#   pass
