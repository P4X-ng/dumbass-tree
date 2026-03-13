# Example: 2MB hugepages for a userspace app (Linux)

Reserve 2GB of 2MB hugepages and mount hugetlbfs.

```bash
dahugepages status

sudo dahugepages alloc --size 2M --count 1024
sudo dahugepages mount /mnt/huge --size 2M --mode 1770

dahugepages status
```

If allocation fails due to fragmentation, reboot and allocate earlier.
