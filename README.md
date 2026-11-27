# Arisan Circle

A rotating savings club (ROSCA) realm on **Gno.land**, inspired by the Indonesian
*arisan*: a group of members each contributes a fixed amount every round, and each
round one member receives the whole pot — rotating in join order until everyone has
received it exactly once. No fees, no custodian, no admin key: the realm holds a
round's contributions only until the round completes, then pays out automatically.

Built for the **Gnome Tavern Hackathon** (DoraHacks).

## Why arisan, why Gno

An arisan is a piece of social infrastructure: a savings club that works because
everyone knows everyone — and breaks the moment one organizer disappears with the
pot or one member stops paying after their early turn. The failure modes are
exactly the ones a deterministic on-chain rotation removes: the contribution is
fixed, the order is fixed, the payout is automatic, and the history can never be
rewritten.

Gno fits this unusually well. The realm *is* the whole application — state, rules
and even the web pages (via `Render`) live in one audited piece of code, with no
separate backend, database or admin server to trust or to shut down. Gno's
permission model also gives the key safety property for a money club for free:
a realm can require that every action comes from a direct user call, so nobody's
wallet can be moved by an intermediary contract or script acting in their name.

## Deployment — Onyx testnet

- Testnet: **Onyx / Test17** (`onyx-1`), RPC `https://rpc.onyx.testnets.gno.land:443`
- Realm: `gno.land/r/g1ulwmlzxtx922c7r8asp6ux23ks8rw6r8m2uftg/arisan`
- Browse: <https://latest.testnets.gno.land/r/g1ulwmlzxtx922c7r8asp6ux23ks8rw6r8m2uftg/arisan>
- Status (Nov 27, 2026): deployment scripted and ready (`demo/deploy-onyx.sh`);
  it runs the moment the deployer address is funded from the Onyx faucet (a
  captcha-gated claim). The end-to-end lifecycle below is verified on a local
  devnet with the identical realm code.

## How it works

| Step | Call | Who |
| --- | --- | --- |
| 1. Open a circle | `CreateCircle(name, contributionUgnot, maxMembers)` | anyone (becomes creator + first member) |
| 2. Join | `JoinCircle(id)` | anyone, while the circle is open and not full (2–12 members) |
| 3. Start | `StartCircle(id)` | creator, once ≥ 2 members joined |
| 4. Contribute | `Contribute(id)` with **exactly** the contribution attached (`-send`) | each member, once per round |
| 5. Payout | automatic | when the last member contributes, the pot is sent to the round's recipient |
| — | `CancelCircle(id)` | creator, only before the circle starts |

Rounds = number of members. The recipient of round *n* is the *n*-th member in join
order. After the final round the circle is `finished` and its full payout history
stays readable on-chain forever.

### What the realm renders (gnoweb)

Home page lists every circle with status, contribution and member count. Each
circle has a detail page (`circle/<id>`) with members in payout order, who already
paid this round, who receives next, and the payout history. Actual output of
`Render("circle/0")` after a complete two-member circle (local devnet run of
`demo/demo.sh`, Nov 27, 2026 — full transcript in `video/demo-transcript.txt`):

```
# KeluargaBesar

- Status: **finished**
- Creator: `g1gmxsclc5g3u7s64yzaw232m9eeden50prh9mdp`
- Contribution: 0.1 GNOT (100000 ugnot) per member, per round
- Pot per round: 0.2 GNOT

## Members (in payout order)

1. `g1gmxsclc5g3u7s64yzaw232m9eeden50prh9mdp`
2. `g15zvsnvsdnh99ft9h2cr7zuplcqk53c6fk88nnp`

## Payout history

- Round 1: `g1gmxsclc5g3u7s64yzaw232m9eeden50prh9mdp`
- Round 2: `g15zvsnvsdnh99ft9h2cr7zuplcqk53c6fk88nnp`
```

A 2-minute demo video assembled from that same real run (terminal session +
rendered circle page + the rejected bypass attempt) is in
[`video/arisan-circle-demo.mp4`](video/arisan-circle-demo.mp4); it can be
regenerated with `video/build_video.py`.

## Security notes

- **Direct user calls only.** Every state-changing function resolves its caller via
  the realm-frame guard recommended in the Gno security guide
  (`cur.Previous().IsUserCall()`), so an intermediary contract — or an ephemeral
  `gnokey maketx run` script — cannot act in a user's name. Verified live: a run
  script calling `CreateCircle` is rejected with
  `arisan: must be called directly by a user account` (see `demo/demo.sh`).
- **Exact payment check.** `Contribute` compares the coins actually attached to the
  call (`unsafe.OriginSend()`) against the circle's contribution: underpaying,
  overpaying, or paying in another denomination is rejected, so the pot is always
  exactly `contribution × members`.
- **No privileged roles.** The creator can only start or cancel (pre-start) their
  own circle. Nobody — including the creator — can move funds outside the automatic
  payout rule, and payouts only ever go to members, in join order.
- **Render safety.** Circle names are restricted to letters, digits, spaces and
  `- _ .` at creation, so user input cannot inject markup into the rendered pages.

## Run it locally

Requirements: the Gno toolchain (`gno`, `gnokey`, `gnodev`) v1.8.0+, `GNOROOT`
pointing at a checkout of the gno source tree.

```sh
cd realm
gno test .        # 7 unit tests: validation, guards, cancel, full lifecycle, render
gno lint .
```

Full end-to-end demo on a local devnet (creates two keys, deploys the realm, runs a
complete two-round circle with real coin movement, and shows the script-bypass
being rejected):

```sh
bash demo/demo.sh
```

## Deploy to the Onyx testnet

1. Get test GNOT from <https://faucet.gno.land> (select the Onyx testnet) to the
   deployer address `g1ulwmlzxtx922c7r8asp6ux23ks8rw6r8m2uftg`.
2. `bash demo/deploy-onyx.sh` — publishes the package and runs a first circle.

## Repository layout

```
realm/            the realm source (arisan.gno), its tests, gnomod.toml
demo/demo.sh      local devnet walkthrough incl. the bypass-rejection check
demo/deploy-onyx.sh   Onyx testnet deployment + smoke test
docs/             demo video script and the DoraHacks submission text
video/            demo video (mp4), the real demo transcript it was built from,
                  and the frame builder script
```

## License

MIT — see [LICENSE](LICENSE).
