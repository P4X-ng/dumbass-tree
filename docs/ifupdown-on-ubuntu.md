# Switching Ubuntu to ifupdown without instantly bricking networking

Ubuntu’s “modern stack” is usually:

- **netplan**: YAML in `/etc/netplan/*.yaml`
- **renderer**: `systemd-networkd` or `NetworkManager`
- **DNS**: `systemd-resolved` (often via the `127.0.0.53` stub)

If you want the old school `/etc/network/interfaces` world, the least-bad approach is:

1) install ifupdown
2) generate an interfaces file
3) disable netplan config (move the YAML aside)
4) reboot and verify
5) rollback if needed

## Hard warning

Do this from a local console (or have IPMI / iDRAC / physical access).
If you do this over your only SSH link, you may have a bad time.

## Minimal plan (wired DHCP only)

### 1) Install ifupdown

```
sudo apt install ifupdown
```

### 2) Generate `/etc/network/interfaces`

```
sudo daifupdown generate --write
```

Review it. Edit static interfaces manually if needed.

### 3) Disable netplan config

```
sudo daifupdown disable-netplan
```

That moves `/etc/netplan/*.yaml` to a timestamped backup dir.

### 4) Reboot

```
sudo reboot
```

## Rollback

From console:

```
sudo mv /etc/netplan/dumbass-disabled-*/. /etc/netplan/
sudo netplan apply
```

(Or just reboot again after restoring.)

## Keeping Wi‑Fi in NetworkManager but using ifupdown for wired

NetworkManager can be configured to ignore interfaces listed in `/etc/network/interfaces`.
This is a common compromise:
- ifupdown manages wired ports
- NetworkManager manages Wi‑Fi + VPN

Check `/etc/NetworkManager/NetworkManager.conf` and the `[ifupdown]` section.

## Tools in this repo

- `daifupdown plan`
- `daifupdown generate`
- `daifupdown disable-netplan`
- `dadns ...` (DNS sanity while you’re at it)
