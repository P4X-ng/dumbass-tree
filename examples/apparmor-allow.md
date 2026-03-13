# AppArmor “allow” example (complain → logprof → enforce)

This is the least-painful loop when AppArmor is breaking an app.

## 1) See denials

```bash
sudo daapparmor denials --since 1h
```

## 2) Put the profile in complain mode (so nothing is blocked while you test)

```bash
sudo daapparmor complain <profile>
```

## 3) Reproduce the problem (generate denials)

Run the app again.

## 4) Update profiles based on logs (interactive)

```bash
sudo daapparmor allow
```

## 5) Enforce again

```bash
sudo daapparmor enforce <profile>
```

