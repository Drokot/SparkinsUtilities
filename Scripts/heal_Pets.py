from Scripts.utilities.items import FindItem, CheckItemExists
from Scripts.utilities.helpers import SendMessage, Pause
from Scripts.glossary.colors import colors

def HealPet(tool_id=0x0E21):
    """
    Heals the weakest or poisoned pet with the specified tool (e.g., bandages).
    """
    SendMessage("Starting pet healing...", colors['green'])
    if not CheckItemExists(tool_id, Player.Backpack, "bandages"):
        return
    while True:
        tool = FindItem(tool_id, Player.Backpack)
        if not tool:
            SendMessage("No bandages found, stopping.", colors['red'])
            return
        pet_filter = Mobiles.Filter()
        pet_filter.RangeMax = 2
        pet_filter.IsHuman = 0
        pet_filter.IsGhost = 0
        pets = Mobiles.ApplyFilter(pet_filter)
        if not pets:
            SendMessage("No pets found, waiting...", colors['yellow'])
            Pause(2000)
            continue
        # Select the pet with lowest health or poisoned
        weakest_pet = min(pets, key=lambda p: p.Hits if not p.Poisoned else -1)
        Items.UseItem(tool)
        Target.WaitForTarget(10000, False)
        Target.TargetExecute(weakest_pet)
        Pause(2000)  # Wait for healing action

if __name__ == "__main__":
    HealPet()