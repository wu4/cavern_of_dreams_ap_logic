from .option import Option
from . import item, carrying

ejection_launch = Option("ejection_launch")
z_target = Option("z_target")
momentum_cancel = Option("momentum_cancel")
ability_toggle = Option("ability_toggle")
out_of_bounds = Option("out_of_bounds")

wing_jump = Option("wing_jump") & item.wings
wing_storage = Option("wing_storage") & item.wings

bubble_jump = Option("bubble_jump", 1) & item.bubble
bubble_jump_and_recoil = Option("bubble_jump", 2) & item.bubble

super_bounce = Option("super_bounce") & item.super_bounce & item.roll & item.air_tail
super_bubble_jump = Option("super_bubble_jump") & item.super_bubble_jump & item.roll & item.bubble

roll_disjoint = Option("roll_disjoint") & item.roll

damage_boost = Option("damage_boost") & carrying.no_temp_items

ground_tail_jump = Option("ground_tail_jump") & item.ground_tail
air_tail_jump = Option("air_tail_jump") & item.air_tail

any_super_jump = super_bounce | super_bubble_jump
