# Dev Notes

## Environment:

Tested under:

* Blender 4.1.1
* Blender 4.2.0 LTS

Developed using the following VSCode Extensions:

* [Blender Development](https://marketplace.visualstudio.com/items?itemName=JacquesLucke.blender-development)
* [Blender Python Code Templates](https://marketplace.visualstudio.com/items?itemName=blenderfreetimeprojects.blender-python-code-templates)
* [Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance)
* [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
* [Python Debugger](https://marketplace.visualstudio.com/items?itemName=ms-python.debugpy)


## Releasing new versions

The GitHub repository is configured with a workflow action to create a release zip upon pushing a new tag.

```sh
# Create and push a tag:
git tag 1.0.0
git push origin 1.0.0`
```

```sh
# Remove a tag:
git --delete tag 1.0.0
git push --delete origin 1.0.0`
```
