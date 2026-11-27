#!/usr/bin/env bash
# Arisan Circle — local end-to-end demo.
#
# Starts a throwaway gnodev chain with the realm deployed, creates two demo
# accounts, then runs a complete two-member circle with real coin movement:
# create -> join -> start -> contribute x2 (pot pays out) -> round 2 -> finished.
# Finally it shows an ephemeral `maketx run` script being REJECTED when it tries
# to call the realm from code instead of as a direct user call.
#
# Requirements: gno toolchain v1.8.0+ on PATH (or in ~/.gno/bin) and GNOROOT set
# to a gno source checkout. Demo keys are created in a temp GNOHOME; their
# passphrase is "demo-pass" (local throwaway accounts only).
set -euo pipefail

export PATH="$PATH:$HOME/.gno/bin"
: "${GNOROOT:=$HOME/.gno/src}"
export GNOROOT
export GNOHOME="$(mktemp -d)/gnokey-home"
PASS="demo-pass"
RPC="http://localhost:26657"
WEB="http://localhost:8888"

cd "$(dirname "$0")/../realm"
PKG_PATH="$(grep '^module' gnomod.toml | awk '{print $2}')"
echo "Realm: $PKG_PATH"

addkey() { printf '%s\n%s\n' "$PASS" "$PASS" | script -qec "gnokey add $1" /dev/null >/dev/null 2>&1; }
addr_of() { gnokey list | grep "^[0-9]*\. $1 " | sed -E 's/.*addr: (g1[a-z0-9]+).*/\1/'; }
call() { # key func args... [send]
  local key="$1" func="$2"; shift 2
  printf '%s\n' "$PASS" | script -qec "gnokey maketx call -pkgpath $PKG_PATH -func $func $* -gas-fee 10000ugnot -gas-wanted 5000000 -chainid dev -remote $RPC $key" /dev/null 2>&1 | grep -E 'OK!|Error|panic' | head -2
}

addkey creator; addkey member2
CREATOR="$(addr_of creator)"; MEMBER2="$(addr_of member2)"
echo "creator: $CREATOR"
echo "member2: $MEMBER2"

gnodev . > /tmp/arisan-gnodev.log 2>&1 &
DEVNET_PID=$!
trap 'kill $DEVNET_PID 2>/dev/null || true' EXIT
for i in $(seq 1 30); do curl -s "$RPC/status" >/dev/null && break; sleep 1; done

echo "== CreateCircle(KeluargaBesar, 100000, 2) ==";  call creator CreateCircle "-args KeluargaBesar -args 100000 -args 2"
echo "== JoinCircle(0) ==";                          call member2 JoinCircle "-args 0"
echo "== StartCircle(0) ==";                         call creator StartCircle "-args 0"
echo "== Round 1: Contribute creator ==";            call creator Contribute "-args 0 -send 100000ugnot"
echo "== Round 1: Contribute member2 (payout!) ==";  call member2 Contribute "-args 0 -send 100000ugnot"
echo "== Round 2: Contribute creator ==";            call creator Contribute "-args 0 -send 100000ugnot"
echo "== Round 2: Contribute member2 (payout!) ==";  call member2 Contribute "-args 0 -send 100000ugnot"

echo "== Final state (Render circle/0) =="
gnokey query vm/qrender -data "$PKG_PATH:circle/0" -remote "$RPC" | sed 's/^data: "//; s/"$//; s/\\n/\n/g'

cat > /tmp/arisan-attack.gno <<EOF
package main

import "$PKG_PATH"

func main(cur realm) {
	arisan.CreateCircle(cross(cur), "Attack Circle", 100000, 2)
}
EOF
echo "== Bypass attempt: maketx run script calling CreateCircle =="
printf '%s\n' "$PASS" | script -qec "gnokey maketx run -gas-fee 10000ugnot -gas-wanted 5000000 -chainid dev -remote $RPC creator /tmp/arisan-attack.gno" /dev/null 2>&1 | grep -o 'must be called directly by a user account' | head -1 \
  && echo "REJECTED as designed." || echo "!! unexpected: script call was not rejected"

echo "Demo complete. gnoweb was at $WEB/r/${PKG_PATH#gno.land/r/} while the devnet ran."
