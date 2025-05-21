from System import Int32, Byte
from System.Collections.Generic import List
from math import sqrt

# Razor Enhanced APIs
import Items
import Mobiles
import Target
import Journal
import Gumps
import Misc
import Player
import PathFinding
import Statics
import Timer

# Configuration
CONFIG = {
    "blue_beetle_serial": 0x043D5FC2,  # Update with your blue beetle's serial
    "fire_beetle_serial": 0x0007950C,  # Update with your fire beetle's serial
    "max_weight": 1600,  # Beetle weight limit (stones)
    "scan_radius": 4,  # Tile scan radius
    "move_timeout": 10000,  # Pathfinding timeout (ms)
    "logs_to_boards": True,  # Convert logs to boards
    "tree_cooldown": 1200000,  # 20 minutes for tree depletion
    "lumberjacking_safety_alert": False,  # Toggle safety checks
    "drag_delay": 800,  # Delay for item movement
    "use_mount": False,  # Toggle mount usage
    "use_pet_storage": True,  # Toggle beetle storage
    "tool_ids": {
        "pickaxe": [0x0E85, 0x0E86, 0x0F39],  # Standard pickaxes
        "axe": [0x0F49, 0x13FB, 0x0F47, 0x1443, 0x0F45, 0x0F4B, 0x0F43],
        "fishing_pole": [0x0DC0]
    },
    "resource_ids": {
        "ore": [0x19B7, 0x19B8, 0x19B9, 0x19BA],
        "granite": [0x1779],
        "sand": [0x11EA],
        "logs": [0x1BDD, 0x1BDE],
        "boards": [0x1BD7, 0x1BD8],
        "fish": [0x09CC, 0x09CD],
        "other_wood": [0x318F, 0x3199, 0x2F5F, 0x3190, 0x3191]
    },
    "mineable_tiles": [
        0x053B, 0x053C, 0x053D, 0x053E, 0x053F,  # Cave floors
        0x0220, 0x0221, 0x0222, 0x0223, 0x0224   # Mountainsides
    ],
    "tree_tiles": [
        0x0C95, 0x0C96, 0x0C99, 0x0C9B, 0x0C9C, 0x0C9D, 0x0C8A, 0x0CA6,
        0x0CA8, 0x0CAA, 0x0CAB, 0x0CC3, 0x0CC4, 0x0CC8, 0x0CC9, 0x0CCA,
        0x0CCB, 0x0CCC, 0x0CCD, 0x0CD0, 0x0CD3, 0x0CD6, 0x0CD8, 0x0CDA,
        0x0CDD, 0x0CE0, 0x0CE3, 0x0CE6, 0x0CF8, 0x0CFB, 0x0CFE, 0x0D01,
        0x0D25, 0x0D27, 0x0D35, 0x0D37, 0x0D38, 0x0D42, 0x0D43, 0x0D59,
        0x0D70, 0x0D85, 0x0D94, 0x0D96, 0x0D98, 0x0D9A, 0x0D9C, 0x0D9E,
        0x0DA0, 0x0DA2, 0x0DA4, 0x0DA8
    ],
    "water_tiles": list(range(0x00A8, 0x00AC)),
    "lockpick_id": 0x14FB,
    "bandage_id": 0x0E21,
    "lockbox_ids": [0x0E7C, 0x0E7D, 0x09AB],
    "colors": {
        "red": 0x0020,
        "cyan": 0x00B7,
        "green": 1152
    }
}

# Adjust tree IDs for UOAlive
if Misc.ShardName() == 'UoAlive':
    tree_ids_to_remove = [0x0C99, 0x0C9B, 0x0C9C, 0x0C9D, 0x0CA6, 0x0CC4]
    CONFIG["tree_tiles"] = [tid for tid in CONFIG["tree_tiles"] if tid not in tree_ids_to_remove]

# Utility Classes
class Tree:
    def __init__(self, x, y, z, id):
        self.x = x
        self.y = y
        self.z = z
        self.id = id

# Utility Functions
def SendMessage(message, color=CONFIG["colors"]["cyan"]):
    try:
        Player.HeadMessage(color, message)
        Misc.SendMessage(message, color)
        with open("sparkins_log.txt", "a") as f:
            f.write(f"{message}\n")
    except Exception as e:
        with open("sparkins_log.txt", "a") as f:
            f.write(f"SendMessage error: {str(e)}\n")

def Pause(milliseconds):
    Misc.Pause(milliseconds)

def CheckItemExists(item_ids, container, item_name="item"):
    item_ids = item_ids if isinstance(item_ids, list) else [item_ids]
    for item_id in item_ids:
        item = Items.FindByID(item_id, -1, container.Serial)
        if item:
            return item
    SendMessage(f"No {item_name} found in backpack!", CONFIG["colors"]["red"])
    return None

