# Btrfs cheatsheet

## Inspect

```bash
btrfs filesystem show
btrfs filesystem df /mnt/btrfs
btrfs filesystem usage /mnt/btrfs
btrfs subvolume list -p /mnt/btrfs
```

## Subvolumes + snapshots

```bash
sudo dabtrfs subvol create /mnt/btrfs/@home
sudo dabtrfs snapshot /mnt/btrfs/@home /mnt/btrfs/@home-$(date +%F) --readonly
sudo dabtrfs subvol list /mnt/btrfs
```

## Scrub

```bash
sudo dabtrfs scrub start /mnt/btrfs
sudo dabtrfs scrub status /mnt/btrfs
```

## Balance (example)

```bash
sudo dabtrfs balance start /mnt/btrfs --dusage 50
```

## Mount with compression (example)

```bash
sudo dabtrfs mount /dev/sdX1 /mnt/btrfs --compress zstd:3 --noatime
```
