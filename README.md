# copr-personal

Specs for [kareylo/personal](https://copr.fedorainfracloud.org/coprs/kareylo/personal/) on COPR.

```bash
sudo dnf copr enable kareylo/personal
```

| Package | Upstream | Spec originally from |
|---|---|---|
| `obsidian` | [obsidianmd/obsidian-releases](https://github.com/obsidianmd/obsidian-releases) | [kritag/copr-cli-tools](https://github.com/kritag/copr-cli-tools) |
| `bibata-cursor-themes` | [ful1e5/Bibata_Cursor](https://github.com/ful1e5/Bibata_Cursor) | [peterwu/copr-rendezvous](https://github.com/peterwu/copr-rendezvous) |
| `claude-desktop-builder` | [dewzor/claude-desktop-fedora](https://github.com/dewzor/claude-desktop-fedora) | upstream, synced as-is |
| `zen-browser` | [zen-browser/desktop](https://github.com/zen-browser/desktop) | written here |

## How it updates

1. `.github/workflows/update.yml` runs nightly and calls `scripts/update.sh` for every package.
2. When upstream has a new version, the spec is bumped and committed.
3. The push fires the COPR webhook, which rebuilds the packages whose directory changed.

COPR builds each package with `.copr/Makefile` (SCM source, `make_srpm` method,
subdirectory `packages/<name>`).

## Adding a package

Create `packages/<name>/` with `<name>.spec` and an `upstream.env`:

```sh
UPDATE_KIND=github-release            # bump Version from the latest GitHub release
UPSTREAM_REPO=owner/repo
UPSTREAM_ASSET_PATTERN='^foo-.*\.tar\.gz$'   # optional: release must ship this asset
```

Then register it on COPR:

```bash
copr-cli add-package-scm kareylo/personal --name <name> \
  --clone-url https://github.com/Kareylo/copr-personal.git \
  --subdir packages/<name> --spec <name>.spec --method make_srpm --webhook-rebuild on
```
