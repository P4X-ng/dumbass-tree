# ZFS cheatsheet (stuff you actually type)

## Inspect

```bash
zpool list
zpool status -v
zfs list -o name,used,avail,refer,mountpoint -r tank
zfs get -r mountpoint,canmount,compression,recordsize,atime tank
```

## Create

```bash
# pool (mirror)
sudo zpool create -o ashift=12 -m /tank tank mirror <disk1> <disk2>

# dataset
sudo zfs create -p tank/home
sudo zfs set mountpoint=/home tank/home
sudo zfs set compression=lz4 tank/home
```

## One big tree layout (datasets mounted under one root)

```bash
# Create a common "everything under /tank" hierarchy
sudo dazfs tree init tank --root /tank --style vault --mount-now
```

## Expand a pool (add capacity)

```bash
# Add another mirror vdev (safe-ish way to grow)
sudo dazfs pool add tank --layout mirror <disk3> <disk4> --yes

# Turn an existing single disk vdev into a mirror (attach)
sudo dazfs pool attach tank <existing-disk-in-pool> <new-disk> --yes
```

## Mounting

```bash
sudo zfs mount tank/home
sudo zfs unmount tank/home
```

## Snapshots

```bash
sudo zfs snapshot tank/home@before
zfs list -t snapshot -r tank/home
sudo zfs rollback tank/home@before
```

## Scrub

```bash
sudo zpool scrub tank
zpool status tank
```

## Common properties

```bash
sudo zfs set atime=off tank/home
sudo zfs set recordsize=1M tank/media
sudo zfs set compression=zstd-3 tank/home
sudo zfs set mountpoint=none canmount=off tank/containers
```

## “dumbass” wrappers

```bash
sudo dazfs pool create tank --layout mirror --mountpoint /tank <disk1> <disk2>
sudo dazfs ds create tank/home --mountpoint /home --compression balanced
sudo dazfs snap create tank/home
sudo dazfs status --pool tank
```
