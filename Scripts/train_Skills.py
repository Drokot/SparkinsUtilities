from Scripts.utilities.items import FindItem, CheckItemExists, FindLockbox
from Scripts.utilities.helpers import SendMessage, Pause, UseSkill, CastSpell
from Scripts.glossary.colors import colors

def TrainHiding():
    """
    Trains Hiding by repeatedly using the skill.
    """
    SendMessage("Starting Hiding training...")
    while True:
        if not UseSkill("Hiding", 10000):
            Pause(1000)
            continue
        Pause(1000)

def TrainDetectHidden():
    """
    Trains Detect Hidden by using the skill on the player's location.
    """
    SendMessage("Starting Detect Hidden training...")
    while True:
        if not UseSkill("Detect Hidden", 10000):
            Pause(1000)
            continue
        Target.WaitForTarget(10000, False)
        Target.Self()
        Pause(1000)

def TrainSpiritSpeak():
    """
    Trains Spirit Speak by channeling nearby corpses.
    """
    SendMessage("Starting Spirit Speak training...")
    while True:
        if not UseSkill("Spirit Speak", 10000):
            Pause(1000)
            continue
        corpse_filter = Items.Filter()
        corpse_filter.RangeMax = 2
        corpse_filter.IsCorpse = 1
        corpses = Items.ApplyFilter(corpse_filter)
        if corpses:
            corpse = corpses[0]
            Target.WaitForTarget(10000, False)
            Target.TargetExecute(corpse)
        else:
            SendMessage("No corpses found, waiting...", colors['yellow'])
        Pause(1000)

def TrainMeditation():
    """
    Trains Meditation by actively meditating.
    """
    SendMessage("Starting Meditation training...")
    while True:
        if not UseSkill("Meditation", 10000):
            Pause(1000)
            continue
        Pause(1000)

def TrainAnimalTaming():
    """
    Trains Animal Taming by taming nearby tamable animals.
    """
    SendMessage("Starting Animal Taming training...")
    while True:
        animal_filter = Mobiles.Filter()
        animal_filter.RangeMax = 5
        animal_filter.IsHuman = 0
        animal_filter.IsGhost = 0
        animals = Mobiles.ApplyFilter(animal_filter)
        if not animals:
            SendMessage("No tamable animals found, waiting...", colors['yellow'])
            Pause(2000)
            continue
        animal = animals[0]
        if not UseSkill("Animal Taming", 10000):
            Pause(1000)
            continue
        Target.WaitForTarget(10000, False)
        Target.TargetExecute(animal)
        Pause(1000)

def TrainMagery():
    """
    Trains Magery by casting Magic Arrow on self.
    """
    SendMessage("Starting Magery training...")
    while True:
        if not CastSpell("Magic Arrow", target=Player.Serial, timeout=10000):
            Pause(1000)
            continue
        Pause(1000)

def TrainStealth():
    """
    Trains Stealth by using the skill after hiding.
    """
    SendMessage("Starting Stealth training...")
    while True:
        if not Player.Hidden:
            if not UseSkill("Hiding", 10000):
                Pause(1000)
                continue
            Pause(1000)
        if not UseSkill("Stealth", 1008):
            Pause(1000)
            continue
        Pause(1000)

def TrainLockpicking():
    """
    Trains Lockpicking by unlocking and relocking a lockbox.
    """
    SendMessage("Starting Lockpicking training...")
    lockpick_id = 0x14FB  # Lockpick
    if not CheckItemExists(lockpick_id, Player.Backpack, "lockpick"):
        return
    lockbox = FindLockbox(radius=2)
    if not lockbox:
        SendMessage("No lockbox found!", colors['red'])
        return
    while True:
        lockpick = FindItem(lockpick_id, Player.Backpack)
        if not lockpick:
            SendMessage("No lockpick found, stopping.", colors['red'])
            return
        Items.UseItem(lockpick)
        Target.WaitForTarget(10000, False)
        Target.TargetExecute(lockbox)
        Pause(1000)

def TrainResistingSpells():
    """
    Trains Resisting Spells by casting Clumsy on self.
    """
    SendMessage("Starting Resisting Spells training...")
    while True:
        if not CastSpell("Clumsy", target=Player.Serial, timeout=10000):
            Pause(1000)
            continue
        Pause(1000)

def TrainHealing():
    """
    Trains Healing by using bandages on self or a nearby mobile.
    """
    SendMessage("Starting Healing training...")
    bandage_id = 0x0E21  # Bandages
    if not CheckItemExists(bandage_id, Player.Backpack, "bandages"):
        return
    while True:
        bandage = FindItem(bandage_id, Player.Backpack)
        if not bandage:
            SendMessage("No bandages found, stopping.", colors['red'])
            return
        Items.UseItem(bandage)
        Target.WaitForTarget(10000, False)
        mobile_filter = Mobiles.Filter()
        mobile_filter.RangeMax = 2
        mobile_filter.IsHuman = 0
        mobile_filter.IsGhost = 0
        mobiles = Mobiles.ApplyFilter(mobile_filter)
        target = mobiles[0] if mobiles else Player
        Target.TargetExecute(target)
        Pause(2000)

def TrainSpellweaving():
    """
    Trains Spellweaving by casting Gift of Renewal on self.
    """
    SendMessage("Starting Spellweaving training...")
    while True:
        if not CastSpell("Gift of Renewal", target=Player.Serial, timeout=10000):
            Pause(1000)
            continue
        Pause(1000)

def TrainNecromancy():
    """
    Trains Necromancy by casting Curse Weapon.
    """
    SendMessage("Starting Necromancy training...")
    while True:
        if not CastSpell("Curse Weapon", timeout=10000):
            Pause(1000)
            continue
        Pause(1000)

def TrainMysticism():
    """
    Trains Mysticism by casting Healing Stone.
    """
    SendMessage("Starting Mysticism training...")
    while True:
        if not CastSpell("Healing Stone", timeout=10000):
            Pause(1000)
            continue
        Pause(1000)

def TrainChivalry():
    """
    Trains Chivalry by casting Consecrate Weapon.
    """
    SendMessage("Starting Chivalry training...")
    while True:
        if not CastSpell("Consecrate Weapon", timeout=10000):
            Pause(1000)
            continue
        Pause(1000)

def TrainBushido():
    """
    Trains Bushido by casting Honorable Execution.
    """
    SendMessage("Starting Bushido training...")
    while True:
        if not CastSpell("Honorable Execution", timeout=10000):
            Pause(1000)
            continue
        Pause(1000)

def TrainNinjitsu():
    """
    Trains Ninjitsu by casting Focus Attack.
    """
    SendMessage("Starting Ninjitsu training...")
    while True:
        if not CastSpell("Focus Attack", timeout=10000):
            Pause(1000)
            continue
        Pause(1000)

if __name__ == "__main__":
    TrainMagery()