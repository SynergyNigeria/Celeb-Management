"""
Run once: python write_templates.py
Rewrites all templates with the new Black/White/Gold design.
"""
import pathlib

B = pathlib.Path(__file__).parent / "templates"

def w(rel, content):
    p = B / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content.strip(), encoding="utf-8")
    print(f"  wrote {rel}")

# ─────────────────────────────────────────────────────────────────────────────
# BASE
# ─────────────────────────────────────────────────────────────────────────────
w("base.html", r"""
{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{% block title %}celebrity-manage{% endblock %}</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,400&display=swap" rel="stylesheet" />
  <script>tailwind.config={theme:{extend:{fontFamily:{sans:["Montserrat","sans-serif"]}}}}</script>
  <style>
    *,*::before,*::after{box-sizing:border-box}
    body{background:#0a0a0a}
    .input-field{width:100%;background:#111;border:1px solid #2a2a2a;border-radius:.5rem;padding:.7rem 1rem;color:#fff;font-size:.875rem;outline:none;transition:border-color .2s;font-family:'Montserrat',sans-serif}
    .input-field:focus{border-color:#C9A84C}
    .input-field::placeholder{color:#555}
    select.input-field{appearance:none;cursor:pointer}
    textarea.input-field{resize:vertical;min-height:90px}
    .btn-gold{background:#C9A84C;color:#000;font-weight:800;padding:.65rem 1.5rem;border-radius:.4rem;transition:background .2s,transform .15s;display:inline-block;text-align:center;cursor:pointer;border:none}
    .btn-gold:hover{background:#dbb95a;transform:translateY(-1px)}
    .btn-outline{background:transparent;color:#C9A84C;font-weight:700;padding:.65rem 1.5rem;border-radius:.4rem;border:1px solid #C9A84C;transition:background .2s;display:inline-block;text-align:center}
    .btn-outline:hover{background:rgba(201,168,76,.1)}
    .btn-ghost{background:#161616;color:#bbb;font-weight:600;padding:.65rem 1.5rem;border-radius:.4rem;border:1px solid #2a2a2a;transition:border-color .2s,color .2s;display:inline-block;text-align:center}
    .btn-ghost:hover{border-color:#555;color:#fff}
    .btn-primary{background:#C9A84C;color:#000;font-weight:800;padding:.65rem 1.5rem;border-radius:.4rem;transition:background .2s;display:inline-block;text-align:center}
    .btn-primary:hover{background:#dbb95a}
    .btn-secondary{background:#161616;color:#bbb;font-weight:600;padding:.65rem 1.5rem;border-radius:.4rem;border:1px solid #2a2a2a;display:inline-block;text-align:center;transition:border-color .2s,color .2s}
    .btn-secondary:hover{border-color:#555;color:#fff}
    .card{background:#111;border:1px solid #1e1e1e;border-radius:.75rem;transition:border-color .25s,box-shadow .25s}
    .card:hover{border-color:rgba(201,168,76,.38);box-shadow:0 8px 40px rgba(201,168,76,.07)}
    .celeb-card::before{content:'';position:absolute;inset:0;border-radius:inherit;background:linear-gradient(180deg,transparent 25%,rgba(0,0,0,.93) 100%);z-index:1}
    .cover-overlay{background:linear-gradient(180deg,transparent 10%,#0a0a0a 100%)}
    .tab-active{border-bottom:2px solid #C9A84C;color:#C9A84C;font-weight:800}
    .gold-line{border:none;border-top:1px solid rgba(201,168,76,.2)}
    .progress-track{background:#1e1e1e;border-radius:999px;overflow:hidden;height:6px}
    .progress-fill{background:linear-gradient(90deg,#A8873A,#dbb95a);height:100%;border-radius:999px;transition:width .6s ease}
    ::-webkit-scrollbar{width:5px;height:5px}
    ::-webkit-scrollbar-track{background:#111}
    ::-webkit-scrollbar-thumb{background:#2a2a2a;border-radius:3px}
    ::-webkit-scrollbar-thumb:hover{background:#C9A84C}
    {% block extra_style %}{% endblock %}
  </style>
</head>
<body class="font-sans text-white min-h-screen antialiased">

  <!-- NAV -->
  <nav class="fixed top-0 left-0 right-0 z-50 bg-black/96 backdrop-blur border-b border-[#1c1c1c]">
    <div class="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
      <a href="{% url 'home' %}" class="flex items-center gap-2 select-none">
        <span class="text-[#C9A84C] font-black text-xs tracking-[.3em]">✦</span>
        <span class="font-black text-[15px] tracking-tight">celebrity<span class="text-[#C9A84C]">-manage</span></span>
      </a>
      <div class="hidden md:flex items-center gap-8 text-[13px] font-semibold">
        <a href="{% url 'home' %}" class="text-zinc-400 hover:text-white transition-colors">Celebrities</a>
        <a href="{% url 'events_list' %}" class="text-zinc-400 hover:text-white transition-colors">Events</a>
        <a href="{% url 'foundations' %}" class="text-zinc-400 hover:text-white transition-colors">Donate</a>
      </div>
      <div class="flex items-center gap-3">
        {% if user.is_authenticated %}
          <a href="{% url 'dashboard' %}" class="hidden md:inline text-[13px] font-semibold text-zinc-400 hover:text-[#C9A84C] transition-colors truncate max-w-[130px]">{{ user.name }}</a>
          {% if user.is_staff %}
            <a href="{% url 'admin:index' %}" class="hidden md:inline text-[12px] font-bold text-[#C9A84C] hover:text-[#dbb95a] transition-colors">Admin &#8599;</a>
          {% endif %}
          <a href="{% url 'logout' %}" class="btn-ghost text-[12px] py-2 px-4">Logout</a>
        {% else %}
          <a href="{% url 'login' %}" class="text-[13px] font-semibold text-zinc-400 hover:text-white transition-colors">Sign in</a>
          <a href="{% url 'register' %}" class="btn-gold text-[12px] py-2 px-5">Join Free</a>
        {% endif %}
      </div>
    </div>
  </nav>

  <!-- TOASTS -->
  {% if messages %}
  <div class="fixed top-20 right-4 z-[999] space-y-2 w-80">
    {% for message in messages %}
    <div class="flex items-start justify-between gap-3 px-4 py-3 rounded-lg text-[13px] font-semibold shadow-xl border
      {% if message.tags == 'success' %}bg-[#0c1f0c] border-[#1a4a1a] text-green-300
      {% elif message.tags == 'error' %}bg-[#1f0c0c] border-[#4a1616] text-red-300
      {% elif message.tags == 'warning' %}bg-[#1f1700] border-[#4a3900] text-amber-300
      {% else %}bg-[#111] border-[#2a2a2a] text-zinc-200{% endif %}">
      <span>{{ message }}</span>
      <button onclick="this.parentElement.remove()" class="opacity-50 hover:opacity-100 leading-none flex-shrink-0">&#xd7;</button>
    </div>
    {% endfor %}
  </div>
  {% endif %}

  <main class="pt-16">{% block content %}{% endblock %}</main>

  <!-- FOOTER -->
  <footer class="border-t border-[#1c1c1c] mt-24 py-14">
    <div class="max-w-7xl mx-auto px-6">
      <div class="flex flex-col md:flex-row justify-between gap-8">
        <div>
          <div class="flex items-center gap-2 mb-3">
            <span class="text-[#C9A84C] text-xs font-black tracking-[.3em]">&#10022;</span>
            <span class="font-black text-[15px]">celebrity<span class="text-[#C9A84C]">-manage</span></span>
          </div>
          <p class="text-zinc-600 text-xs leading-relaxed max-w-xs">The all-in-one platform for celebrity fan memberships, events &amp; foundations.</p>
        </div>
        <div class="flex flex-wrap gap-x-10 gap-y-3 text-xs font-semibold text-zinc-600">
          <a href="{% url 'home' %}" class="hover:text-[#C9A84C] transition-colors">Celebrities</a>
          <a href="{% url 'events_list' %}" class="hover:text-[#C9A84C] transition-colors">Events</a>
          <a href="{% url 'foundations' %}" class="hover:text-[#C9A84C] transition-colors">Donate</a>
          {% if user.is_authenticated %}
          <a href="{% url 'dashboard' %}" class="hover:text-[#C9A84C] transition-colors">Dashboard</a>
          <a href="{% url 'logout' %}" class="hover:text-[#C9A84C] transition-colors">Logout</a>
          {% else %}
          <a href="{% url 'register' %}" class="hover:text-[#C9A84C] transition-colors">Create Account</a>
          <a href="{% url 'login' %}" class="hover:text-[#C9A84C] transition-colors">Sign In</a>
          {% endif %}
        </div>
      </div>
      <hr class="gold-line mt-10 mb-6" />
      <p class="text-center text-zinc-700 text-xs tracking-wide">&copy; 2026 celebrity-manage &nbsp;&middot;&nbsp; All rights reserved.</p>
    </div>
  </footer>

  {% block extra_js %}{% endblock %}
</body>
</html>
""".strip())

