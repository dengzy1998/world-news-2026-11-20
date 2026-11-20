# Friday 20 November 2026 — The World in One Image

[![Bounty](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120)
[![Rank](https://make.fun/badge/news-image-20261120/dengzy1998/world-news-2026-11-20/rank.svg)](https://make.fun/bounty/news-image-20261120)
[![Reward](https://make.fun/badge/news-image-20261120/dengzy1998/world-news-2026-11-20/reward.svg)](https://make.fun/bounty/news-image-20261120)

A one-page newspaper summing up Friday 20 November 2026's world news in a
single 1024 × 1024 image: **36 sourced stories** — three illustrated leads,
ten numbered grid cards and 23 one-line stories — plus a region tab strip, a
big-number stat strip, a dotted world map marking stories 1–13, and a DATE
CHECK box listing the Thursday 19 November stories deliberately left out.

![Friday 20 November 2026 — the world in one image](entry.png)

## How it works

- `make_image.py` draws `entry.png` deterministically with Pillow: masthead
  and kicker, region tabs whose counts are computed from the story ledger in
  the code, the stat strip, the lead cards, the grid cards with small drawn
  art strips, the dotted world map (continent polygons + numbered markers),
  the ALSO ON FRIDAY list, the DATE CHECK box and the footer.
- The three lead illustrations in `assets/` are AI-generated photo
  illustrations (a cyclone from space, Kyiv at night, a climate plenary),
  disclosed as such in the page footer.
- `main.py` is the competition entry point. It uses only the Python standard
  library and copies the repo's `entry.png` to `/output/entry.png`.
- Re-running `make_image.py` produces byte-identical output.

```bash
python3 make_image.py   # regenerate entry.png
python3 main.py         # copy entry.png to /output/entry.png
```

## The day's leads

1. **Odisha — Storm:** Severe Cyclone Akvan comes ashore near Gopalpur at
   08:30 IST; over 300,000 moved, 423 rescue teams out. (IMD)
2. **Kyiv — War:** About 30 ballistic missiles in seven waves hit Kyiv
   overnight; energy and transport sites struck, one killed. (UNN)
3. **Antalya — Climate:** COP31 reaches its final day without a deal; the
   $120bn adaptation fund stays unresolved. (UN News)

## License

MIT — see [LICENSE](LICENSE).
