# Sparkin's Epic Mining Adventure
# Adapted for UOAlive using Classic Client and Enhanced Razor
# Crafted with Grok 3.0 for Sparkin's Adventure Tome
# Embark on a thrilling quest to unearth the earth's treasures! Mine until the veins run dry,
# then heed the call to seek new riches. Use the world map (zoomed in) to conquer 8x8 zones.
# Keep an eye on your beetle's weight, brave adventurer, as this script automates the grind
# but demands your heroic oversight!
#
# REQUIREMENTS:
# - 50+ Tinkering skill to forge mighty tool kits and shovels
# - ~20 iron ingots or pre-crafted shovels to fuel your quest
# - A fire beetle to smelt your spoils
# - A blue (giant) beetle to haul your glittering hoard
#
### CONFIG ###
# Serials for your trusty beetle companions (prompts for selection if not set)
fire_beetle = Target.PromptTarget('Target your fire beetle, brave miner!', 43) or 0x0007950C
blue_beetle = Target.PromptTarget('Target your blue beetle, noble steed!', 161) or 0x043D5FC2
# Minimum tool kits to keep (2+ to avoid crafting woes)
tool_kits_to_keep = 2
# Number of shovels to maintain (higher for fewer interruptions)
shovels_to_keep = 5
# Optional: Use prospecting tool to unearth greater riches
use_prospecting = True
# Optional: Wield sturdy shovels (high durability, e.g., from Bulk Order Deeds)
use_sturdy_shovels = False
### CONFIG ###

from AutoComplete import *
import random

# Constants
SHOVEL = 0x0F39
TOOL_KIT = 0x1EB8
INGOT = 0x1BF2
PROSPECTING_TOOL = 0x0FB4
ORE_TYPES = [0x19B7, 0x19B8, 0x19B9, 0x19BA, 0x0DF8, 0x1726]
TINKERING_GUMP = 0xfe708543
SMELT_WEIGHT_THRESHOLD = 400  # Smelt when weight exceeds MaxWeight - this value

# Item filter for ores
ore_filter = Items.Filter()
ore_filter.Graphics.AddRange(ORE_TYPES)
ore_filter.Enabled = True
ore_filter.OnGround = False
ore_filter.Movable = True

# Adventure counters
ore_mined_count = 0
ingots_moved_count = 0

# Exciting message pools
MINING_MESSAGES = [
    "Strike the earth, hero! Seek the hidden veins!",
    "Dig deep, adventurer! Riches await!",
    "Your shovel sings as it carves the stone!"
]
SMELTING_MESSAGES = [
    "The fire beetle roars, forging your ores into glory!",
    "Flames dance, transforming stone to metal!",
    "By fire and might, your haul is smelted!"
]
NO_ORE_MESSAGES = [
    "The earth yields no more! Seek a new vein, champion!",
    "This vein is spent! Onward to new treasures!",
    "The ground is barren! March to fresh riches!"
]
RARE_FIND_MESSAGES = [
    "By the gods, a rare find sparkles in the dust!",
    "A treasure of legend! Your name will echo in tales!",
    "Woot! A gem of the earth, yours to claim!"
]

# Color palette for messages
COLORS = {
    'success': 66,   # Green for success
    'action': 2127,  # Orange for actions
    'error': 38,     # Red for errors
    'rare': 1153,    # Bright cyan for rare finds
    'info': 2125     # Yellow for info
}

def play_sound(sound_id):
    """Play an in-game sound effect if supported."""
    try:
        Misc.SendMessage("", sound_id)
    except:
        pass  # Silently fail if sound not supported

def get_tool_kits():
    """Retrieve all tool kits in player's backpack."""
    return Items.FindAllByID(TOOL_KIT, 0, Player.Backpack.Serial, True)

def get_shovels():
    """Retrieve all shovels in player's backpack (sturdy or regular)."""
    return Items.FindAllByID(SHOVEL, -1 if use_sturdy_shovels else 0, Player.Backpack.Serial, True)

