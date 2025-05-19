from Scripts.utilities.items import FindItem, CheckItemExists
from Scripts.utilities.helpers import SendMessage, Pause
from Scripts.glossary.colors import colors

def FishAuto(tool_id=0x0DC0):
    """
    Automates fishing with the specified tool (e.g., fishing pole).
    """
    SendMessage("Starting auto fishing...", colors['green'])
    if not CheckItemExists(tool_id, Player.Backpack, "fishing pole"):
        return
    while True:
        tool = FindItem(tool_id, Player.Backpack)
        if not tool:
            SendMessage("No fishing pole found, stopping.", colors['red'])
            return
        Items.UseItem(tool)
        Target.WaitForTarget(10000, False)
        # Target a nearby water tile (simplified)
        Target.TargetExecute(Player.Position.X + 2, Player.Position.Y + 2, Player.Position.Z)
        Pause(2000)  # Wait for fishing action

if __name__ == "__main__":
    FishAuto()