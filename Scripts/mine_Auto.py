from Scripts.utilities.items import FindItem, CheckItemExists
from Scripts.utilities.helpers import SendMessage, Pause
from Scripts.glossary.colors import colors

def MineAuto(tool_id=0x0E86):
    """
    Automates mining with the specified tool (e.g., pickaxe).
    """
    SendMessage("Starting auto mining...", colors['green'])
    if not CheckItemExists(tool_id, Player.Backpack, "pickaxe"):
        return
    while True:
        tool = FindItem(tool_id, Player.Backpack)
        if not tool:
            SendMessage("No pickaxe found, stopping.", colors['red'])
            return
        Items.UseItem(tool)
        Target.WaitForTarget(10000, False)
        Target.TargetExecute(Player.Position.X, Player.Position.Y, Player.Position.Z)
        Pause(2000)  # Wait for mining action

if __name__ == "__main__":
    MineAuto()