def open_tinkering_gump():
    """Open and navigate to the tools tab in the tinkering gump."""
    if Gumps.CurrentGump() != TINKERING_GUMP:
        tool_kit = get_tool_kits()[0] if get_tool_kits() else None
        if not tool_kit:
            Player.HeadMessage(COLORS['error'], "No tool kits found, brave smith!")
            return False
        Items.UseItem(tool_kit)
        Gumps.WaitForGump(TINKERING_GUMP, 3000)
    
    if not Gumps.LastGumpTextExistByLine(24, "scissors"):
        Gumps.SendAction(TINKERING_GUMP, 15)  # Navigate to tools tab
        Gumps.WaitForGump(TINKERING_GUMP, 3000)
    return True

def make_tool_kit():
    """Forge a single tool kit with legendary skill."""
    if not open_tinkering_gump():
        return False
    Gumps.SendAction(TINKERING_GUMP, 23)  # Craft tool kit
    Gumps.WaitForGump(TINKERING_GUMP, 3000)
    play_sound(0x2A)  # Hammer sound
    return True

def make_shovel():
    """Craft a mighty shovel to conquer the earth."""
    if not open_tinkering_gump():
        return False
    Gumps.SendAction(TINKERING_GUMP, 72)  # Craft shovel
    Gumps.WaitForGump(TINKERING_GUMP, 3000)
    play_sound(0x2A)  # Hammer sound
    return True

def make_tools():
    """Forge tools to sustain your epic quest."""
    kits = len(get_tool_kits())
    shovels = len(get_shovels())
    
    while kits < tool_kits_to_keep:
        Player.HeadMessage(COLORS['info'], f"Forging tool kit ({kits}/{tool_kits_to_keep}) with masterful skill...")
        if not make_tool_kit():
            Player.HeadMessage(COLORS['error'], "Alas, the forge fails you!")
            break
        kits += 1
        Misc.Pause(300)
    
    while shovels < shovels_to_keep:
        Player.HeadMessage(COLORS['info'], f"Crafting shovel ({shovels}/{shovels_to_keep}) to rend the earth...")
        if not make_shovel():
            Player.HeadMessage(COLORS['error'], "The anvil betrays you, hero!")
            break
        shovels += 1
        Misc.Pause(300)
    
    Gumps.CloseGump(TINKERING_GUMP)

def move_ingots():
    """Haul your glittering ingots to the blue beetle's hoard."""
    global ingots_moved_count
    # Verify blue beetle exists and is valid
    beetle = Mobiles.FindBySerial(blue_beetle)
    if not beetle:
        Player.HeadMessage(COLORS['error'], f"Alas, your blue beetle (serial {hex(blue_beetle)}) is lost!")
        return False
    
    # Ensure beetle is close enough (within 2 tiles)
    if Misc.Distance(Player.Position.X, Player.Position.Y, beetle.Position.X, beetle.Position.Y) > 2:
        Player.HeadMessage(COLORS['error'], "Your beetle wanders too far, noble miner!")
        return False
    
    # Find all ingots in player's backpack
    ingots = Items.FindAllByID(INGOT, -1, Player.Backpack.Serial, True)
    if not ingots:
        Player.HeadMessage(COLORS['error'], "No ingots to haul, adventurer!")
        return False
    
    # Move ingots to beetle
    moved = False
    for ingot in ingots:
        amount_to_move = max(0, ingot.Amount - 50) if ingot.Hue == 0 else ingot.Amount
        if amount_to_move > 0:  # Move only if there are ingots to transfer
            Player.HeadMessage(COLORS['action'], f"Hauling {amount_to_move} ingot(s) (Hue: {ingot.Hue}) to your trusty beetle!")
            Journal.Clear()
            Items.Move(ingot, blue_beetle, amount_to_move)
            Misc.Pause(1000)  # Ensure server processes the move
            if Journal.Search("cannot move"):
                Player.HeadMessage(COLORS['error'], "The gods block your haul!")
                return False
            ingots_moved_count += amount_to_move
            moved = True
            play_sound(0x57)  # Coin sound
    
    if not moved:
        Player.HeadMessage(COLORS['error'], "No ingots needed to be hauled.")
    else:
        Player.HeadMessage(COLORS['success'], f"Total ingots hauled: {ingots_moved_count}")
    return True

