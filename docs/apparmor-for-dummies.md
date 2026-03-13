# AppArmor for dummies (a.k.a. “just let me allow the thing”)

AppArmor is **mandatory access control** (MAC) for Linux: it restricts what a process can do
*even if file permissions would otherwise allow it*. It’s **path-based** (unlike SELinux labels),
so renaming/moving binaries and files can matter.

This doc is intentionally practical.

---

## The 3 modes that matter

- **enforce**: AppArmor *blocks* disallowed actions, and logs denials.
- **complain**: AppArmor does **not block**, but **logs** what *would have been denied*.
- **disabled**: profile isn’t applied.

For profile development you almost always want: **complain → test → logprof → enforce**.

---

## Where profiles live

Typically: `/etc/apparmor.d/`

Some distros name profiles like paths (e.g. `usr.bin.man`) and inside the file you’ll see a `profile ... { }` block.

---

## Where denials show up

Most commonly in the kernel/audit logs. On systemd systems:

```bash
journalctl -k --since 1h | grep 'apparmor="DENIED"'
```

Or use the wrapper:

```bash
sudo daapparmor denials --since 1h
```

---

## “apparmor allow” (the workflow)

If you already have a profile and you’re getting DENIED messages:

1) Put it in complain mode while you test:

```bash
sudo daapparmor complain <profile-or-file>
```

2) Re-run the thing that’s failing (generate denials)

3) Update profiles based on the logs:

```bash
sudo daapparmor allow
```

This runs **aa-logprof**, which is interactive: it shows denials and suggests minimal rules.

4) Put it back into enforce mode:

```bash
sudo daapparmor enforce <profile-or-file>
```

---

## Generating a new profile for a binary

If you don’t even have a profile yet, this is usually easiest:

```bash
sudo daapparmor gen /usr/bin/myapp
```

That wraps **aa-genprof**.

---

## Big gotchas

- **Don’t “allow everything”**. It defeats the point. Prefer the smallest rules that make the app work.
- Path-based MAC means weird things can happen when paths change (symlinks, bind mounts, snaps/flatpaks).
- Profiles can stack with confinement from containers / systemd / seccomp.

---

## When you should just disable a profile

Sometimes the profile shipped by a package is broken for your config and you need uptime more than confinement.
Disabling is a tradeoff:

```bash
sudo daapparmor disable <profile-or-file>
```

Then revisit later and fix it properly (complain → allow → enforce).

