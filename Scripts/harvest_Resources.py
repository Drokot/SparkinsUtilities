from Scripts.utilities.items import FindItem, CheckItemExists
from Scripts.utilities.helpers import SendMessage, Pause
from Scripts.glossary.colors import colors

def HarvestResources(tool_id=0x0F52):
    """
    Harvests ground resources (e.g., feathers, hides) with a tool (e.g., dagger).
    """
    SendMessage("Starting resource harvesting...", colors['green'])
    if tool_id and not CheckItemExists(tool_id, Player.Backpack, "dagger"):
        return
    while True:
        corpse_filter = Items.Filter()
        corpse_filter.RangeMax = 2
        corpse_filter.IsCorpse = 1
        corpses = Items.ApplyFilter(corpse_filter)
        if not corpses:
            SendMessage("No corpses found, waiting...", colors['yellow'])
            Pause(2000)
            continue
        corpse = corpses[0]
        if tool_id:
            tool = FindItem(tool_id, Player.Backpack)
            if not tool:
                SendMessage("No dagger found, stopping.", colors['red'])
                return
            Items.UseItem(tool)
            Target.WaitForTarget(10000, False)
            Target.TargetExecute(corpse)
        else:
            Items.UseItem(corpse)  # Direct looting
        Pause(1000)  # Wait for harvesting action

if __name__ == "__main__":
    HarvestResources()