# Wayland / X11 cheatsheet

## What session am I on?
```bash
dax status
echo $XDG_SESSION_TYPE
loginctl show-session "$XDG_SESSION_ID" -p Type -p Desktop
```

## Is XWayland running?
```bash
pgrep -x Xwayland && echo "XWayland running"
```

## Common “force X11” env vars
GTK:
```bash
GDK_BACKEND=x11 app
```

Qt:
```bash
QT_QPA_PLATFORM=xcb app
```

## Screen sharing on Wayland: what to check
- PipeWire running (user service)
- xdg-desktop-portal running (user service)
- Correct portal backend for your compositor/DE

Useful:
```bash
systemctl --user status pipewire
systemctl --user status xdg-desktop-portal
```

