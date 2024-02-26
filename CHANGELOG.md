210224:
- Implemented changelogs (aka this very file)
- code.py:
	- Added a bunch of comments to make the code easier to follow along
	- Added the basis for two extra modifiers for the C-Stick (not implemented properly)
	- Added toggles for debug mode and forced FGC mode

260224:
- code.py:
	- Changed the polling logic on right stick to more closely match that of the left stick (including ad-hoc (and superfluous) SOCD cleaning)
	- Added a safe button polling function (:86) for keys that *may* not be defined like MOD_V and MOD_W
- CHANGELOG made to be a Markdown file for display purposes
- Retroactively dated previous changelog instead of assigning a build version (which is still 0.1a internally; commits will be sorted by date until the first RC)
