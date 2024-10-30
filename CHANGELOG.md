1.1.0 (October 30th 2024):
...Yeah it's been a while
- Fixed everything that prevented 1.0.3 from working in the first place
- Expanding on the config:
	- Smash mode is unchanged
	- Versus mode now uses PS-style bindings (e.g. "CIRCLE", "SQUARE", etc) due to having practically no overlap with the Switch syntax 
- Cleaned up the repository to keep it lean (most extras will be redirected elsewhere)

1.0.3 (May 14th 2024):
Intermediary commit (not working)
- Lots of work done towards making button checks asynchronous and safe
- Reworked the config file structure (documentation will be written once I'm done)

1.0 (April 30 2024):

- Initial full release
- CHANGELOG.md (aka this exact file):
	- Wiped the slate clean to conform to the new release scheme
- VERSION:
	- Bumped version to 1.0
	- Future revs will adopt the following release formatting: `<Major revision>.<Minor revision>.<Push number>`
- boot.py:
	- Split report descriptors across different files (legacy and XInput)
- Known issues:
	- As outlined in `README.md`, Tekken 8 currently has an issue differentiating multiple instances of PythonPad
