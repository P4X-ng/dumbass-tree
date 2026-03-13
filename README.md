# dumbass-tree 🌳

A tiny repo of **dumbass-friendly** wrappers + docs for Linux things that are powerful but annoying.

Tools included:

- **ZFS** (`bin/dazfs`) — pools, datasets, mountpoints, compress...es, “one big tree” layouts, snapshots, scrubs, pool grow helpers
- **Hugepages** (`bin/dahugepages`) — inspect/allocate hugepages, mount `hugetlbfs`, tweak THP
- **Btrfs** (`bin/dabtrfs`) — subvolumes, snapshots, scrub/balance helpers (lighter coverage)
- **AppArmor** (`bin/daapparmor`) — status/denials + a sane “complain → allow → enforce” workflow
- **Terminal browsing** (`bin/dabrowse`) — pick the best available terminal browser (carbonyl/browsh/w3m/links/lynx)
- **Display stack** (`bin/dax`) — “am I on X11 or Wayland?”, plus quick explanation
- **USB networking** (`bin/dausbnet`) — detect USB net ifaces, bring them up, try DHCP, generate networkd config
- **Thunderbolt** (`bin/dathunderbolt`) — boltctl wrapper for authorizing/enrolling devices (with safety rails)
- **DNS sanity** (`bin/dadns`) — explain stub resolv.conf, show real DNS, toggle resolved/NM modes
- **ifupdown migration** (`bin/daifupdown`) — plan + generate `/etc/network/interfaces`, optionally disable netplan YAML
- **iproute2 helper** (`bin/daip`) — brief status + “explain” the scary ip tokens
- **tmux/screen scrollback** (`bin/datmux`) — config snippets you can paste/apply
- **Peer-to-peer links** (`bin/dap2p`) — ethernet static setup + USB gadget helpers (g_ether, g_mass_storage)
- **Safer dd** (`bin/dadd`) — write ISO/images to USB with two-tier warnings + make file-backed FAT images
- **Share page capture** (`bin/dasharepage`) — WARC capture with “don’t leak tokens” warnings
- **Work in RAM** (`bin/darunram`) — copy-to-tmpfs + optional rsync-back workflow

These scripts **do not replace** `man zfs`, `man zpool`, `man btrfs`, etc. They just turn common
operations into fewer keystrokes with safer defaults, clearer error messages, and a `--dry-run`
mode so you can see what will happen first.

## Safety rails (on purpose)

For irreversible/destructive ops, the tools require either:

- **`--yes`** (explicit “I know what I’m doing”), **or**
- an **interactive confirmation prompt** (type a token like `DESTROY tank`)

If you run them non-interactively (CI, scripts), you must pass `--yes` so they don’t hang.

> ⚠️ **Data-loss warning**
> Pool creation / formatting / destroy / rollback can permanently delete data. Use `--dry-run`,
> triple-check device paths (`/dev/disk/by-id/...` recommended), and keep backups.

## Quick start

### Install (local user)

```bash
./scripts/install-local.sh
```

Make sure `~/.local/bin` is in your `PATH`.

### ZFS examples

```bash
# Create a mirrored pool (will prompt unless --yes)
sudo dazfs pool create tank --layout mirror /dev/disk/by-id/ata-AAA /dev/disk/by-id/ata-BBB

# Create a dataset mounted at /home with “balanced” compression
sudo dazfs ds create tank/home --mountpoint /home --compression balanced

# Build a unified “one big tree” under /tank
sudo dazfs tree init tank --root /tank --style vault --mount-now
```

### AppArmor examples

```bash
daapparmor status
sudo daapparmor denials --since 1h

# Typical profile-dev loop:
sudo daapparmor complain <profile>
# run the app to generate denials...
sudo daapparmor allow
sudo daapparmor enforce <profile>
```

## Docs to read first

- `docs/zfs-for-dummies.md`
- `docs/hugepages-for-dummies.md`
- `docs/btrfs-for-dummies.md`
- `docs/apparmor-for-dummies.md`
- `docs/wayland-for-dummies.md`
- `docs/usbnet-for-dummies.md`
- `docs/thunderbolt-for-dummies.md`
- `docs/terminal-only.md`
- `docs/quick-wins.md`

## License

MIT — see `LICENSE`.