# ─────────────────────────────────────────────────────────────────────────────
# HOME
# ─────────────────────────────────────────────────────────────────────────────
w("celebs/home.html", r"""
{% extends "base.html" %}
{% block title %}celebrity-manage — Fan Platform{% endblock %}
{% block content %}

<!-- HERO -->
<section class="relative overflow-hidden bg-black pt-20 pb-28 px-6 text-center">
  <div class="absolute inset-0 pointer-events-none" style="background:radial-gradient(ellipse 70% 50% at 50% 0%,rgba(201,168,76,.07) 0%,transparent 70%)"></div>
  <div class="relative max-w-3xl mx-auto">
    <div class="inline-flex items-center gap-2 bg-[#161616] border border-[#C9A84C]/30 text-[#C9A84C] text-[11px] font-bold px-4 py-1.5 rounded-full mb-8 tracking-[.15em] uppercase">
      <span>&#10022;</span><span>Celebrity Fan Platform</span>
    </div>
    <h1 class="text-5xl md:text-7xl font-black leading-[1.05] mb-6 tracking-tight">
      Connect With<br/>Your <span class="text-[#C9A84C]">Favourite</span> Stars
    </h1>
    <p class="text-zinc-400 text-lg max-w-lg mx-auto mb-10 leading-relaxed">
      Exclusive memberships, charitable foundations, and live events &mdash; all in one place.
    </p>
    <div class="flex flex-col sm:flex-row gap-3 justify-center">
      <a href="#celebs" class="btn-gold px-10 py-3.5 text-[15px]">Explore Celebrities</a>
      {% if not user.is_authenticated %}
      <a href="{% url 'register' %}" class="btn-ghost px-10 py-3.5 text-[15px]">Join For Free</a>
      {% endif %}
    </div>
  </div>
</section>

<!-- STATS BAR -->
<div class="bg-[#111] border-y border-[#1e1e1e]">
  <div class="max-w-4xl mx-auto px-6 py-6 grid grid-cols-2 md:grid-cols-4 gap-6 text-center">
    <div>
      <div class="text-3xl font-black text-[#C9A84C]">{{ celebs.count }}</div>
      <div class="text-[10px] text-zinc-600 mt-1 uppercase tracking-[.15em]">Celebrities</div>
    </div>
    <div>
      <div class="text-3xl font-black text-[#C9A84C]">{{ total_events }}</div>
      <div class="text-[10px] text-zinc-600 mt-1 uppercase tracking-[.15em]">Events</div>
    </div>
    <div>
      <div class="text-3xl font-black text-[#C9A84C]">{{ total_foundations }}</div>
      <div class="text-[10px] text-zinc-600 mt-1 uppercase tracking-[.15em]">Foundations</div>
    </div>
    <div>
      <div class="text-3xl font-black text-[#C9A84C]">{{ total_members }}+</div>
      <div class="text-[10px] text-zinc-600 mt-1 uppercase tracking-[.15em]">Members</div>
    </div>
  </div>
</div>

<!-- FEATURED -->
{% if featured %}
<section class="max-w-7xl mx-auto px-6 pt-16">
  <div class="flex items-center gap-3 mb-6">
    <span class="text-[#C9A84C] text-xs font-black tracking-[.2em] uppercase">&#10022; Featured</span>
    <hr class="flex-1 border-[#1e1e1e]" />
  </div>
  <div class="grid md:grid-cols-2 gap-4">
    {% for c in featured %}
    <a href="{% url 'celeb_detail' c.slug %}" class="relative block rounded-xl overflow-hidden h-72 group">
      {% if c.cover_image %}
        <img src="{{ c.cover_image.url }}" class="absolute inset-0 w-full h-full object-cover opacity-60 group-hover:opacity-75 group-hover:scale-105 transition-all duration-500" alt="{{ c.name }}" />
      {% elif c.photo %}
        <img src="{{ c.photo.url }}" class="absolute inset-0 w-full h-full object-cover opacity-50 group-hover:opacity-65 group-hover:scale-105 transition-all duration-500" alt="{{ c.name }}" />
      {% else %}
        <div class="absolute inset-0 bg-[#111]"></div>
      {% endif %}
      <div class="absolute inset-0 bg-gradient-to-t from-black/95 to-transparent"></div>
      <div class="absolute top-4 left-4 z-10">
        <span class="inline-flex items-center gap-1.5 bg-black/70 border border-[#C9A84C]/40 text-[#C9A84C] text-[11px] font-bold px-3 py-1 rounded-full tracking-[.1em] uppercase">&#10022; Featured</span>
      </div>
      <div class="absolute bottom-0 left-0 p-7 z-10">
        <p class="text-[#C9A84C] text-[11px] font-bold uppercase tracking-[.15em] mb-1.5">{{ c.get_category_display }}</p>
        <h3 class="text-3xl font-black tracking-tight">{{ c.name }}</h3>
        {% if c.tagline %}<p class="text-zinc-400 text-sm mt-1">{{ c.tagline }}</p>{% endif %}
      </div>
    </a>
    {% endfor %}
  </div>
</section>
{% endif %}

<!-- SEARCH + FILTER -->
<section id="celebs" class="max-w-7xl mx-auto px-6 pt-14">
  <div class="flex flex-col md:flex-row gap-5 items-start md:items-end justify-between mb-8">
    <div>
      <p class="text-[#C9A84C] text-[11px] font-bold uppercase tracking-[.2em] mb-1">Browse</p>
      <h2 class="text-3xl font-black tracking-tight">All Celebrities</h2>
    </div>
    <form method="get" action="{% url 'home' %}#celebs" class="flex flex-wrap gap-2.5">
      <input name="q" value="{{ search }}" type="text" placeholder="Search name&hellip;" class="input-field w-44 text-sm" />
      <select name="category" class="input-field w-40 text-sm">
        <option value="">All Categories</option>
        {% for val, label in categories %}
        <option value="{{ val }}" {% if category == val %}selected{% endif %}>{{ label }}</option>
        {% endfor %}
      </select>
      <button type="submit" class="btn-gold py-[.65rem] px-5 text-sm">Filter</button>
      {% if search or category %}
      <a href="{% url 'home' %}" class="btn-ghost py-[.65rem] px-4 text-sm">Clear</a>
      {% endif %}
    </form>
  </div>

  {% if celebs %}
  <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
    {% for c in celebs %}
    <a href="{% url 'celeb_detail' c.slug %}" class="relative block rounded-xl overflow-hidden bg-[#111] celeb-card group h-72 border border-[#1e1e1e] hover:border-[#C9A84C]/30 transition-colors">
      {% if c.photo %}
        <img src="{{ c.photo.url }}" alt="{{ c.name }}" class="absolute inset-0 w-full h-full object-cover group-hover:scale-105 transition-transform duration-500 opacity-80" />
      {% else %}
        <div class="absolute inset-0 bg-[#161616]"></div>
      {% endif %}
      {% if c.is_featured %}
      <div class="absolute top-3 right-3 z-10 bg-black/80 border border-[#C9A84C]/50 text-[#C9A84C] text-[10px] font-black px-2.5 py-1 rounded-full tracking-[.1em]">&#10022; FEATURED</div>
      {% endif %}
      <div class="absolute bottom-0 left-0 right-0 z-[2] p-4">
        <span class="text-[10px] font-bold px-2.5 py-1 rounded bg-black/60 border border-white/10 capitalize mb-2 inline-block text-zinc-300 tracking-[.05em]">{{ c.get_category_display }}</span>
        <h3 class="text-base font-black leading-tight tracking-tight">{{ c.name }}</h3>
        {% if c.nationality %}<p class="text-zinc-500 text-[11px] mt-0.5">{{ c.nationality }}</p>{% endif %}
      </div>
    </a>
    {% endfor %}
  </div>
  {% else %}
  <div class="py-24 text-center text-zinc-600">
    <p class="text-4xl mb-4">&#128269;</p>
    <p class="text-base font-semibold">No celebrities found.</p>
    <a href="{% url 'home' %}" class="text-[#C9A84C] text-sm mt-3 inline-block hover:underline">Clear filters</a>
  </div>
  {% endif %}
  <div class="h-20"></div>
</section>

{% endblock %}
{% block extra_js %}
<script>
document.addEventListener("DOMContentLoaded",()=>{
  if(window.location.hash==="#celebs") document.getElementById("celebs")?.scrollIntoView({behavior:"smooth"});
});
</script>
{% endblock %}
""".strip())

