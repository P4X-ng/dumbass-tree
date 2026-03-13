# Quick wins (Linux + ZFS + hugepages)

This is a grab bag of “small changes, big impact”. Read the warnings.

---

## ZFS quick wins

### Always use stable device names
Use `/dev/disk/by-id/...` for pool creation and device ops. It prevents “nvme0n1 moved” disasters.

### SSD/NVMe: enable autotrim
On pools on SSD/NVMe:

```bash
zpool set autotrim=on tank
```

### Turn off atime unless you need it
```bash
zfs set atime=off tank
```

### Compression: start with lz4
It’s fast and often improves performance by reducing IO.

```bash
zfs set compression=lz4 tank
# or wrapper profile:
dazfs ds compression tank/home --profile fast
```

If you want better ratio and you can afford CPU, try zstd at modest levels (like zstd-3).

### Set recordsize per workload (huge win)
- big sequential files (media, backups): `recordsize=1M`
- random IO (VMs, DBs): `recordsize=16K` (sometimes 8K)

Example:

```bash
zfs set recordsize=1M tank/media
zfs set recordsize=16K tank/vm
```

### Schedule scrubs
Scrubs find latent errors. Run them regularly (monthly is common).

```bash
sudo zpool scrub tank
```

---

## Hugepages quick wins

### THP: don’t leave it on “always” blindly
THP can help or hurt depending on workload (latency-sensitive apps often prefer `madvise` or `never`).

Check:

```bash
cat /sys/kernel/mm/transparent_hugepage/enabled
```

Wrapper:

```bash
dahugepages thp
sudo dahugepages thp --set madvise
```

### Reserve hugepages for specific workloads
Databases, DPDK, some VMs: reserve 2M or 1G pages intentionally.

---

## Linux quick wins

### NVMe scheduler
For many NVMe devices, the `none` scheduler is a good default.

```bash
cat /sys/block/nvme0n1/queue/scheduler
echo none | sudo tee /sys/block/nvme0n1/queue/scheduler
```

Make it persistent with a udev rule if you like.

### The “I live in terminals” trio
- tmux
- fzf
- ripgrep

If you do nothing else, do those.

---

## Warnings

- Boot/kernel args can have security and stability tradeoffs.
- Storage ops are not forgiving: verify device paths every time.
- Performance tuning without measurement is how you create weird bugs. Benchmark first.

