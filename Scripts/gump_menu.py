from Scripts.utilities.helpers import SendMessage, Pause
from Scripts.glossary.colors import colors
from Scripts.heal_Pets import HealPet
from Scripts.mine_Auto import MineAuto
from Scripts.lumber_Auto import LumberAuto
from Scripts.sand_Auto import SandAuto
from Scripts.fish_Auto import FishAuto
from Scripts.train_Skills import TrainHiding, TrainDetectHidden, TrainSpiritSpeak, TrainMeditation, TrainAnimalTaming, TrainMagery, TrainStealth, TrainLockpicking, TrainResistingSpells, TrainHealing, TrainSpellweaving, TrainNecromancy, TrainMysticism, TrainChivalry, TrainBushido, TrainNinjitsu
from Scripts.harvest_Resources import HarvestResources

def CreateMainGump():
    """
    Creates and displays the main gump menu for Sparkin's Utilities.
    """
    gump = Gumps.CreateGump(True, False, False, True)  # Closable, not movable, not resizable, draggable
    
    # Gump background
    Gumps.AddBackground(gump, 0, 0, 300, 350, 9200)
    Gumps.AddLabel(gump, 20, 20, 1152, "Sparkin's Utilities")
    
    # Utility buttons
    Gumps.AddButton(gump, 20, 60, 4005, 4007, 1, 0, 0)  # Heal Pet
    Gumps.AddLabel(gump, 50, 60, 0, "Heal Pet")
    Gumps.AddButton(gump, 20, 100, 4005, 4007, 2, 0, 0)  # Mine Auto
    Gumps.AddLabel(gump, 50, 100, 0, "Mine Auto")
    Gumps.AddButton(gump, 20, 140, 4005, 4007, 3, 0, 0)  # Lumber Auto
    Gumps.AddLabel(gump, 50, 140, 0, "Lumber Auto")
    Gumps.AddButton(gump, 20, 180, 4005, 4007, 4, 0, 0)  # Sand Auto
    Gumps.AddLabel(gump, 50, 180, 0, "Sand Auto")
    Gumps.AddButton(gump, 20, 220, 4005, 4007, 5, 0, 0)  # Fish Auto
    Gumps.AddLabel(gump, 50, 220, 0, "Fish Auto")
    Gumps.AddButton(gump, 20, 260, 4005, 4007, 6, 0, 0)  # Training
    Gumps.AddLabel(gump, 50, 260, 0, "Training")
    Gumps.AddButton(gump, 20, 300, 4005, 4007, 7, 0, 0)  # Harvest Resources
    Gumps.AddLabel(gump, 50, 300, 0, "Harvest Resources")
    
    # Close button
    Gumps.AddButton(gump, 20, 320, 4017, 4019, 0, 0, 0)  # Close gump
    Gumps.AddLabel(gump, 50, 320, 0, "Close")
    
    Gumps.SendGump(1001, Player.Serial, 0, gump.gumpDefinition, gump.gumpStrings)
    return gump

def CreateHealPetGump():
    """
    Creates a gump for selecting the healing tool.
    """
    gump = Gumps.CreateGump(True, False, False, True)
    Gumps.AddBackground(gump, 0, 0, 300, 200, 9200)
    Gumps.AddLabel(gump, 20, 20, 1152, "Select Healing Tool")
    Gumps.AddButton(gump, 20, 60, 4005, 4007, 1, 0, 0)  # Bandages
    Gumps.AddLabel(gump, 50, 60, 0, "Bandages (0x0E21)")
    Gumps.AddButton(gump, 20, 160, 4014, 4016, 0, 0, 0)  # Back
    Gumps.AddLabel(gump, 50, 160, 0, "Back")
    Gumps.SendGump(1002, Player.Serial, 0, gump.gumpDefinition, gump.gumpStrings)
    return gump

