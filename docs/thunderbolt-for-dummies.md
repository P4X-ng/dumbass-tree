# Thunderbolt for dummies (a.k.a. “external PCIe, what could go wrong”)

Thunderbolt is incredible when it works.

It also has a security model because it can expose PCIe tunnels, which means:
- very high privilege access paths
- historically, real-world attacks (DMA-style)

So modern systems often require **authorization** of devices.

---

## The moving parts on Linux

- **Kernel** exposes Thunderbolt info + authorization controls (sysfs)
- **boltd** is a system daemon that manages devices and authorization
- **boltctl** is the CLI you use to talk to boltd

---

## The dumbass workflow

### 1) Check controller security + service status
```bash
dathunderbolt status
```

You’ll see something like:
- controller security level
- whether boltd is running
- devices (authorized vs not)

### 2) List devices (including unauthorized)
```bash
boltctl -U short list
# or:
dathunderbolt list
```

Copy the UUID of the device you want.

### 3) Authorize it (temporary)
```bash
sudo dathunderbolt authorize <uuid>
```

### 4) Enroll it (remember / auto-authorize later)
```bash
sudo dathunderbolt enroll <uuid> --policy auto
```

Only do this for devices you trust.

---

## Common “it half works” symptom

> My monitor works, but the dock USB ports / ethernet don’t.

That often means: the device is connected, but not fully authorized.
Enroll it.

---

## Troubleshooting checklist

### Check kernel sees Thunderbolt
```bash
lsmod | grep thunderbolt
dmesg -T | grep -i thunder
```

### Check domains/controller state
```bash
boltctl -U short domains -v
```

### Check boltd logs
```bash
journalctl -u boltd -b
```

---

## Security note (because it matters)

If you’re on a high-security box:
- consider keeping Thunderbolt disabled in BIOS/UEFI
- or keep security mode at least “user/secure” and never auto-enroll random devices

This is one of those “your threat model decides” things.

