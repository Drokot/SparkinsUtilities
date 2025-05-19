from Scripts.utilities.items import FindItem, CheckItemExists
from Scripts.utilities.helpers import SendMessage, Pause
from Scripts.glossary.colors import colors

def LumberAuto(tool_id=0x0F43):
    """
    Automates lumberjacking with the specified tool (e.g., hatchet).
    """
    SendMessage("Starting auto lumberjacking...", colors['green'])
    if not CheckItemExists(tool_id, Player.Backpack, "hatchet"):
        return
    while True:
        tool = FindItem(tool_id, Player.Backpack)
        if not tool:
            SendMessage("No hatchet found, stopping.", colors['red'])
            return
        Items.UseItem(tool)
        Target.WaitForTarget(10000, False)
        # Target a nearby tree (simplified, assumes player targets manually)
        Target.TargetExecute(Player.Position.X + 1, Player.Position.Y + 1, Player.Position.Z)
        Pause(2000)  # Wait for chopping action

if __name__ == "__main__":
    LumberAuto()