def CreateMineAutoGump():
    """
    Creates a gump for selecting the mining tool.
    """
    gump = Gumps.CreateGump(True, False, False, True)
    Gumps.AddBackground(gump, 0, 0, 300, 200, 9200)
    Gumps.AddLabel(gump, 20, 20, 1152, "Select Mining Tool")
    Gumps.AddButton(gump, 20, 60, 4005, 4007, 1, 0, 0)  # Pickaxe
    Gumps.AddLabel(gump, 50, 60, 0, "Pickaxe (0x0E86)")
    Gumps.AddButton(gump, 20, 100, 4005, 4007, 2, 0, 0)  # Shovel
    Gumps.AddLabel(gump, 50, 100, 0, "Shovel (0x0F39)")
    Gumps.AddButton(gump, 20, 160, 4014, 4016, 0, 0, 0)  # Back
    Gumps.AddLabel(gump, 50, 160, 0, "Back")
    Gumps.SendGump(1003, Player.Serial, 0, gump.gumpDefinition, gump.gumpStrings)
    return gump

def CreateLumberAutoGump():
    """
    Creates a gump for selecting the lumberjacking tool.
    """
    gump = Gumps.CreateGump(True, False, False, True)
    Gumps.AddBackground(gump, 0, 0, 300, 200, 9200)
    Gumps.AddLabel(gump, 20, 20, 1152, "Select Lumberjacking Tool")
    Gumps.AddButton(gump, 20, 60, 4005, 4007, 1, 0, 0)  # Hatchet
    Gumps.AddLabel(gump, 50, 60, 0, "Hatchet (0x0F43)")
    Gumps.AddButton(gump, 20, 100, 4005, 4007, 2, 0, 0)  # Axe
    Gumps.AddLabel(gump, 50, 100, 0, "Axe (0x0F47)")
    Gumps.AddButton(gump, 20, 160, 4014, 4016, 0, 0, 0)  # Back
    Gumps.AddLabel(gump, 50, 160, 0, "Back")
    Gumps.SendGump(1004, Player.Serial, 0, gump.gumpDefinition, gump.gumpStrings)
    return gump

def CreateSandAutoGump():
    """
    Creates a gump for selecting the sand mining tool.
    """
    gump = Gumps.CreateGump(True, False, False, True)
    Gumps.AddBackground(gump, 0, 0, 300, 200, 9200)
    Gumps.AddLabel(gump, 20, 20, 1152, "Select Sand Mining Tool")
    Gumps.AddButton(gump, 20, 60, 4005, 4007, 1, 0, 0)  # Shovel
    Gumps.AddLabel(gump, 50, 60, 0, "Shovel (0x0F39)")
    Gumps.AddButton(gump, 20, 160, 4014, 4016, 0, 0, 0)  # Back
    Gumps.AddLabel(gump, 50, 160, 0, "Back")
    Gumps.SendGump(1005, Player.Serial, 0, gump.gumpDefinition, gump.gumpStrings)
    return gump

def CreateFishAutoGump():
    """
    Creates a gump for selecting the fishing tool.
    """
    gump = Gumps.CreateGump(True, False, False, True)
    Gumps.AddBackground(gump, 0, 0, 300, 200, 9200)
    Gumps.AddLabel(gump, 20, 20, 1152, "Select Fishing Tool")
    Gumps.AddButton(gump, 20, 60, 4005, 4007, 1, 0, 0)  # Fishing Pole
    Gumps.AddLabel(gump, 50, 60, 0, "Fishing Pole (0x0DC0)")
    Gumps.AddButton(gump, 20, 160, 4014, 4016, 0, 0, 0)  # Back
    Gumps.AddLabel(gump, 50, 160, 0, "Back")
    Gumps.SendGump(1006, Player.Serial, 0, gump.gumpDefinition, gump.gumpStrings)
    return gump

