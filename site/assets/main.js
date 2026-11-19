/* buenaobra.net — sprites, boot sequence, plain mode, typing tagline, terminal */
(() => {
  "use strict";

  const root = document.documentElement;
  const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const store = {
    get(k) { try { return window.localStorage.getItem(k); } catch { return null; } },
    set(k, v) { try { window.localStorage.setItem(k, v); } catch { /* ignore */ } },
    sget(k) { try { return window.sessionStorage.getItem(k); } catch { return null; } },
    sset(k, v) { try { window.sessionStorage.setItem(k, v); } catch { /* ignore */ } },
  };

  /* ---------- Pixel sprites (rendered as crisp SVG) ---------- */
  const PAL = {
    k: "#050605", h: "#1a1f1a", s: "#c68a5b", c: "#00ff41", m: "#0b6b22",
    w: "#e6ffe0", y: "#c8ffd4", g: "#00ff41",
  };
  const SPRITES = {
    avatar: [
      "....kkkkkkkk....",
      "...khhhhhhhhk...",
      "..khhhhhhhhhhk..",
      "..khhsssssshhk..",
      ".ckhsssssssshkc.",
      ".ckssksssskssck.",
      ".ckssssssssssck.",
      ".cksssskksssskc.",
      "..kssssssssssk..",
      "...kssssssssk...",
      "....kkssssk.....",
      "..kkmmmmmmmmkk..",
      ".kmmmmccmmmmmmk.",
      ".kmmmmmcmmmmmmk.",
      ".kmmmmmmmmmmmmk.",
      ".kkkkkkkkkkkkkk.",
    ],
    moto: [
      "..........kkk...",
      "...kkkk..kcc....",
      "..kmmmmkkkcc....",
      ".kmmmmmmmmmkk...",
      "kkkkmmmmmmmmkk..",
      ".kwwk..kk..kwwk.",
      "kw..wk....kw..wk",
      "kw..wk....kw..wk",
      ".kwwk......kwwk.",
    ],
  };
  function renderSprite(el) {
    const rows = SPRITES[el.dataset.sprite];
    if (!rows) return;
    const scale = Number(el.dataset.scale) || 8;
    const w = Math.max(...rows.map((r) => r.length));
    const h = rows.length;
    let rects = "";
    rows.forEach((row, y) => {
      [...row].forEach((ch, x) => {
        if (PAL[ch]) rects += `<rect x="${x}" y="${y}" width="1" height="1" fill="${PAL[ch]}"/>`;
      });
    });
    el.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${w} ${h}" width="${w * scale}" height="${h * scale}" aria-hidden="true">${rects}</svg>`;
  }
  document.querySelectorAll(".sprite[data-sprite]").forEach(renderSprite);

  /* ---------- Plain mode ---------- */
  const toggle = document.getElementById("mode-toggle");
  function setMode(mode, save) {
    if (mode === "plain") root.setAttribute("data-mode", "plain");
    else root.removeAttribute("data-mode");
    const plain = mode === "plain";
    toggle.setAttribute("aria-pressed", String(plain));
    toggle.textContent = plain ? "neon mode" : "plain mode";
    if (save) store.set("mode", mode);
  }
  // ?mode=plain (the link on the PDF resume) opens the professional view without changing the saved choice.
  const asked = new URLSearchParams(location.search).get("mode");
  setMode(asked === "plain" || asked === "neon" ? asked : store.get("mode") === "plain" ? "plain" : "neon", false);
  toggle.addEventListener("click", () => setMode(root.dataset.mode === "plain" ? "neon" : "plain", true));

  /* ---------- Digital rain (neon mode, motion allowed) ---------- */
  (function rain() {
    const cv = document.createElement("canvas");
    cv.className = "rain"; cv.setAttribute("aria-hidden", "true");
    document.body.prepend(cv);
    const ctx = cv.getContext("2d");
    const glyphs = "アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワン0123456789:.=*+<>|";
    const size = 16;
    let drops = [], w = 0, h = 0, last = 0;
    function fit() {
      w = cv.width = window.innerWidth; h = cv.height = window.innerHeight;
      const cols = Math.ceil(w / size);
      drops = Array.from({ length: cols }, () => Math.floor(Math.random() * -h / size));
      ctx.fillStyle = "#1c1e1c"; ctx.fillRect(0, 0, w, h);
    }
    function frame(t) {
      requestAnimationFrame(frame);
      if (document.hidden || root.dataset.mode === "plain" || t - last < 60) return;
      last = t;
      draw();
    }
    function draw() {
      ctx.fillStyle = "rgba(28, 30, 28, .09)"; ctx.fillRect(0, 0, w, h);
      ctx.font = `${size}px monospace`;
      for (let i = 0; i < drops.length; i++) {
        const y = drops[i] * size;
        if (y > 0) {
          ctx.fillStyle = Math.random() < .08 ? "#c8ffd4" : "#00ff41";
          ctx.fillText(glyphs[(Math.random() * glyphs.length) | 0], i * size, y);
        }
        drops[i] = y > h && Math.random() > .975 ? 0 : drops[i] + 1;
      }
    }
    const still = () => { for (let n = 0; n < 80; n++) draw(); };  // a static frame of rain, no motion
    fit();
    if (reduced) { still(); window.addEventListener("resize", () => { fit(); still(); }); }
    else { window.addEventListener("resize", fit); requestAnimationFrame(frame); }
  })();

  /* ---------- Print (Ctrl+P still prints the page; the resume is resume.pdf) ---------- */
  document.querySelectorAll('[data-action="print"]').forEach((b) => b.addEventListener("click", () => window.print()));

  /* ---------- Typing tagline ---------- */
  const tag = document.getElementById("tagline");
  function typeTagline() {
    if (reduced || !tag || root.dataset.mode === "plain") return;
    const full = tag.textContent;
    tag.textContent = "";
    let i = 0;
    const tick = () => {
      tag.textContent = full.slice(0, ++i);
      if (i < full.length) setTimeout(tick, full[i - 1] === "." ? 260 : 28);
    };
    tick();
  }

  /* ---------- Boot sequence ---------- */
  const boot = document.getElementById("boot");
  const bootLog = document.getElementById("boot-log");
  const BOOT = [
    "BUENAOBRA BIOS v2.0.26  (c) Mark Lester Buenaobra",
    "CPU: tinkerer-class, 15 yrs supporting users  OK",
    "MEM: 100% CSAT, telco + Genie Health ....... OK",
    "NET: UTC+8 → US hours, remote link ........ OK",
    "Loading modules: m365 entra ad intune mimecast servicenow",
    "Mounting /homelab (proxmox · ansible · traefik) . OK",
    "",
    "Mabuhay! Welcome to buenaobra.net",
  ];
  function endBoot() {
    if (boot.hidden) return;
    boot.classList.add("fade");
    setTimeout(() => { boot.hidden = true; typeTagline(); }, 350);
    store.sset("booted", "1");
    window.removeEventListener("keydown", endBoot);
  }
  if (!reduced && !store.sget("booted") && root.dataset.mode !== "plain" && !location.hash) {
    boot.hidden = false;
    let line = 0;
    const next = () => {
      if (boot.hidden) return;
      if (line < BOOT.length) {
        bootLog.textContent += BOOT[line++] + "\n";
        setTimeout(next, 150);
      } else {
        setTimeout(endBoot, 550);
      }
    };
    next();
    boot.addEventListener("click", endBoot);
    window.addEventListener("keydown", endBoot);
  } else {
    typeTagline();
  }

  /* ---------- Terminal easter egg ---------- */
  const term = document.getElementById("term");
  const termBtn = document.getElementById("term-toggle");
  const out = document.getElementById("term-out");
  const form = document.getElementById("term-form");
  const input = document.getElementById("term-input");
  const history = [];
  let hIdx = 0;

  const esc = (s) => s.replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  function print(html) { out.insertAdjacentHTML("beforeend", html + "\n"); out.scrollTop = out.scrollHeight; }
  function go(id) { document.getElementById(id)?.scrollIntoView({ behavior: reduced ? "auto" : "smooth" }); }

  const CMDS = {
    help: () => [
      "available commands:",
      "  whoami      who is this guy",
      "  about       jump to about",
      "  experience  jump to career log",
      "  skills      list skills",
      "  certs       achievements",
      "  homelab     what runs at home",
      "  contact     how to reach me",
      "  resume      download the 2-page resume (PDF)",
      "  neofetch    system info",
      "  plain       toggle plain mode",
      "  clear       clear screen",
      "  exit        close terminal",
    ].join("\n"),
    whoami: () => "Mark Lester Buenaobra: IT support engineer, MSP helpdesk, Microsoft 365 & Entra ID.\nLifelong tinkerer. Builder of things that run themselves.",
    about: () => { go("about"); return "→ scrolling to about.md"; },
    experience: () => { go("experience"); return "→ git log --career"; },
    skills: () => "STRONG   m365 · exchange · entra id · ad/gpo · mimecast · macos · servicenow · rmm\nWORKING  intune · linux · docker · proxmox · traefik · caddy · dns\nLEARNING powershell · networking · ansible · azure",
    certs: () => "★ Datto RMM (Kaseya Certified Technician)  ★ AZ-900  ★ MS-900\n◇ AZ-104 (in progress)  ◇ SC-300 (in progress)  ◇ Apple Device Support (in progress)",
    homelab: () => { go("lab"); return "proxmox → adguard → traefik → pocket id sso → forgejo · vaultwarden · itflow · gatus → ntfy\nmanaged with ansible. → scrolling to homelab"; },
    contact: () => 'email    <a href="mailto:marklester@buenaobra.net">marklester@buenaobra.net</a>\nlinkedin <a href="https://www.linkedin.com/in/mark-lester-buenaobra-53095b312" target="_blank" rel="noopener">mark-lester-buenaobra</a>',
    resume: () => { setTimeout(() => { location.href = "resume.pdf"; }, 100); return "→ opening resume.pdf"; },
    neofetch: () => [
      '<span class="c-cyan">   ▄▄▄▄▄▄▄   </span>  <span class="c-green">marklester</span>@<span class="c-green">buenaobra.net</span>',
      '<span class="c-cyan">  █ ▀▄▄▄▀ █  </span>  ----------------',
      '<span class="c-cyan">  █ █▄▄▄█ █  </span>  OS: Human 1.0 (Filipino edition)',
      '<span class="c-cyan">  █▄▄▄▄▄▄▄█  </span>  Uptime: 15 years supporting users',
      '<span class="c-cyan">    ▀▀ ▀▀    </span>  Shell: active-listening',
      "               Location: Metro Manila, UTC+8",
      "               Packages: m365, entra, ad, intune, proxmox",
      "               Mode: open to work (NZ ♥)",
    ].join("\n"),
    plain: () => { setMode(root.dataset.mode === "plain" ? "neon" : "plain", true); return "mode toggled."; },
    clear: () => { out.innerHTML = ""; return null; },
    exit: () => { closeTerm(); return null; },
    sudo: (args) => args.join(" ") === "hire-me" || args.join(" ") === "hire marklester" || args.join(" ") === "hire lester"
      ? '[sudo] password for recruiter: ********\naccess granted. → <a href="mailto:marklester@buenaobra.net">marklester@buenaobra.net</a>'
      : "marklester is not in the sudoers file. This incident will be reported. (try: sudo hire-me)",
    mabuhay: () => "Mabuhay! 🇵🇭 Salamat sa pagbisita.",
    ls: () => "about.md  career.log  case-studies/  homelab/  skills.txt  side-quests.txt  resume.pdf",
    rm: () => "nice try. 🙂",
  };

  function run(raw) {
    const line = raw.trim();
    print(`<span class="c-green">marklester@buenaobra.net</span>:<span class="c-cyan">~</span>$ ${esc(line)}`);
    if (!line) return;
    history.push(line); hIdx = history.length;
    const [cmd, ...args] = line.split(/\s+/);
    const fn = CMDS[cmd.toLowerCase()];
    const res = fn ? fn(args) : `command not found: ${esc(cmd)}. type 'help'`;
    if (res) print(res);
  }

  function openTerm() {
    term.hidden = false; termBtn.setAttribute("aria-expanded", "true");
    if (!out.textContent) print("buenaobra.net terminal. type <span class=\"c-cyan\">help</span> to begin.");
    input.focus();
  }
  function closeTerm() { term.hidden = true; termBtn.setAttribute("aria-expanded", "false"); termBtn.focus(); }

  termBtn.addEventListener("click", () => (term.hidden ? openTerm() : closeTerm()));
  term.querySelector(".term-close").addEventListener("click", closeTerm);
  form.addEventListener("submit", (e) => { e.preventDefault(); run(input.value); input.value = ""; });
  input.addEventListener("keydown", (e) => {
    if (e.key === "ArrowUp" && hIdx > 0) { input.value = history[--hIdx]; e.preventDefault(); }
    else if (e.key === "ArrowDown") { hIdx = Math.min(history.length, hIdx + 1); input.value = history[hIdx] || ""; e.preventDefault(); }
    else if (e.key === "Escape") closeTerm();
  });
  window.addEventListener("keydown", (e) => {
    if (e.key === "`" && document.activeElement !== input && root.dataset.mode !== "plain") { e.preventDefault(); term.hidden ? openTerm() : closeTerm(); }
  });
})();