# ─────────────────────────────────────────────────────────────────────────────
# CELEB DETAIL
# ─────────────────────────────────────────────────────────────────────────────
w("celebs/detail.html", r"""
{% extends "base.html" %}
{% block title %}{{ celeb.name }} &mdash; celebrity-manage{% endblock %}
{% block content %}

<!-- COVER -->
<div class="relative h-64 md:h-80 bg-[#111] overflow-hidden">
  {% if celeb.cover_image %}
    <img src="{{ celeb.cover_image.url }}" class="w-full h-full object-cover opacity-40" alt="{{ celeb.name }}" />
  {% elif celeb.photo %}
    <img src="{{ celeb.photo.url }}" class="w-full h-full object-cover opacity-25" alt="{{ celeb.name }}" />
  {% endif %}
  <div class="absolute inset-0 cover-overlay"></div>
</div>

<!-- PROFILE HEADER -->
<div class="max-w-5xl mx-auto px-6 -mt-20 relative z-10">
  <div class="flex flex-col md:flex-row gap-6 items-end mb-8">
    <div class="w-32 h-32 md:w-40 md:h-40 rounded-xl overflow-hidden border-2 border-[#C9A84C]/40 shadow-2xl flex-shrink-0 bg-[#111]">
      {% if celeb.photo %}
        <img src="{{ celeb.photo.url }}" class="w-full h-full object-cover" alt="{{ celeb.name }}" />
      {% else %}
        <div class="w-full h-full flex items-center justify-center text-3xl bg-[#161616]">&#10022;</div>
      {% endif %}
    </div>
    <div class="pb-1 flex-1">
      <p class="text-[#C9A84C] text-[11px] font-bold uppercase tracking-[.2em] mb-2">{{ celeb.get_category_display }}</p>
      <h1 class="text-4xl md:text-5xl font-black leading-tight tracking-tight">{{ celeb.name }}</h1>
      {% if celeb.tagline %}<p class="text-zinc-400 mt-1.5 text-base">{{ celeb.tagline }}</p>{% endif %}
      <div class="flex flex-wrap gap-4 mt-3 text-[13px]">
        {% if celeb.nationality %}<span class="text-zinc-500">{{ celeb.nationality }}</span>{% endif %}
        {% if celeb.instagram %}<a href="{{ celeb.instagram }}" target="_blank" class="text-zinc-400 hover:text-white transition-colors underline decoration-[#C9A84C]/40">Instagram</a>{% endif %}
        {% if celeb.twitter %}<a href="{{ celeb.twitter }}" target="_blank" class="text-zinc-400 hover:text-white transition-colors underline decoration-[#C9A84C]/40">Twitter / X</a>{% endif %}
        {% if celeb.youtube %}<a href="{{ celeb.youtube }}" target="_blank" class="text-zinc-400 hover:text-white transition-colors underline decoration-[#C9A84C]/40">YouTube</a>{% endif %}
      </div>
    </div>
    <div class="pb-1 flex gap-2 flex-wrap">
      <a href="{% url 'membership_list' celeb.slug %}" class="btn-gold py-2.5 px-5 text-sm">Join</a>
      <a href="{% url 'foundations' %}?celeb={{ celeb.slug }}" class="btn-outline py-2.5 px-5 text-sm">Donate</a>
      <a href="{% url 'events_list' %}?celeb={{ celeb.slug }}" class="btn-ghost py-2.5 px-5 text-sm">Events</a>
    </div>
  </div>

  <!-- TABS -->
  <div class="flex border-b border-[#1e1e1e] mb-8 gap-7 overflow-x-auto">
    <button onclick="showTab('about')" id="tab-about" class="tab-btn tab-active pb-3 text-sm whitespace-nowrap transition-colors">About</button>
    <button onclick="showTab('memberships')" id="tab-memberships" class="tab-btn pb-3 text-sm text-zinc-500 hover:text-white whitespace-nowrap transition-colors">Memberships</button>
    <button onclick="showTab('events')" id="tab-events" class="tab-btn pb-3 text-sm text-zinc-500 hover:text-white whitespace-nowrap transition-colors">Events</button>
    <button onclick="showTab('foundations')" id="tab-foundations" class="tab-btn pb-3 text-sm text-zinc-500 hover:text-white whitespace-nowrap transition-colors">Foundations</button>
  </div>

  <!-- ABOUT -->
  <div id="pane-about" class="pb-20">
    <div class="grid md:grid-cols-3 gap-8">
      <div class="md:col-span-2">
        <h2 class="text-lg font-bold mb-4 tracking-tight">Biography</h2>
        <p class="text-zinc-300 leading-relaxed whitespace-pre-line text-[15px]">{{ celeb.bio }}</p>
      </div>
      <div class="space-y-4">
        <div class="card p-5">
          <h3 class="text-[10px] font-bold uppercase tracking-[.2em] text-zinc-500 mb-4">Details</h3>
          <div class="space-y-3 text-sm">
            <div class="flex justify-between"><span class="text-zinc-500">Category</span><span class="capitalize text-[#C9A84C] font-semibold">{{ celeb.get_category_display }}</span></div>
            {% if celeb.nationality %}<div class="flex justify-between"><span class="text-zinc-500">Nationality</span><span class="text-zinc-300">{{ celeb.nationality }}</span></div>{% endif %}
          </div>
        </div>
        <a href="{% url 'membership_list' celeb.slug %}" class="card flex items-center gap-4 p-5 no-underline block">
          <span class="text-2xl">&#127903;</span>
          <div>
            <p class="font-bold text-sm">Memberships</p>
            <p class="text-xs text-zinc-500 mt-0.5">{{ celeb.membership_tiers.count }} tier{% if celeb.membership_tiers.count != 1 %}s{% endif %} available</p>
          </div>
          <span class="ml-auto text-[#C9A84C] text-xs font-bold">&rarr;</span>
        </a>
        <a href="{% url 'events_list' %}?celeb={{ celeb.slug }}" class="card flex items-center gap-4 p-5 no-underline block">
          <span class="text-2xl">&#128197;</span>
          <div>
            <p class="font-bold text-sm">Events</p>
            <p class="text-xs text-zinc-500 mt-0.5">{{ celeb.events.count }} event{% if celeb.events.count != 1 %}s{% endif %}</p>
          </div>
          <span class="ml-auto text-[#C9A84C] text-xs font-bold">&rarr;</span>
        </a>
      </div>
    </div>
  </div>

  <!-- MEMBERSHIPS -->
  <div id="pane-memberships" class="hidden pb-20">
    <div class="flex items-center justify-between mb-6">
      <h2 class="text-lg font-bold tracking-tight">Membership Tiers</h2>
      <a href="{% url 'membership_list' celeb.slug %}" class="btn-gold py-2 px-5 text-sm">View All</a>
    </div>
    <div class="grid md:grid-cols-3 gap-5">
      {% for tier in celeb.membership_tiers.all %}
      <div class="card p-6 flex flex-col gap-4">
        <div class="flex items-start justify-between">
          <span class="text-[11px] font-bold px-3 py-1 rounded border
            {% if tier.badge_color == 'gold' %}bg-[#C9A84C]/10 text-[#C9A84C] border-[#C9A84C]/25
            {% elif tier.badge_color == 'blue' %}bg-blue-900/20 text-blue-300 border-blue-800/30
            {% elif tier.badge_color == 'platinum' %}bg-zinc-800/50 text-zinc-200 border-zinc-600/30
            {% else %}bg-zinc-800/50 text-zinc-400 border-zinc-700/30{% endif %}
            tracking-[.08em]">{{ tier.name }}</span>
          <span class="text-2xl font-black text-[#C9A84C]">${{ tier.price }}</span>
        </div>
        <p class="text-zinc-400 text-sm">{{ tier.description }}</p>
        <a href="{% url 'membership_purchase' tier.pk %}" class="block text-center btn-gold py-2.5 text-sm mt-auto">Join Now</a>
      </div>
      {% empty %}
      <p class="col-span-3 text-zinc-500 text-sm">No membership tiers yet.</p>
      {% endfor %}
    </div>
  </div>

  <!-- EVENTS -->
  <div id="pane-events" class="hidden pb-20">
    <div class="flex items-center justify-between mb-6">
      <h2 class="text-lg font-bold tracking-tight">Events</h2>
      <a href="{% url 'events_list' %}?celeb={{ celeb.slug }}" class="btn-ghost py-2 px-5 text-sm">View All</a>
    </div>
    <div class="space-y-3">
      {% for ev in celeb.events.all|slice:":5" %}
      <a href="{% url 'event_detail' celeb.slug ev.slug %}" class="card flex gap-4 p-4 no-underline block">
        <div class="w-16 h-16 rounded-lg overflow-hidden bg-[#161616] flex-shrink-0 flex items-center justify-center text-xl">
          {% if ev.image %}<img src="{{ ev.image.url }}" class="w-full h-full object-cover" />{% else %}&#127908;{% endif %}
        </div>
        <div class="flex-1 min-w-0">
          <div class="flex gap-2 mb-1 flex-wrap">
            <span class="text-[10px] bg-[#C9A84C]/10 text-[#C9A84C] border border-[#C9A84C]/20 px-2 py-0.5 rounded capitalize font-semibold">{{ ev.get_event_type_display }}</span>
            <span class="text-[10px] px-2 py-0.5 rounded font-semibold
              {% if ev.status == 'upcoming' %}bg-green-950/60 text-green-400 border border-green-900/30
              {% elif ev.status == 'completed' %}bg-zinc-800/60 text-zinc-500 border border-zinc-700/30
              {% elif ev.status == 'cancelled' %}bg-red-950/60 text-red-400 border border-red-900/30
              {% else %}bg-blue-950/60 text-blue-400 border border-blue-900/30{% endif %}">{{ ev.get_status_display }}</span>
          </div>
          <h3 class="font-bold text-sm leading-snug">{{ ev.title }}</h3>
          <p class="text-[12px] text-zinc-500 mt-0.5">{{ ev.event_date|date:"M j, Y" }} &middot; {{ ev.location }}</p>
        </div>
        <div class="text-right flex-shrink-0 flex flex-col justify-center">
          {% if ev.is_free %}<span class="text-green-400 text-sm font-bold">Free</span>
          {% else %}<span class="text-[#C9A84C] text-sm font-black">${{ ev.ticket_price }}</span>{% endif %}
        </div>
      </a>
      {% empty %}
      <p class="text-zinc-500 text-sm">No events listed yet.</p>
      {% endfor %}
    </div>
  </div>

  <!-- FOUNDATIONS -->
  <div id="pane-foundations" class="hidden pb-20">
    <div class="flex items-center justify-between mb-6">
      <h2 class="text-lg font-bold tracking-tight">Foundations</h2>
      <a href="{% url 'foundations' %}?celeb={{ celeb.slug }}" class="btn-outline py-2 px-5 text-sm">View All</a>
    </div>
    <div class="grid md:grid-cols-2 gap-5">
      {% for f in celeb.foundations.all %}
      <div class="card overflow-hidden">
        {% if f.cover_image %}<img src="{{ f.cover_image.url }}" class="w-full h-36 object-cover" />{% endif %}
        <div class="p-5">
          <h3 class="font-bold mb-2 tracking-tight">{{ f.name }}</h3>
          <p class="text-zinc-400 text-sm mb-4 line-clamp-2">{{ f.description }}</p>
          <div class="flex justify-between text-[11px] text-zinc-500 mb-1.5">
            <span class="font-semibold">${{ f.amount_raised }} raised</span>
            <span class="text-[#C9A84C] font-bold">{{ f.progress_pct }}%</span>
          </div>
          <div class="progress-track mb-4">
            <div class="progress-fill" style="width:{% widthratio f.amount_raised f.target_amount 100 %}%"></div>
          </div>
          <a href="{% url 'donate_foundation' f.pk %}" class="block text-center btn-outline py-2.5 text-sm">Donate Now</a>
        </div>
      </div>
      {% empty %}
      <p class="col-span-2 text-zinc-500 text-sm">No foundations listed yet.</p>
      {% endfor %}
    </div>
  </div>
</div>
{% endblock %}
{% block extra_js %}
<script>
function showTab(name){
  ["about","memberships","events","foundations"].forEach(t=>{
    document.getElementById("pane-"+t).classList.add("hidden");
    const b=document.getElementById("tab-"+t);
    b.classList.remove("tab-active");
    b.classList.add("text-zinc-500");
    b.classList.remove("text-white");
  });
  document.getElementById("pane-"+name).classList.remove("hidden");
  const a=document.getElementById("tab-"+name);
  a.classList.add("tab-active");
  a.classList.remove("text-zinc-500");
}
</script>
{% endblock %}
""".strip())