def CreateTrainingGump():
    """
    Creates a gump for selecting the skill to train.
    """
    gump = Gumps.CreateGump(True, False, False, True)
    Gumps.AddBackground(gump, 0, 0, 300, 650, 9200)  # Increased height for 16 skills
    Gumps.AddLabel(gump, 20, 20, 1152, "Select Skill to Train")
    
    # Training buttons
    Gumps.AddButton(gump, 20, 60, 4005, 4007, 1, 0, 0)  # Hiding
    Gumps.AddLabel(gump, 50, 60, 0, "Hiding")
    Gumps.AddButton(gump, 20, 100, 4005, 4007, 2, 0, 0)  # Detect Hidden
    Gumps.AddLabel(gump, 50, 100, 0, "Detect Hidden")
    Gumps.AddButton(gump, 20, 140, 4005, 4007, 3, 0, 0)  # Spirit Speak
    Gumps.AddLabel(gump, 50, 140, 0, "Spirit Speak")
    Gumps.AddButton(gump, 20, 180, 4005, 4007, 4, 0, 0)  # Meditation
    Gumps.AddLabel(gump, 50, 180, 0, "Meditation")
    Gumps.AddButton(gump, 20, 220, 4005, 4007, 5, 0, 0)  # Animal Taming
    Gumps.AddLabel(gump, 50, 220, 0, "Animal Taming")
    Gumps.AddButton(gump, 20, 260, 4005, 4007, 6, 0, 0)  # Magery
    Gumps.AddLabel(gump, 50, 260, 0, "Magery")
    Gumps.AddButton(gump, 20, 300, 4005, 4007, 7, 0, 0)  # Stealth
    Gumps.AddLabel(gump, 50, 300, 0, "Stealth")
    Gumps.AddButton(gump, 20, 340, 4005, 4007, 8, 0, 0)  # Lockpicking
    Gumps.AddLabel(gump, 50, 340, 0, "Lockpicking")
    Gumps.AddButton(gump, 20, 380, 4005, 4007, 9, 0, 0)  # Resisting Spells
    Gumps.AddLabel(gump, 50, 380, 0, "Resisting Spells")
    Gumps.AddButton(gump, 20, 420, 4005, 4007, 10, 0, 0)  # Healing
    Gumps.AddLabel(gump, 50, 420, 0, "Healing")
    Gumps.AddButton(gump, 20, 460, 4005, 4007, 11, 0, 0)  # Spellweaving
    Gumps.AddLabel(gump, 50, 460, 0, "Spellweaving")
    Gumps.AddButton(gump, 20, 500, 4005, 4007, 12, 0, 0)  # Necromancy
    Gumps.AddLabel(gump, 50, 500, 0, "Necromancy")
    Gumps.AddButton(gump, 20, 540, 4005, 4007, 13, 0, 0)  # Mysticism
    Gumps.AddLabel(gump, 50, 540, 0, "Mysticism")
    Gumps.AddButton(gump, 20, 580, 4005, 4007, 14, 0, 0)  # Chivalry
    Gumps.AddLabel(gump, 50, 580, 0, "Chivalry")
    Gumps.AddButton(gump, 20, 620, 4005, 4007, 15, 0, 0)  # Bushido
    Gumps.AddLabel(gump, 50, 620, 0, "Bushido")
    Gumps.AddButton(gump, 20, 660, 4005, 4007, 16, 0, 0)  # Ninjitsu
    Gumps.AddLabel(gump, 50, 660, 0, "Ninjitsu")
    
    # Back button
    Gumps.AddButton(gump, 20, 680, 4014, 4016, 0, 0, 0)  # Back
    Gumps.AddLabel(gump, 50, 680, 0, "Back")
    
    Gumps.SendGump(1007, Player.Serial, 0, gump.gumpDefinition, gump.gumpStrings)
    return gump

def CreateHarvestResourcesGump():
    """
    Creates a gump for selecting the harvesting tool.
    """
    gump = Gumps.CreateGump(True, False, False, True)
    Gumps.AddBackground(gump, 0, 0, 300, 200, 9200)
    Gumps.AddLabel(gump, 20, 20, 1152, "Select Harvesting Tool")
    Gumps.AddButton(gump, 20, 60, 4005, 4007, 1, 0, 0)  # Dagger
    Gumps.AddLabel(gump, 50, 60, 0, "Dagger (0x0F52)")
    Gumps.AddButton(gump, 20, 100, 4005, 4007, 2, 0, 0)  # None
    Gumps.AddLabel(gump, 50, 100, 0, "None (Direct Pickup)")
    Gumps.AddButton(gump, 20, 160, 4014, 4016, 0, 0, 0)  # Back
    Gumps.AddLabel(gump, 50, 160, 0, "Back")
    Gumps.SendGump(1008, Player.Serial, 0, gump.gumpDefinition, gump.gumpStrings)
    return gump

