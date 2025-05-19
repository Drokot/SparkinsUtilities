# Sparkin's Utilities
A collection of gump-driven Python scripts for Razor Enhanced, tailored for the UOAlive shard in Ultima Online.

## Overview
Sparkin's Utilities provides TOS-compliant scripts for automating tasks like pet healing, resource gathering, skill training, and ground resource harvesting on UOAlive. Scripts are accessed via an in-game gump menu, requiring human interaction (e.g., menu selections) to comply with UOAlive's anti-macroing rules.

## Installation
1. Download and install [Razor Enhanced](http://razorenhanced.net/).
2. Configure [ClassicUO](https://www.classicuo.eu/) for UOAlive and point it to Razor Enhanced.
3. Clone this repository or copy the `Scripts` folder to your Razor Enhanced script directory.
4. In Razor Enhanced, set the script folder to `SparkinsUtilities/Scripts`.
5. Add `gump_menu.py` in the Scripts tab and assign a hotkey (e.g., F1).

## Available Scripts
- **gump_menu.py**: Displays a gump menu to select utilities (F1 hotkey).
- **heal_Pets.py**: Heals the weakest or poisoned pet with a selected tool (e.g., bandages).
- **mine_Auto.py**: Mines automatically, moves to new spots, and recalls to bank when pack animal is full.
- **lumber_Auto.py**: Lumberjacks automatically, moves to new trees, and recalls to bank when pack animal is full.
- **sand_Auto.py**: Mines sand automatically, moves to new sand tiles, and recalls to bank when pack animal is full.
- **fish_Auto.py**: Fishes automatically, moves to new water tiles, and recalls to bank when pack animal is full.
- **train_Skills.py**: Trains skills via a Training submenu, including:
  - Hiding, Detect Hidden, Spirit Speak, Meditation, Animal Taming
  - Casting skills: Magery, Spellweaving, Necromancy, Mysticism, Chivalry, Bushido, Ninjitsu
  - Other skills: Stealth, Lockpicking, Resisting Spells, Healing
- **harvest_Resources.py**: Automatically harvests ground resources (feathers, hides, bones, reagents) and cuts corpses, moving to new spots and recalling to bank when pack animal is full.

## Usage
1. Load `gump_menu.py` in Razor Enhanced.
2. Assign a hotkey (e.g., F1) in the Hotkeys tab.
3. Ensure required items (e.g., bandages, pickaxe, hatchet, shovel, fishing pole, dagger, lockpicks) are in your backpack.
4. For casting skills, ensure you have the appropriate spellbook and mana.
5. Press F1 to open the gump menu.
6. Select a utility (e.g., "Training") and choose a skill (e.g., Necromancy) to run the script.

## UOAlive TOS Compliance
- Scripts require human interaction (e.g., gump selections) to avoid bans.
- Resource-gathering macros (e.g., mining, lumberjacking, harvesting) must be monitored to comply with UOAlive's rules against AFK automation.
- Skill training scripts should be used in safe areas (e.g., your house) to avoid unintended interactions.

## Contributing
Feel free to submit pull requests or issues on GitHub. Ensure scripts comply with UOAlive's TOS.

## License
MIT License (see LICENSE file).