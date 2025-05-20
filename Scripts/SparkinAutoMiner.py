from AutoComplete import *
from System.Collections.Generic import List
from System import Int32
from math import sqrt
import datetime

### CONFIG ###
def prompt_valid_beetle(prompt_message, hue, max_attempts=3, timeout_ms=10000):
    for attempt in range(max_attempts):
        try:
            serial = Target.PromptTarget(prompt_message, hue)
            if serial == -1:
                log_message(f'Failed to target {prompt_message.lower()}, attempt {attempt + 1}/{max_attempts}')
                Misc.SendMessage(f'Please target a valid {prompt_message.lower()}', 33)
                Misc.Pause(1000)
                continue
            mobile = Mobiles.FindBySerial(serial)
            if not mobile or "beetle" not in mobile.Name.lower():
                log_message(f'Invalid mobile selected for {prompt_message.lower()}, serial: {hex(serial)}')
                Misc.SendMessage(f'Selected mobile is not a beetle. Try again.', 33)
                continue
            return serial
        except Exception as e:
            log_message(f'Error targeting {prompt_message.lower()}: {str(e)}')
            Misc.SendMessage(f'Error targeting {prompt_message.lower()}. Retrying...', 33)
            Misc.Pause(1000)
    log_message(f'Failed to target {prompt_message.lower()} after {max_attempts} attempts')
    Misc.SendMessage(f'Failed to target {prompt_message.lower()}. Script will pause.', 33)
    return -1

# Initialize beetle serials
fire_beetle = -1
blue_beetle = -1
for _ in range(2):
    fire_beetle = prompt_valid_beetle('Target your fire beetle', 43)
    if fire_beetle == -1:
        log_message('Fire beetle targeting failed. Pausing script.')
        Misc.SendMessage('Fire beetle targeting failed. Please restart the script.', 33)
        Misc.Pause(60000)
        continue
    blue_beetle = prompt_valid_beetle('Target your blue beetle', 161)
    if blue_beetle == -1:
        log_message('Blue beetle targeting failed. Pausing script.')
        Misc.SendMessage('Blue beetle targeting failed. Please restart the script.', 33)
        Misc.Pause(60000)
        continue
    if fire_beetle == blue_beetle:
        log_message('Fire and blue beetle serials are identical. Retrying.')
        Misc.SendMessage('Fire and blue beetles cannot be the same. Retry targeting.', 33)
        fire_beetle = blue_beetle = -1
        Misc.Pause(1000)
        continue
    break
else:
    log_message('Failed to target valid beetles after retries. Script halting.')
    Misc.SendMessage('Could not target valid beetles. Script stopped.', 33)
    exit()

tool_kits_to_keep = 2
shovels_to_keep = 5
min_ingots_for_crafting = 10
TINKERING_GUMP = 0x3cd35884

prospect = True
sturdy = False

scan_radius = 8
mining_cooldown = 1800000
beetle_weight_limit = 1600
smelt_weight_threshold = 25
resource_move_threshold = 25
granite_amount_threshold = 25
sand_amount_threshold = 1000
batch_size = 50
search_subcontainers = False
pause_duration = 3500
max_moves_per_cycle = 5
max_stack_weight = 15
smelt_cooldown = 15000
max_attempts = 3
DEBUG = True

GRANITE_TYPES = [0x1779]
ORE_TYPES = [0x19B7, 0x19B8, 0x19B9, 0x19BA]  # Fixed syntax: 0x19B８ → 0x19B8
SAND = 0x19B7
INGOT = 0x1BF2
SHOVEL = 0x0F39
TOOL_KIT = 0x1EB8
PROSPECT_TOOL = 0x0FB4

