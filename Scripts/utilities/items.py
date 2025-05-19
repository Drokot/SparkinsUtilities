from Scripts.glossary.colors import colors
from Scripts.utilities.helpers import SendMessage

def FindItem(item_id, container, timeout=1000):
    """
    Find an item by ID in the specified container.
    Returns the item object or None if not found.
    """
    Items.FindByID(item_id, -1, container.Serial, timeout)
    item = Items.FindByID(item_id, -1, container.Serial)
    if not item:
        SendMessage(f"Item {hex(item_id)} not found in container!", colors['red'])
        return None
    return item

def CheckItemExists(item_id, container, item_name="item"):
    """
    Check if an item exists in the container.
    Returns True if found, False otherwise.
    """
    item = FindItem(item_id, container)
    if not item:
        SendMessage(f"No {item_name} found in backpack!", colors['red'])
        return False
    return True

def FindLockbox(radius=2):
    """
    Find a lockbox within the specified radius.
    Returns the lockbox object or None if not found.
    """
    lockbox_ids = [0x0E7C, 0x0E7D, 0x09AB]  # Common lockbox IDs
    lockbox_filter = Items.Filter()
    lockbox_filter.RangeMax = radius
    lockbox_filter.Graphics = List[Int32](lockbox_ids)
    lockboxes = Items.ApplyFilter(lockbox_filter)
    return lockboxes[0] if lockboxes else None