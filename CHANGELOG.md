#  (2026-04-27)

## [0.2.7](https://github.com/stom66/blender-asset-exporter/compare/0.2.6...0.2.7) (2026-04-27)


### Bug Fixes

* correctly use gltf presets, not fbx ([fcfdc9a](https://github.com/stom66/blender-asset-exporter/commit/fcfdc9ae80ab73898b0dff5292b2aa83307ee8a4))


### Features

* improve export preset loading and skip armatures ([5101a5d](https://github.com/stom66/blender-asset-exporter/commit/5101a5d5b7717f32b6fd1bf23935da693b525358))
* report errors from preset loader ([d10d8f1](https://github.com/stom66/blender-asset-exporter/commit/d10d8f1c0e5b39bf497a0df8011ad35f8d0c5982))

## [0.2.6](https://github.com/stom66/blender-asset-exporter/compare/0.2.4...0.2.6) (2025-07-01)


### Features

* add "ignore_root_transforms" to FBX settings, change default colelction rpefix to "_" ([0e73d2c](https://github.com/stom66/blender-asset-exporter/commit/0e73d2c236f010585f160813d1f4fb089700ed6f))
* add suggested extensions for development ([1bb4c3c](https://github.com/stom66/blender-asset-exporter/commit/1bb4c3cb3b1ba313912b69ea4baa8170f3daa617))
* change update_presets to avoid error ([144a72a](https://github.com/stom66/blender-asset-exporter/commit/144a72a14f0e53b919f2f8b1978074f49b469da7))
* version bump ([ad76b5f](https://github.com/stom66/blender-asset-exporter/commit/ad76b5f36b47aeaca166dd3a34402520c028bf9c))

## [0.2.4](https://github.com/stom66/blender-asset-exporter/compare/0.2.3...0.2.4) (2024-09-05)


### Bug Fixes

* properly handle multiline content when reading changelog ([fd6597a](https://github.com/stom66/blender-asset-exporter/commit/fd6597a6d80bf43a191dc46a103a908714cd3a74))
* remove export objects override ([78ee7aa](https://github.com/stom66/blender-asset-exporter/commit/78ee7aac8a503152750ef1f779d6752d5e6ede9a))


### Features

* auto-refresh export presets dropdown ([3c07c44](https://github.com/stom66/blender-asset-exporter/commit/3c07c44c34ec271e3ccbafba1faeb7ccc5e65d7f))

## [0.2.3](https://github.com/stom66/blender-asset-exporter/compare/0.2.2...0.2.3) (2024-08-28)


### Bug Fixes

* fbx split nla tracks now exported after main asset to include non-armatures ([be4a2b3](https://github.com/stom66/blender-asset-exporter/commit/be4a2b3a4dab4a6cbffdcbd1db31c29a14d0ff40))

## [0.2.2](https://github.com/stom66/blender-asset-exporter/compare/0.2.1...0.2.2) (2024-08-27)


### Bug Fixes

* split fbx option now only exports armatures to animation files ([7678773](https://github.com/stom66/blender-asset-exporter/commit/76787735eea507741358ec59a4d3e9745a4d3f1b))

## [0.2.1](https://github.com/stom66/blender-asset-exporter/compare/0.2.0...0.2.1) (2024-08-26)


### Bug Fixes

* update blender manifest ([81e3f9e](https://github.com/stom66/blender-asset-exporter/commit/81e3f9e6d860aa21e6f0390a0d62ea16554d90a5))

# [0.2.0](https://github.com/stom66/blender-asset-exporter/compare/0.1.3...0.2.0) (2024-08-26)


### Features

* add options to remove "Smooth by Angle" modifiers on export ([885cb09](https://github.com/stom66/blender-asset-exporter/commit/885cb094e082a9f435c0c78f3e6bc384e7fa188b))

## [0.1.3](https://github.com/stom66/blender-asset-exporter/compare/0.1.2...0.1.3) (2024-08-25)


### Bug Fixes

* action workflow uses changelog cli ([7e61203](https://github.com/stom66/blender-asset-exporter/commit/7e612036b16369dd041dce8b6a4050db9be9b2c2))
* correct plugin version number in details ([ebe1de2](https://github.com/stom66/blender-asset-exporter/commit/ebe1de2324eb539df05af1eb8b27750f3322cc9d))
* release notes now only show latest changes ([ebd0ae9](https://github.com/stom66/blender-asset-exporter/commit/ebd0ae9db2c494cfae3ce2ad437c2c8bf2b70079))

## [0.1.2](https://github.com/stom66/blender-asset-exporter/compare/0.1.1...0.1.2) (2024-08-23)


### Features

* add self.report error and info messages for export operations ([02dd37b](https://github.com/stom66/blender-asset-exporter/commit/02dd37b1acd724ec51778c504ffa59e355a79131))

## [0.1.1](https://github.com/stom66/blender-asset-exporter/compare/0.1.0...0.1.1) (2024-08-23)


### Features

* add "ignore root transform" option when exporting glTF files ([d1dd372](https://github.com/stom66/blender-asset-exporter/commit/d1dd372d9d56086716dd21cdc78c2fd4c834ded2))

# [0.1.0](https://github.com/stom66/blender-asset-exporter/compare/3edb5afefa51b8e1f3fc5f3c834c226e9eecbee9...0.1.0) (2024-08-22)


### Bug Fixes

* avoid rebase, pull with all history ([8aeceb2](https://github.com/stom66/blender-asset-exporter/commit/8aeceb2142b7a4b34e3fb3ae87acc617ba714b90))
* corect zip folder structure ([fd7053f](https://github.com/stom66/blender-asset-exporter/commit/fd7053f07bace9542ae0b8704256cc49c551634e))
* correct minimum blender version and license ([3edb5af](https://github.com/stom66/blender-asset-exporter/commit/3edb5afefa51b8e1f3fc5f3c834c226e9eecbee9))
* correct write perms ([5444c58](https://github.com/stom66/blender-asset-exporter/commit/5444c58544a0bed41bad8abb76b5c33c58cbc479))
* correct zip folder structure ([2104aad](https://github.com/stom66/blender-asset-exporter/commit/2104aad82375727f7efba9706825f5c9da574164))
* fetch and rebase after committing changelog ([cf08de8](https://github.com/stom66/blender-asset-exporter/commit/cf08de8c015636fc4afcd8cd46756c9a86d5a737))
* skip CHANGELOG commit ([8ee257e](https://github.com/stom66/blender-asset-exporter/commit/8ee257e880cc225e1c344f9738ee395e2da1c5f9))
* specify branch to push to ([1ff42da](https://github.com/stom66/blender-asset-exporter/commit/1ff42da114d1ff4db20ad086b1196928006aae58))
* zip contents moved to folder ([6ce81cd](https://github.com/stom66/blender-asset-exporter/commit/6ce81cd5c6178cb1cd7cd14a153194c9581f67d7))


### Features

* Allows manual trigger from GitHub UI ([98e982b](https://github.com/stom66/blender-asset-exporter/commit/98e982b1843a6830fcdbb43d922f9438f132d880))
* implement automatic changelog ([d16867d](https://github.com/stom66/blender-asset-exporter/commit/d16867ddd896dd1f19cdd216bdb47fe97a3e5a4f))
* new revised create-release workflow ([3ec04e6](https://github.com/stom66/blender-asset-exporter/commit/3ec04e6621328ed4656dbe5bbe3ad2f10a2db38f))
