# Sparkin's Utilities - Single File Implementation for Razor Enhanced 0.8.2.242

# Utility Functions
def SendMessage(message, color=0x00B7):  # Cyan
    Player.HeadMessage(color, message)

def Pause(milliseconds):
    Misc.Pause(milliseconds)

def UseSkill(skill_name, timeout=10000):
    Player.UseSkill(skill_name)
    Pause(timeout)
    if Journal.Search("You must wait") or Journal.Search("already performing"):
        SendMessage(f"{skill_name} on cooldown!", 0x0020)  # Red
        Journal.Clear()
        return False
    Journal.Clear()
    return True

def CastSpell(spell_name, target=None, timeout=10000):
    Spells.Cast(spell_name)
    Pause(timeout)
    if Journal.Search("not enough mana") or Journal.Search("fizzles"):
        SendMessage(f"Failed to cast {spell_name}!", 0x0020)
        Journal.Clear()
        return False
    if target:
        Target.WaitForTarget(timeout, False)
        if isinstance(target, int):
            Target.TargetExecute(target)
        else:
            Target.TargetExecute(target)
    Journal.Clear()
    return True

# Item Functions
def FindItem(item_id, container, timeout=1000):
    Items.FindByID(item_id, -1, container.Serial, timeout)
    item = Items.FindByID(item_id, -1, container.Serial)
    if not item:
        SendMessage(f"Item {hex(item_id)} not found in container!", 0x0020)
        return None
    return item

def CheckItemExists(item_id, container, item_name="item"):
    item = FindItem(item_id, container)
    if not item:
        SendMessage(f"No {item_name} found in backpack!", 0x0020)
        return False
    return True

def FindLockbox(radius=2):
    lockbox_ids = [0x0E7C, 0x0E7D, 0x09AB]
    lockbox_filter = Items.Filter()
    lockbox_filter.RangeMax = radius
    lockbox_filter.Graphics = List[Int32](lockbox_ids)
    lockboxes = Items.ApplyFilter(lockbox_filter)
    return lockboxes[0] if lockboxes else None

# Skill Training Functions
def TrainHiding():
    SendMessage("Starting Hiding training...", 0x00B7)
    while Player.GetSkillValue("Hiding") < 100.0:
        if not UseSkill("Hiding"):
            Pause(5000)
        Pause(1000)

def TrainDetectHidden():
    SendMessage("Starting Detect Hidden training...", 0x00B7)
    while Player.GetSkillValue("Detect Hidden") < 100.0:
        if not UseSkill("Detect Hidden"):
            Pause(5000)
        else:
            Target.WaitForTarget(10000, False)
            Target.Self()
        Pause(1000)

def TrainSpiritSpeak():
    SendMessage("Starting Spirit Speak training...", 0x00B7)
    while Player.GetSkillValue("Spirit Speak") < 100.0:
        if not UseSkill("Spirit Speak"):
            Pause(5000)
        Pause(1000)

def TrainMeditation():
    SendMessage("Starting Meditation training...", 0x00B7)
    while Player.GetSkillValue("Meditation") < 100.0:
        if not UseSkill("Meditation"):
            Pause(5000)
        Pause(1000)

def TrainAnimalTaming():
    SendMessage("Starting Animal Taming training. Target a creature...", 0x00B7)
    while Player.GetSkillValue("Animal Taming") < 100.0:
        if not UseSkill("Animal Taming"):
            Pause(5000)
        else:
            Target.WaitForTarget(10000, False)
            SendMessage("Select a creature...", 0x00B7)
        Pause(1000)

def TrainMagery():
    SendMessage("Starting Magery training...", 0x00B7)
    while Player.GetSkillValue("Magery") < 100.0:
        if not CastSpell("Magic Arrow", Player.Serial):
            Pause(5000)
        Pause(1000)

def TrainStealth():
    SendMessage("Starting Stealth training...", 0x00B7)
    while Player.GetSkillValue("Stealth") < 100.0:
        if not Player.BuffsExist("Hiding"):
            UseSkill("Hiding")
            Pause(5000)
        if not UseSkill("Stealth"):
            Pause(5000)
        Pause(1000)

def TrainLockpicking():
    SendMessage("Starting Lockpicking training...", 0x00B7)
    lockpick_id = 0x14FB
    while Player.GetSkillValue("Lockpicking") < 100.0:
        if not CheckItemExists(lockpick_id, Player.Backpack, "lockpick"):
            SendMessage("Stopping: No lockpicks!", 0x0020)
            break
        lockbox = FindLockbox()
        if not lockbox:
            SendMessage("Stopping: No lockbox found!", 0x0020)
            break
        if not UseSkill("Lockpicking"):
            Pause(5000)
        else:
            Target.WaitForTarget(10000, False)
            Target.TargetExecute(lockbox)
        Pause(1000)

def TrainResistingSpells():
    SendMessage("Starting Resisting Spells training...", 0x00B7)
    while Player.GetSkillValue("Resisting Spells") < 100.0:
        if not CastSpell("Magic Arrow", Player.Serial):
            Pause(5000)
        Pause(1000)

def TrainHealing():
    SendMessage("Starting Healing training...", 0x00B7)
    bandage_id = 0x0E21
    while Player.GetSkillValue("Healing") < 100.0:
        if not CheckItemExists(bandage_id, Player.Backpack, "bandage"):
            SendMessage("Stopping: No bandages!", 0x0020)
            break
        if not UseSkill("Healing"):
            Pause(5000)
        else:
            Target.WaitForTarget(10000, False)
            Target.Self()
        Pause(1000)

def TrainSpellweaving():
    SendMessage("Starting Spellweaving training...", 0x00B7)
    while Player.GetSkillValue("Spellweaving") < 100.0:
        if not CastSpell("Arcane Circle"):
            Pause(5000)
        Pause(1000)

def TrainNecromancy():
    SendMessage("Starting Necromancy training...", 0x00B7)
    while Player.GetSkillValue("Necromancy") < 100.0:
        if not CastSpell("Curse Weapon"):
            Pause(5000)
        Pause(1000)

def TrainMysticism():
    SendMessage("Starting Mysticism training...", 0x00B7)
    while Player.GetSkillValue("Mysticism") < 100.0:
        if not CastSpell("Nether Bolt", Player.Serial):
            Pause(5000)
        Pause(100