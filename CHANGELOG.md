270224: (also untested but no actual code change)
- Made CHANGELOG.md show most recent patch first because it makes more sense
- Dates are to be formatted day/month/year instead of whatever backwards order the freedom land prefers

260224: (untested)
- code.py:
	- Changed the polling logic on right stick to more closely match that of the left stick (including ad-hoc (and superfluous) SOCD cleaning)
	- Added a safe button polling function (:86) for keys that *may* not be defined like MOD\_V and MOD\_W
- CHANGELOG made to be a Markdown file for display purposes
- Retroactively dated previous changelog instead of assigning a build version (which is still 0.1a internally; commits will be sorted by date until the first RC)

210224: (tested)
- Implemented changelogs (aka this very file)
- code.py:
	- Added a bunch of comments to make the code easier to follow along
	- Added the basis for two extra modifiers for the C-Stick (not implemented properly)
	- Added toggles for debug mode and forced FGC mode
