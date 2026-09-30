#!/usr/bin/env bash
# Cairo and pango headers for machines that have the libraries but not the -devel packages, and no
# root to install them: typical of a cluster node (RHEL, Rocky, Alma and other dnf-based systems).
#
# manim's two native dependencies (pycairo, manimpango) publish no Linux wheels, so uv compiles
# them, and the compiler needs cairo and pango headers, .pc files and the unversioned .so links.
# This unpacks the -devel RPMs into .native/ and rewrites them to point there, leaving the system
# untouched. At run time the libraries still resolve through ld.so against the system's
# /usr/lib64, so nothing needs LD_LIBRARY_PATH afterwards.
#
# scripts/setup.sh calls this when pkg-config cannot find cairo. Needs dnf, rpm2cpio and cpio.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PREFIX="$HERE/.native"
RPMS="$PREFIX/.rpms"

PKGS=(
  cairo-devel pango-devel glib2-devel fribidi-devel harfbuzz-devel
  pixman-devel fontconfig-devel freetype-devel libpng-devel graphite2-devel
  libxcb-devel libX11-devel libXext-devel libXrender-devel libXft-devel
  expat-devel zlib-devel libuuid-devel libxml2-devel
)

rm -rf "$PREFIX"
mkdir -p "$RPMS"
dnf download --arch "$(uname -m)" --destdir "$RPMS" "${PKGS[@]}"

for rpm in "$RPMS"/*.rpm; do
  ( cd "$PREFIX" && rpm2cpio "$rpm" | cpio -idmu --quiet )
done

# The .pc files hardcode /usr/include and /usr/lib64 rather than deriving them from ${prefix}, so
# pkg-config's own relocation cannot move them, and would double-prefix what is rewritten here:
# hence PKG_CONFIG_DONT_DEFINE_PREFIX wherever this prefix is used.
sed -i -E \
  -e "s|^(prefix\|exec_prefix)=/usr$|\\1=$PREFIX/usr|" \
  -e "s|(=\|-I\|-L)/usr/(include\|lib64)|\\1$PREFIX/usr/\\2|g" \
  "$PREFIX"/usr/lib64/pkgconfig/*.pc

# The .so links the -devel packages ship are relative to a lib64 that holds the real libraries;
# this one does not, so point them at the system copies.
for link in "$PREFIX"/usr/lib64/*.so; do
  [ -L "$link" ] || continue
  target="$(readlink "$link")"
  [ -e "$link" ] || ln -sf "/usr/lib64/$(basename "$target")" "$link"
done

rm -rf "$RPMS"
echo "native prefix ready: $PREFIX"
PKG_CONFIG_DONT_DEFINE_PREFIX=1 PKG_CONFIG_PATH="$PREFIX/usr/lib64/pkgconfig" \
  pkg-config --modversion cairo pangocairo
