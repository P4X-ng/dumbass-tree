# Peer-to-peer links (Ethernet / USB gadget)

## Ethernet cable between two machines

### Option 1: IPv6 link-local (often already works)

Most Linux boxes auto-configure an IPv6 link-local address (`fe80::...`).
You can often just:

- plug the cable
- use `ping6` / `ssh` with the link-local address (needs interface scope)

### Option 2: quick static IPv4

On machine A:

```
sudo dap2p eth up eno1 192.168.77.1/24
```

On machine B:

```
sudo ip link set dev eno1 up
sudo ip addr add 192.168.77.2/24 dev eno1
ping 192.168.77.1
```

## USB-C peer-to-peer: reality check

Two laptops connected with a plain USB-C cable are usually **host-host**.
That *does not* create a network link automatically.

Working alternatives:
- Ethernet
- Thunderbolt/USB4 networking (if supported)
- USB gadget networking (one side must be gadget-capable)
- a proper USB bridge cable

## USB gadget networking

On the gadget-capable device:

```
sudo dap2p gadget net
```

You should get a `usb0` interface on the gadget side.
The host side will see a new USB Ethernet interface.
