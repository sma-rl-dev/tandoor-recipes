# Tester environment

## Quick start

```bash
./tester-env --port 9085 deploy
./tester-env --port 9085 seed
./tester-env --port 9085 verify
```

Login at http://localhost:9085/ with `admin` / `adminadmin`.

Reset the project-owned containers and volumes with:

```bash
./tester-env --port 9085 reset
```

## Deterministic seed

The active `Harbor Kitchen` household contains five recipes: `Lemon Herb Salmon`,
`Smoky Chickpea Stew`, `Garden Vegetable Pasta`, `Blueberry Oat Muffins`, and
`Tomato Basil Soup`. `Weeknight Favorites` contains the first three. Recipe
timestamps are fixed from 2024-01-15 through 2024-05-05; the seed manifest is
`tester-env-seed.json`.

`./tester-env --port 9085 reset`, `deploy`, `seed`, and `verify` completed two
identical cycles. Both reported `Verified Harbor Kitchen: 5 recipes, 3
Weeknight Favorites entries, active admin household.` with snapshot SHA-256
`08bba3e7a6b0cd2d141623ea9714716af58ac6d9429ca084960c845350a92daf`.

## Evidence

This fork is based on upstream tag `2.6.15`
(`7e1c427a0e17858ddc41bd198c79ccad77d3bd69`). Its Dockerfile builds the
`vue3` Vite assets required after login. Browser smoke verified login,
onboarding skip, and creating then deleting a temporary recipe. Browser seed
verification showed `Harbor Kitchen` with five recipes and `Weeknight
Favorites` with three entries.