def MoveToSpot(x, y, z, timeout=CONFIG["move_timeout"]):
    try:
        px = Player.Position.X
        py = Player.Position.Y
        if abs(px - x) <= 1 and abs(py - y) <= 1:
            return True
    except Exception as e:
        SendMessage(f"MoveToSpot Player.Position error: {str(e)}", CONFIG["colors"]["red"])
        return False
    offsets = [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
    for dx, dy in offsets:
        target_x, target_y = x + dx, y + dy
        route = PathFinding.Route()
        route.MaxRetry = 5
        route.StopIfStuck = False
        route.X = target_x
        route.Y = target_y
        if PathFinding.Go(route):
            Pause(timeout)
            try:
                if abs(Player.Position.X - x) <= 1 and abs(Player.Position.Y - y) <= 1:
                    SendMessage(f"Moved to ({target_x}, {target_y}) near ({x}, {y}, {z})")
                    return True
            except Exception as e:
                SendMessage(f"MoveToSpot Player.Position check error: {str(e)}", CONFIG["colors"]["red"])
                return False
    SendMessage(f"Failed to move to ({x}, {y}, {z}) or any adjacent spot!", CONFIG["colors"]["red"])
    return False

def TransferResources(resource_ids, destination_serial, min_count=10):
    destination = Mobiles.FindBySerial(destination_serial)
    if not destination:
        SendMessage("Destination beetle not found!", CONFIG["colors"]["red"])
        return False
    for item_id in resource_ids:
        item = Items.FindByID(item_id, -1, Player.Backpack.Serial)
        while item and item.Amount >= min_count:
            SendMessage(f"Moving stack of {item.Name} ({item.Amount}) to beetle")
            Items.Move(item.Serial, destination_serial, item.Amount)
            Pause(CONFIG["drag_delay"])
            prev_item = Items.FindBySerial(item.Serial)
            if not prev_item or prev_item.RootContainer != Player.Backpack.Serial:
                SendMessage(f"Moved {item.Amount} {item.Name} to beetle")
                break
            amount_before = item.Amount
            Items.Move(item.Serial, destination_serial, 1)
            Pause(CONFIG["drag_delay"])
            item = Items.FindBySerial(item.Serial)
            amount_after = item.Amount if item and item.RootContainer == Player.Backpack.Serial else 0
            while amount_after != amount_before and item:
                SendMessage(f"Moving 1 {item.Name} (remaining: {amount_after})")
                amount_before = amount_after
                Items.Move(item.Serial, destination_serial, 1)
                Pause(CONFIG["drag_delay"])
                item = Items.FindBySerial(item.Serial)
                amount_after = item.Amount if item and item.RootContainer == Player.Backpack.Serial else 0
            try:
                if Player.Weight <= Player.MaxWeight:
                    SendMessage("Moved enough to beetle to move normally", CONFIG["colors"]["green"])
                    return True
            except Exception as e:
                SendMessage(f"TransferResources Player.Weight error: {str(e)}", CONFIG["colors"]["red"])
                return False
            SendMessage("Beetle is overweight!", CONFIG["colors"]["red"])
            return False
    return True

def SmeltOres():
    try:
        fire_beetle = Mobiles.FindBySerial(CONFIG["fire_beetle_serial"])
        if not fire_beetle:
            SendMessage("Fire beetle not found!", CONFIG["colors"]["red"])
            return False
        try:
            if abs(Player.Position.X - fire_beetle.Position.X) > 2 or abs(Player.Position.Y - fire_beetle.Position.Y) > 2:
                SendMessage("Moving closer to fire beetle...")
                MoveToSpot(fire_beetle.Position.X, fire_beetle.Position.Y, fire_beetle.Position.Z)
        except Exception as e:
            SendMessage(f"SmeltOres Player.Position error: {str(e)}", CONFIG["colors"]["red"])
            return False
        for ore_id in CONFIG["resource_ids"]["ore"]:
            ore = Items.FindByID(ore_id, -1, Player.Backpack.Serial)
            if ore and ore.Amount >= 10:
                Items.UseItem(ore)
                Target.WaitForTarget(5000, False)
                Target.TargetExecute(fire_beetle)
                Pause(2000)
                SendMessage(f"Smelted {ore.Amount} ore")
        TransferResources([0x1BF2], CONFIG["blue_beetle_serial"], 5)  # Ingots
        return True
    except Exception as e:
        SendMessage(f"SmeltOres error: {str(e)}", CONFIG["colors"]["red"])
        return False

def PromptTarget(message="Select a target..."):
    SendMessage(message)
    Target.PromptTarget()
    Pause(10000)
    target = Target.GetLast()
    if not target:
        SendMessage("No target selected!", CONFIG["colors"]["red"])
        return None
    try:
        if isinstance(target, int):
            SendMessage(f"Target is integer serial: {hex(target)}")
            # Try to resolve as Mobile or Item
            mobile = Mobiles.FindBySerial(target)
            if mobile:
                SendMessage(f"Resolved as mobile: Serial {hex(mobile.Serial)}, Position {mobile.Position.X},{mobile.Position.Y},{mobile.Position.Z}")
                return mobile
            item = Items.FindBySerial(target)
            if item:
                SendMessage(f"Resolved as item: Serial {hex(item.Serial)}, Position {item.Position.X},{item.Position.Y},{item.Position.Z}")
                return item
            SendMessage(f"Could not resolve integer serial {hex(target)}, treating as tile")
            # Assume tile targeting, prompt for coordinates
            return {"Serial": target, "Position": None}
        else:
            SendMessage(f"Target selected: Serial {hex(target.Serial)}, Position {target.Position.X},{target.Position.Y},{target.Position.Z}")
            return target
    except Exception as e:
        SendMessage(f"PromptTarget error: {str(e)}", CONFIG["colors"]["red"])
        return None

def FindLockbox(radius=2):
    lockbox_filter = Items.Filter()
    lockbox_filter.RangeMax = radius
    lockbox_filter.Graphics = List[Int32](CONFIG["lockbox_ids"])
    lockboxes = Items.ApplyFilter(lockbox_filter)
    return lockboxes[0] if lockboxes else None

def SetMiningContext(tool):
    gump_id = 987660
    SendMessage("Please set pickaxe context menu to 'ore and gems' (or 'ore and stone' for GM mining)")
    try:
        gd = Gumps.CreateGump(movable=True, closable=False)
        Gumps.AddPage(gd, 0)
        Gumps.AddBackground(gd, 0, 0, 300, 120, 9260)
        Gumps.AddLabel(gd, 30, 20, 1153, "Set Pickaxe Context")
        Gumps.AddLabel(gd, 50, 50, CONFIG["colors"]["cyan"], "Set to 'ore and gems' or 'ore and stone'?")
        Gumps.AddButton(gd, 100, 80, 4011, 4012, 1, 1, 0)
        Gumps.AddLabel(gd, 130, 80, 1152, "Done")
        Gumps.SendGump(gump_id, Player.Serial, 150, 150, gd.gumpDefinition, gd.gumpStrings)
        Gumps.WaitForGump(gump_id, 30000)
        Gumps.CloseGump(gump_id)
        SendMessage("Context menu set, proceeding with mining...")
    except Exception as e:
        SendMessage(f"SetMiningContext error: {str(e)}", CONFIG["colors"]["red"])

def CheckLOS(x, y, z):
    try:
        route = PathFinding.Route()
        route.X = x
        route.Y = y
        route.MaxRetry = 1
        route.StopIfStuck = True
        result = PathFinding.CanSee(route)
        return result
    except:
        return False

def Mount():
    if CONFIG["use_mount"]:
        Pause(1000)
        try:
            mount_serial = Misc.ReadSharedValue("mount")
            if mount_serial:
                mount = Mobiles.FindBySerial(mount_serial)
                if mount:
                    Mobiles.UseMobile(mount)
                    SendMessage("Remounted")
        except Exception as e:
            SendMessage(f"Mount error: {str(e)}", CONFIG["colors"]["red"])

def DebugTileScan():
    SendMessage("Scanning UOAlive ground tiles for debugging...")
    tile_ids = set()
    try:
        px = Player.Position.X
        py = Player.Position.Y
    except Exception as e:
        SendMessage(f"DebugTileScan Player.Position error: {str(e)}", CONFIG["colors"]["red"])
        return
    for x in range(px - CONFIG["scan_radius"], px + CONFIG["scan_radius"]):
        for y in range(py - CONFIG["scan_radius"], py + CONFIG["scan_radius"]):
            try:
                statics = Statics.GetStaticsTileInfo(x, y, Player.Map)
                for tile in statics:
                    tile_ids.add(tile.StaticID)
                    SendMessage(f"Ground tile at ({x}, {y}, {tile.StaticZ}): ID {hex(tile.StaticID)}")
            except Exception as e:
                SendMessage(f"Error scanning tile at ({x}, {y}): {str(e)}", CONFIG["colors"]["red"])
    with open("sparkins_log.txt", "a") as f:
        f.write(f"Unique UOAlive ground tile IDs: {[hex(tid) for tid in sorted(tile_ids)]}\n")
    SendMessage(f"Found {len(tile_ids)} unique ground tile IDs. Check sparkins_log.txt.")

# Resource Gathering Functions
def GatherMining():
    SendMessage("Starting UOAlive Mining...")
    try:
        SendMessage(f"Current map: {Player.Map}")
        tool = CheckItemExists(CONFIG["tool_ids"]["pickaxe"], Player.Backpack, "pickaxe")
        if not tool:
            SendMessage("No pickaxe found, exiting mining.", CONFIG["colors"]["red"])
            return
        SendMessage(f"Pickaxe: Serial {hex(tool.Serial)}, ID {hex(tool.ItemID)}, Uses {tool.UsesRemaining if hasattr(tool, 'UsesRemaining') else 'Unknown'}")
        SetMiningContext(tool)

        # Initial manual mining test
        SendMessage("Please manually select a mineable tile to test mining...")
        target = PromptTarget("Select a mineable tile (e.g., cave floor or mountainside)...")
        if not target:
            SendMessage("No valid target selected, exiting mining.", CONFIG["colors"]["red"])
            return
        try:
            x = target.Position.X
            y = target.Position.Y
            z = target.Position.Z
            SendMessage(f"Testing manual mining at ({x}, {y}, {z})")
        except AttributeError:
            SendMessage("Target has no Position attribute, assuming tile serial", CONFIG["colors"]["red"])
            # Prompt for manual coordinates
            SendMessage("Please manually select the tile again to confirm position...")
            target = PromptTarget("Re-select the mineable tile...")
            if not target:
                SendMessage("No valid target selected, exiting mining.", CONFIG["colors"]["red"])
                return
            try:
                x = target.Position.X
                y = target.Position.Y
                z = target.Position.Z
                SendMessage(f"Retrying manual mining at ({x}, {y}, {z})")
            except AttributeError:
                SendMessage("Target still invalid, exiting mining.", CONFIG["colors"]["red"])
                return

        # Manual mining test
        Journal.Clear()
        Misc.Resync()
        Items.UseItem(tool)
        if Target.WaitForTarget(4000, False):
            Target.TargetExecute(x, y, z)
            Pause(4000)
            journal_messages = Journal.GetTextByType('System') + Journal.GetTextByType('Regular')
            for msg in journal_messages:
                SendMessage(f"Manual Journal: {msg}", CONFIG["colors"]["red"])
            if any(msg in m for m in journal_messages for msg in [
                "You dig some", "You loosen some rocks", "You put", "You mine some"
            ]):
                SendMessage("Manual mining successful! Using this tile for auto-mining...")
            else:
                SendMessage("Manual mining failed. Check journal messages, context menu, and skill level.", CONFIG["colors"]["red"])
                return
        else:
            SendMessage("Manual target not prompted, check pickaxe and client focus.", CONFIG["colors"]["red"])
            return

        # Auto-mining loop
        SendMessage(f"Auto-mining at manually selected tile ({x}, {y}, {z})")
        retries = 5
        while retries > 0:
            if not MoveToSpot(x, y, z):
                SendMessage(f"Failed to move to ({x}, {y}, {z}), exiting mining.", CONFIG["colors"]["red"])
                break
            tool = CheckItemExists(CONFIG["tool_ids"]["pickaxe"], Player.Backpack, "pickaxe")
            if not tool:
                SendMessage("No valid pickaxe found, exiting mining.", CONFIG["colors"]["red"])
                break
            Journal.Clear()
            SendMessage(f"Using pickaxe {hex(tool.Serial)} (Retry {6 - retries}/5)")
            Misc.Resync()
            Items.UseItem(tool)
            if Target.WaitForTarget(4000, False):
                try:
                    Target.TargetExecuteRelative(Player.Serial, 1)
                except Exception as e:
                    SendMessage(f"TargetExecuteRelative Player.Serial error: {str(e)}", CONFIG["colors"]["red"])
                    retries -= 1
                    continue
                Pause(4000)
                journal_messages = Journal.GetTextByType('System') + Journal.GetTextByType('Regular')
                for msg in journal_messages:
                    SendMessage(f"Journal: {msg}", CONFIG["colors"]["red"])
                if any(msg in m for m in journal_messages for msg in [
                    "You dig some", "You loosen some rocks", "You put", "You mine some"
                ]):
                    SendMessage("Mining successful, processing resources...")
                    SmeltOres()
                    TransferResources(CONFIG["resource_ids"]["ore"], CONFIG["blue_beetle_serial"], 5)
                    TransferResources(CONFIG["resource_ids"]["granite"], CONFIG["blue_beetle_serial"], 5)
                    TransferResources(CONFIG["resource_ids"]["sand"], CONFIG["blue_beetle_serial"], 5)
                    retries = 5  # Reset retries on success
                elif any(msg in m for m in journal_messages for msg in [
                    "There is no metal here to mine", "no sand here", "no ore here", "cannot mine that",
                    "can\'t mine there", "Target cannot be seen", "too far away", "must wait to perform",
                    "You can\'t use this here"
                ]):
                    SendMessage(f"Invalid tile at ({x}, {y}, {z}), prompting new manual selection...", CONFIG["colors"]["red"])
                    target = PromptTarget("Select a new mineable tile...")
                    if target:
                        try:
                            x = target.Position.X
                            y = target.Position.Y
                            z = target.Position.Z
                            SendMessage(f"Switching to new tile ({x}, {y}, {z})")
                            retries = 5
                        except AttributeError:
                            SendMessage("New target has no Position, exiting mining.", CONFIG["colors"]["red"])
                            break
                    else:
                        SendMessage("No new tile selected, exiting mining.", CONFIG["colors"]["red"])
                        break
                else:
                    SendMessage(f"No clear journal response, retrying...")
                    retries -= 1
            else:
                SendMessage(f"Target not prompted for pickaxe {hex(tool.Serial)}, retrying...", CONFIG["colors"]["red"])
                retries -= 1
            try:
                if Player.Weight > Player.MaxWeight - 50:
                    SendMessage("Weight limit reached, transferring resources...")
                    SmeltOres()
                    TransferResources(CONFIG["resource_ids"]["ore"], CONFIG["blue_beetle_serial"], 5)
                    TransferResources(CONFIG["resource_ids"]["granite"], CONFIG["blue_beetle_serial"], 5)
                    TransferResources(CONFIG["resource_ids"]["sand"], CONFIG["blue_beetle_serial"], 5)
            except Exception as e:
                SendMessage(f"Weight check Player.Weight error: {str(e)}", CONFIG["colors"]["red"])
                break
            Journal.Clear()
            Pause(100)
    except Exception as e:
        SendMessage(f"GatherMining error: {str(e)}", CONFIG["colors"]["red"])

def GatherLumberjacking():
    SendMessage("Starting Lumberjacking...")
    trees = []
    block_count = 0

    def equip_axe():
        try:
            left_hand = Player.GetItemOnLayer('LeftHand')
            if left_hand and left_hand.ItemID in CONFIG["tool_ids"]["axe"]:
                SendMessage("Axe already equipped.")
                return True
        except Exception as e:
            SendMessage(f"equip_axe Player.GetItemOnLayer error: {str(e)}", CONFIG["colors"]["red"])
            return False
        for item in Player.Backpack.Contains:
            if item.ItemID in CONFIG["tool_ids"]["axe"]:
                try:
                    Player.EquipItem(item.Serial)
                    Pause(600)
                    SendMessage(f"Equipped axe: {item.Name}.")
                    return True
                except Exception as e:
                    SendMessage(f"equip_axe Player.EquipItem error: {str(e)}", CONFIG["colors"]["red"])
                    return False
        SendMessage("No axe found to equip! Stopping lumberjacking.", CONFIG["colors"]["red"])
        return False

    def get_number_in_beetle(resource_id):
        beetle_mobile = Mobiles.FindBySerial(CONFIG["blue_beetle_serial"])
        if not beetle_mobile:
            return 0
        number = 0
        for item in beetle_mobile.Backpack.Contains:
            if item.ItemID == resource_id:
                number += item.Amount
        return number

    def move_to_beetle():
        if CONFIG["logs_to_boards"]:
            for item in Player.Backpack.Contains:
                if item.ItemID == CONFIG["resource_ids"]["logs"][0]:
                    axe = Player.GetItemOnLayer('LeftHand')
                    if axe:
                        Items.UseItem(axe)
                        Target.WaitForTarget(1500, False)
                        Target.TargetExecute(item)
                        Pause(CONFIG["drag_delay"])

        beetle_mobile = Mobiles.FindBySerial(CONFIG["blue_beetle_serial"])
        if not beetle_mobile:
            SendMessage("Beetle not found!", CONFIG["colors"]["red"])
            return False

        resource_id = CONFIG["resource_ids"]["boards"][0] if CONFIG["logs_to_boards"] else CONFIG["resource_ids"]["logs"][0]
        for item in Player.Backpack.Contains:
            if item.ItemID == resource_id:
                number_in_beetle = get_number_in_beetle(resource_id)
                if number_in_beetle + item.Amount < CONFIG["max_weight"]:
                    Items.Move(item.Serial, beetle_mobile.Serial, 0)
                    Pause(CONFIG["drag_delay"])
                else:
                    SendMessage("Beetle full, stopping!", CONFIG["colors"]["red"])
                    return False

        ground_items = Items.Filter()
        ground_items.Movable = True
        ground_items.RangeMax = 2
        ground_items.Graphics = List[Int32]([resource_id])
        items = Items.ApplyFilter(ground_items)
        for item in items:
            number_in_beetle = get_number_in_beetle(resource_id)
            if number_in_beetle + item.Amount < CONFIG["max_weight"]:
                Items.Move(item.Serial, beetle_mobile.Serial, 0)
                Pause(CONFIG["drag_delay"])
            else:
                SendMessage("Beetle full, stopping!", CONFIG["colors"]["red"])
                return False

        return True

    def scan_trees():
        trees.clear()
        SendMessage("Scanning for trees...")
        try:
            min_x = Player.Position.X - CONFIG["scan_radius"]
            max_x = Player.Position.X + CONFIG["scan_radius"]
            min_y = Player.Position.Y - CONFIG["scan_radius"]
            max_y = Player.Position.Y + CONFIG["scan_radius"]
        except Exception as e:
            SendMessage(f"scan_trees Player.Position error: {str(e)}", CONFIG["colors"]["red"])
            return
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                statics = Statics.GetStaticsTileInfo(x, y, Player.Map)
                for tile in statics:
                    if tile.StaticID in CONFIG["tree_tiles"] and not Timer.Check(f"{x},{y}"):
                        trees.append(Tree(x, y, tile.StaticZ, tile.StaticID))
        trees.sort(key=lambda tree: sqrt((tree.x - Player.Position.X) ** 2 + (tree.y - Player.Position.Y) ** 2))
        SendMessage(f"Found {len(trees)} trees.")

    def range_tree(tree):
        try:
            px, py = Player.Position.X, Player.Position.Y
        except Exception as e:
            SendMessage(f"range_tree Player.Position error: {str(e)}", CONFIG["colors"]["red"])
            return False
        tx, ty = tree.x, tree.y
        return (tx >= px - 1 and tx <= px + 1) and (ty >= py - 1 and ty <= py + 1)

    def move_to_tree(tree):
        SendMessage(f"Moving to tree at ({tree.x}, {tree.y})")
        Misc.Resync()
        offsets = [(0, 1), (1, 0), (-1, 0), (0, -1)]
        for dx, dy in offsets:
            if MoveToSpot(tree.x + dx, tree.y + dy, tree.z):
                Misc.Pause(1000)
                if range_tree(tree):
                    SendMessage(f"Reached tree at ({tree.x}, {tree.y})")
                    return True
        SendMessage(f"Failed to reach tree at ({tree.x}, {tree.y})", CONFIG["colors"]["red"])
        return False

    def cut_tree(tree):
        nonlocal block_count
        if not equip_axe():
            return False
        if Target.HasTarget():
            SendMessage("Canceling existing target!", CONFIG["colors"]["red"])
            Target.Cancel()
            Pause(500)
        try:
            if Player.Weight >= Player.MaxWeight - 10:
                if not move_to_beetle():
                    return False
        except Exception as e:
            SendMessage(f"cut_tree Player.Weight error: {str(e)}", CONFIG["colors"]["red"])
            return False
        Journal.Clear()
        try:
            axe = Player.GetItemOnLayer('LeftHand')
            if not axe:
                SendMessage("No axe equipped after equip attempt! Stopping.", CONFIG["colors"]["red"])
                return False
        except Exception as e:
            SendMessage(f"cut_tree Player.GetItemOnLayer error: {str(e)}", CONFIG["colors"]["red"])
            return False
        Items.UseItem(axe)
        Target.WaitForTarget(2000, True)
        Target.TargetExecute(tree.x, tree.y, tree.z, tree.id)
        Timer.Create('chopTimer', 10000)
        while not (Journal.SearchByType('You hack at the tree for a while, but fail to produce any useable wood.', 'System') or
                   Journal.SearchByType('You chop some', 'System') or
                   Journal.SearchByType('There\'s not enough wood here to harvest.', 'System') or
                   not Timer.Check('chopTimer')):
            Pause(100)
        if Journal.SearchByType('There\'s not enough wood here to harvest.', 'System'):
            SendMessage("Tree depleted, marking cooldown.")
            Timer.Create(f"{tree.x},{tree.y}", CONFIG["tree_cooldown"])
            return True
        elif Journal.Search('That is too far away'):
            block_count += 1
            Journal.Clear()
            if block_count > 3:
                block_count = 0
                SendMessage("Possible block detected, marking tree cooldown.", CONFIG["colors"]["red"])
                Timer.Create(f"{tree.x},{tree.y}", CONFIG["tree_cooldown"])
                return True
            return cut_tree(tree)
        elif Journal.Search('bloodwood'):
            SendMessage("Bloodwood harvested!", 1194)
            Timer.Create('chopTimer', 10000)
            return cut_tree(tree)
        elif Journal.Search('heartwood'):
            SendMessage("Heartwood harvested!", 1193)
            Timer.Create('chopTimer', 10000)
            return cut_tree(tree)
        elif Journal.Search('frostwood'):
            SendMessage("Frostwood harvested!", 1151)
            Timer.Create('chopTimer', 10000)
            return cut_tree(tree)
        elif not Timer.Check('chopTimer'):
            SendMessage("Tree timeout, marking cooldown.")
            Timer.Create(f"{tree.x},{tree.y}", CONFIG["tree_cooldown"])
            return True
        return cut_tree(tree)

    def safety_net():
        if not CONFIG["lumberjacking_safety_alert"]:
            return
        toon_filter = Mobiles.Filter()
        toon_filter.Enabled = True
        toon_filter.IsHuman = True
        toon_filter.Friend = False
        toon_filter.Notorieties = List[Byte](bytes([1, 2, 3, 4, 5, 6, 7]))
        invul_filter = Mobiles.Filter()
        invul_filter.Enabled = True
        invul_filter.Friend = False
        invul_filter.Notorieties = List[Byte](bytes([7]))
        toons = Mobiles.ApplyFilter(toon_filter)
        invuls = Mobiles.ApplyFilter(invul_filter)
        if toons:
            toon = Mobiles.Select(toons, 'Nearest')
            SendMessage(f"Toon near: {toon.Name}", CONFIG["colors"]["red"])
        if invuls:
            invul = Mobiles.Select(invuls, 'Nearest')
            SendMessage(f"ALERT: Invulnerable mobile: {invul.Name}", CONFIG["colors"]["red"])

    if not equip_axe():
        return
    while True:
        scan_trees()
        if not trees:
            SendMessage("No trees found in range! Move closer to trees.", CONFIG["colors"]["red"])
            break
        while trees:
            safety_net()
            if move_to_tree(trees[0]):
                if not cut_tree(trees[0]):
                    break
            trees.pop(0)
        Pause(100)

def GatherFishing():
    SendMessage("Starting Fishing...")
    try:
        tool = CheckItemExists(CONFIG["tool_ids"]["fishing_pole"], Player.Backpack, "fishing_pole")
        if not tool:
            SendMessage("No fishing pole found, exiting fishing.", CONFIG["colors"]["red"])
            return
        water_spots = []
        try:
            px = Player.Position.X
            py = Player.Position.Y
        except Exception as e:
            SendMessage(f"GatherFishing Player.Position error: {str(e)}", CONFIG["colors"]["red"])
            return
        for x in range(px - CONFIG["scan_radius"], px + CONFIG["scan_radius"]):
            for y in range(py - CONFIG["scan_radius"], py + CONFIG["scan_radius"]):
                try:
                    statics = Statics.GetStaticsTileInfo(x, y, Player.Map)
                    for tile in statics:
                        if tile.StaticID in CONFIG["water_tiles"]:
                            z = Player.Position.Z
                            water_spots.append((x, y, z))
                            SendMessage(f"Found water tile {hex(tile.StaticID)} at ({x}, {y}, {z})")
                except Exception as e:
                    SendMessage(f"Error scanning tile at ({x}, {y}): {str(e)}", CONFIG["colors"]["red"])
                    continue
        if not water_spots:
            SendMessage("No water tiles found in range!", CONFIG["colors"]["red"])
            return
        SendMessage(f"Found {len(water_spots)} water spots.")
        while water_spots:
            spot = water_spots[0]
            if MoveToSpot(spot[0], spot[1], spot[2]):
                Items.UseItem(tool)
                Target.WaitForTarget(5000, False)
                Target.TargetExecute(spot[0], spot[1], spot[2])
                Pause(2000)
                journal_messages = Journal.GetTextByType('System')
                if journal_messages:
                    SendMessage(f"Journal: {journal_messages[-1]}", CONFIG["colors"]["red"])
                if Journal.Search("no fish"):
                    SendMessage("No fish here, moving to next...")
                    water_spots.pop(0)
                TransferResources(CONFIG["resource_ids"]["fish"], CONFIG["blue_beetle_serial"])
            try:
                if Player.Weight > Player.MaxWeight - 50:
                    SendMessage("Weight limit reached, transferring resources...")
                    TransferResources(CONFIG["resource_ids"]["fish"], CONFIG["blue_beetle_serial"])
            except Exception as e:
                SendMessage(f"GatherFishing Player.Weight error: {str(e)}", CONFIG["colors"]["red"])
                break
            Journal.Clear()
            Pause(1000)
    except Exception as e:
        SendMessage(f"GatherFishing error: {str(e)}", CONFIG["colors"]["red"])

# Gump Menu Functions
def ShowMainMenu():
    gump_id = 987654
    SendMessage("Creating main menu gump...")
    try:
        gd = Gumps.CreateGump(movable=True, closable=True)
        Gumps.AddPage(gd, 0)
        Gumps.AddBackground(gd, 0, 0, 350, 150, 9200)
        Gumps.AddLabel(gd, 50, 20, 1152, "Sparkin's Adventurer's Tome")
        Gumps.AddImage(gd, 20, 20, 9000)
        categories = [
            ("Exit", "Close the tome", CONFIG["colors"]["red"]),
            ("Resource Gathering", "Mine, chop, fish", CONFIG["colors"]["cyan"])
        ]
        for i, (cat, tooltip, color) in enumerate(categories):
            x, y = 50, 80 + i * 60
            Gumps.AddButton(gd, x, y, 4005, 4007, i, 1, 0)
            Gumps.AddLabel(gd, x + 30, y, color, cat)
            Gumps.AddTooltip(gd, 1011000 + i, tooltip)
        Gumps.SendGump(gump_id, Player.Serial, 150, 150, gd.gumpDefinition, gd.gumpStrings)
        if Gumps.WaitForGump(gump_id, 5000):
            gump_data = Gumps.GetGumpData(gump_id)
            choice = gump_data.buttonid if gump_data and gump_data.buttonid >= 0 else -1
        else:
            choice = -1
        Gumps.CloseGump(gump_id)
        SendMessage(f"Main menu closed, choice: {choice}")
        return choice
    except Exception as e:
        SendMessage(f"ShowMainMenu error: {str(e)}", CONFIG["colors"]["red"])
        return -1

def ShowConfirmExitMenu():
    gump_id = 987659
    SendMessage("Creating exit confirmation gump...")
    try:
        gd = Gumps.CreateGump(movable=True, closable=True)
        Gumps.AddPage(gd, 0)
        Gumps.AddBackground(gd, 0, 0, 250, 120, 9260)
        Gumps.AddLabel(gd, 30, 20, 1153, "Confirm Exit")
        Gumps.AddLabel(gd, 50, 50, CONFIG["colors"]["red"], "Close Sparkin's Tome?")
        Gumps.AddButton(gd, 50, 80, 4011, 4012, 1, 1, 0)
        Gumps.AddLabel(gd, 80, 80, 1152, "Yes")
        Gumps.AddButton(gd, 130, 80, 4008, 4009, 0, 1, 0)
        Gumps.AddLabel(gd, 160, 80, 1152, "No")
        Gumps.SendGump(gump_id, Player.Serial, 150, 150, gd.gumpDefinition, gd.gumpStrings)
        if Gumps.WaitForGump(gump_id, 5000):
            gump_data = Gumps.GetGumpData(gump_id)
            choice = gump_data.buttonid if gump_data and gump_data.buttonid >= 0 else 0
        else:
            choice = 0
        Gumps.CloseGump(gump_id)
        SendMessage(f"Exit menu closed, choice: {choice}")
        return choice == 1
    except Exception as e:
        SendMessage(f"ShowConfirmExitMenu error: {str(e)}", CONFIG["colors"]["red"])
        return False

def ShowGatheringMenu():
    gump_id = 987655
    SendMessage("Creating gathering menu gump...")
    try:
        gd = Gumps.CreateGump(movable=True, closable=True)
        Gumps.AddPage(gd, 0)
        Gumps.AddBackground(gd, 0, 0, 300, 230, 5120)
        Gumps.AddLabel(gd, 50, 20, CONFIG["colors"]["cyan"], "Resource Gathering")
        options = [
            ("Back", "Return to main tome", 1152),
            ("Mining", "Mine ore and smelt", CONFIG["colors"]["cyan"]),
            ("Lumberjacking", "Chop trees", 0x00B2),
            ("Fishing", "Cast lines", 0x00B9),
            ("Debug Tiles", "Scan ground tile IDs", CONFIG["colors"]["red"])
        ]
        for i, (opt, tooltip, color) in enumerate(options):
            Gumps.AddButton(gd, 50, 60 + i * 30, 4029, 4030, i, 1, 0)
            Gumps.AddLabel(gd, 80, 60 + i * 30, color, opt)
            Gumps.AddTooltip(gd, 1011000 + i, tooltip)
        Gumps.SendGump(gump_id, Player.Serial, 150, 150, gd.gumpDefinition, gd.gumpStrings)
        if Gumps.WaitForGump(gump_id, 5000):
            gump_data = Gumps.GetGumpData(gump_id)
            choice = gump_data.buttonid if gump_data and gump_data.buttonid >= 0 else -1
        else:
            choice = -1
        Gumps.CloseGump(gump_id)
        SendMessage(f"Gathering menu closed, choice: {choice}")
        return choice
    except Exception as e:
        SendMessage(f"ShowGatheringMenu error: {str(e)}", CONFIG["colors"]["red"])
        return -1

def MainMenu():
    SendMessage("Sparkin's Adventurer's Tome opened! Select an adventure.")
    try:
        SendMessage(f"Player info: Name={Player.Name}, Serial={hex(Player.Serial)}, Position={Player.Position.X},{Player.Position.Y},{Player.Position.Z}, Map={Player.Map}")
    except Exception as e:
        SendMessage(f"MainMenu Player info error: {str(e)}", CONFIG["colors"]["red"])
    gump_active = False
    while True:
        if not gump_active:
            SendMessage("Opening main menu...")
            gump_active = True
            try:
                main_choice = ShowMainMenu()
                SendMessage(f"Main menu choice: {main_choice}")
            except Exception as e:
                SendMessage(f"ShowMainMenu error: {str(e)}", CONFIG["colors"]["red"])
                gump_active = False
                break
            gump_active = False
            if main_choice == 0:
                gump_active = True
                try:
                    if ShowConfirmExitMenu():
                        SendMessage("Closing Sparkin's Adventurer's Tome...")
                        break
                except Exception as e:
                    SendMessage(f"ShowConfirmExitMenu error: {str(e)}", CONFIG["colors"]["red"])
                gump_active = False
                continue
            elif main_choice == 1:
                while True:
                    gump_active = True
                    try:
                        gather_choice = ShowGatheringMenu()
                        SendMessage(f"Gathering menu choice: {gather_choice}")
                    except Exception as e:
                        SendMessage(f"ShowGatheringMenu error: {str(e)}", CONFIG["colors"]["red"])
                        gump_active = False
                        break
                    gump_active = False
                    if gather_choice == 0:
                        SendMessage("Returning to main tome...")
                        break
                    elif gather_choice == 1:
                        GatherMining()
                    elif gather_choice == 2:
                        GatherLumberjacking()
                    elif gather_choice == 3:
                        GatherFishing()
                    elif gather_choice == 4:
                        DebugTileScan()
                    Pause(100)
        Pause(100)

# Entry Point
if __name__ == "__main__":
    with open("sparkins_log.txt", "a") as f:
        f.write("Script started\n")
    try:
        SendMessage(f"Player: {Player.Name}, Connected: {Player.IsConnected()}")
    except Exception as e:
        SendMessage(f"Main Player API error: {str(e)}", CONFIG["colors"]["red"])
    SendMessage("Opening Sparkin's Adventurer's Tome...")
    if CONFIG["use_pet_storage"]:
        Misc.SetSharedValue("petForStorage1", CONFIG["blue_beetle_serial"])
    MainMenu()