# ─────────────────────────────────────────────────────────────────────────────
# MEMBERSHIPS LIST
# ─────────────────────────────────────────────────────────────────────────────
w("memberships/list.html", r"""
{% extends "base.html" %}
{% block title %}{{ celeb.name }} &mdash; Memberships &mdash; celebrity-manage{% endblock %}
{% block content %}
<div class="max-w-5xl mx-auto px-6 py-14">
  <nav class="text-[12px] text-zinc-600 mb-10 flex items-center gap-2">
    <a href="{% url 'home' %}" class="hover:text-[#C9A84C] transition-colors">Home</a>
    <span>&rsaquo;</span>
    <a href="{% url 'celeb_detail' celeb.slug %}" class="hover:text-[#C9A84C] transition-colors">{{ celeb.name }}</a>
    <span>&rsaquo;</span><span class="text-zinc-400">Membership</span>
  </nav>
  <div class="text-center mb-14">
    <div class="w-20 h-20 mx-auto rounded-xl overflow-hidden border border-[#C9A84C]/30 mb-5 bg-[#111]">
      {% if celeb.photo %}<img src="{{ celeb.photo.url }}" class="w-full h-full object-cover" />
      {% else %}<div class="w-full h-full flex items-center justify-center text-2xl">&#10022;</div>{% endif %}
    </div>
    <p class="text-[#C9A84C] text-[11px] font-bold uppercase tracking-[.2em] mb-2">{{ celeb.name }}</p>
    <h1 class="text-4xl font-black tracking-tight mb-2">Choose Your <span class="text-[#C9A84C]">Membership</span></h1>
    <p class="text-zinc-500 text-sm">Select a plan that matches your level of fandom</p>
  </div>
  {% if tiers %}
  <div class="grid md:grid-cols-3 gap-6">
    {% for tier in tiers %}
    <div class="relative card p-7 flex flex-col gap-5 {% if forloop.counter == 2 %}border-[#C9A84C]/50{% endif %}">
      {% if forloop.counter == 2 %}
      <div class="absolute -top-3.5 left-1/2 -translate-x-1/2 bg-[#C9A84C] text-black text-[10px] font-black px-4 py-1 rounded-full whitespace-nowrap tracking-[.1em] uppercase">MOST POPULAR</div>
      {% endif %}
      <div>
        <span class="text-[11px] font-bold px-3 py-1.5 rounded border inline-block mb-4 tracking-[.08em]
          {% if tier.badge_color == 'gold' %}bg-[#C9A84C]/10 text-[#C9A84C] border-[#C9A84C]/25
          {% elif tier.badge_color == 'blue' %}bg-blue-900/20 text-blue-300 border-blue-700/30
          {% elif tier.badge_color == 'platinum' %}bg-zinc-700/30 text-zinc-200 border-zinc-600/30
          {% else %}bg-zinc-800/40 text-zinc-400 border-zinc-700/30{% endif %}">{{ tier.name }}</span>
        <p class="text-5xl font-black text-[#C9A84C]">${{ tier.price }}</p>
        <p class="text-[11px] text-zinc-600 mt-1.5 tracking-[.05em]">{{ tier.duration_days }}-day membership</p>
      </div>
      <p class="text-zinc-400 text-sm flex-1">{{ tier.description }}</p>
      <ul class="space-y-2">
        {% for benefit in tier.benefits_list %}
        <li class="flex gap-2.5 text-[13px] text-zinc-300">
          <span class="text-[#C9A84C] font-black mt-0.5 flex-shrink-0">&#10003;</span>{{ benefit }}
        </li>
        {% endfor %}
      </ul>
      {% if tier.pk in user_tier_ids %}
        <div class="w-full btn-ghost py-3 text-sm text-green-400 border-green-900/40 text-center cursor-not-allowed select-none">&#10003; Active Plan</div>
      {% elif user.is_authenticated %}
        <a href="{% url 'membership_purchase' tier.pk %}" class="block text-center btn-gold py-3 text-sm">Join Now</a>
      {% else %}
        <a href="{% url 'login' %}?next={% url 'membership_list' celeb.slug %}" class="block text-center btn-outline py-3 text-sm">Sign In to Join</a>
      {% endif %}
    </div>
    {% endfor %}
  </div>
  {% else %}
  <div class="text-center py-20 text-zinc-600">
    <p class="text-4xl mb-4">&#127903;</p>
    <p class="text-base font-semibold">No membership tiers yet for {{ celeb.name }}.</p>
    <a href="{% url 'celeb_detail' celeb.slug %}" class="text-[#C9A84C] mt-4 inline-block hover:underline text-sm">&larr; Back to profile</a>
  </div>
  {% endif %}
</div>
{% endblock %}
""".strip())

# ─────────────────────────────────────────────────────────────────────────────
# MEMBERSHIP CONFIRM
# ─────────────────────────────────────────────────────────────────────────────
w("memberships/confirm.html", r"""
{% extends "base.html" %}
{% block title %}Confirm Membership &mdash; celebrity-manage{% endblock %}
{% block content %}
<div class="max-w-md mx-auto px-6 py-20">
  <div class="card p-8">
    <div class="text-center mb-8">
      <div class="w-14 h-14 rounded-xl bg-[#C9A84C]/10 border border-[#C9A84C]/25 flex items-center justify-center text-2xl mx-auto mb-4">&#127903;</div>
      <h1 class="text-2xl font-black tracking-tight">Confirm Membership</h1>
      <p class="text-zinc-500 text-sm mt-1.5">Review before activating your plan</p>
    </div>
    <div class="space-y-3 bg-[#0d0d0d] border border-[#1e1e1e] rounded-lg p-5 mb-7">
      <div class="flex justify-between text-sm"><span class="text-zinc-500">Celebrity</span><span class="font-semibold">{{ tier.celebrity.name }}</span></div>
      <div class="flex justify-between text-sm"><span class="text-zinc-500">Plan</span>
        <span class="font-bold
          {% if tier.badge_color == 'gold' %}text-[#C9A84C]
          {% elif tier.badge_color == 'blue' %}text-blue-300
          {% elif tier.badge_color == 'platinum' %}text-zinc-200
          {% else %}text-zinc-300{% endif %}">{{ tier.name }}</span>
      </div>
      <div class="flex justify-between text-sm"><span class="text-zinc-500">Duration</span><span class="text-zinc-300">{{ tier.duration_days }} days</span></div>
      <hr class="gold-line" />
      <div class="flex justify-between text-base font-black">
        <span>Total</span><span class="text-[#C9A84C]">${{ tier.price }}</span>
      </div>
    </div>
    {% if tier.benefits_list %}
    <div class="mb-7">
      <p class="text-[10px] font-bold uppercase tracking-[.2em] text-zinc-600 mb-3">What&rsquo;s included</p>
      <ul class="space-y-2">
        {% for b in tier.benefits_list %}
        <li class="flex gap-2.5 text-sm text-zinc-300">
          <span class="text-[#C9A84C] font-black flex-shrink-0 mt-0.5">&#10003;</span>{{ b }}
        </li>
        {% endfor %}
      </ul>
    </div>
    {% endif %}
    <form method="post">
      {% csrf_token %}
      <button type="submit" class="w-full btn-gold py-3.5 text-base">Activate Membership &mdash; ${{ tier.price }}</button>
    </form>
    <a href="{% url 'membership_list' tier.celebrity.slug %}" class="block text-center mt-4 text-sm text-zinc-600 hover:text-zinc-300 transition-colors">&larr; Cancel</a>
  </div>
  <p class="text-center text-[11px] text-zinc-700 mt-4">Simulated purchase &mdash; no real payment is processed.</p>
</div>
{% endblock %}
""".strip())

