# Thunderbolt cheatsheet

## Status
```bash
dathunderbolt status
boltctl -U short domains
boltctl -U short list
```

## Authorize / enroll / forget
```bash
sudo boltctl authorize <uuid>
sudo boltctl enroll --policy auto <uuid>
sudo boltctl forget <uuid>
```

## Details
```bash
boltctl info <uuid>
journalctl -u boltd -b
```

