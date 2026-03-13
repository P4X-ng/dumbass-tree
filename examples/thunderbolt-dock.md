# Example: Thunderbolt dock that “half works”

Symptom:
- external monitor works
- dock USB/ethernet does not

Steps:

```bash
dathunderbolt status
dathunderbolt list
dathunderbolt info <uuid-from-list>

# If you trust the device:
sudo dathunderbolt enroll <uuid> --policy auto

# Unplug/replug the dock
```

Check logs:
```bash
journalctl -u boltd -b
```
