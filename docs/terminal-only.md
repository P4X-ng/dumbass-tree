# Living in your terminal (browser + “VS Code” without leaving)

You can get *pretty* close to “no GUI apps” if you treat this as two problems:

1) **Reduce how often you need a browser** (RSS, CLI tools, APIs, git, etc.)
2) When you do need a browser, use the **least-bad terminal option** (or a minimal GUI browser with great keybindings)

---

## Browser options in/for the terminal

### 1) Carbonyl (most “real web” in a terminal)
Carbonyl is Chromium rendered inside a terminal grid. It can handle a lot of modern web stuff.

If you have it:

```bash
dabrowse --engine carbonyl https://github.com
```

### 2) Browsh (modern sites → text)
Browsh uses headless Firefox and renders pages as text. Great for bandwidth + SSH workflows.

```bash
dabrowse --engine browsh https://news.ycombinator.com
```

### 3) Classic text browsers (best for docs, wikis, simple sites)
- `w3m`
- `links`
- `lynx`

```bash
dabrowse --engine w3m https://example.com
```

---

## “Browser solves VS Code” (the realistic approach)

If you *must* have VS Code features, you have 3 terminal-ish options:

### Option A: just use a terminal editor with LSP
- **neovim** + built-in LSP (or `coc.nvim`)
- **helix**
- **emacs** (if that’s your thing)

This is the “no browser required” path.

### Option B: run VS Code remotely, keep local minimal
- ssh into a dev box
- run everything in tmux
- use a minimal browser only when needed

### Option C: code-server / web IDE + terminal browser
If your terminal browser can handle the web IDE, you can keep the “app” in terminal.
This is the most fragile option (JS-heavy UIs can be rough).

---

## Terminal quick wins

- **tmux** (or zellij): never lose your session
- **fzf**: fuzzy search everything
- **ripgrep (rg)**: fast code search
- **fd**: sane find
- **jq**: JSON surgery
- **lazygit**: a TUI that replaces 90% of “open GUI git client”
- **btop**: system monitor that doesn’t suck

---

## A pattern that works: remote browser
If you hate running browsers on your workstation, run the browser on a box and use it over SSH/mosh.
This was basically Browsh’s original reason to exist.

