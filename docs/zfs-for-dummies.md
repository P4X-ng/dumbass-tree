# ZFS for dummies (a.k.a. “why is my filesystem a volume manager?”)

ZFS is *two things glued together*:

1) A **volume manager** (it builds storage out of disks)
2) A **filesystem** (it stores your files)

That’s why it feels weird if you’re used to “mkfs.ext4 /dev/sdX; mount it”.

---

## 60‑second mental model

**Disks → vdevs → pool → datasets → snapshots**

- **Disk**: a block device. Prefer stable names like `/dev/disk/by-id/...`
- **vdev**: a “virtual device” made of one or more disks  
  Examples: a single disk, a **mirror**, or a **raidz** group
- **pool**: the big storage bucket built from one or more vdevs  
  Example: pool name `tank`
- **dataset**: a thing inside a pool with its own properties (mountpoint, compression, quotas, …)  
  The most common dataset type is a **filesystem**.
- **snapshot**: a read-only, instant “point in time” view of a dataset  
  Cheap to create; uses space only for changed blocks.

---

## Vocabulary that matters (and trips people)

### Pool
A pool is what you create with `zpool create`. It’s the top-level name, e.g. `tank`.

### Dataset
A dataset is *a ZFS object inside a pool*. Most of the time you mean:

- **Filesystem dataset**: what you expect: it can mount at a path, stores files
- (Other dataset types exist: volumes “zvols”, snapshots, bookmarks, clones)

You create filesystems with:

```bash
zfs create tank/home
```

### “Mountpoint” is a property, not an afterthought
ZFS doesn’t treat mounting as “whatever you typed into /etc/fstab”.
Each filesystem dataset has a `mountpoint` property:

```bash
zfs get mountpoint tank/home
zfs set mountpoint=/home tank/home
```

Mounting happens via:

- `zfs mount tank/home` (manual), or
- the ZFS mount service on boot (automatic), depending on your OS/distro

### `canmount` controls whether it *can* mount
Three common values:

- `canmount=on` (default): mounts when appropriate
- `canmount=noauto`: will not auto-mount; you can mount it manually
- `canmount=off`: never mount it (useful for “container datasets”)

### Properties inherit
If you set `compression=lz4` on `tank`, datasets under it inherit that unless overridden.

---

## “One big filesystem” (what people usually mean by “merge”)

There are *two different* things people mean when they ask this:

### 1) “Make multiple disks look like one big filesystem”
That’s literally what a **pool** is.

- Your pool (`tank`) is one virtual storage bucket.
- Datasets inside that pool all draw from the same free space (unless you apply quotas/reservations).

To grow a pool later, you **add a vdev** (new disk / mirror / raidz group):

```bash
# add another mirror vdev (capacity increases; redundancy stays mirror-per-vdev)
sudo zpool add tank mirror <disk3> <disk4>

# add a single disk vdev (capacity increases; BUT this removes redundancy for that vdev)
sudo zpool add tank <disk3>
```

**Important warning:** pool reliability is basically the reliability of the *worst* vdev you add.
If you add a single-disk vdev to a pool, that disk becomes a single point of failure for the pool.

This repo’s wrapper makes you say `--yes` for this on purpose:

```bash
sudo dazfs pool add tank --layout mirror <disk3> <disk4> --yes
```

### 2) “Make multiple datasets feel like one directory tree”
ZFS can’t union-mount two directories into the *same* directory, but it *can* mount datasets
**under one root**, so it looks like one tree:

```bash
# root dataset mounted at /tank
sudo zpool create -m /tank tank mirror <disk1> <disk2>

# these datasets mount *under* /tank
sudo zfs create tank/media
sudo zfs set mountpoint=/tank/media tank/media

sudo zfs create tank/backups
sudo zfs set mountpoint=/tank/backups tank/backups
```

That feels like “one filesystem” to your shell, but you still get per-subtree knobs:
compression, recordsize, quotas, snapshots, etc.

Wrapper for this:

```bash
sudo dazfs tree init tank --root /tank --style vault --mount-now
```

### What ZFS *doesn’t* do by itself
If you specifically want “merge directories from multiple sources into one directory” (UnionFS / overlay),
that’s not a native ZFS feature. On Linux you’d look at overlayfs/mergerfs/unionfs-fuse (separate topic,
with their own caveats).

---

## Compression without murdering your CPU

ZFS compression is usually worth it.

Common algorithms (what you’ll actually use):

- **lz4**: extremely fast, great default for “I don’t want to think”
- **zstd** (levels): better ratio, more CPU cost as level rises

Practical rules:

- If you care about latency or have lots of writes: **lz4**
- If you care about disk space and you’re not CPU-bound: **zstd-3** (nice sweet spot)
- Avoid “max level” zstd on a busy NAS unless you *know* you have CPU headroom

Also:
- Already-compressed files (videos, zip files) won’t compress much.
- Compression cost happens mostly on **writes**; reads are often faster because less I/O.

This repo’s wrapper uses **profiles**:
- `fast` → lz4
- `balanced` → zstd-3 (falls back to lz4 if unsupported)
- `max` → zstd-10 (falls back to lz4)

---

## The commands you’ll use 90% of the time

### Create a pool (mirror example)

```bash
sudo zpool create -o ashift=12 -m /tank \
  tank mirror /dev/disk/by-id/ata-AAA /dev/disk/by-id/ata-BBB
```

Notes:
- `ashift=12` is the usual “modern 4K sector safe” default.
- `-m /tank` sets the root dataset mountpoint.

### Create datasets

```bash
sudo zfs create tank/home
sudo zfs set mountpoint=/home tank/home
sudo zfs set compression=lz4 tank/home
```

### List things

```bash
zpool list
zpool status -v
zfs list -o name,used,avail,refer,mountpoint -r tank
```

### Snapshots

```bash
sudo zfs snapshot tank/home@before-upgrade
zfs list -t snapshot -r tank/home
sudo zfs rollback tank/home@before-upgrade
```

### Scrub (health check)

```bash
sudo zpool scrub tank
zpool status tank
```

---

## Common “why is this happening?” moments

### “I set a mountpoint but it didn’t mount”
Check:

```bash
zfs get mountpoint,canmount tank/home
```

Then try:

```bash
sudo zfs mount tank/home
```

Also check if a parent dataset is set to `canmount=off` or has `mountpoint=none`.

### “Should I use compression=on?”
Usually: no. Use explicit algorithms like `lz4` or `zstd-3`.

### “What dataset layout should I use?”
Think in vdevs:

- **One disk** = no redundancy
- **Mirror** = simple redundancy, good IOPS
- **RAIDZ** = parity redundancy, capacity-efficient, different performance tradeoffs

ZFS expands easily by adding vdevs, but you generally can’t “reshape” a vdev in place.

---

## Use the dumbass wrapper (dazfs)

Everything here works with raw `zpool`/`zfs`.
The wrapper just helps with defaults and fewer gotchas.

Examples:

```bash
sudo dazfs --dry-run pool create tank --layout mirror --mountpoint /tank \
  /dev/disk/by-id/ata-AAA /dev/disk/by-id/ata-BBB

sudo dazfs ds create tank/home --mountpoint /home --compression balanced
sudo dazfs snap create tank/home
sudo dazfs status --pool tank

# "one big tree" layout under /tank
sudo dazfs tree init tank --root /tank --style vault --mount-now
```

See also:
- `docs/zfs-cheatsheet.md`
- `man/dazfs.1`