def prospect_tile():
    """Scour the earth for greater riches with your prospecting tool."""
    if not use_prospecting:
        return False
    prospect_tool = Items.FindByID(PROSPECTING_TOOL, 0, Player.Backpack.Serial)
    if not prospect_tool:
        Player.HeadMessage(COLORS['error'], "No prospecting tool to seek greater veins!")
        return False
    land = Statics.GetStaticsTileInfo(Player.Position.X, Player.Position.Y, Player.Map)
    if land:
        Items.UseItem(prospect_tool)
        Target.WaitForTarget(3000)
        Target.TargetExecute(Player.Position.X, Player.Position.Y, Player.Position.Z, land[0].StaticID)
        Player.HeadMessage(COLORS['info'], "Prospecting the vein for legendary yields!")
        play_sound(0x242)  # Mining sound
        return True
    return False

# Main mining loop
Journal.Clear()
prospected = False
Player.HeadMessage(COLORS['success'], "Embark on Sparkin's Epic Mining Adventure!")
while not Player.IsGhost:
    max_weight = Player.MaxWeight
    smelt_weight = max_weight - SMELT_WEIGHT_THRESHOLD

    # Ensure a shovel is available
    try:
        tool = get_shovels()[0]
    except IndexError:
        Player.HeadMessage(COLORS['info'], "Your shovel is spent! Forging anew...")
        make_tools()
        try:
            tool = get_shovels()[0]
        except IndexError:
            Player.HeadMessage(COLORS['error'], "No shovels remain! Your quest falters!")
            break

    # Prospect the tile if not done
    if not prospected and use_prospecting:
        prospected = prospect_tile()
        Misc.Pause(300)

    # Mine the tile
    Player.HeadMessage(COLORS['action'], random.choice(MINING_MESSAGES))
    Target.TargetResource(tool, 'ore')
    ore_mined_count += 1
    play_sound(0x242)  # Mining sound
    Misc.Pause(300)

    # Check for no ore
    if Journal.Search('There is no metal here to mine'):
        x, y = Player.Position.X, Player.Position.Y
        Player.HeadMessage(COLORS['error'], random.choice(NO_ORE_MESSAGES))
        prospected = False
        Journal.Clear()
        while Player.Position.X == x and Player.Position.Y == y:
            Misc.Pause(100)

    # Announce rare finds
    if Journal.Search('Woot! You have found a'):
        message = Journal.GetLineText('You have found a', False)
        Player.HeadMessage(COLORS['rare'], random.choice(RARE_FIND_MESSAGES))
        Journal.Clear(message)
        play_sound(0x3D)  # Fanfare sound

    # Smelt ores if overweight
    if Player.Weight >= smelt_weight:
        Player.HeadMessage(COLORS['action'], random.choice(SMELTING_MESSAGES))
        ores = Items.ApplyFilter(ore_filter)
        for ore in ores:
            if ore.ItemID == 0x19B7 and ore.Amount == 1:  # Skip single small ores
                continue
            Items.UseItem(ore)
            if Target.WaitForTarget(1500):
                Target.TargetExecute(fire_beetle)
            Misc.Pause(600)
            play_sound(0x2E)  # Fire sound
        
        Misc.Pause(1000)

    # Move ingots to beetle if near max weight
    if Player.Weight > max_weight - 100:
        Player.HeadMessage(COLORS['action'], "Your pack groans! Hauling ingots to your beetle...")
        if not move_ingots():
            Player.HeadMessage(COLORS['error'], "Failed to haul ingots! Check your beetle and hoard.")
    
    # Periodic progress update
    if ore_mined_count % 10 == 0:
        Player.HeadMessage(COLORS['success'], f"Adventure Log: {ore_mined_count} ores mined, {ingots_moved_count} ingots hauled!")