# mas-tools — Macro Automation Studio Claude Code marketplace

Private Claude Code marketplace for Macro Automation Studio tooling. Lets the team
author macros end-to-end — UIBuilder forms, runtime dashboards, and the Python script
that ties them together — just by describing what you want to Claude.

## Plugins

| Plugin | What it does |
| --- | --- |
| `mas-macros` | Generates `.uibproj` (script-runner argument forms), `.uibrt` (runtime dashboards), and the Python script that consumes args and drives the dashboard via the `mas` SDK. |

## Install

This marketplace is hosted in a private GitHub repo. Anyone with read access can install it:

```bash
# In Claude Code:
/plugin marketplace add macroautomationcorp/mas-macros-plugin
/plugin install mas-macros@mas-tools
```

The marketplace clones via the user's existing GitHub credentials (SSH key or `gh auth login`),
so private repo access "just works" as long as the user has been granted access to the repo.

To pull updates after the marketplace owner pushes a new version:

```bash
/plugin marketplace update mas-tools
```

## Usage

Once installed, just talk to Claude in any Claude Code session:

- **"Create a UIBuilder form for my macro with two text inputs and a checkbox"** → invokes
  `generating-args-form`, produces a valid `.uibproj` file.
- **"Make a runtime dashboard with a progress bar and a streaming line chart"** → invokes
  `generating-runtime-dashboard`, produces a valid `.uibrt` file.
- **"Write a macro that opens an app, finds a button, taps it, and reports progress"** →
  invokes `writing-macro-script`, produces a Python script using the `mas` SDK that ties
  args, runtime UI, and device interaction together.

Drop the generated files into your macro's project directory. The UIBuilder validates
arg keys before exporting `ui.xml` and `script_args.py`, so anything Claude misses gets
caught at export time.

## Repository layout

```
mas-macros-plugin/
├── .claude-plugin/
│   └── marketplace.json              # marketplace catalog (name: mas-tools)
└── plugins/
    └── mas-macros/
        ├── .claude-plugin/
        │   └── plugin.json           # plugin manifest
        └── skills/
            ├── generating-args-form/
            │   ├── SKILL.md
            │   ├── references/
            │   └── examples/
            ├── generating-runtime-dashboard/
            │   ├── SKILL.md
            │   ├── references/
            │   └── examples/
            └── writing-macro-script/
                ├── SKILL.md
                ├── references/
                └── examples/
```

Three names worth keeping straight:

- **Repo:** `mas-macros-plugin` — what GitHub knows it as.
- **Marketplace:** `mas-tools` — the catalog defined in `.claude-plugin/marketplace.json`.
- **Plugin:** `mas-macros` — the published entry inside that catalog.

`/plugin install mas-macros@mas-tools` reads as "install the `mas-macros` plugin
from the `mas-tools` marketplace".

## Releasing a new version

The plugin is pinned by the `version` field in `plugins/mas-macros/.claude-plugin/plugin.json`.
Bump it on every release so users actually receive updates when they run
`/plugin marketplace update mas-tools`. Tag the release in git for traceability.

## Adding a new skill

1. Create `plugins/mas-macros/skills/<gerund-name>/SKILL.md`.
2. Add `references/` (one level deep) and `examples/` directories as needed.
3. Bump `plugin.json` `version`.
4. Push.
