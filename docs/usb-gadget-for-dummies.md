# USB gadget mode for dummies

USB gadget mode means: **your Linux machine pretends to be a USB device**.

This only works on hardware that supports USB device mode (common on SBCs like Raspberry Pi).
Most laptops do not support it.

Check:
- `/sys/class/udc` exists and is non-empty

## Mass storage gadget (file-backed)

Create a FAT image file:

```
dadd fatimg create /tmp/share.img --size 8G --label SHARE
```

Expose it as a USB thumb drive (gadget side):

```
sudo dap2p gadget msd /tmp/share.img
```

Plug into the host. It should see a new USB disk.

⚠️  Don’t mount it read-write on both sides at once. You will corrupt it.

## USB Ethernet gadget

```
sudo dap2p gadget net
```

Then configure `usb0` with DHCP or a static address.
