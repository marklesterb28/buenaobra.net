#!/usr/bin/env python3
"""Build site/assets/homelab.svg, the public homelab network diagram for buenaobra.net.

Adapted from the homelab repo's docs/diagram/build.py (same layout and palette), with the
data cut down so it is safe to publish: no IP addresses, VM ids, hardware specs, device
inventory, subdomain list, second domain, or download tooling.

Run:  uv run python tools/build-diagram.py
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "site" / "assets" / "homelab.svg"
W, H = 1800, 1340

# Palette and fonts match buenaobra.net
BG, BG2, PANEL, LINE = "#141614", "#1c1e1c", "#232623", "#3d453d"
TEXT, DIM, NEON, MINT, LITE = "#e4efe4", "#9fb09f", "#00ff41", "#c8ffd4", "#7dff9e"
CF, TS = "#ffb347", "#5ad1ff"  # Cloudflare amber, Tailscale cyan
MONO = "'JetBrains Mono', 'Cascadia Code', Consolas, ui-monospace, monospace"

out = []


def add(s):
    out.append(s)


def text(x, y, s, size=13, fill=TEXT, weight=400, anchor="start"):
    add(f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-weight="{weight}" '
        f'text-anchor="{anchor}">{escape(s)}</text>')


def box(x, y, w, h, stroke=LINE, fill=PANEL, dash=None, r=4, sw=1.2):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" '
        f'stroke="{stroke}" stroke-width="{sw}"{d}/>')


def line(points, stroke=NEON, sw=2, dash=None, arrow=False):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    m = ' marker-end="url(#arrow)"' if arrow else ""
    pts = " ".join(f"{x},{y}" for x, y in points)
    add(f'<polyline points="{pts}" fill="none" stroke="{stroke}" stroke-width="{sw}" '
        f'stroke-linejoin="round"{d}{m}/>')


def badge(x, y, label, color):
    w = 8 * len(label) + 12
    add(f'<rect x="{x}" y="{y - 13}" width="{w}" height="18" rx="2" fill="none" '
        f'stroke="{color}" stroke-width="1"/>')
    text(x + 6, y, label, size=11, fill=color, weight=600)
    return w


def node(x, y, w, h, name, meta, items, tags=(), accent=NEON):
    """A server card: title bar, one meta line, then service lines."""
    box(x, y, w, h, stroke=LINE, fill=BG2)
    add(f'<rect x="{x}" y="{y}" width="4" height="{h}" fill="{accent}"/>')
    text(x + 16, y + 26, name, size=17, fill=accent, weight=700)
    bx = x + w - 10
    for label, color in reversed(tags):
        bx -= 8 * len(label) + 12
        badge(bx, y + 25, label, color)
        bx -= 6
    text(x + 16, y + 46, meta, size=12, fill=DIM)
    add(f'<line x1="{x + 16}" y1="{y + 56}" x2="{x + w - 16}" y2="{y + 56}" stroke="{LINE}"/>')
    yy = y + 78
    for it in items:
        name_, note = it if isinstance(it, tuple) else (it, "")
        if name_.startswith("  "):
            text(x + 34, yy, name_.strip(), size=12, fill=DIM)
        else:
            text(x + 16, yy, "›", size=13, fill=NEON, weight=700)
            text(x + 30, yy, name_, size=13, fill=TEXT, weight=600)
            if note:
                text(x + 30 + 8 * len(name_) + 10, yy, note, size=12, fill=DIM)
        yy += 19


# ------------------------------------------------------------------ data (public-safe)
TAILNET = ("tailnet", TS)
TUNNEL = ("tunnel", CF)

VMS = [
    ("dns", "name resolution", [
        ("AdGuard Home", "DNS + ad blocking"),
        "  answers *.buenaobra.net → caddy",
        ("Beszel agent", "metrics"),
    ], (TAILNET,)),
    ("caddy", "the front door", [
        ("Traefik", "reverse proxy, HTTPS"),
        "  wildcard cert, Let's Encrypt DNS-01",
        "  forward_auth → Tinyauth",
        "  LAN + tailnet listener",
        ("Beszel agent", "metrics"),
    ], (TAILNET,)),
    ("hub", "git, identity and management", [
        ("Forgejo", "git, infra as code"),
        ("Pocket ID", "passkeys, OIDC"),
        ("Tinyauth", "forward auth"),
        ("Homepage", "dashboard"),
        ("Gatus", "uptime checks"),
        ("ntfy", "push alerts"),
        ("Beszel", "metrics hub"),
        ("Renovate", "weekly update PRs"),
        ("Ansible", "config + patching"),
    ], (TAILNET,)),
    ("psa", "my MSP practice", [
        ("ITFlow", "PSA, tickets, invoices"),
        "  Apache + MariaDB",
        ("cloudflared", "→ public PSA site"),
        "  Cloudflare Access in front",
    ], (TUNNEL,)),
    ("vault", "secrets", [
        ("Vaultwarden", "passwords"),
        "  tailnet only, no public name",
        ("Beszel agent", "metrics"),
    ], (TAILNET,)),
    ("apps", "things I build", [
        ("ChoreCast", "household chores app"),
        "  own repo, Docker Compose",
    ], ()),
    ("radio", "music for the family", [
        ("SUB/WAVE", "24/7 radio with an AI DJ"),
        "  plays the Navidrome library",
        "  free LLM writes, local voice speaks",
        ("cloudflared", "→ public, admin behind Access"),
    ], (TUNNEL,)),
]

# ------------------------------------------------------------------ draw
# No fixed width/height: opened on its own the diagram scales to fit the
# window; embedded, the <img> (or its CSS) sets the size.
add(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
    f'preserveAspectRatio="xMidYMid meet" style="background:{BG}" '
    f'font-family="{MONO}" role="img" aria-labelledby="t d">')
add('<title id="t">Lester\'s homelab network</title>'
    '<desc id="d">Cloudflare and Tailscale at the edge, an ISP router and one flat LAN, a Proxmox host '
    'running a VM per role (dns, caddy, hub, psa, vault, apps, radio) and a Windows desktop for media, '
    'with single sign-on through Pocket ID and automation through Ansible, Renovate, Gatus, Beszel and ntfy.</desc>')
add('<defs>'
    '<pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse">'
    '<path d="M24 0H0V24" fill="none" stroke="#1f241f" stroke-width="1"/></pattern>'
    '<marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
    f'<path d="M0 0L10 5L0 10z" fill="{NEON}"/></marker>'
    '</defs>')
add(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
add(f'<rect width="{W}" height="{H}" fill="url(#grid)"/>')

# Title
text(40, 52, "HOMELAB//NET", size=30, fill=NEON, weight=800)
text(290, 52, "network diagram", size=20, fill=MINT)
text(40, 76, "> one Proxmox host, one Windows desktop, one flat LAN, Tailscale for away-from-home", size=13, fill=DIM)
text(W - 40, 52, "Nov 2026", size=14, fill=DIM, anchor="end")
text(W - 40, 72, "a VM per role · managed as code", size=11, fill=DIM, anchor="end")

# ---- top row: internet, Cloudflare, Tailscale, legend
add(f'<path d="M95 205 a38 38 0 0 1 10-74 a52 52 0 0 1 98-14 a40 40 0 0 1 70 30 '
    f'a34 34 0 0 1 -6 58 z" fill="{BG2}" stroke="{LINE}" stroke-width="1.5"/>')
text(188, 168, "Internet", size=16, fill=TEXT, weight=700, anchor="middle")
text(188, 188, "ISP fiber", size=12, fill=DIM, anchor="middle")

cx, cy, cw, ch = 330, 100, 560, 200
box(cx, cy, cw, ch, stroke=CF, fill=PANEL, dash="6 4")
text(cx + 16, cy + 28, "Cloudflare", size=17, fill=CF, weight=700)
text(cx + 130, cy + 28, "DNS · registrar · edge", size=12, fill=DIM)
text(cx + 16, cy + 56, "buenaobra.net", size=14, fill=TEXT, weight=700)
for i, s in enumerate([
    "Pages: this resume site",
    "Email Routing → my inbox",
    "*.buenaobra.net → caddy,",
    "  reachable only over Tailscale",
    "radio: Tunnel → radio, public",
]):
    text(cx + 16, cy + 78 + i * 19, s, size=12, fill=DIM if s.startswith("  ") else TEXT)
text(cx + 300, cy + 56, "PSA site", size=14, fill=TEXT, weight=700)
for i, s in enumerate([
    "Tunnel → psa (ITFlow)",
    "Access: email one-time PIN",
    "no open ports at home",
]):
    text(cx + 300, cy + 78 + i * 19, s, size=12, fill=TEXT)
text(cx + 16, cy + ch - 14, "DNSSEC · TLS 1.2+ · Full (strict) · DMARC", size=11, fill=DIM)

tx, ty, tw, th = 910, 100, 470, 200
box(tx, ty, tw, th, stroke=TS, fill=PANEL, dash="6 4")
text(tx + 16, ty + 28, "Tailscale", size=17, fill=TS, weight=700)
text(tx + 120, ty + 28, "WireGuard mesh · MagicDNS", size=12, fill=DIM)
for i, s in enumerate([
    "Servers are tagged; my own devices join",
    "Least-privilege grants, tested on every save",
    "Away from home: Tailscale on, then the",
    "  same https://*.buenaobra.net names work",
    "Vaultwarden is reachable only here",
]):
    text(tx + 16, ty + 56 + i * 21, s, size=12, fill=DIM if s.startswith("  ") else TEXT)

lx, ly, lw, lh = 1400, 100, 360, 200
box(lx, ly, lw, lh, stroke=LINE, fill=PANEL)
text(lx + 16, ly + 28, "Legend", size=15, fill=MINT, weight=700)
line([(lx + 16, ly + 52), (lx + 76, ly + 52)], stroke=NEON, sw=3)
text(lx + 90, ly + 56, "Ethernet, 1 Gbps LAN", size=12)
line([(lx + 16, ly + 80), (lx + 76, ly + 80)], stroke=CF, sw=2, dash="7 5")
text(lx + 90, ly + 84, "Cloudflare Tunnel", size=12)
line([(lx + 16, ly + 108), (lx + 76, ly + 108)], stroke=TS, sw=2, dash="2 4")
text(lx + 90, ly + 112, "Tailscale (encrypted)", size=12)
badge(lx + 16, ly + 140, "SSO", NEON)
text(lx + 90, ly + 140, "Pocket ID passkey first", size=12)
badge(lx + 16, ly + 166, "tailnet", TS)
text(lx + 90, ly + 166, "node is on Tailscale", size=12)
badge(lx + 16, ly + 190, "tunnel", CF)
text(lx + 90, ly + 190, "published via Cloudflare", size=12)

# ---- router and LAN backbone
rx, ry, rw, rh = 120, 330, 420, 64
box(rx, ry, rw, rh, stroke=NEON, fill=BG2)
text(rx + 16, ry + 26, "ISP router", size=15, fill=NEON, weight=700)
text(rx + 16, ry + 48, "gateway · DHCP reservations · one flat LAN", size=12, fill=DIM)
line([(188, 210), (188, ry)], stroke=NEON, sw=3)
BACKBONE_Y = 430
line([(60, BACKBONE_Y), (W - 60, BACKBONE_Y)], stroke=NEON, sw=3)
line([(330, ry + rh), (330, BACKBONE_Y)], stroke=NEON, sw=3)
text(W - 60, BACKBONE_Y - 10, "home LAN · 1 Gbps", size=12, fill=LITE, anchor="end")

# ---- Proxmox host with VM cards
px, py, pw, ph = 40, 470, 1100, 610
box(px, py, pw, ph, stroke=NEON, fill="#171a17", dash="8 5", sw=1.5)
text(px + 18, py + 30, "pve", size=20, fill=NEON, weight=800)
text(px + 70, py + 30, "Proxmox VE", size=14, fill=TEXT, weight=600)
text(px + 18, py + 52, "a VM per role · Docker Compose inside · everything defined in git", size=12, fill=DIM)
line([(px + 540, BACKBONE_Y), (px + 540, py)], stroke=NEON, sw=3)

cw_, gap = 340, 20
cols = [px + 20, px + 20 + cw_ + gap, px + 20 + 2 * (cw_ + gap)]
placement = {
    "dns": (cols[0], py + 70, 170), "psa": (cols[0], py + 260, 170),
    "caddy": (cols[1], py + 70, 200), "vault": (cols[1], py + 290, 150),
    "hub": (cols[2], py + 70, 250), "apps": (cols[2], py + 335, 105),
    "radio": (cols[0], py + 450, 150),
}
for name, meta, items, tags in VMS:
    x, y, h = placement[name]
    node(x, y, cw_, h, name, meta, items, tags)

# names box beside the radio card
rtx, rty = cols[1], py + 450
box(rtx, rty, pw - 40 - cw_ - gap, 150, stroke=LINE, fill=BG2)
text(rtx + 16, rty + 26, "https://<service>.buenaobra.net", size=14, fill=MINT, weight=700)
for i, t in enumerate([
    "every name → caddy → service · one wildcard certificate",
    "admin UIs sit behind Pocket ID single sign-on",
    "nothing is port-forwarded; names resolve at home or over Tailscale",
    "only the PSA and the radio are public, through Cloudflare Tunnels",
]):
    yy = rty + 56 + i * 24
    text(rtx + 16, yy, "›", size=13, fill=NEON, weight=700)
    text(rtx + 30, yy, t, size=12)
badge(rtx + 420, rty + 80, "SSO", NEON)

# Tunnel: Cloudflare → psa (around the left edge)
line([(cx + 340, cy + ch), (cx + 340, 316), (26, 316), (26, py + 345), (cols[0], py + 345)],
     stroke=CF, sw=2, dash="7 5")
line([(26, py + 345), (26, py + 525), (cols[0], py + 525)], stroke=CF, sw=2, dash="7 5")  # → radio

# ---- desktop
kx, ky, kw, kh = 1170, 470, 590, 330
box(kx, ky, kw, kh, stroke=NEON, fill="#171a17", dash="8 5", sw=1.5)
text(kx + 18, ky + 30, "desktop", size=20, fill=NEON, weight=800)
text(kx + 126, ky + 30, "Windows 11 Pro", size=14, fill=TEXT, weight=600)
text(kx + 18, ky + 52, "daily driver · the media library lives here", size=12, fill=DIM)
line([(kx + 300, BACKBONE_Y), (kx + 300, ky)], stroke=NEON, sw=3)
node(kx + 20, ky + 70, 270, 160, "media", "native Windows apps", [
    ("Jellyfin", "movies, TV"),
    ("Navidrome", "music"),
], ())
node(kx + 300, ky + 70, 270, 160, "WSL2", "Ubuntu + Docker", [
    ("ChoreCast", "Android builds"),
    "  SDK + adb to TV/phone",
    ("dev tools", "git, python"),
], ())
node(kx + 20, ky + 240, 550, 72, "workstation", "Claude Code · agentwatch (session viewer) · infra repo", [], (TAILNET,))

# ---- clients
clx, cly, clw, clh = 1170, 830, 590, 250
box(clx, cly, clw, clh, stroke=TS, fill="#171a17", dash="2 4", sw=1.5)
text(clx + 18, cly + 30, "clients", size=20, fill=TS, weight=800)
text(clx + 120, cly + 30, "at home on the LAN, away over Tailscale", size=13, fill=DIM)
line([(W - 60, BACKBONE_Y), (W - 22, BACKBONE_Y), (W - 22, cly + 100), (clx + clw, cly + 100)],
     stroke=TS, sw=2, dash="2 4")
text(W - 28, cly + 92, "Wi-Fi", size=11, fill=TS, anchor="end")
for i, (d, apps) in enumerate([
    ("TV", "Jellyfin · music"),
    ("phones + tablet", "Jellyfin · music · browser"),
    ("browsers", "dashboard start page"),
    ("radio players", "VLC · browser · the family's phones"),
]):
    y = cly + 66 + i * 40
    box(clx + 20, y - 22, clw - 40, 32, stroke=LINE, fill=BG2)
    text(clx + 34, y, d, size=13, fill=TEXT, weight=700)
    text(clx + 230, y, apps, size=12, fill=DIM)
    if d not in ("browsers", "radio players"):
        badge(clx + clw - 100, y, "tailnet", TS)

# ---- bottom: request flow and automation
fy = 1110
box(40, fy, 1100, 190, stroke=LINE, fill=PANEL)
text(58, fy + 30, "How a request gets in", size=15, fill=MINT, weight=700)
steps = [
    ("browser", "https://<svc>…"),
    ("AdGuard", "name → caddy"),
    ("Traefik", "TLS, routing"),
    ("Tinyauth", "signed in?"),
    ("Pocket ID", "passkey"),
    ("service", "dashboard, etc."),
]
sw_, sg = 158, 22
for i, (a, b) in enumerate(steps):
    x = 58 + i * (sw_ + sg)
    box(x, fy + 52, sw_, 62, stroke=NEON if i in (3, 4) else LINE, fill=BG2)
    text(x + sw_ / 2, fy + 78, a, size=14, fill=NEON, weight=700, anchor="middle")
    text(x + sw_ / 2, fy + 99, b, size=12, fill=DIM, anchor="middle")
    if i < len(steps) - 1:
        line([(x + sw_ + 2, fy + 83), (x + sw_ + sg - 3, fy + 83)], stroke=NEON, sw=2, arrow=True)
text(58, fy + 142, "Away from home the first hop is Tailscale, so the same names work from anywhere I'm signed in.",
     size=12, fill=DIM)
text(58, fy + 164, "Apps with their own OIDC (Gatus, Forgejo, Beszel, Proxmox) sign in with Pocket ID directly.",
     size=12, fill=DIM)

box(1170, fy, 590, 190, stroke=LINE, fill=PANEL)
text(1188, fy + 30, "Keeping it running", size=15, fill=MINT, weight=700)
for i, (a, b) in enumerate([
    ("Ansible", "config, secrets in Vault, monthly patching"),
    ("unattended-upgrades", "daily security updates"),
    ("Renovate", "pinned images, weekly PRs"),
    ("Gatus + Beszel", "checks and metrics"),
    ("ntfy", "alerts to my phone, incl. Proxmox"),
    ("Pocket ID", "one passkey for every admin UI"),
]):
    y = fy + 58 + i * 21
    text(1188, y, "›", size=13, fill=NEON, weight=700)
    text(1202, y, a, size=13, fill=TEXT, weight=600)
    text(1202 + 8 * len(a) + 12, y, b, size=12, fill=DIM)

add("</svg>")
OUT.write_text("\n".join(out), encoding="utf-8")
print(f"wrote {OUT} ({OUT.stat().st_size // 1024} KB)")

# The public homelab-showcase repo shows the same diagram. If it is checked
# out next to this repo, keep its copy identical (then commit it there).
SHOWCASE = OUT.parents[2].parent / "homelab-showcase" / "homelab.svg"
if SHOWCASE.parent.is_dir():
    SHOWCASE.write_bytes(OUT.read_bytes())
    print(f"wrote {SHOWCASE}")
