# Example: simple ZFS layouts

## Layout A: “normal” datasets (system-ish)

### Goal
- mirror two disks
- mount pool at /tank
- create dataset tank/home mounted at /home
- set compression to balanced

### Commands

```bash
# Always dry-run first
sudo dazfs --dry-run pool create tank --layout mirror --mountpoint /tank \
  /dev/disk/by-id/ata-AAA /dev/disk/by-id/ata-BBB

# Run it
sudo dazfs pool create tank --layout mirror --mountpoint /tank \
  /dev/disk/by-id/ata-AAA /dev/disk/by-id/ata-BBB

sudo dazfs ds create tank/home --mountpoint /home --compression balanced

# sanity check
dazfs status --pool tank
```

---

## Layout B: “one big tree” under a root (what people mean by “merge”)

### Goal
- keep everything under a single root directory (e.g. /tank)
- but still split into datasets so you can tune per-subtree properties

### Commands

```bash
sudo dazfs tree init tank --root /tank --style vault --mount-now

# you can now tune just media, e.g.
sudo dazfs ds compression tank/media --profile fast
```
