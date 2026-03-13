# DNS for dummies (Ubuntu / systemd-resolved / NetworkManager)

If you’ve ever looked at `/etc/resolv.conf` and seen:

```
nameserver 127.0.0.53
```

…and immediately thought “what the hell”, you’re not alone.

That line usually means: **your system is using `systemd-resolved` as a local DNS stub**.
It does *not* mean your upstream DNS server is literally 127.0.0.53.

## The 4 common `/etc/resolv.conf` modes

On systemd-based distros, `/etc/resolv.conf` is often a symlink:

- **stub mode (recommended default on many distros)**  
  `/etc/resolv.conf -> /run/systemd/resolve/stub-resolv.conf`  
  Shows only `127.0.0.53` (the local stub), and search domains.

- **static stub file**  
  `/etc/resolv.conf -> /usr/lib/systemd/resolv.conf` (or `/lib/...`)  
  Also points to `127.0.0.53`, but usually lacks search domains.

- **“real DNS list” mode (bypass stub)**  
  `/etc/resolv.conf -> /run/systemd/resolve/resolv.conf`  
  Contains the upstream DNS server IPs.  
  Traditional apps bypass `systemd-resolved` and talk to upstream servers directly.

- **classic / managed by something else**  
  `/etc/resolv.conf` is a normal file (or managed by `resolvconf`, etc).  
  In this mode `systemd-resolved` may read it rather than manage it.

## The one command that ends confusion

```
resolvectl status
```

That shows the real per-link DNS servers and search domains.

## “Make it not stupid” recipes

### Recipe A: Keep `systemd-resolved`, but make `/etc/resolv.conf` human-readable

```
sudo ln -sf /run/systemd/resolve/resolv.conf /etc/resolv.conf
```

Tradeoff: classic resolv.conf format can’t express “split DNS per interface” well.

### Recipe B: Keep stub mode, but stop guessing

Keep the symlink to `stub-resolv.conf`, and just use:

```
resolvectl status
```

### Recipe C: Disable `systemd-resolved` cleanly (hard mode)

If NetworkManager is configured to use `systemd-resolved`, you **must** change NM first.

Create a drop-in:

`/etc/NetworkManager/conf.d/99-dns.conf`

```
[main]
dns=default
```

Then:

```
sudo systemctl restart NetworkManager
sudo systemctl disable --now systemd-resolved
sudo systemctl mask systemd-resolved
```

Finally, make sure `/etc/resolv.conf` is a regular file again (or managed by resolvconf).

## Tools in this repo

- `dadns status` — shows symlinks and DNS wiring
- `dadns set-mode stub|real|static` — choose a mode with safety rails
- `dadns nm-dns systemd-resolved|default|none` — toggle NetworkManager’s DNS plugin
