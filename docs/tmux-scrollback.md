# tmux/screen scrollback that feels normal

## tmux

Two things matter:
- `history-limit` (tmux’s scrollback)
- `mouse on` (scrollwheel scrolls)

Get a config snippet:

```
datmux tmux
```

Append it to `~/.tmux.conf`:

```
datmux tmux --write
```

## GNU screen

Get a snippet:

```
datmux screen
```

Append to `~/.screenrc`:

```
datmux screen --write
```

If you enable the optional `ti@:te@` tweak, full-screen apps may behave differently.
