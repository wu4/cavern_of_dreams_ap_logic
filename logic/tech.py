from .option import Option
from .has import Collected
from . import item, carrying

ejection_launch = Option("ejection_launch")
z_target = Option("z_target")
momentum_cancel = Option("momentum_cancel")
ability_toggle = Option("ability_toggle")
out_of_bounds = Option("out_of_bounds")

wing_jump = Option("wing_jump") & (item.wings | carrying.mr_kerringtons_wings)
wing_storage = Option("wing_storage") & (
    item.wings | carrying.mr_kerringtons_wings)

bubble_jump = Option("bubble_jump", value=1,
                     greater_or_equal=True) & item.bubble
bubble_jump_and_recoil = Option("bubble_jump", value=2) & item.bubble

roll_disjoint = Option("roll_disjoint") & item.roll

damage_boost = Option("damage_boost") & carrying.no_temp_items

ground_tail_jump = Option("ground_tail_jump") & item.ground_tail
air_tail_jump = Option("air_tail_jump") & item.air_tail

# these techs are given to the player as items
super_bounce = Collected("Super Bounce") & item.roll & item.air_tail
super_bubble_jump = Collected("Super Bubble Jump") & item.roll & item.bubble

any_super_jump = super_bounce | super_bubble_jump