mining_static_ids = [
    0x053B, 0x053C, 0x053D, 0x053E, 0x053F, 0x0540, 0x0541, 0x0542,
    0x0543, 0x0544, 0x0545, 0x0546, 0x0547, 0x0548, 0x0549, 0x054A,
    0x054B, 0x054C, 0x054D, 0x054E, 0x054F, 0x0550, 0x0551, 0x0552,
    0x0533, 0x0554, 0x0555, 0x0556, 0x0557, 0x0558, 0x0559, 0x055A,
    0x0016, 0x0017, 0x0018, 0x0019, 0x001A, 0x001B, 0x001C, 0x001D,
    0x0010, 0x0011, 0x0012, 0x0013, 0x0014, 0x0015,
    0x00B1, 0x00B2, 0x00B3, 0x00B4
]

class MiningSpot:
    def __init__(self, x, y, z, id):
        self.x = x
        self.y = y
        self.z = z
        self.id = id

mining_spots = []
prospected = False
last_mining_success = False
attempts = 0

def log_message(message):
    if DEBUG:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open('C:/Users/kc7rj/Downloads/Scripts/miner_log.txt', 'a') as f:
            f.write(f'[{timestamp}] {message}\n')

def wait_for_journal(search_strings, timeout_ms=5000):
    start_time = datetime.datetime.now()
    while (datetime.datetime.now() - start_time).total_seconds() * 1000 < timeout_ms:
        journal_lines = Journal.GetTextBySerial(Player.Serial)
        if any(any(s.lower() in line.lower() for s in search_strings) for line in journal_lines):
            return journal_lines
        Misc.Pause(100)
    log_message(f'No expected journal messages within {timeout_ms}ms')
    return []

def get_tool_kits():
    try:
        return Items.FindAllByID(TOOL_KIT, 0, Player.Backpack.Serial, True)
    except:
        log_message('Error getting tool kits')
        return []

def get_shovels():
    try:
        return Items.FindAllByID(SHOVEL, -1 if sturdy else 0, Player.Backpack.Serial, True)
    except:
        log_message('Error getting shovels')
        return []

def gump_check():
    tool_kits = get_tool_kits()
    if not tool_kits:
        log_message('No tool kits found')
        return False
    try:
        Items.UseItem(tool_kits[0])
        Misc.Pause(1000)
        return Gumps.WaitForGump(TINKERING_GUMP, 10000)
    except:
        log_message('Error checking tinker gump')
        return False

def make_tool_kit():
    if not gump_check():
        return False
    Journal.Clear()
    try:
        Gumps.SendAction(TINKERING_GUMP, 23)
        Misc.Pause(8000)
        journal_lines = wait_for_journal(['you create', 'you have created'], 10000)
        success = any('you create' in line.lower() or 'you have created' in line.lower() for line in journal_lines)
        log_message(f'Tool kit creation {"succeeded" if success else "failed"}')
        return success
    except:
        log_message('Error making tool kit')
        return False

def make_shovel():
    if not gump_check():
        return False
    Journal.Clear()
    try:
        Gumps.SendAction(TINKERING_GUMP, 202)
        Misc.Pause(8000)
        journal_lines = wait_for_journal(['you create', 'you have created'], 10000)
        success = any('you create' in line.lower() or 'you have created' in line.lower() for line in journal_lines)
        log_message(f'Shovel creation {"succeeded" if success else "failed"}')
        return success
    except:
        log_message('Error making shovel')
        return False

def make_tools():
    kits = len(get_tool_kits())
    shovels = len(get_shovels())
    ingots = Items.FindByID(INGOT, 0, Player.Backpack.Serial)
    ingot_count = ingots.Amount if ingots else 0
    if ingot_count < min_ingots_for_crafting:
        log_message(f'Not enough ingots for crafting: {ingot_count}/{min_ingots_for_crafting}')
        return False
    while shovels < shovels_to_keep and ingot_count >= 4:
        if make_shovel():
            shovels += 1
            ingot_count -= 4
        else:
            return False
        Misc.Pause(1000)
    while kits < tool_kits_to_keep and ingot_count >= 2:
        if make_tool_kit():
            kits += 1
            ingot_count -= 2
        else:
            return False
        Misc.Pause(1000)
    log_message(f'Crafted tools: {shovels} shovels, {kits} tool kits')
    return True

