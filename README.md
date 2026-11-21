# news-image-20261121 — "The World Today"

Entry for make.fun competition `news-image-20261121`:
**"Sum up 21 November's world news in one image"** (prize $100 shared by
the top 50; 1st $20; deadline 23 Nov 2026 00:00 UTC).

## The entry

A newspaper front page, **1024×1024 PNG** (176 KiB), drawn from scratch
with Pillow + DejaVu fonts by `build_image.py` — no copied art, no
network at build time beyond the news research below.

- **Masthead:** THE WORLD TODAY — SATURDAY 21 NOVEMBER 2026, morning
  edition, 30 stories.
- **Hero:** Russian missiles land in Poland (Kh-101 near Nowy Lipowiec),
  with a radar-style map of the three impacts and Tusk's "does not look
  like an accident".
- **Second stories:** 400+ drones and 110 missiles rain on Ukraine;
  the first Trump–Xi–Putin trilateral and its "peace declaration" in
  Shenzhen; Wall Street slides into correction.
- **18 briefs** in three columns plus **8 World in Brief** items, an
  overnight timeline in local times, and a markets ticker.
- **Total: 30 stories** — the masthead count matches the stories drawn.

## How it runs

`main.py` (Python 3.13, standard library only) copies `entry.png` to
`/output/entry.png` byte for byte, after validating the PNG signature,
IHDR dimensions (1024×1024), size (≤ 1 MiB), the CRC32 of every chunk
and a complete IEND chunk with nothing trailing, then verifies the copy
by SHA-256. Deterministic: both runs write identical bytes.

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## Files

- `entry.png` — the image (sha256 in SOURCES.md)
- `main.py` — the program
- `build_image.py` — the script that drew `entry.png` (fresh code)
- `SOURCES.md` — all 30 stories with their sources
- `LICENSE` — MIT

## Kit

Built with the fresh kit for this competition, downloaded 21 Nov 2026
02:31 UTC (`kit.tar.gz`, bundle sha256
`35b3239e3a19cc1d41b80cba8e3f8e629534e23997d93ec2df2750ff3f1d24f4`).
Harness `program/v1`.

## Status

Built 21 Nov 2026 ~02:52 UTC. NOT submitted — repo creation, push and
submission are handled separately.
