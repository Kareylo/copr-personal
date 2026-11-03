#!/usr/bin/env bash
# Usage: scripts/update.sh <package>
#
# Checks packages/<package>/upstream.env against upstream and rewrites the
# package dir when a new version is out. Prints the new version on stdout if
# something changed, nothing otherwise. Needs curl, jq and GH_TOKEN (or an
# unauthenticated GitHub API quota).
set -euo pipefail

pkg="${1:?usage: $0 <package>}"
root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
dir="$root/packages/$pkg"
spec="$dir/$pkg.spec"
env="$dir/upstream.env"
# shellcheck source=/dev/null
. "$env"

gh_api() {
    curl -fsSL -H "Accept: application/vnd.github+json" \
        ${GH_TOKEN:+-H "Authorization: Bearer $GH_TOKEN"} \
        "https://api.github.com/$1"
}

spec_field() { sed -n "s/^$1:[[:space:]]*//p" "$2" | head -1; }

current="$(spec_field Version "$spec")"

case "$UPDATE_KIND" in
github-release)
    # Newest non-draft, non-prerelease release carrying the asset we need.
    latest="$(gh_api "repos/$UPSTREAM_REPO/releases?per_page=30" | jq -r \
        --arg pat "${UPSTREAM_ASSET_PATTERN:-.}" '
        [.[] | select(.draft | not) | select(.prerelease | not)
             | select(any(.assets[]; .name | test($pat)))][0].tag_name // empty')"
    [ -n "$latest" ] || { echo "$pkg: no usable release found" >&2; exit 1; }
    latest="${latest#v}"
    [ "$latest" = "$current" ] && exit 0
    # Only move forward.
    [ "$(printf '%s\n%s\n' "$current" "$latest" | sort -V | tail -1)" = "$latest" ] || exit 0

    sed -i -E "s/^(Version:[[:space:]]*).*/\1$latest/; s/^(Release:[[:space:]]*)[0-9]+/\11/" "$spec"
    entry="* $(LC_ALL=C date -u '+%a %b %d %Y') ${PACKAGER:-copr-personal bot <noreply@github.com>} - $latest-1
- Update to $latest
"
    awk -v e="$entry" '{print} /^%changelog/ {print e}' "$spec" > "$spec.new" && mv "$spec.new" "$spec"
    echo "$latest"
    ;;
spec-sync)
    sha="$(gh_api "repos/$UPSTREAM_REPO/commits/$UPSTREAM_BRANCH" | jq -r .sha)"
    [ "$sha" = "$UPSTREAM_REF" ] && exit 0
    tmp="$(mktemp)"
    trap 'rm -f "$tmp"' EXIT
    curl -fsSL "https://raw.githubusercontent.com/$UPSTREAM_REPO/$sha/$UPSTREAM_SPEC" -o "$tmp"
    latest="$(spec_field Version "$tmp")-$(spec_field Release "$tmp")"
    [ "$latest" = "$current-$(spec_field Release "$spec")" ] && exit 0
    # Upstream bumped the spec: take it as-is and pin that commit.
    cp "$tmp" "$spec"
    sed -i "s/^UPSTREAM_REF=.*/UPSTREAM_REF=$sha/" "$env"
    echo "${latest%%-*}"
    ;;
*)
    echo "$pkg: unknown UPDATE_KIND '$UPDATE_KIND'" >&2
    exit 1
    ;;
esac