def get_beetle_weight():
    beetle_mobile = Mobiles.FindBySerial(blue_beetle)
    if not beetle_mobile or not beetle_mobile.Backpack:
        log_message('Blue beetle inaccessible for weight check')
        return 0
    total = 0
    try:
        for item in beetle_mobile.Backpack.Contains:
            if not item or item.Amount <= 0:
                continue
            weight = item.Amount * 0.1
            try:
                props = Items.GetPropValue(item.Serial, "Weight")
                if props is not None:
                    weight = props
                elif item.ItemID == INGOT:
                    weight = item.Amount * 0.1
                elif item.ItemID == 0x1779:
                    weight = item.Amount * 0.5
                elif item.ItemID == SAND:
                    prop_string = Items.GetPropStringByIndex(item.Serial, 0)
                    if prop_string and "sand" in prop_string.lower():
                        weight = item.Amount * 0.1
            except:
                log_message(f'Error getting weight for item ID={hex(item.Serial)}')
                pass
            total += weight
    except:
        log_message('Error calculating beetle weight')
    log_message(f'Beetle weight: {total}/{beetle_weight_limit}')
    return total

def move_all_granite_to_beetle():
    beetle_mobile = Mobiles.FindBySerial(blue_beetle)
    if not beetle_mobile or not beetle_mobile.Backpack:
        log_message('Blue beetle inaccessible for granite move')
        return False
    distance = sqrt((Player.Position.X - beetle_mobile.Position.X)**2 + (Player.Position.Y - beetle_mobile.Position.Y)**2)
    if distance > 12:
        log_message(f'Blue beetle too far: {distance:.1f} tiles')
        return False
    try:
        Misc.Resync()
        granite_items = Items.FindAllByID(0x1779, -1, Player.Backpack.Serial, search_subcontainers)
        log_message(f'Found {len(granite_items)} granite stacks')
        if not granite_items:
            return False
        total_amount = sum(g.Amount for g in granite_items)
        if total_amount <= granite_amount_threshold:
            log_message(f'Granite amount {total_amount} below threshold {granite_amount_threshold}')
            return False
        moved_any = False
        for g in granite_items:
            for _ in range(3):
                try:
                    Misc.Resync()
                    Items.Move(g.Serial, blue_beetle, g.Amount)
                    Misc.Pause(pause_duration)
                    updated_item = Items.FindBySerial(g.Serial)
                    if not updated_item or updated_item.Amount <= g.Amount - g.Amount:
                        moved_any = True
                        log_message(f'Moved {g.Amount} granite to beetle')
                        break
                except:
                    Misc.Pause(500)
                    log_message(f'Retry failed for granite ID={hex(g.Serial)}')
        return moved_any
    except:
        log_message('Error in move_all_granite_to_beetle')
        return False

