# Arisan Circle

A rotating savings club (ROSCA) realm on **Gno.land**, inspired by the Indonesian
*arisan*: a group of members each contributes a fixed amount every round, and each
round one member receives the whole pot — rotating in join order until everyone has
received it exactly once. No fees, no custodian, no admin key: the realm holds a
round's contributions only until the round completes, then pays out automatically.

Built for the **Gnome Tavern Hackathon** (DoraHacks).

## Live deployment

- Testnet: **Onyx / Test17** (`onyx-1`), RPC `https://rpc.onyx.testnets.gno.land:443`
- Realm: `gno.land/r/g1ulwmlzxtx922c7r8asp6ux23ks8rw6r8m2uftg/arisan`
- Browse: <https://latest.testnets.gno.land/r/g1ulwmlzxtx922c7r8asp6ux23ks8rw6r8m2uftg/arisan>

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
paid this round, who receives next, and the payout history. Sample output from a
completed two-member circle (local devnet run):

```
# KeluargaBesar

- Status: **finished**
- Contribution: 0.1 GNOT (100000 ugnot) per member, per round
- Pot per round: 0.2 GNOT

## Payout history

- Round 1: `g1ulwmlzxtx922c7r8asp6ux23ks8rw6r8m2uftg`
- Round 2: `g1kzystp5z8r7cswq8wwse4c57gge3szv5jp23uc`
```

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
```

## License

MIT — see [LICENSE](LICENSE).
