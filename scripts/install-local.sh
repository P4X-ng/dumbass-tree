#!/usr/bin/env bash
set -euo pipefail

# Simple installer: symlink tools into ~/.local/bin (no root required).
# Ensure ~/.local/bin is in your PATH.

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST="${HOME}/.local/bin"

mkdir -p "${DEST}"

ln -sf "${ROOT_DIR}/bin/dazfs" "${DEST}/dazfs"
ln -sf "${ROOT_DIR}/bin/dahugepages" "${DEST}/dahugepages"
ln -sf "${ROOT_DIR}/bin/dabtrfs" "${DEST}/dabtrfs"

ln -sf "${ROOT_DIR}/bin/daapparmor" "${DEST}/daapparmor"
ln -sf "${ROOT_DIR}/bin/dabrowse" "${DEST}/dabrowse"

ln -sf "${ROOT_DIR}/bin/dax" "${DEST}/dax"
ln -sf "${ROOT_DIR}/bin/dausbnet" "${DEST}/dausbnet"
ln -sf "${ROOT_DIR}/bin/dathunderbolt" "${DEST}/dathunderbolt"

ln -sf "${ROOT_DIR}/bin/dadns" "${DEST}/dadns"
ln -sf "${ROOT_DIR}/bin/daifupdown" "${DEST}/daifupdown"
ln -sf "${ROOT_DIR}/bin/daip" "${DEST}/daip"
ln -sf "${ROOT_DIR}/bin/datmux" "${DEST}/datmux"
ln -sf "${ROOT_DIR}/bin/dap2p" "${DEST}/dap2p"
ln -sf "${ROOT_DIR}/bin/dadd" "${DEST}/dadd"
ln -sf "${ROOT_DIR}/bin/dasharepage" "${DEST}/dasharepage"
ln -sf "${ROOT_DIR}/bin/darunram" "${DEST}/darunram"

echo "Installed symlinks into: ${DEST}"
echo "Make sure ${DEST} is in your PATH."
