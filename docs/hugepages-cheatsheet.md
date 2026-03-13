# Hugepages cheatsheet (Linux)

## Inspect

```bash
dahugepages status
cat /proc/meminfo | egrep -i 'Huge|AnonHuge|ShmemHuge'
cat /sys/kernel/mm/transparent_hugepage/enabled
```

## Reserve 2MB hugepages (example: 1024 pages = 2GB)

```bash
sudo dahugepages alloc --size 2M --count 1024
```

## Free them

```bash
sudo dahugepages free --size 2M
```

## Mount hugetlbfs

```bash
sudo dahugepages mount /mnt/huge --size 2M --mode 1770
mount | grep hugetlbfs
```

## THP mode

```bash
dahugepages thp
sudo dahugepages thp --set madvise   # or always / never
```

## Persistence helpers

```bash
dahugepages persist --size 2M --count 1024 --mountpoint /mnt/huge
```
