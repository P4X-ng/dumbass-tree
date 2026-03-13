# Glossary (quick + blunt)

## ZFS
- **vdev**: a building block of a pool (disk / mirror / raidz group)
- **pool**: storage made of one or more vdevs (`zpool create`)
- **dataset**: object inside a pool; usually a filesystem (`zfs create`)
- **zvol**: dataset type that acts like a block device (VM disks, iSCSI targets)
- **snapshot**: point-in-time view of a dataset (`zfs snapshot`)
- **clone**: writable copy of a snapshot

## Hugepages (Linux)
- **page**: smallest unit of memory mapping (usually 4KB)
- **hugepage**: bigger page (2MB / 1GB) for fewer TLB/page-table entries
- **THP**: Transparent Huge Pages (kernel tries automatically)
- **hugetlb**: explicit reserved hugepages (static pool)

## Btrfs
- **subvolume**: a filesystem tree inside a Btrfs filesystem
- **snapshot**: cheap copy of a subvolume (copy-on-write)
- **scrub**: checksum verification + repair (when redundancy exists)
- **balance**: reorganize block groups / allocation

## AppArmor (Linux)
- **profile**: a policy that confines a program (usually defined under /etc/apparmor.d)
- **enforce**: block disallowed actions
- **complain**: don't block, but log what would be denied (best for profile development)
- **DENIED**: log message indicating a blocked/would-be-blocked action


## Wayland / X11
- **X11 / Xorg**: the classic Linux/Unix display server protocol + server
- **Wayland**: a newer display protocol + architecture intended to replace X11
- **compositor**: the thing that draws windows and routes input; on Wayland it *is* the display server
- **XWayland**: an X11 server that runs as a Wayland client to support legacy X11 apps

## USB networking
- **CDC-ECM / CDC-NCM / CDC-Ether**: common USB networking protocols/drivers (non-RNDIS)
- **RNDIS**: Microsoft's USB networking protocol; still common on phones/modems, but kind of cursed
- **DHCP**: automatic IP config (what you usually want)

## Thunderbolt
- **domain**: a Thunderbolt controller instance (what `boltctl domains` shows)
- **authorize**: allow a device to connect for this session
- **enroll**: authorize + remember a device in boltd database for future auto-authorization
