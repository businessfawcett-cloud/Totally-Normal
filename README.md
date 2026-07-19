# The Invisible Site

A website generated entirely from a [Whitespace](https://en.wikipedia.org/wiki/Whitespace_(programming_language)) program.

The source code (`site.ws`) contains **zero visible characters** — only spaces, tabs, and linefeeds.

## How to run

```bash
# Generate the whitespace file from HTML
python text_to_ws.py site.html site.ws

# Serve it as a website
python serve_ws.py site.ws
# Open http://localhost:8080

# Or just run it directly
python run_ws.py site.ws > output.html
```

## File structure

```
site.html         # The readable HTML source (for editing)
site.ws           # The invisible Whitespace program (169KB of whitespace)
text_to_ws.py     # Converts text files to Whitespace programs
run_ws.py         # Whitespace interpreter
serve_ws.py       # Web server that runs WS and serves the output
```

## Why?

Because we can. The Whitespace language (2003) is Turing-complete and can compute anything. Encoding a website in it proves that even the most useless tools can produce something visible.

The `site.ws` file will appear empty on GitHub. No syntax highlighting. No diffs. Just vibes.

## Stack

- **Whitespace** — the programming language
- **Python** — interpreter + web server
- **HTML/CSS/JS** — the actual website content
