# Dev Notes

## Environment:

Tested under:

* Blender 4.1.1
* Blender 4.2.0 LTS

Developed using the following VSCode Extensions:

* [Blender Development](https://marketplace.visualstudio.com/items?itemName=JacquesLucke.blender-development)
* [Blender Python Code Templates](https://marketplace.visualstudio.com/items?itemName=blenderfreetimeprojects.blender-python-code-templates)
* [Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.pylance)
* [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
* [Python Debugger](https://marketplace.visualstudio.com/items?itemName=ms-python.debugpy)


## Dev setup

* Install the recommend extensions via `Ctrl+Shift+P` -> `Extensions: Show Recommended Extensions`
* Download Blender portable to somewhere
* In VSCode, `Ctrl+Shift+P` -> `Blender: Start`
* Configure it to start the portable blender we downloaded
* Edit code, changes are handled by the Blender Development extension


## Releasing new versions

The GitHub Actions workflow creates a GitHub Release and zip when you **push a version tag**. It checks out **full git history** (`fetch-depth: 0`), regenerates **`CHANGELOG.md`** from all semver tags (`conventional-changelog` with `-r 0`), attaches that file as the release body and inside the zip.

### Bump version, commit, tag, and push

From the repo root, run `scripts/release_bump.py`. It updates **`blender_manifest.toml`** and **`__init__.py`** (`bl_info["version"]`) together.

Examples:

```sh
# Patch bump (0.2.7 -> 0.2.8): write files only
python scripts/release_bump.py patch

# Minor or major
python scripts/release_bump.py minor
python scripts/release_bump.py major

# Exact version
python scripts/release_bump.py 1.0.0

# Commit, create tag matching the new version, push branch + tag (typical release)
python scripts/release_bump.py patch --commit --tag --push
```

`--tag` requires `--commit` so the tag points at a commit that includes the version bump.

### Changelog preview (local)

Requires [Node.js](https://nodejs.org/) and git tags in your clone:

```sh
npx --yes conventional-changelog-cli -p angular -o CHANGELOG.md -r 0
```

If you have commits on `main` that are **after** the latest tag, you may see a blank “unreleased” section at the top; a tag build on CI only sees the tagged commit, so release zips stay clean.

### Manual tag (if you edited versions yourself)

```sh
git tag 1.0.0
git push origin HEAD
git push origin 1.0.0
```

### Remove a remote tag

```sh
git tag --delete 1.0.0
git push --delete origin 1.0.0
```
