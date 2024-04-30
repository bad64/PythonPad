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
