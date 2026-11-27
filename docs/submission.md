# DoraHacks submission package — Gnome Tavern Hackathon

Deadline: **Dec 18, 2026, 01:00 UTC**. Submit from the builder account
**affif-agent**. Everything below is copy-paste ready; only the deployment link
and video link are filled in after the Onyx deploy + recording.

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
- Demo video: _(YouTube/Loom link — record per docs/demo-video-script.md)_

## User's manual steps (the only ones)

1. **Faucet** (~1 min): open https://faucet.gno.land, paste
   `g1ulwmlzxtx922c7r8asp6ux23ks8rw6r8m2uftg`, select **Onyx**, solve the captcha.
   → then tell the agent "faucet done"; deployment + on-chain smoke test are
   agent-side and take a few minutes.
2. **Join the hackathon** on DoraHacks (logged in as affif-agent): open
   https://dorahacks.io/hackathon/gnome-tavern → Join Hackathon → create the
   BUIDL/project and paste the fields from this file (repo link, deployment link,
   video link once recorded).
3. **Record the demo video** on the phone following
   `docs/demo-video-script.md` (~2 minutes), upload (YouTube unlisted is fine),
   paste the link into the submission.
4. If the project wins: complete DoraHacks KYC by **Dec 22, 2026** and provide a
   Gno.land wallet address for the GNOT prize within 30 days of the announcement.
