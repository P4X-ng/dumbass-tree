# USB networking for dummies (why isn’t DHCP working)

USB networking is *deceptively* annoying because it can mean 3 different things:

1) **USB ethernet adapter** (dongle)
2) **Phone USB tethering** (creates a network interface)
3) **USB gadget mode** (your Linux box acts like a USB network device)

Most of the time you mean #1 or #2.

---

## The dumbass workflow (host side)

### 1) See what interfaces appeared
```bash
dausbnet status
ip link
```

You’re looking for something like:
- `enx<MAC...>` (very common for USB ethernet)
- `usb0` (common for tethering / RNDIS / gadgets)

### 2) Bring it up + DHCP
```bash
sudo dausbnet dhcp enxdeadbeefcafe
```

If your system is managed by NetworkManager, the equivalent is often:
```bash
nmcli device
sudo nmcli device connect enxdeadbeefcafe
```

### 3) Confirm you got an IP + route
```bash
ip -br addr show dev enxdeadbeefcafe
ip route
ping -c 1 1.1.1.1
```

---

## “I still have no IP”

### Check the kernel sees the device
```bash
dmesg -T | tail -200
lsusb
```

### Check link state
```bash
ip link show dev enxdeadbeefcafe
ethtool enxdeadbeefcafe   # if installed
```

### If NetworkManager is present: check it didn’t disable the device
If someone did `nmcli device disconnect`, NM can keep the device disconnected until you reconnect it.
(That one gets people constantly.)

---

## Making it persistent (systemd-networkd)

If you use systemd-networkd and want “USB ethernet always uses DHCP”:

```bash
sudo dausbnet persist --write
sudo systemctl restart systemd-networkd
```

⚠️ Don’t do this if NetworkManager is managing your networking.
Pick one manager per interface.

---

## Phone tethering gotchas

- On Android, you typically need to enable “USB tethering” *after* plugging in.
- Some phones expose RNDIS, others expose CDC-NCM/ECM.
- If it creates `usb0` but you get no DHCP, try re-toggling tethering.

---

## USB gadget mode (advanced)

This is the “my laptop pretends to be a USB ethernet device” trick.
It’s awesome, but it’s a separate topic (configfs, gadget drivers, etc.).

If you want this: say so and we’ll add a dedicated `dagadget` tool.

