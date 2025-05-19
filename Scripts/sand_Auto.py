from Scripts.utilities.items import FindItem, CheckItemExists
from Scripts.utilities.helpers import SendMessage, Pause
from Scripts.glossary.colors import colors

def SandAuto(tool_id=0x0F39):
    """
    Automates sand mining with the specified tool (e.g., shovel).
    """
    SendMessage("Starting auto sand mining...", colors['green'])
    if not CheckItemExists(tool_id, Player.Backpack, "shovel"):
        return
    while True:
        tool = FindItem(tool_id, Player.Backpack)
        if not tool:
            SendMessage("No shovel found, stopping.", colors['red'])
            return
        Items.UseItem(tool)
        Target.WaitForTarget(10000, False)
        Target.TargetExecute(Player.Position.X, Player.Position.Y, Player.Position.Z)
        Pause(2000)  # Wait for digging action

if __name__ == "__main__":
    SandAuto()