# USB networking cheatsheet

## Find the USB network interfaces
```bash
dausbnet status
ip -br link
```

## DHCP now
```bash
sudo dausbnet dhcp <iface>
```

## NetworkManager quick commands
```bash
nmcli device
sudo nmcli device connect <iface>
nmcli -t -f DEVICE,TYPE,STATE,CONNECTION dev
```

## systemd-networkd quick commands
```bash
networkctl list
networkctl status <iface>
sudo networkctl reconfigure <iface>
```