# ─────────────────────────────────────────────────────────────────────────────
# FOUNDATIONS
# ─────────────────────────────────────────────────────────────────────────────
w("donations/foundations.html", r"""
{% extends "base.html" %}
{% block title %}Foundations &amp; Causes &mdash; celebrity-manage{% endblock %}
{% block content %}
<div class="max-w-6xl mx-auto px-6 py-14">
  <div class="mb-12">
    <p class="text-[#C9A84C] text-[11px] font-bold uppercase tracking-[.2em] mb-2">Give Back</p>
    <h1 class="text-4xl font-black tracking-tight mb-1">Foundations <span class="text-[#C9A84C]">&amp; Causes</span></h1>
    <p class="text-zinc-500 text-sm">Make a difference through foundations backed by your favourite stars</p>
  </div>
  <form method="get" class="flex flex-wrap gap-3 mb-10">
    <select name="celeb" onchange="this.form.submit()" class="input-field w-52 text-sm">
      <option value="">All Celebrities</option>
      {% for c in celebs %}
      <option value="{{ c.slug }}" {% if selected_slug == c.slug %}selected{% endif %}>{{ c.name }}</option>
      {% endfor %}
    </select>
    {% if selected_slug %}
    <a href="{% url 'foundations' %}" class="btn-ghost py-[.65rem] px-4 text-sm">Clear</a>
    {% endif %}
  </form>
  {% if foundations %}
  <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
    {% for f in foundations %}
    <div class="card overflow-hidden flex flex-col">
      {% if f.cover_image %}
        <img src="{{ f.cover_image.url }}" class="w-full h-40 object-cover" />
      {% else %}
        <div class="h-40 bg-[#161616] flex items-center justify-center">
          <span class="text-[#C9A84C]/30 text-5xl">&#10022;</span>
        </div>
      {% endif %}
      <div class="p-6 flex flex-col flex-1">
        <div class="flex items-center justify-between mb-2">
          <span class="text-[11px] font-bold text-[#C9A84C] tracking-[.05em]">{{ f.celebrity.name }}</span>
          {% if f.cause_type %}<span class="text-[10px] bg-[#161616] border border-[#2a2a2a] px-2.5 py-0.5 rounded text-zinc-500 font-semibold">{{ f.cause_type }}</span>{% endif %}
        </div>
        <h3 class="text-base font-bold mb-2 tracking-tight">{{ f.name }}</h3>
        <p class="text-zinc-500 text-[13px] mb-4 line-clamp-2 leading-relaxed flex-1">{{ f.description }}</p>
        <div class="flex justify-between text-[11px] text-zinc-600 mb-1.5">
          <span class="font-semibold">${{ f.amount_raised }} raised</span>
          <span class="text-[#C9A84C] font-bold">{{ f.progress_pct }}% of ${{ f.target_amount }}</span>
        </div>
        <div class="progress-track mb-4">
          <div class="progress-fill" style="width:{% widthratio f.amount_raised f.target_amount 100 %}%"></div>
        </div>
        <div class="flex justify-between items-center text-[11px] text-zinc-600 mb-4">
          <span>{{ f.donations.count }} donor{% if f.donations.count != 1 %}s{% endif %}</span>
        </div>
        <a href="{% url 'donate_foundation' f.pk %}" class="block text-center btn-gold py-2.5 text-sm mt-auto">Donate Now</a>
      </div>
    </div>
    {% endfor %}
  </div>
  {% else %}
  <div class="text-center py-20 text-zinc-600">
    <p class="text-4xl mb-4 opacity-30">&#10022;</p>
    <p class="text-base font-semibold">No foundations found.</p>
  </div>
  {% endif %}
</div>
{% endblock %}
""".strip())

# ─────────────────────────────────────────────────────────────────────────────
# DONATE
# ─────────────────────────────────────────────────────────────────────────────
w("donations/donate.html", r"""
{% extends "base.html" %}
{% block title %}Donate &mdash; {{ foundation.name }} &mdash; celebrity-manage{% endblock %}
{% block content %}
<div class="max-w-5xl mx-auto px-6 py-14">
  <nav class="text-[12px] text-zinc-600 mb-10 flex items-center gap-2">
    <a href="{% url 'foundations' %}" class="hover:text-[#C9A84C] transition-colors">Foundations</a>
    <span>&rsaquo;</span>
    <a href="{% url 'celeb_detail' foundation.celebrity.slug %}" class="hover:text-[#C9A84C] transition-colors">{{ foundation.celebrity.name }}</a>
    <span>&rsaquo;</span><span class="text-zinc-400">{{ foundation.name }}</span>
  </nav>
  <div class="grid md:grid-cols-2 gap-10">
    <!-- Left -->
    <div>
      {% if foundation.cover_image %}
        <img src="{{ foundation.cover_image.url }}" class="w-full h-52 object-cover rounded-xl mb-6" />
      {% endif %}
      <p class="text-[#C9A84C] text-[11px] font-bold uppercase tracking-[.2em] mb-2">{{ foundation.celebrity.name }}</p>
      <h1 class="text-3xl font-black tracking-tight mb-3">{{ foundation.name }}</h1>
      <p class="text-zinc-300 leading-relaxed mb-6 text-[15px]">{{ foundation.description }}</p>
      <div class="card p-5 mb-6">
        <div class="flex justify-between text-sm mb-2.5">
          <span class="text-zinc-500">Amount Raised</span>
          <span class="font-black text-[#C9A84C]">${{ foundation.amount_raised }}</span>
        </div>
        <div class="progress-track mb-2.5">
          <div class="progress-fill" style="width:{% widthratio foundation.amount_raised foundation.target_amount 100 %}%"></div>
        </div>
        <div class="flex justify-between text-[11px] text-zinc-600">
          <span class="font-semibold text-[#C9A84C]">{{ foundation.progress_pct }}% of goal</span>
          <span>Goal: ${{ foundation.target_amount }}</span>
        </div>
      </div>
      {% if recent %}
      <div>
        <p class="text-[10px] font-bold uppercase tracking-[.2em] text-zinc-600 mb-3">Recent Donors</p>
        <div class="space-y-2">
          {% for d in recent %}
          <div class="flex justify-between card px-4 py-3 text-sm">
            <span class="text-zinc-300">{% if d.is_anonymous %}Anonymous{% else %}{{ d.user.name }}{% endif %}</span>
            <span class="text-[#C9A84C] font-bold">${{ d.amount }}</span>
          </div>
          {% endfor %}
        </div>
      </div>
      {% endif %}
    </div>
    <!-- Right: form -->
    <div>
      <div class="card p-7 sticky top-24">
        <h2 class="text-xl font-black mb-6 tracking-tight">Make a Donation</h2>
        <div class="mb-5">
          <p class="text-[10px] font-bold uppercase tracking-[.2em] text-zinc-500 mb-3">Quick Amount</p>
          <div class="flex flex-wrap gap-2" id="quick-btns">
            <button type="button" onclick="setAmt(5,this)" class="quick-amt bg-[#161616] border border-[#2a2a2a] px-4 py-2 rounded text-sm font-bold transition-all hover:bg-[#C9A84C] hover:text-black hover:border-[#C9A84C]">$5</button>
            <button type="button" onclick="setAmt(10,this)" class="quick-amt bg-[#161616] border border-[#2a2a2a] px-4 py-2 rounded text-sm font-bold transition-all hover:bg-[#C9A84C] hover:text-black hover:border-[#C9A84C]">$10</button>
            <button type="button" onclick="setAmt(25,this)" class="quick-amt bg-[#161616] border border-[#2a2a2a] px-4 py-2 rounded text-sm font-bold transition-all hover:bg-[#C9A84C] hover:text-black hover:border-[#C9A84C]">$25</button>
            <button type="button" onclick="setAmt(50,this)" class="quick-amt bg-[#161616] border border-[#2a2a2a] px-4 py-2 rounded text-sm font-bold transition-all hover:bg-[#C9A84C] hover:text-black hover:border-[#C9A84C]">$50</button>
            <button type="button" onclick="setAmt(100,this)" class="quick-amt bg-[#161616] border border-[#2a2a2a] px-4 py-2 rounded text-sm font-bold transition-all hover:bg-[#C9A84C] hover:text-black hover:border-[#C9A84C]">$100</button>
          </div>
        </div>
        <form method="post" class="space-y-4">
          {% csrf_token %}
          <input type="hidden" name="foundation" value="{{ foundation.pk }}">
          <div>
            <label class="text-[10px] font-bold uppercase tracking-[.2em] text-zinc-500 mb-1.5 block">Amount (USD) *</label>
            {{ form.amount }}
            {% if form.amount.errors %}<p class="text-red-400 text-[12px] mt-1">{{ form.amount.errors.0 }}</p>{% endif %}
          </div>
          <div>
            <label class="text-[10px] font-bold uppercase tracking-[.2em] text-zinc-500 mb-1.5 block">Message (optional)</label>
            {{ form.message }}
          </div>
          <label class="flex items-center gap-3 cursor-pointer select-none">
            {{ form.is_anonymous }}
            <span class="text-sm text-zinc-400">Donate anonymously</span>
          </label>
          <button type="submit" class="w-full btn-gold py-3.5">Donate Now</button>
        </form>
        <p class="text-center text-[11px] text-zinc-700 mt-3">Simulated &mdash; no real payment processed.</p>
      </div>
    </div>
  </div>
</div>
{% endblock %}
{% block extra_js %}
<script>
function setAmt(n,el){
  document.querySelector('[name="amount"]').value=n;
  document.querySelectorAll('.quick-amt').forEach(b=>{
    b.style.background='#161616';b.style.color='';b.style.borderColor='#2a2a2a';
  });
  el.style.background='#C9A84C';el.style.color='#000';el.style.borderColor='#C9A84C';
}
document.addEventListener("DOMContentLoaded",()=>{
  document.querySelectorAll("input[type=number],textarea").forEach(el=>el.classList.add("input-field"));
  document.querySelectorAll("input[type=checkbox]").forEach(el=>{
    el.classList.add("w-4","h-4","cursor-pointer");
    el.style.accentColor="#C9A84C";
  });
});
</script>
{% endblock %}
""".strip())

