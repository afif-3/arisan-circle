#!/usr/bin/env bash
# Arisan Circle — deploy to the Gno.land Onyx testnet (Test17, chain id onyx-1)
# and run a smoke-test circle.
#
# Prerequisite: the deployer key "tavernbuilder"
# (g1ulwmlzxtx922c7r8asp6ux23ks8rw6r8m2uftg) must hold test GNOT from
# https://faucet.gno.land (select the Onyx testnet). ~1 GNOT is plenty:
# the package is ~9 KB and the storage deposit is ~100 ugnot/byte.
set -euo pipefail

export PATH="$PATH:$HOME/.gno/bin"
: "${GNOROOT:=$HOME/.gno/src}"
export GNOROOT
: "${GNOHOME:=$HOME/workspace/gnome-tavern/.gnokey-home}"
export GNOHOME

RPC="https://rpc.onyx.testnets.gno.land:443"
CHAIN="onyx-1"
KEY="tavernbuilder"
cd "$(dirname "$0")/../realm"
PKG_PATH="$(grep '^module' gnomod.toml | awk '{print $2}')"

echo "Deploying $PKG_PATH to $CHAIN via $RPC"
gnokey maketx addpkg \
  -pkgdir . -pkgpath "$PKG_PATH" \
  -gas-fee 1000000ugnot -gas-wanted 20000000 -max-deposit 5000000ugnot \
  -chainid "$CHAIN" -remote "$RPC" \
  "$KEY"

echo
echo "Deployed. Browse it at:"
echo "  https://latest.testnets.gno.land/r/${PKG_PATH#gno.land/r/}"
echo
echo "Smoke test (needs a second funded key named member2 in the same keybase):"
echo "  gnokey maketx call -pkgpath $PKG_PATH -func CreateCircle -args DemoCircle -args 100000 -args 2 -gas-fee 10000ugnot -gas-wanted 5000000 -chainid $CHAIN -remote $RPC $KEY"
