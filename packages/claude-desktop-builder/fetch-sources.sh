#!/usr/bin/env bash
# Build Source0 (claude-desktop-builder-<version>.tar.gz) from dewzor's repo
# at the commit pinned in upstream.env, laid out like upstream's
# copr/make-srpm.sh does it.
set -euo pipefail

spec="$1"
srcdir="$2"
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=/dev/null
. "$here/upstream.env"

name="$(rpmspec -q --srpm --qf '%{name}' "$spec")"
version="$(rpmspec -q --srpm --qf '%{version}' "$spec")"

stage="$(mktemp -d)"
trap 'rm -rf "$stage"' EXIT

curl -fL --retry 3 -o "$stage/upstream.tar.gz" \
    "https://github.com/${UPSTREAM_REPO}/archive/${UPSTREAM_REF}.tar.gz"
mkdir "$stage/src"
tar -xzf "$stage/upstream.tar.gz" -C "$stage/src" --strip-components=1

dest="$stage/$name-$version"
mkdir -p "$dest/copr"
cp "$stage/src/build-official.sh" "$stage/src/README.md" "$stage/src/LICENSE-MIT" "$dest/"
cp "$stage/src/copr/claude-desktop-update" \
   "$stage/src/copr/claude-desktop-update.service" \
   "$stage/src/copr/claude-desktop-update.timer" \
   "$stage/src/copr/claude-desktop-update.1" "$dest/copr/"
chmod 0755 "$dest/build-official.sh" "$dest/copr/claude-desktop-update"

tar -czf "$srcdir/$name-$version.tar.gz" --owner=root --group=root -C "$stage" "$name-$version"
