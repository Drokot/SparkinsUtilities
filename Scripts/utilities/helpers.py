from Scripts.glossary.colors import colors

def SendMessage(message, color=colors['cyan']):
    """
    Send a message to the player with a specified color.
    """
    Player.HeadMessage(color, message)

def Pause(milliseconds):
    """
    Pause script execution for the specified time.
    """
    Misc.Pause(milliseconds)

def MoveToTile(x, y, z, max_attempts=10):
    """
    Move to the specified tile using pathfinding.
    Returns True if successful, False if blocked.
    """
    for _ in range(max_attempts):
        if Player.Position.X == x and Player.Position.Y == y:
            return True
        Player.PathFindTo(x, y, z)
        Pause(1000)  # Wait for movement
        if Player.Position.X == x and Player.Position.Y == y:
            return True
    SendMessage("Cannot reach tile ({}, {})!".format(x, y), colors['red'])
    return False

def RecallToRunebook(runebook_serial, rune_index):
    """
    Recall to a specific rune in a runebook.
    Returns True if successful, False otherwise.
    """
    Items.UseItem(runebook_serial)
    Pause(500)
    if Gumps.HasGump():
        Gumps.SendAction(Gumps.CurrentGump(), 5 + rune_index * 6)  # Recall action
        Pause(3000)  # Wait for recall
        if Player.Position != Misc.ReadSharedValue("last_position"):
            SendMessage("Recalled successfully!", colors['green'])
            Misc.SetSharedValue("last_position", Player.Position)
            return True
    SendMessage("Failed to recall!", colors['red'])
    return False

def UseSkill(skill_name, timeout=10000):
    """
    Use the specified skill and wait for the server response.
    Returns True if successful, False if failed (e.g., on cooldown).
    """
    Player.UseSkill(skill_name)
    Pause(timeout)
    if Journal.Search("You must wait")