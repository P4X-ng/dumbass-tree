# Work in RAM, then save back

If you’re doing builds / experiments that churn disks, tmpfs is your friend.

This repo has:

```
darunram shell ./myproject --persist
```

It copies the dir to `/dev/shm`, drops you into a shell there, and on exit
(optionally) rsyncs back.

This is not true COW overlayfs, but it’s stupid-simple and works without root.