def move_resources():
    beetle_mobile = Mobiles.FindBySerial(blue_beetle)
    if not beetle_mobile or not beetle_mobile.Backpack:
        log_message('Blue beetle inaccessible for resource move')
        return False
    distance = sqrt((Player.Position.X - beetle_mobile.Position.X)**2 + (Player.Position.Y - beetle_mobile.Position.Y)**2)
    if distance > 12:
        log_message(f'Blue beetle too far: {distance:.1f} tiles')
        return False
    try:
        Misc.Resync()
        total_weight = get_beetle_weight()
        moved_any = False
        ingot_weight_per_unit = 0.1
        sand_weight_per_unit = 0.1
        move_count = 0
        ingots = Items.FindAllByID(INGOT, -1, Player.Backpack.Serial, search_subcontainers)
        sand_items = Items.FindAllByID(SAND, -1, Player.Backpack.Serial, search_subcontainers)
        sand_items = [s for s in sand_items if "sand" in (Items.GetPropStringByIndex(s.Serial, 0) or "").lower()]
        total_sand_amount = sum(s.Amount for s in sand_items)
        log_message(f'Found {len(ingots)} ingot stacks, {len(sand_items)} sand stacks, total sand: {total_sand_amount}')
        for i in ingots:
            if move_count >= max_moves_per_cycle:
                break
            if not i or i.Amount < 1:
                continue
            current_batch = min(batch_size, i.Amount)
            batch_weight = current_batch * ingot_weight_per_unit
            if total_weight + batch_weight > beetle_weight_limit:
                log_message(f'Beetle weight limit reached: {total_weight + batch_weight}/{beetle_weight_limit}')
                return moved_any
            for _ in range(3):
                try:
                    Misc.Resync()
                    Items.Move(i.Serial, blue_beetle, current_batch)
                    Misc.Pause(pause_duration)
                    updated_item = Items.FindBySerial(i.Serial)
                    if not updated_item or updated_item.Amount <= i.Amount - current_batch:
                        total_weight += batch_weight
                        move_count += 1
                        moved_any = True
                        log_message(f'Moved {current_batch} ingots to beetle')
                        break
                except:
                    Misc.Pause(500)
                    log_message(f'Retry failed for ingot ID={hex(i.Serial)}')
        if total_sand_amount > sand_amount_threshold:
            for s in sand_items:
                if move_count >= max_moves_per_cycle:
                    break
                if not s or s.Amount < 1:
                    continue
                current_batch = min(batch_size, s.Amount)
                batch_weight = current_batch * sand_weight_per_unit
                if total_weight + batch_weight > beetle_weight_limit:
                    log_message(f'Beetle weight limit reached: {total_weight + batch_weight}/{beetle_weight_limit}')
                    return moved_any
                for _ in range(3):
                    try:
                        Misc.Resync()
                        Items.Move(s.Serial, blue_beetle, current_batch)
                        Misc.Pause(pause_duration)
                        updated_item = Items.FindBySerial(s.Serial)
                        if not updated_item or updated_item.Amount <= s.Amount - current_batch:
                            total_weight += batch_weight
                            move_count += 1
                            moved_any = True
                            log_message(f'Moved {current_batch} sand to beetle')
                            break
                    except:
                        Misc.Pause(500)
                        log_message(f'Retry failed for sand ID={hex(s.Serial)}')
        return moved_any
    except:
        log_message('Error in move_resources')
        return False

def scan_mining_spots():
    global mining_spots
    mining_spots = []
    min_x = Player.Position.X - scan_radius
    max_x = Player.Position.X + scan_radius
    min_y = Player.Position.Y - scan_radius
    max_y = Player.Position.Y + scan_radius
    step = 1
    try:
        for x in range(min_x, max_x + 1, step):
            for y in range(min_y, max_y + 1, step):
                statics = Statics.GetStaticsTileInfo(x, y, Player.Map)
                if statics:
                    for tile in statics:
                        if tile.StaticID in mining_static_ids and not Timer.Check(f'{x},{y}'):
                            mining_spots.append(MiningSpot(x, y, tile.StaticZ, tile.StaticID))
                else:
                    mining_spots.append(MiningSpot(x, y, Player.Position.Z, 0x0000))
    except:
        log_message('Error scanning mining spots')
    try:
        target = Target.PromptGroundTarget('Target a sand tile', 33)
        if target:
            statics = Statics.GetStaticsTileInfo(target.X, target.Y, Player.Map)
            if statics:
                for tile in statics:
                    if tile.StaticID not in mining_static_ids:
                        mining_static_ids.append(tile.StaticID)
            else:
                mining_spots.append(MiningSpot(target.X, target.Y, Player.Position.Z, 0x0000))
    except:
        log_message('Error targeting sand tile')
    mining_spots.sort(key=lambda spot: sqrt((spot.x - Player.Position.X)**2 + (spot.y - Player.Position.Y)**2))
    log_message(f'Scanned {len(mining_spots)} mining spots')

