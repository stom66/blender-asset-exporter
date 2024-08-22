# Dev Notes

Misc notes for development.

## Releasing new versions

The GitHub repository is configured with a workflow action to create a release zip upon pushing a new tag.

Create and push a tag:

```sh
# Create and push a tag:
git tag 1.0.0
git push origin 1.0.0`
```

Remove a tag:

```sh
# Create and push a tag:
git --delete tag 1.0.0
git push --delete origin 1.0.0`
```