# ─────────────────────────────────────────────────────────────────────────────
# EVENTS LIST
# ─────────────────────────────────────────────────────────────────────────────
w("events/list.html", r"""
{% extends "base.html" %}
{% block title %}Events &mdash; celebrity-manage{% endblock %}
{% block content %}
<div class="max-w-6xl mx-auto px-6 py-14">
  <div class="flex flex-col md:flex-row items-start md:items-end justify-between mb-10 gap-5">
    <div>
      <p class="text-[#C9A84C] text-[11px] font-bold uppercase tracking-[.2em] mb-2">Calendar</p>
      <h1 class="text-4xl font-black tracking-tight">All Events</h1>
      <p class="text-zinc-500 text-sm mt-1">Concerts, meet &amp; greets, charity events and more</p>
    </div>
    <form method="get" class="flex flex-wrap gap-2.5">
      <input name="q" value="{{ search }}" placeholder="Search events&hellip;" class="input-field w-44 text-sm" />
      <select name="celeb" class="input-field w-40 text-sm">
        <option value="">All Celebrities</option>
        {% for c in celebs %}
        <option value="{{ c.slug }}" {% if selected_slug == c.slug %}selected{% endif %}>{{ c.name }}</option>
        {% endfor %}
      </select>
      <select name="status" class="input-field w-32 text-sm">
        <option value="">All Status</option>
        {% for val, label in status_choices %}
        <option value="{{ val }}" {% if status_filter == val %}selected{% endif %}>{{ label }}</option>
        {% endfor %}
      </select>
      <button type="submit" class="btn-gold py-[.65rem] px-5 text-sm">Filter</button>
      {% if selected_slug or status_filter or search %}
      <a href="{% url 'events_list' %}" class="btn-ghost py-[.65rem] px-4 text-sm">Clear</a>
      {% endif %}
    </form>
  </div>
  {% if events %}
  <div class="space-y-3">
    {% for ev in events %}
    <a href="{% url 'event_detail' ev.celebrity.slug ev.slug %}" class="card flex gap-5 p-5 no-underline block">
      <div class="w-20 h-20 md:w-24 md:h-24 rounded-lg overflow-hidden bg-[#161616] flex-shrink-0 flex items-center justify-center text-2xl">
        {% if ev.image %}<img src="{{ ev.image.url }}" class="w-full h-full object-cover" />{% else %}&#127908;{% endif %}
      </div>
      <div class="flex-1 min-w-0">
        <div class="flex flex-wrap gap-2 mb-2">
          <span class="text-[10px] bg-[#C9A84C]/10 text-[#C9A84C] border border-[#C9A84C]/20 px-2 py-0.5 rounded capitalize font-bold">{{ ev.get_event_type_display }}</span>
          <span class="text-[10px] px-2 py-0.5 rounded font-bold
            {% if ev.status == 'upcoming' %}bg-green-950/50 text-green-400 border border-green-900/30
            {% elif ev.status == 'completed' %}bg-zinc-800/60 text-zinc-500 border border-zinc-700/30
            {% elif ev.status == 'cancelled' %}bg-red-950/50 text-red-400 border border-red-900/30
            {% else %}bg-blue-950/50 text-blue-400 border border-blue-900/30{% endif %}">{{ ev.get_status_display }}</span>
          <span class="text-[10px] text-zinc-500 bg-[#161616] border border-[#2a2a2a] px-2 py-0.5 rounded font-semibold">{{ ev.celebrity.name }}</span>
        </div>
        <h3 class="font-bold text-base tracking-tight leading-snug">{{ ev.title }}</h3>
        <p class="text-[12px] text-zinc-500 mt-1">&#128197; {{ ev.event_date|date:"M j, Y · g:i A" }}</p>
        <p class="text-[12px] text-zinc-600">&#128205; {{ ev.location }}{% if ev.city %}, {{ ev.city }}{% endif %}{% if ev.country %}, {{ ev.country }}{% endif %}</p>
      </div>
      <div class="text-right flex-shrink-0 flex flex-col justify-center gap-1">
        {% if ev.is_free %}<span class="text-green-400 font-bold text-sm">Free</span>
        {% else %}<span class="text-[#C9A84C] font-black text-base">${{ ev.ticket_price }}</span>{% endif %}
        {% if ev.seats_total %}<span class="text-[11px] text-zinc-600">{{ ev.seats_available }} left</span>{% endif %}
      </div>
    </a>
    {% endfor %}
  </div>
  {% else %}
  <div class="text-center py-24 text-zinc-600">
    <p class="text-4xl mb-4 opacity-30">&#128197;</p>
    <p class="text-base font-semibold">No events found.</p>
    {% if selected_slug or status_filter or search %}
    <a href="{% url 'events_list' %}" class="text-[#C9A84C] mt-3 inline-block hover:underline text-sm">Clear filters</a>
    {% endif %}
  </div>
  {% endif %}
</div>
{% endblock %}
""".strip())

# ─────────────────────────────────────────────────────────────────────────────
# EVENT DETAIL
# ─────────────────────────────────────────────────────────────────────────────
w("events/detail.html", r"""
{% extends "base.html" %}
{% block title %}{{ event.title }} &mdash; celebrity-manage{% endblock %}
{% block content %}
<div class="max-w-4xl mx-auto px-6 py-14">
  <nav class="text-[12px] text-zinc-600 mb-10 flex items-center gap-2">
    <a href="{% url 'events_list' %}" class="hover:text-[#C9A84C] transition-colors">Events</a>
    <span>&rsaquo;</span>
    <a href="{% url 'celeb_detail' celeb.slug %}" class="hover:text-[#C9A84C] transition-colors">{{ celeb.name }}</a>
    <span>&rsaquo;</span><span class="text-zinc-400">{{ event.title }}</span>
  </nav>
  <div class="grid md:grid-cols-3 gap-10">
    <div class="md:col-span-2">
      {% if event.image %}
        <img src="{{ event.image.url }}" class="w-full h-60 object-cover rounded-xl mb-8" />
      {% endif %}
      <div class="flex flex-wrap gap-2 mb-4">
        <span class="text-[10px] bg-[#C9A84C]/10 text-[#C9A84C] border border-[#C9A84C]/20 px-3 py-1 rounded capitalize font-bold tracking-[.05em]">{{ event.get_event_type_display }}</span>
        <span class="text-[10px] px-3 py-1 rounded font-bold border
          {% if event.status == 'upcoming' %}bg-green-950/50 text-green-400 border-green-900/30
          {% elif event.status == 'completed' %}bg-zinc-800/60 text-zinc-500 border-zinc-700/30
          {% elif event.status == 'cancelled' %}bg-red-950/50 text-red-400 border-red-900/30
          {% else %}bg-blue-950/50 text-blue-400 border-blue-900/30{% endif %}">{{ event.get_status_display }}</span>
      </div>
      <h1 class="text-4xl font-black mb-4 tracking-tight leading-tight">{{ event.title }}</h1>
      <p class="text-zinc-300 leading-relaxed whitespace-pre-line text-[15px]">{{ event.description }}</p>
    </div>
    <!-- Sidebar -->
    <div class="space-y-4">
      <div class="card p-6 space-y-5">
        <div>
          <p class="text-[10px] text-zinc-600 uppercase tracking-[.2em] mb-1.5">Celebrity</p>
          <a href="{% url 'celeb_detail' celeb.slug %}" class="font-bold hover:text-[#C9A84C] transition-colors">{{ celeb.name }}</a>
        </div>
        <hr class="gold-line" />
        <div>
          <p class="text-[10px] text-zinc-600 uppercase tracking-[.2em] mb-1.5">Date &amp; Time</p>
          <p class="font-bold">{{ event.event_date|date:"F j, Y" }}</p>
          <p class="text-sm text-zinc-500">{{ event.event_date|time:"g:i A" }}</p>
        </div>
        <hr class="gold-line" />
        <div>
          <p class="text-[10px] text-zinc-600 uppercase tracking-[.2em] mb-1.5">Location</p>
          <p class="font-semibold text-sm">{{ event.location }}</p>
          {% if event.venue %}<p class="text-[12px] text-zinc-500">{{ event.venue }}</p>{% endif %}
          {% if event.city or event.country %}<p class="text-[12px] text-zinc-500">{{ event.city }}{% if event.city and event.country %}, {% endif %}{{ event.country }}</p>{% endif %}
        </div>
        <hr class="gold-line" />
        <div>
          <p class="text-[10px] text-zinc-600 uppercase tracking-[.2em] mb-1.5">Entry</p>
          {% if event.is_free %}<p class="text-green-400 font-black text-2xl">Free</p>
          {% else %}<p class="text-[#C9A84C] font-black text-2xl">${{ event.ticket_price }}</p>{% endif %}
        </div>
        {% if event.seats_total %}
        <hr class="gold-line" />
        <div>
          <p class="text-[10px] text-zinc-600 uppercase tracking-[.2em] mb-1.5">Availability</p>
          <p class="font-semibold text-sm text-zinc-300">{{ event.seats_available }} / {{ event.seats_total }} seats left</p>
          <div class="progress-track mt-2">
            <div class="progress-fill" style="width:{% widthratio event.seats_booked event.seats_total 100 %}%"></div>
          </div>
        </div>
        {% endif %}
      </div>
      {% if event.status == 'cancelled' %}
        <div class="card p-4 text-center text-red-400 text-sm font-bold border-red-900/30">Event Cancelled</div>
      {% elif event.status == 'completed' %}
        <div class="card p-4 text-center text-zinc-500 text-sm font-bold">Event Completed</div>
      {% elif is_registered %}
        <div class="card p-4 text-center text-green-400 text-sm font-bold border-green-900/30">&#10003; You&rsquo;re Registered!</div>
      {% elif user.is_authenticated %}
        <a href="{% url 'event_register' event.pk %}" class="block text-center btn-gold py-3.5 text-[15px]">
          {% if event.is_free %}Register (Free){% else %}Register &mdash; ${{ event.ticket_price }}{% endif %}
        </a>
      {% else %}
        <a href="{% url 'login' %}?next={{ request.path }}" class="block text-center btn-outline py-3.5 text-[15px]">Sign In to Register</a>
      {% endif %}
      <a href="{% url 'events_list' %}" class="block text-center text-[13px] text-zinc-600 hover:text-zinc-300 transition-colors">&larr; All Events</a>
    </div>
  </div>
</div>
{% endblock %}
""".strip())

