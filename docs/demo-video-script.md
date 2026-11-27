# Demo video script — Arisan Circle (target: ~2 minutes)

The DoraHacks submission requires a demo video. Easiest path: **phone screen
recording** of the live testnet realm in the browser (gnoweb) + the Adena wallet
app for the transactions. Record in landscape or portrait — either is fine.
Speak or stay silent; on-screen text below says what to show, in order.

Prerequisite (one-time, ~1 minute): claim test GNOT for the project address
`g1ulwmlzxtx922c7r8asp6ux23ks8rw6r8m2uftg` at https://faucet.gno.land
(select **Onyx**), and import the project key into Adena (the key file/mnemonic
is held by the agent — ask for the import step when ready). Deployment happens
right after the faucet claim lands.

## Shot list

**0:00–0:15 — The problem (voice or caption)**
"Arisan is how millions of Indonesians save together: everyone chips in each
round, one person takes the pot, rotating until all have received. Today it runs
on trust and group chats. Arisan Circle puts the whole rotation on-chain."

**0:15–0:35 — The realm home page**
Open https://latest.testnets.gno.land/r/g1ulwmlzxtx922c7r8asp6ux23ks8rw6r8m2uftg/arisan
Scroll the circle list. Tap into the demo circle's page: show members in payout
order, contribution amount, pot size.

**0:35–1:10 — A live round**
In Adena (or via the gnoweb "execute" helper), call `Contribute` on the demo
circle with exactly 0.1 GNOT attached, from the last unpaid member. Approve the
transaction. Back in the browser, refresh the circle page: the payout history now
shows the round paid to the recipient — automatically, no one pressed "pay".

**1:10–1:30 — Balances**
Show the recipient's balance before/after in Adena (or on an explorer):
+0.2 GNOT pot received.

**1:30–1:50 — The safety property (optional but strong)**
Show the README "Security notes": contributions are checked to the exact coin,
and a contract/script cannot call the realm in a user's name — only direct user
calls are accepted.

**1:50–2:00 — Close**
"Complete lifecycle, no fees, no custodian. Code and tests are public —
link in the description."

## Fallback if testnet recording is inconvenient

Record the terminal instead: run `bash demo/demo.sh` (local devnet) and screen
record the full lifecycle plus the rejected bypass attempt, narrating the same
points. The on-chain behavior shown is identical; state in the video description
that the same realm is deployed on Onyx (link included).
