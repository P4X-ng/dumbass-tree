# iproute2 for dummies (without dumbing it down)

`iproute2` is the correct toolset. It just loves to speak in flags.

## Use these first

```
ip -br link
ip -br addr
ip -br route
```

`-br` = brief. It’s the difference between “readable” and “why is my screen screaming”.

## Common words in `ip addr`

- `scope global` = routable address
- `scope link` = link-local (same L2 segment only)
- `dynamic` = learned dynamically (DHCP/SLAAC)
- `noprefixroute` = don’t add an automatic connected route for the prefix
- `tentative` = IPv6 DAD not finished yet
- `deprecated` = still present but should not be used for new connections

## Tools in this repo

- `daip brief`
- `daip explain <words...>`
- `daip cheat`
