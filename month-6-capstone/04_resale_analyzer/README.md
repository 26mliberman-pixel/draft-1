# Capstone 04: Resale Appreciation Analyzer

> *"Best item to buy from a catalog to resell for the highest appreciation?"*

This little web app answers exactly that question. You feed it a catalog of
items you *could* buy (sneakers, watches, trading cards, consoles, handbags,
Lego sets...), tell it what each one costs and what it currently resells for,
and it **ranks them** so you can instantly see which one is the best to buy
and flip.

## What "appreciation" means

Appreciation is how much an item gained in value, as a percentage:

```
appreciation % = (resale_price - buy_price) / buy_price * 100
```

Example: you buy a sneaker for **$200** and it now resells for **$350**.

```
(350 - 200) / 200 * 100 = 75%   ->  it appreciated 75%
```

### Why we also show "per year" (annualized)

A 30% gain in **3 months** is far better than a 30% gain over **2 years**,
because you can flip the fast one again and again. So the app also computes the
**annualized** appreciation — the growth rate per year — and ranks the catalog
by that. The item at the top is your best buy-to-flip.

```
annualized % = (resale / buy) ** (12 / months_held) - 1   (as a %)
```

## Features

1. **Add items** to your catalog (buy price, resale price, months held)
2. **Best Buy banner** — the single highest-appreciating item, front and center
3. **Ranked catalog** — every item sorted best-to-worst
4. **Filter by category** (Sneakers, Watches, Trading Cards, ...)
5. **Delete items** you no longer care about
6. **Auto-seeded** with realistic example data on first run

## Run it

```bash
pip install flask
python app.py
```

Then open **http://127.0.0.1:5000** in your browser.

The catalog is stored in a local SQLite file (`resale.db`) that is created
automatically the first time you run the app.

## Skills combined

| Skill | Where it's used |
|-------|-----------------|
| Flask (Month 5) | The whole web interface and routes |
| SQLite (Month 5) | Storing and querying the catalog |
| Functions & control flow (Month 2) | The appreciation maths |
| Lists, dicts, sorting (Month 3) | Ranking the items |
| Math & string formatting (Month 1) | Percentages and dollar amounts |

## Ideas to extend it (your turn!)

- Add a **fees** field (eBay/StockX take a cut) and rank by *net* profit
- Track **price history** over time and chart it
- Pull live resale prices from an **API** (Month 4 skills)
- Add a **"buy now?" score** combining appreciation speed and resale volume

> ⚠️ This is a learning project, not financial advice. Resale prices are
> volatile — past appreciation does not guarantee future returns.