def move_to_mining_spot():
    global mining_spots, prospected
    if not mining_spots:
        Misc.Pause(5000)
        scan_mining_spots()
        if not mining_spots:
            log_message('No mining spots available')
            return False
    spot = mining_spots[0]
    try:
        Misc.Resync()
        coords = PathFinding.Route()
        coords.MaxRetry = 10
        coords.StopIfStuck = False
        coords.X = spot.x
        coords.Y = spot.y
        path_attempts = [
            (spot.x, spot.y),
            (spot.x, spot.y + 1),
            (spot.x + 1, spot.y),
            (spot.x - 1, spot.y),
            (spot.x, spot.y - 1)
        ]
        for x, y in path_attempts:
            coords.X = x
            coords.Y = y
            if PathFinding.Go(coords):
                Misc.Pause(1500)
                if abs(Player.Position.X - spot.x) <= 1 and abs(Player.Position.Y - spot.y) <= 1:
                    prospected = False
                    log_message(f'Moved to spot ({spot.x}, {spot.y})')
                    return True
                else:
                    log_message(f'Pathfinding desync at ({spot.x}, {spot.y}), retrying')
                    Misc.Pause(1000)
                    break
        log_message(f'Failed to pathfind to spot ({spot.x}, {spot.y})')
        return False
    except:
        log_message('Error in move_to_mining_spot')
        return False

def smelt_ores():
    fire_beetle_mobile = Mobiles.FindBySerial(fire_beetle)
    if not fire_beetle_mobile:
        log_message(f'Fire beetle inaccessible, serial: {hex(fire_beetle)}')
        return False
    distance = sqrt((Player.Position.X - fire_beetle_mobile.Position.X)**2 + (Player.Position.Y - fire_beetle_mobile.Position.Y)**2)
    if distance > 12:
        log_message(f'Fire beetle too far: {distance:.1f} tiles')
        return False
    try:
        Misc.Resync()
        ores = Items.FindAllByID(-1, -1, Player.Backpack.Serial, search_subcontainers)
        ores = [o for o in ores if o.ItemID in ORE_TYPES and o.ItemID != 0x1779 and "sand" not in (Items.GetPropStringByIndex(o.Serial, 0) or "").lower()]
        log_message(f'Found {len(ores)} ore stacks for smelting')
        if not ores:
            return False
        smelted_any = False
        Journal.Clear()
        for ore in ores:
            for _ in range(3):
                try:
                    Misc.Resync()
                    Items.UseItemOnMobile(ore.Serial, fire_beetle)
                    journal_lines = wait_for_journal(['you smelt the ore', 'you burn away impurities'], 5000)
                    if any('you smelt' in line.lower() or 'burn away' in line.lower() for line in journal_lines):
                        log_message(f'Smelted ore ID={hex(ore.ItemID)}, Amount={ore.Amount}')
                        smelted_any = True
                        break
                    Misc.Pause(500)
                except:
                    log_message(f'Retry failed for ore ID={hex(ore.Serial)}')
        Timer.Create('smelt_cooldown', smelt_cooldown)
        return smelted_any
    except:
        log_message('Error in smelt_ores')
        return False

