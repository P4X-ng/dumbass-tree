# Hugepages for dummies (Linux)

Hugepages are a **performance** feature that trades flexibility for fewer page-table / TLB overheads.

If you don’t know why you want hugepages, you probably don’t need them.
If you *do* need them (DPDK, certain DBs, low-latency workloads), you want a checklist you can repeat.

---

## Two different things people call “hugepages”

### 1) Transparent Huge Pages (THP)
- Kernel automatically tries to back memory with huge pages when it can.
- You can set THP mode: `always`, `madvise`, or `never`.
- Good default for many systems is often `madvise` (apps opt in).

### 2) Explicit / “static” hugepages (hugetlb)
- You reserve a fixed number of huge pages (2MB or 1GB).
- Apps map them through `hugetlbfs` or special APIs.
- Great for things like DPDK.
- Downside: the pages must be physically contiguous; allocating late (after uptime) can fail.

This repo’s `dahugepages` helper focuses on inspecting + controlling both.

---

## What size hugepages exist?

Most common:

- **2MB** hugepages: widely supported, easier to allocate
- **1GB** hugepages: fewer TLB misses, harder to allocate; usually needs boot-time reservation

You can see what your kernel exposes under:

- `/sys/kernel/mm/hugepages/hugepages-2048kB/`
- `/sys/kernel/mm/hugepages/hugepages-1048576kB/` (if supported)

---

## The 80/20 workflow

### 1) Check current status

```bash
dahugepages status
```

That reads:
- `/proc/meminfo` HugePages*
- sysfs hugepages counters
- THP mode (`/sys/kernel/mm/transparent_hugepage/enabled`)
- current hugetlbfs mounts (`/proc/mounts`)

### 2) Reserve some 2MB hugepages

Example: reserve 1024 × 2MB = 2GB of hugepages

```bash
sudo dahugepages alloc --size 2M --count 1024
```

Verify:

```bash
dahugepages status
```

If allocation fails, it’s usually fragmentation. Try allocating earlier (soon after boot), or reboot with a reservation.

### 3) Mount hugetlbfs (optional but common)

```bash
sudo dahugepages mount /mnt/huge --size 2M --mode 1770
```

Apps (DPDK, etc.) can use `/mnt/huge`.

### 4) Set THP mode (if you care)

```bash
dahugepages thp
sudo dahugepages thp --set madvise
```

---

## Persistence (survives reboot)

Hugepages configuration often needs to be done at boot:

- via `sysctl` (for default hugepages)
- via kernel cmdline (especially for 1G hugepages)
- via systemd unit / init scripts

This repo doesn’t automatically edit your bootloader config, but `dahugepages persist`
prints the lines you’d typically add (sysctl + fstab).

---

## Common gotchas

- **Hugepages reserved are not usable as normal RAM** until freed.
- **1G pages** often require boot-time reservation; trying to allocate later may fail.
- **THP is not the same as hugetlb**. Turning THP off does not free hugetlb pages, etc.
- Some workloads hate THP (latency spikes). Others love it (fewer TLB misses). Test.

See also:
- `docs/hugepages-cheatsheet.md`
- `man/dahugepages.1`