# ─────────────────────────────────────────────────────────────────────────────
# EVENT CONFIRM
# ─────────────────────────────────────────────────────────────────────────────
w("events/confirm.html", r"""
{% extends "base.html" %}
{% block title %}Confirm Registration &mdash; celebrity-manage{% endblock %}
{% block content %}
<div class="max-w-md mx-auto px-6 py-20">
  <div class="card p-8">
    <div class="text-center mb-8">
      <div class="w-14 h-14 rounded-xl bg-[#C9A84C]/10 border border-[#C9A84C]/25 flex items-center justify-center text-2xl mx-auto mb-4">&#127908;</div>
      <h1 class="text-2xl font-black tracking-tight">Confirm Registration</h1>
      <p class="text-zinc-500 text-sm mt-1.5">You&rsquo;re about to register for this event</p>
    </div>
    <div class="space-y-3 bg-[#0d0d0d] border border-[#1e1e1e] rounded-lg p-5 mb-7">
      <div class="flex justify-between text-sm"><span class="text-zinc-500">Event</span><span class="font-semibold text-right max-w-[55%] leading-snug">{{ event.title }}</span></div>
      <div class="flex justify-between text-sm"><span class="text-zinc-500">Celebrity</span><span class="font-semibold">{{ event.celebrity.name }}</span></div>
      <div class="flex justify-between text-sm"><span class="text-zinc-500">Date</span><span>{{ event.event_date|date:"M j, Y · g:i A" }}</span></div>
      <div class="flex justify-between text-sm"><span class="text-zinc-500">Location</span><span class="text-right max-w-xs text-zinc-300">{{ event.location }}</span></div>
      <hr class="gold-line" />
      <div class="flex justify-between text-base font-black">
        <span>Fee</span>
        <span class="{% if event.is_free %}text-green-400{% else %}text-[#C9A84C]{% endif %}">{% if event.is_free %}Free{% else %}${{ event.ticket_price }}{% endif %}</span>
      </div>
    </div>
    <form method="post">
      {% csrf_token %}
      <button type="submit" class="w-full btn-gold py-3.5 text-base">Confirm Registration</button>
    </form>
    <a href="{% url 'event_detail' event.celebrity.slug event.slug %}" class="block text-center mt-4 text-sm text-zinc-600 hover:text-zinc-300 transition-colors">&larr; Cancel</a>
  </div>
  <p class="text-center text-[11px] text-zinc-700 mt-4">Simulated &mdash; no real payment is processed.</p>
</div>
{% endblock %}
""".strip())

# ─────────────────────────────────────────────────────────────────────────────
# REGISTER
# ─────────────────────────────────────────────────────────────────────────────
w("users/register.html", r"""
{% extends "base.html" %}
{% block title %}Create Account &mdash; celebrity-manage{% endblock %}
{% block content %}
<div class="min-h-[80vh] flex items-center justify-center px-4 py-20">
  <div class="w-full max-w-md">
    <div class="text-center mb-8">
      <a href="{% url 'home' %}" class="inline-flex items-center gap-2 mb-6 select-none">
        <span class="text-[#C9A84C] font-black text-sm tracking-[.3em]">&#10022;</span>
        <span class="font-black text-[17px]">celebrity<span class="text-[#C9A84C]">-manage</span></span>
      </a>
      <h2 class="text-2xl font-black tracking-tight mb-1">Create Your Account</h2>
      <p class="text-zinc-500 text-sm">Join the platform and access exclusive fan content</p>
    </div>
    <div class="card p-8">
      <form method="post" class="space-y-5">
        {% csrf_token %}
        <div>
          <label class="text-[10px] font-bold uppercase tracking-[.2em] text-zinc-500 mb-1.5 block">Full Name</label>
          {{ form.name }}
          {% if form.name.errors %}<p class="text-red-400 text-[12px] mt-1">{{ form.name.errors.0 }}</p>{% endif %}
        </div>
        <div>
          <label class="text-[10px] font-bold uppercase tracking-[.2em] text-zinc-500 mb-1.5 block">Email Address</label>
          {{ form.email }}
          {% if form.email.errors %}<p class="text-red-400 text-[12px] mt-1">{{ form.email.errors.0 }}</p>{% endif %}
        </div>
        <div>
          <label class="text-[10px] font-bold uppercase tracking-[.2em] text-zinc-500 mb-1.5 block">Country</label>
          {{ form.country }}
          {% if form.country.errors %}<p class="text-red-400 text-[12px] mt-1">{{ form.country.errors.0 }}</p>{% endif %}
        </div>
        <div>
          <label class="text-[10px] font-bold uppercase tracking-[.2em] text-zinc-500 mb-1.5 block">Password</label>
          {{ form.password1 }}
          {% if form.password1.errors %}<p class="text-red-400 text-[12px] mt-1">{{ form.password1.errors.0 }}</p>{% endif %}
        </div>
        <div>
          <label class="text-[10px] font-bold uppercase tracking-[.2em] text-zinc-500 mb-1.5 block">Confirm Password</label>
          {{ form.password2 }}
          {% if form.password2.errors %}<p class="text-red-400 text-[12px] mt-1">{{ form.password2.errors.0 }}</p>{% endif %}
        </div>
        {% if form.non_field_errors %}
        <div class="bg-[#1f0c0c] border border-[#4a1616] rounded-lg p-3 text-red-300 text-[13px]">
          {% for err in form.non_field_errors %}{{ err }}{% endfor %}
        </div>
        {% endif %}
        <button type="submit" class="w-full btn-gold py-3.5 text-base mt-2">Create Account</button>
      </form>
      <hr class="gold-line my-6" />
      <p class="text-center text-[13px] text-zinc-500">
        Already have an account?
        <a href="{% url 'login' %}" class="text-[#C9A84C] hover:underline font-bold ml-1">Sign in</a>
      </p>
    </div>
  </div>
</div>
{% endblock %}
{% block extra_js %}
<script>document.querySelectorAll("input").forEach(el=>el.classList.add("input-field"));</script>
{% endblock %}
""".strip())