def HandleGumpResponse(gump_id, button_id):
    """
    Handles user input from gump menus.
    """
    if gump_id == 1001:  # Main menu
        if button_id == 0:  # Close
            return
        elif button_id == 1:  # Heal Pet
            CreateHealPetGump()
        elif button_id == 2:  # Mine Auto
            CreateMineAutoGump()
        elif button_id == 3:  # Lumber Auto
            CreateLumberAutoGump()
        elif button_id == 4:  # Sand Auto
            CreateSandAutoGump()
        elif button_id == 5:  # Fish Auto
            CreateFishAutoGump()
        elif button_id == 6:  # Training
            CreateTrainingGump()
        elif button_id == 7:  # Harvest Resources
            CreateHarvestResourcesGump()
    
    elif gump_id == 1002:  # Heal Pet menu
        if button_id == 0:  # Back
            CreateMainGump()
        elif button_id == 1:  # Bandages
            HealPet(tool_id=0x0E21)
            CreateMainGump()
    
    elif gump_id == 1003:  # Mine Auto menu
        if button_id == 0:  # Back
            CreateMainGump()
        elif button_id == 1:  # Pickaxe
            MineAuto(tool_id=0x0E86)
            CreateMainGump()
        elif button_id == 2:  # Shovel
            MineAuto(tool_id=0x0F39)
            CreateMainGump()
    
    elif gump_id == 1004:  # Lumber Auto menu
        if button_id == 0:  # Back
            CreateMainGump()
        elif button_id == 1:  # Hatchet
            LumberAuto(tool_id=0x0F43)
            CreateMainGump()
        elif button_id == 2:  # Axe
            LumberAuto(tool_id=0x0F47)
            CreateMainGump()
    
    elif gump_id == 1005:  # Sand Auto menu
        if button_id == 0:  # Back
            CreateMainGump()
        elif button_id == 1:  # Shovel
            SandAuto(tool_id=0x0F39)
            CreateMainGump()
    
    elif gump_id == 1006:  # Fish Auto menu
        if button_id == 0:  # Back
            CreateMainGump()
        elif button_id == 1:  # Fishing Pole
            FishAuto(tool_id=0x0DC0)
            CreateMainGump()
    
    elif gump_id == 1007:  # Training menu
        if button_id == 0:  # Back
            CreateMainGump()
        elif button_id == 1:  # Hiding
            TrainHiding()
            CreateMainGump()
        elif button_id == 2:  # Detect Hidden
            TrainDetectHidden()
            CreateMainGump()
        elif button_id == 3:  # Spirit Speak
            TrainSpiritSpeak()
            CreateMainGump()
        elif button_id == 4:  # Meditation
            TrainMeditation()
            CreateMainGump()
        elif button_id == 5:  # Animal Taming
            TrainAnimalTaming()
            CreateMainGump()
        elif button_id == 6:  # Magery
            TrainMagery()
            CreateMainGump()
        elif button_id == 7:  # Stealth
            TrainStealth()
            CreateMainGump()
        elif button_id == 8:  # Lockpicking
            TrainLockpicking()
            CreateMainGump()
        elif button_id == 9:  # Resisting Spells
            TrainResistingSpells()
            CreateMainGump()
        elif button_id == 10:  # Healing
            TrainHealing()
            CreateMainGump()
        elif button_id == 11:  # Spellweaving
            TrainSpellweaving()
            CreateMainGump()
        elif button_id == 12:  # Necromancy
            TrainNecromancy()
            CreateMainGump()
        elif button_id == 13:  # Mysticism
            TrainMysticism()
            CreateMainGump()
        elif button_id == 14:  # Chivalry
            TrainChivalry()
            CreateMainGump()
        elif button_id == 15:  # Bushido
            TrainBushido()
            CreateMainGump()
        elif button_id == 16:  # Ninjitsu
            TrainNinjitsu()
            CreateMainGump()
    
    elif gump_id == 1008:  # Harvest Resources menu
        if button_id == 0:  # Back
            CreateMainGump()
        elif button_id == 1:  # Dagger
            HarvestResources(tool_id=0x0F52)
            CreateMainGump()
        elif button_id == 2:  # None
            HarvestResources(tool_id=None)
            CreateMainGump()

def ShowMainMenu():
    """
    Entry point to show the main gump menu. Trigger with a hotkey (e.g., F1).
    """
    SendMessage("Opening Sparkin's Utilities menu...")
    CreateMainGump()

if __name__ == "__main__":
    ShowMainMenu()