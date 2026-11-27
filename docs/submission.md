# DoraHacks submission package — Gnome Tavern Hackathon

Deadline: **Dec 18, 2026, 01:00 UTC**. Submit from the builder account
**affif-agent**. Everything below is copy-paste ready. Status Nov 27, 2026:
SUBMITTED (BUIDL 52085, "Under Review") and the realm is **LIVE on Onyx** —
addpkg tx at height 1441376, **GPAS checks passed 2026-11-27 03:10:15 UTC**,
approver enable landed the same day (package status `live`), and a full
3-round circle (KeluargaBesar) was completed on-chain:
https://latest.testnets.gno.land/r/g1ulwmlzxtx922c7r8asp6ux23ks8rw6r8m2uftg/arisan/circle/0

## Project name

Arisan Circle

## Tagline

A rotating savings club (ROSCA) on Gno.land — the Indonesian arisan, with the
rotation enforced by a realm instead of trust.

## Description

Arisan is a rotating savings and credit association used by millions across
Southeast Asia: members contribute a fixed amount every round, and each round one
member receives the whole pot, rotating until everyone has received it once.
Off-chain, it depends entirely on the organizer's honesty and everyone's memory.

Arisan Circle is a complete Gno.land realm that runs the entire lifecycle
on-chain:

- Anyone can open a circle (2–12 members, fixed ugnot contribution).
- Members join while the circle is open; the creator starts it.
- Every round, each member contributes exactly the agreed amount; the moment the
  last contribution lands, the realm automatically pays the full pot to that
  round's recipient (rotation = join order). No fees, no custodian, no admin key.
- Creators can cancel only before the start; nobody can redirect a payout.
- The realm renders gnoweb pages: a circle directory, per-circle status, who has
  paid, who receives next, and the permanent payout history.

Security follows the Gno security guide: every state-changing entry point
requires a direct user call (an intermediary contract or a `maketx run` script
cannot act in a user's name — demonstrated live in the repo's demo script), and
contributions are verified against the coins actually attached to the call, to
the exact ugnot and denomination.

The repository includes 7 unit tests (validation, join/start guards, cancel,
exact-payment guards, a full multi-round lifecycle with real payouts, rendering),
a one-command local demo (`demo/demo.sh`) that runs a whole circle on a local
devnet including the rejected bypass attempt, and a one-command Onyx deploy
script.

## Links to fill in

- GitHub repo: https://github.com/afif-3/arisan-circle
- Live deployment (Onyx testnet):
  https://latest.testnets.gno.land/r/g1ulwmlzxtx922c7r8asp6ux23ks8rw6r8m2uftg/arisan
  _(package LIVE on Onyx since Nov 27, 2026 — addpkg tx
  `YobxWn/8+Y31mj7GZNX/z6WDABndjqfA2XzN8c3aFlA=` at height 1441376; GPAS checks
  passed 2026-11-27 03:10:15 UTC; approver enable landed; full 3-round circle
  completed on-chain at /circle/0)_
- Demo video: upload `video/arisan-circle-demo.mp4` from the repo (2 min 02 s,
  assembled from the real local-devnet demo run: full circle lifecycle, the
  realm's rendered payout-history page, and the rejected script-bypass attempt;
  source transcript in `video/demo-transcript.txt`) to YouTube (unlisted is
  fine) and paste the link here. A phone re-recording on the live testnet is
  also possible per `docs/demo-video-script.md` once the deployment is up.

## User's manual steps (the only ones)

1. **Faucet** — DONE (Nov 27, 2026): the deployer was funded with 10 GNOT and
   the package was submitted the same morning; nothing left to do here. The
   on-chain lifecycle exercise runs agent-side as soon as the realm is
   enabled by the chain approver.
2. **Join the hackathon** on DoraHacks (logged in as affif-agent): open
   https://dorahacks.io/hackathon/gnome-tavern → Join Hackathon → create the
   BUIDL/project and paste the fields from this file (repo link, deployment link,
   video link once recorded).
3. **Demo video**: the ready-made file `video/arisan-circle-demo.mp4` is in the
   repo — upload it (YouTube unlisted is fine) and paste the link into the
   submission. (Optional upgrade: re-record on the phone against the live
   testnet realm following `docs/demo-video-script.md`.)
4. If the project wins: complete DoraHacks KYC by **Dec 22, 2026** and provide a
   Gno.land wallet address for the GNOT prize within 30 days of the announcement.
