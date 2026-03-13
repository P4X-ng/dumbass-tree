# Example: Btrfs subvolumes + snapshot

Assuming you already mounted the filesystem at /mnt/btrfs:

```bash
sudo dabtrfs subvol create /mnt/btrfs/@home
sudo dabtrfs snapshot /mnt/btrfs/@home /mnt/btrfs/@home-$(date +%F) --readonly

dabtrfs subvol list /mnt/btrfs
```
