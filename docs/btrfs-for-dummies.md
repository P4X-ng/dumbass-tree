# Btrfs for dummies (Linux)

Btrfs is a copy-on-write filesystem with built-in snapshots, checksums, and flexible layouts.

If ZFS feels like “filesystem + volume manager”, Btrfs feels like “filesystem + snapshots everywhere”.

This repo’s `dabtrfs` helper focuses on the stuff you actually do day-to-day:
subvolumes, snapshots, scrub, and balance.

---

## Mental model

- **Filesystem**: what you format with `mkfs.btrfs`
- **Subvolume**: a lightweight filesystem-like tree inside the filesystem
  - Snapshots are subvolumes too
- **Snapshot**: a cheap point-in-time copy (copy-on-write)
- **Scrub**: verify checksums and try to repair from redundant copies (if present)
- **Balance**: reorganize block groups (useful after changing usage patterns)

---

## The 80/20 workflow

### Create a subvolume layout (common pattern)

Many people create “@” subvolumes and mount them:

- `@` for root
- `@home` for `/home`
- `@var` for `/var`

Example (assuming `/mnt/btrfs` is mounted):

```bash
sudo dabtrfs subvol create /mnt/btrfs/@
sudo dabtrfs subvol create /mnt/btrfs/@home
sudo dabtrfs subvol create /mnt/btrfs/@var
```

### Snapshot a subvolume

```bash
sudo dabtrfs snapshot /mnt/btrfs/@home /mnt/btrfs/@home-$(date +%F) --readonly
```

### Scrub regularly

```bash
sudo dabtrfs scrub start /mnt/btrfs
sudo dabtrfs scrub status /mnt/btrfs
```

### Balance (don’t spam it)

Balance is not a cron-every-hour thing. Use it when you have a reason
(e.g. after large deletes, after changing RAID profile, etc.).

```bash
sudo dabtrfs balance start /mnt/btrfs --dusage 50
```

---

## Compression

Btrfs compression is commonly enabled via mount options like:

- `compress=zstd:3` (often a good default)
- `compress=lzo` (fast)
- `compress-force=zstd:3` (forces compression even when heuristics would skip)

`dabtrfs mount` helps generate / run a mount with sane compression options.

---

## Gotchas

- Copy-on-write filesystems can fragment. For VM images / databases you may want
  workload-specific tuning (nodatacow or per-directory flags). Know what you’re doing first.
- RAID5/6 on Btrfs has had a rocky history. If you want “appliance-grade” parity RAID,
  research your kernel/tooling version carefully and test recovery scenarios.

See also:
- `docs/btrfs-cheatsheet.md`
- `man/dabtrfs.1`