def main():
    global prospected, mining_spots, last_mining_success, attempts, fire_beetle, blue_beetle
    try:
        Journal.Clear()
        if fire_beetle == -1 or blue_beetle == -1:
            log_message(f'Invalid beetle serials: fire={hex(fire_beetle)}, blue={hex(blue_beetle)}. Retargeting.')
            Misc.SendMessage('Invalid beetle serials. Please restart the script to retarget.', 33)
            Misc.Pause(60000)
            return
        while not Player.IsGhost:
            Misc.Resync()
            fire_beetle_mobile = Mobiles.FindBySerial(fire_beetle)
            blue_beetle_mobile = Mobiles.FindBySerial(blue_beetle)
            if not fire_beetle_mobile or not blue_beetle_mobile:
                log_message('Beetles inaccessible, prompting retarget')
                Misc.SendMessage('Beetles not found. Retargeting...', 33)
                fire_beetle = prompt_valid_beetle('Target your fire beetle', 43)
                blue_beetle = prompt_valid_beetle('Target your blue beetle', 161)
                if fire_beetle == -1 or blue_beetle == -1 or fire_beetle == blue_beetle:
                    log_message('Retargeting failed. Pausing script.')
                    Misc.SendMessage('Retargeting failed. Please restart the script.', 33)
                    Misc.Pause(60000)
                    continue
            max_weight = Player.MaxWeight
            smelt_weight = max_weight - smelt_weight_threshold
            resource_weight = max_weight - resource_move_threshold
            hard_weight_limit = max_weight - 10
            log_message(f'Player weight: {Player.Weight}/{max_weight}')
            if Player.Weight >= hard_weight_limit:
                log_message('Weight at hard limit, forcing smelting/movement')
                if not Timer.Check('smelt_cooldown'):
                    smelt_ores()
                move_all_granite_to_beetle()
                move_resources()
                Misc.Pause(1000)
                continue
            elif Player.Weight >= smelt_weight or Player.Weight >= resource_weight:
                log_message('Weight threshold reached')
                if not Timer.Check('smelt_cooldown'):
                    smelt_ores()
                move_all_granite_to_beetle()
                move_resources()
                Misc.Pause(1000)
                continue
            shovels = get_shovels()
            if not shovels:
                log_message('No shovels found')
                make_tools()
                continue
            if len(shovels) < shovels_to_keep:
                make_tools()
            tool = shovels[0]
            if not mining_spots:
                scan_mining_spots()
                if not mining_spots:
                    log_message('No spots after scan')
                    Misc.Pause(3000)
                    continue
            if not move_to_mining_spot():
                mining_spots.pop(0)
                attempts = 0
                log_message('Failed to move to spot, trying next')
                continue
            spot = mining_spots[0]
            resource = 'sand' if spot.id in [0x0016, 0x0017, 0x0018, 0x0019, 0x001A, 0x001B, 0x001C, 0x001D, 0x0010, 0x0011, 0x0012, 0x0013, 0x0014, 0x0015, 0x00B1, 0x00B2, 0x00B3, 0x00B4] or spot.id == 0x0000 else 'ore'
            if prospect and not prospected and resource == 'ore':
                prospect_tool = Items.FindByID(PROSPECT_TOOL, -1, Player.Backpack.Serial)
                if prospect_tool:
                    Items.UseItem(prospect_tool)
                    Target.WaitForTarget(2000)
                    Target.TargetExecute(spot.x, spot.y, spot.z, spot.id)
                    Misc.Pause(500)
                    prospected = True
                    log_message('Prospected spot')
            if tool:
                Journal.Clear()
                last_mining_success = False
                Target.TargetResource(tool, resource)
                Target.TargetExecute(spot.x, spot.y, spot.z, spot.id)
                journal_lines = wait_for_journal(['you put', 'sand in your', 'no sand here', 'no ore here'], 5000)
                if any('you put' in line.lower() or 'sand in your' in line.lower() for line in journal_lines):
                    last_mining_success = True
                    m = next((line for line in journal_lines if 'you put' in line.lower() or 'sand in your' in line.lower()), 'Mining success')
                    Journal.Clear(m)
                    attempts = 0
                    log_message(f'Mined {resource} at ({spot.x}, {spot.y})')
                if any('no sand here' in line.lower() or 'no ore here' in line.lower() for line in journal_lines):
                    Timer.Create(f'{spot.x},{spot.y}', mining_cooldown)
                    mining_spots.pop(0)
                    attempts = 0
                    log_message(f'Spot depleted at ({spot.x}, {spot.y})')
                    continue
                attempts += 1
                if attempts >= max_attempts:
                    Timer.Create(f'{spot.x},{spot.y}', mining_cooldown)
                    mining_spots.pop(0)
                    attempts = 0
                    log_message(f'Max attempts reached, removing spot ({spot.x}, {spot.y})')
                if Player.Weight >= smelt_weight and not Timer.Check('smelt_cooldown'):
                    smelt_ores()
    except Exception as e:
        log_message(f'Main loop error: {str(e)}')

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        log_message(f'Script failed to start: {str(e)}')