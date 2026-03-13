# Wayland for dummies (and X11 for grumpy people)

If you’ve ever thought:

> “I just want my windows to show up. Why is this a thesis.”

…welcome.

---

## The one-line definition

- **X11 / Xorg**: the old “display server” world.
- **Wayland**: the newer “display protocol + compositor-is-the-server” world.

Wayland is not a single program. It’s a protocol + architecture.

---

## The model that makes it click

### X11 (classic)

- You run an **X server** (`Xorg`)
- You run a **window manager**
- Optionally you run a **compositor** (picom, etc.)
- Apps talk X11 to the X server

X11 was built with remote/network transparency as a first-class feature (ssh -X etc).

### Wayland (modern)

- You run a **compositor**, and it *is* the display server  
  Examples: GNOME **mutter**, KDE **kwin**, **sway**, **hyprland**, **weston**

Apps talk Wayland to the compositor.

---

## “Ok but why do people bitch about Wayland?”

Because Wayland changes a bunch of implicit X11 behaviors:

### 1) Global stuff is no longer “free”
On X11, lots of clients could:
- watch all keyboard input
- snoop other windows
- capture the screen

Wayland shifts a bunch of these powers into the compositor / “portal” APIs.

This is *more secure*, but it breaks older assumptions.

### 2) Screen sharing / screen recording is different
Wayland typically expects:
- PipeWire
- xdg-desktop-portal (+ a backend for your compositor/DE)

On modern desktops this usually “just works”… until it doesn’t.

### 3) Remote display workflows differ
X11’s `ssh -X` workflow is baked into the protocol.
Wayland doesn’t do that the same way. People use:
- RDP/VNC style tools
- waypipe / compositor-specific remoting

If your whole life is `ssh -X`, X11 will feel easier.

---

## XWayland (the bridge)

Wayland sessions usually run **XWayland**, which is basically:
- a full X11 server
- running *as a Wayland client*

This is what lets legacy X11 apps keep working.

---

## Quick: how do I know what I’m on?

### Terminal signals
```bash
echo $XDG_SESSION_TYPE     # x11 or wayland (usually)
echo $WAYLAND_DISPLAY      # set on Wayland
echo $DISPLAY              # set on X11 (and also often set on Wayland via XWayland)
```

### dumbass-tree helper
```bash
dax status
```

---

## What should *you* pick?

### If you want the simplest “it works” for weird tools:
- Try **X11** first

### If you want a modern desktop with better isolation:
- Try **Wayland** (and expect a few papercuts)

My recommendation: treat them like kernels.
You don’t need loyalty. You need results.

---

## Common fixes / tricks

### Force a single app to use X11 (inside a Wayland session)
Sometimes needed for old tooling.

GTK:
```bash
GDK_BACKEND=x11 your-app
```

Qt:
```bash
QT_QPA_PLATFORM=xcb your-app
```

(Yes it’s cursed. No you’re not alone.)

---

## Where to go next

- If you want a terminal-first desktop: look at sway (Wayland) or i3 (X11)
- If you want “just give me a DE”: GNOME/KDE handle most of the pain for you

