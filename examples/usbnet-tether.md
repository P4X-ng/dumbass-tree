# Example: phone USB tethering (host side)

1) Plug phone in
2) Enable “USB tethering” on the phone
3) On Linux:

```bash
dausbnet status

# assume it shows usb0
sudo dausbnet dhcp usb0

ip route
ping -c 1 1.1.1.1
```

If you still get nothing:
- toggle tethering off/on
- try a different cable/port
- check `dmesg -T | tail -200`
