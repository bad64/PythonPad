290324: (tested)
- GamepadDriver.py:
	- Renamed to gamepad\_driver.py for Pythonic complicance
	- Added new class methods: `set_socd_type()`, `get_socd_type()`, `lock_socd()`, `unlock_socd()`
	- Added SOCD parameters to the class (see above)
- config.json:
	- No actual changes, but `code.py` now checks for valid inputs for the `defaultMode` and `socdType` properties
- versus.py:
	- Last Input Wins SOCD cleaning now works
	- Incidentally this means Versus Mode is now feature complete !
- smash.py:
	- Last Input Wins SOCD cleaning now works
	- Smash Mode is now feature complete as well !
- VERSION:
	- Bumped up to 0.9 RC, want to test further and iron out some kinks before 1.0

260324: (tested)
- Separated the directional input routines in their own files for readability's sake
- config:
	- New property: `socdType` (accepts "LRN" or "last")
	- Config files are currently **NOT** up to date
- GamepadDriver:
	- Added getters for the current controller state

190324: (no testing needed)  
Only documentative changes  
- VERSION bumped to 0.2 as I'm feeling close(r) to an RC
- README changes
	- Relocated some sections of the main README over to the one in the `config` folder
	- Updated contents in general to reflect changes I missed in the previous update
- Structure changes
	- `config` subfolders now use their board names for extra clarity

180324: (tested)
- VERSION file is no longer required (the firmware will skip it if not found/corrupted/etc)
- Default boot mode can now be specified under the "general" section as `defaultMode`
- Silenced debug-only errors when attempting to assign a modifier value to a Button as an input (it's expected behaviour)

110324: (untested)
- Added ESP32-S3-WROOM-1-N8R2 (henceforth known as "One Board") support
- Moved the config files to per-mcu subdirectories
- Rewrote some parts of the README to reflect new and upcoming changes

270224: (tested)
- Testing on the Adafruit Feather ESP32-S3
- Made CHANGELOG.md show most recent patch first because it makes more sense
- Dates are to be formatted day/month/year instead of whatever backwards order the freedom land prefers
- code.py:
	- Added clearer error defs in a couple cases
	- Added board specific defines to deal with non-general general purpose input output naming conventions (just one define so far though)
	- Renamed function `safetest()` to just `test()` for upcoming refactoring

260224: (untested)
- code.py:
	- Changed the polling logic on right stick to more closely match that of the left stick (including ad-hoc (and superfluous) SOCD cleaning)
	- Added a safe button polling function for keys that *may* not be defined like MOD\_V and MOD\_W
- CHANGELOG made to be a Markdown file for display purposes
- Retroactively dated previous changelog instead of assigning a build version (which is still 0.1a internally; commits will be sorted by date until the first RC)

210224: (tested)
- Implemented changelogs (aka this very file)
- code.py:
	- Added a bunch of comments to make the code easier to follow along
	- Added the basis for two extra modifiers for the C-Stick (not implemented properly)
	- Added toggles for debug mode and forced FGC mode
