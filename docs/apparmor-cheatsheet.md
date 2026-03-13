# AppArmor cheatsheet

## Status

```bash
aa-status
daapparmor status
```

## See denials

```bash
daapparmor denials --since 1h
journalctl -k --since 1h | grep 'apparmor="DENIED"'
```

## The “make it stop yelling” workflow

```bash
sudo daapparmor complain <profile>
# run your app / reproduce the failure
sudo daapparmor allow
sudo daapparmor enforce <profile>
```

## Generate a new profile

```bash
sudo daapparmor gen /usr/bin/foo
```

## Reload AppArmor

```bash
sudo daapparmor reload
```

