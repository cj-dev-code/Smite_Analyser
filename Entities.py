# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 14:32:18 2020

@author: josep
"""

class Entity:
    TRUE = 0
    PHSYICAL = 1
    MAGICAl = -1
    # Health always reflects the health at an instant. IT IS NOT BASE HEALTH.
    def __init__(self, health, base_damage, phys_prot, mag_prot, perc_mit, flat_mit,
                 phys_damage_percent, mag_damage_percent,
                 flat_phys_pen, flat_mag_pen, percent_phys_pen, percent_mag_pen):
        self._TYPE = "ENTITY"
    
    # Should apply damage to other by taking away their health appropriately
    # returns damage dealt
    def damage_to(self, other, damage_type): # 1 for physical, 0 for true, -1 for magical
        #TODO: implement damage_dealt algorithm from word of thoth.
        damage_dealt = 0
        protections = other.phys_prot if damage_type == Entity.PHYSICAL else other.mag_prot
        return damage_dealt
        
    # Returns total EH as a tuple (against physicals, against magicals, against anything)
    def total_effective_health(self):
        #TODO: Implement tEH formula from word of thoth
        pass
    
    # Should set the killed attribute of the entity to true and give the appropriate
    # amount of xp to all the teammates involved in the fight
    # THE ACTUAL KILLER OF THE ENTITY MUST ALWAYS COME FIRST in the list of killers "other"
    def killed_by(self, other):
        #TODO: implement killedBY XP and gold formula from word of thoth
        # Assume the enemy is a god unless their type is entity.
        #   Then you give them the appropriate amount of gold/xp
        #   Otherwise, dont give gold/xp
        pass
    
    def update_per_tick(self):
        pass
    
    
class Minion(Entity):
    DAMAGE_TYPE = 1
    def __init__(self, damage, health, phys_prot, mag_prot, damage_vs_towers, xp_reward, gold_reward):
        self._damage = damage
        self._health = health
        self._phys_prot = phys_prot
        self._mag_prot = mag_prot
        self._dvt = damage_vs_towers
        self._xp_reward = xp_reward
        self._gold_reward = gold_reward

class Tower(Entity):
    DAMAGE_TYPE = 1
    def __init__(self, health, base_damage, health_regen):
        Entity.__init__(self, health, base_damage, 125, 125, 0, 0, 
                        .85, 1.20, 0,0,0,0)
        self._shot_scaling = .2 # 20 percent shot scaling on all towers
        self._backdoor_mitigation = False
        self._health_regen = health_regen
        
    def toggle_backdoor_mitigations(self):
        self._backdoor_mitigation = not self._backdoor_mitigation
        self._percent_mitigation += (2*self._backdoor_mitigation-1)*.5
        
class God(Entity):
    '''
    god_data is a dict of lists of dim 1.
    '''
    def __init__(self, name, god_data):
        self._name = name
        self._items = 0
        self._ccr = 0
        
        
        self._god_data = god_data
        g = self._god_data
        Entity.__init__(self, health, g['])
        
    def cast_1(self, teammates, enemies):
        pass
    def cast_2(self, teammates, enemies):
        pass    
    def cast_3(self, teammates, enemies):
        pass
    def cast_4(self, teammates, enemies):
        pass
    
    def level_up(self):
        self._health += self._health_per_level
        self._mana += self._mana_per_level
        self._hp5 += self._hp5_per_level
        self._mp5 += self._mp5_per_level
        self._phys_prot += self._phys_prot_per_level
        self._mag_prot += self._mag_prot_per_level
        self._attk_speed += self._attk_speed_per_level*self._base_attk_speed
        self._aa_damage += self._aa_damage_per_level
        
        self._level += 1
        
    def add_item(self, item):
        assert self._item < 6, "Cannot build more than 6 items!"
        self._health += item._health
        self._mana += item._mana
        self._hp5 += item._hp5
        self._mp5 += item._mp5
        self._phys_prot += item._phys_prot
        self._mag_prot += item._mag_prot
        self._attk_speed += item._attk_speed*self._base_attk_speed
        self._flat_phys_pen += item._flat_phys_pen
        self._flat_mag_pen += item._flat_mag_pen
        self._perc_phys_pen += item._perc_phys_pen
        self._perc_mag_pen += item._perc_mag_pen
        self._ccr += item._l
        self._item += 1
        
class Ability:
    def __init__(self, perc_phys_pow, perc_mag_pow, flat_phys_dmg, flat_mag_dmg, 
                 mana_cost, cooldown, cc_effect_enemy, cc_effect_caster, 
                 slow_on_enemy, slow_on_caster, casting_range):
        pass
    
    # Teammates: List, with caster first
    # enemies: list, with primary attacking enemy first.
    def cast(self, teammates, enemies):
        pass