# ─────────────────────────────────────────────────────────────────────────────
# LOGIN
# ─────────────────────────────────────────────────────────────────────────────
w("users/login.html", r"""
{% extends "base.html" %}
{% block title %}Sign In &mdash; celebrity-manage{% endblock %}
{% block content %}
<div class="min-h-[80vh] flex items-center justify-center px-4 py-20">
  <div class="w-full max-w-md">
    <div class="text-center mb-8">
      <a href="{% url 'home' %}" class="inline-flex items-center gap-2 mb-6 select-none">
        <span class="text-[#C9A84C] font-black text-sm tracking-[.3em]">&#10022;</span>
        <span class="font-black text-[17px]">celebrity<span class="text-[#C9A84C]">-manage</span></span>
      </a>
      <h2 class="text-2xl font-black tracking-tight mb-1">Welcome Back</h2>
      <p class="text-zinc-500 text-sm">Sign in to access your fan account</p>
    </div>
    <div class="card p-8">
      <form method="post" class="space-y-5">
        {% csrf_token %}
        {% if request.GET.next %}<input type="hidden" name="next" value="{{ request.GET.next }}">{% endif %}
        <div>
          <label class="text-[10px] font-bold uppercase tracking-[.2em] text-zinc-500 mb-1.5 block">Email Address</label>
          {{ form.username }}
          {% if form.username.errors %}<p class="text-red-400 text-[12px] mt-1">{{ form.username.errors.0 }}</p>{% endif %}
        </div>
        <div>
          <label class="text-[10px] font-bold uppercase tracking-[.2em] text-zinc-500 mb-1.5 block">Password</label>
          {{ form.password }}
          {% if form.password.errors %}<p class="text-red-400 text-[12px] mt-1">{{ form.password.errors.0 }}</p>{% endif %}
        </div>
        {% if form.non_field_errors %}
        <div class="bg-[#1f0c0c] border border-[#4a1616] rounded-lg p-3 text-red-300 text-[13px]">
          {% for err in form.non_field_errors %}{{ err }}{% endfor %}
        </div>
        {% endif %}
        <button type="submit" class="w-full btn-gold py-3.5 text-base">Sign In</button>
      </form>
      <hr class="gold-line my-6" />
      <p class="text-center text-[13px] text-zinc-500">
        New here?
        <a href="{% url 'register' %}" class="text-[#C9A84C] hover:underline font-bold ml-1">Create an account</a>
      </p>
    </div>
  </div>
</div>
{% endblock %}
{% block extra_js %}
<script>document.querySelectorAll("input").forEach(el=>el.classList.add("input-field"));</script>
{% endblock %}
""".strip())

# ─────────────────────────────────────────────────────────────────────────────
# DASHBOARD
# ─────────────────────────────────────────────────────────────────────────────
w("users/dashboard.html", r"""
{% extends "base.html" %}
{% block title %}My Dashboard &mdash; celebrity-manage{% endblock %}
{% block content %}
<div class="max-w-5xl mx-auto px-6 py-14">
  <div class="flex flex-col md:flex-row items-start md:items-center justify-between mb-12 gap-4">
    <div>
      <p class="text-[#C9A84C] text-[11px] font-bold uppercase tracking-[.2em] mb-1.5">Welcome back</p>
      <h1 class="text-3xl font-black tracking-tight">{{ user.name }}</h1>
      <p class="text-zinc-500 text-sm mt-1">{{ user.email }} &nbsp;&middot;&nbsp; {{ user.country }}</p>
    </div>
    <a href="{% url 'logout' %}" class="btn-ghost text-sm py-2.5 px-6">Logout</a>
  </div>
  <!-- Stats -->
  <div class="grid grid-cols-3 gap-4 mb-12">
    <div class="card p-5 text-center">
      <p class="text-3xl font-black text-[#C9A84C]">{{ memberships.count }}</p>
      <p class="text-[10px] text-zinc-600 mt-1.5 uppercase tracking-[.15em]">Memberships</p>
    </div>
    <div class="card p-5 text-center">
      <p class="text-3xl font-black text-[#C9A84C]">{{ donations.count }}</p>
      <p class="text-[10px] text-zinc-600 mt-1.5 uppercase tracking-[.15em]">Donations</p>
    </div>
    <div class="card p-5 text-center">
      <p class="text-3xl font-black text-[#C9A84C]">{{ event_regs.count }}</p>
      <p class="text-[10px] text-zinc-600 mt-1.5 uppercase tracking-[.15em]">Events</p>
    </div>
  </div>
  <!-- Memberships -->
  <section class="mb-12">
    <div class="flex items-center justify-between mb-5">
      <h2 class="text-lg font-black tracking-tight">My Memberships</h2>
      <a href="{% url 'home' %}" class="text-[13px] text-[#C9A84C] hover:underline font-semibold">Browse more &rarr;</a>
    </div>
    {% if memberships %}
    <div class="grid md:grid-cols-2 gap-3">
      {% for m in memberships %}
      <div class="card flex gap-4 p-5 {% if m.is_active and m.expires_at > now %}border-[#C9A84C]/30{% endif %}">
        <div class="w-12 h-12 rounded-lg bg-[#161616] overflow-hidden flex-shrink-0 flex items-center justify-center text-base">
          {% if m.tier.celebrity.photo %}<img src="{{ m.tier.celebrity.photo.url }}" class="w-full h-full object-cover" />
          {% else %}&#10022;{% endif %}
        </div>
        <div class="flex-1 min-w-0">
          <p class="font-bold text-sm truncate">{{ m.tier.celebrity.name }} &mdash; {{ m.tier.name }}</p>
          <p class="text-[11px] text-zinc-600 mt-0.5">Expires {{ m.expires_at|date:"M j, Y" }}</p>
          <p class="text-[11px] mt-1 font-bold">
            {% if m.is_active and m.expires_at > now %}
              <span class="text-green-400">&#9679; Active</span>
            {% else %}
              <span class="text-red-400">&#9679; Expired</span>
            {% endif %}
          </p>
        </div>
        <p class="text-[#C9A84C] font-black text-sm flex-shrink-0">${{ m.amount_paid }}</p>
      </div>
      {% endfor %}
    </div>
    {% else %}
    <div class="card p-8 text-center text-zinc-600">
      <p class="text-3xl mb-3 opacity-25">&#127903;</p>
      <p class="font-semibold mb-3 text-sm">No memberships yet</p>
      <a href="{% url 'home' %}" class="btn-gold py-2 px-5 text-sm">Explore Celebrities</a>
    </div>
    {% endif %}
  </section>
  <!-- Donations -->
  <section class="mb-12">
    <div class="flex items-center justify-between mb-5">
      <h2 class="text-lg font-black tracking-tight">My Donations</h2>
      <a href="{% url 'foundations' %}" class="text-[13px] text-[#C9A84C] hover:underline font-semibold">Donate more &rarr;</a>
    </div>
    {% if donations %}
    <div class="space-y-2.5">
      {% for d in donations %}
      <div class="card flex items-center justify-between px-5 py-4">
        <div class="min-w-0 flex-1">
          <p class="font-semibold text-sm">{{ d.foundation.name }}</p>
          <p class="text-[11px] text-zinc-600 mt-0.5">{{ d.foundation.celebrity.name }} &nbsp;&middot;&nbsp; {{ d.donated_at|date:"M j, Y" }}</p>
          {% if d.message %}<p class="text-[11px] text-zinc-500 mt-1 italic truncate max-w-xs">&ldquo;{{ d.message|truncatechars:60 }}&rdquo;</p>{% endif %}
        </div>
        <p class="text-[#C9A84C] font-black text-sm flex-shrink-0 ml-4">${{ d.amount }}</p>
      </div>
      {% endfor %}
    </div>
    {% else %}
    <div class="card p-8 text-center text-zinc-600">
      <p class="text-3xl mb-3 opacity-25">&#10022;</p>
      <p class="font-semibold mb-3 text-sm">No donations yet</p>
      <a href="{% url 'foundations' %}" class="btn-outline py-2 px-5 text-sm">Browse Foundations</a>
    </div>
    {% endif %}
  </section>
  <!-- Events -->
  <section>
    <div class="flex items-center justify-between mb-5">
      <h2 class="text-lg font-black tracking-tight">My Events</h2>
      <a href="{% url 'events_list' %}" class="text-[13px] text-[#C9A84C] hover:underline font-semibold">Browse events &rarr;</a>
    </div>
    {% if event_regs %}
    <div class="space-y-2.5">
      {% for r in event_regs %}
      <a href="{% url 'event_detail' r.event.celebrity.slug r.event.slug %}" class="card flex items-center justify-between px-5 py-4 no-underline block">
        <div class="min-w-0 flex-1">
          <p class="font-semibold text-sm">{{ r.event.title }}</p>
          <p class="text-[11px] text-zinc-600 mt-0.5">{{ r.event.celebrity.name }} &nbsp;&middot;&nbsp; {{ r.event.event_date|date:"M j, Y" }}</p>
          <p class="text-[11px] text-zinc-600">&#128205; {{ r.event.location }}</p>
        </div>
        <div class="text-right flex-shrink-0 ml-4">
          {% if r.event.is_free %}<span class="text-green-400 text-sm font-bold">Free</span>
          {% else %}<span class="text-[#C9A84C] text-sm font-black">${{ r.amount_paid }}</span>{% endif %}
          <p class="text-[11px] text-zinc-600 mt-0.5">{{ r.event.get_status_display }}</p>
        </div>
      </a>
      {% endfor %}
    </div>
    {% else %}
    <div class="card p-8 text-center text-zinc-600">
      <p class="text-3xl mb-3 opacity-25">&#128197;</p>
      <p class="font-semibold mb-3 text-sm">No event registrations yet</p>
      <a href="{% url 'events_list' %}" class="btn-ghost py-2 px-5 text-sm">Find Events</a>
    </div>
    {% endif %}
  </section>
</div>
{% endblock %}
""".strip())

print("\nDone! All 13 templates written.")
