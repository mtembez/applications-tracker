"""Starlette ASGI Server providing a high-octane Multicolor Dashboard with Aceternity & Magic UI animations and Celestial Lion artwork."""
import json
from starlette.applications import Starlette
from starlette.responses import JSONResponse, HTMLResponse
from starlette.routing import Route
from starlette.requests import Request

from . import db
from .models import ApplicationCreate, AppStatus, LocationType, EventType

DASHBOARD_HTML = r"""<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Applications Tracker | Celestial Multicolor Systems Console</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Geist:wght@300;400;500;600;700;800&family=Geist+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #030305;
      --sidebar: rgba(8, 8, 12, 0.85);
      --surface: rgba(14, 14, 20, 0.7);
      --surface-hover: rgba(22, 22, 32, 0.85);
      --surface-active: rgba(28, 28, 42, 0.95);
      --border: rgba(255, 255, 255, 0.08);
      --border-subtle: rgba(255, 255, 255, 0.05);
      --border-hover: rgba(255, 255, 255, 0.2);
      
      /* Vibrant Multicolor Palette */
      --cyan: #06b6d4;
      --sky: #38bdf8;
      --violet: #8b5cf6;
      --fuchsia: #d946ef;
      --rose: #f43f5e;
      --emerald: #10b981;
      --amber: #f59e0b;
      --indigo: #6366f1;

      --text: #f8fafc;
      --text-muted: #94a3b8;
      --text-dim: #64748b;
      --primary: #ffffff;
      --primary-invert: #000000;
      
      --font-sans: 'Geist', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      --font-mono: 'Geist Mono', monospace;
      --ease: cubic-bezier(0.16, 1, 0.3, 1);
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }
    html, body {
      background-color: var(--bg);
      color: var(--text);
      font-family: var(--font-sans);
      letter-spacing: -0.015em;
      height: 100vh;
      overflow: hidden;
      -webkit-font-smoothing: antialiased;
      position: relative;
    }

    /* Magic UI: Ambient Multi-Color Aurora Mesh Background */
    .aurora-bg {
      position: fixed; inset: 0; pointer-events: none; z-index: 0; overflow: hidden;
    }
    .aurora-sphere {
      position: absolute; border-radius: 50%; filter: blur(100px); opacity: 0.35;
      animation: aurora-drift 18s ease-in-out infinite alternate;
    }
    .sphere-1 { width: 550px; height: 550px; background: radial-gradient(circle, var(--sky) 0%, transparent 70%); top: -10%; left: 15%; }
    .sphere-2 { width: 650px; height: 650px; background: radial-gradient(circle, var(--violet) 0%, transparent 70%); bottom: -15%; right: 5%; animation-duration: 22s; }
    .sphere-3 { width: 450px; height: 450px; background: radial-gradient(circle, var(--fuchsia) 0%, transparent 70%); top: 30%; right: 25%; animation-duration: 15s; }
    .sphere-4 { width: 500px; height: 500px; background: radial-gradient(circle, var(--amber) 0%, transparent 70%); bottom: 10%; left: 10%; animation-duration: 25s; opacity: 0.25; }

    @keyframes aurora-drift {
      0% { transform: translate(0, 0) scale(1) rotate(0deg); }
      50% { transform: translate(40px, -30px) scale(1.08) rotate(10deg); }
      100% { transform: translate(-30px, 40px) scale(0.95) rotate(-10deg); }
    }

    /* Aceternity UI: Celestial Glowing Lion Emblem in Background */
    .lion-backdrop-canvas {
      position: fixed;
      right: 4%;
      top: 50%;
      transform: translateY(-46%);
      width: 780px;
      height: 780px;
      pointer-events: none;
      z-index: 0;
      opacity: 0.18;
      transition: opacity 0.5s ease;
      animation: lion-ambient-pulse 8s ease-in-out infinite alternate;
    }
    @keyframes lion-ambient-pulse {
      0% { transform: translateY(-46%) scale(0.98); filter: drop-shadow(0 0 20px rgba(56, 189, 248, 0.2)); }
      100% { transform: translateY(-48%) scale(1.02); filter: drop-shadow(0 0 45px rgba(168, 85, 247, 0.45)); }
    }

    /* Layout Shell: Left Sidebar + Main Content */
    .app-shell { display: flex; height: 100vh; width: 100vw; position: relative; z-index: 1; }

    /* Left Sidebar with Glassmorphism */
    aside {
      width: 250px; min-width: 250px;
      background: var(--sidebar);
      backdrop-filter: blur(20px);
      border-right: 1px solid var(--border);
      display: flex; flex-direction: column; justify-content: space-between;
      user-select: none;
    }
    .sidebar-top { padding: 16px 14px; }
    .workspace-header {
      display: flex; align-items: center; justify-content: space-between;
      padding: 8px 10px; border-radius: 8px; cursor: pointer;
      background: rgba(255, 255, 255, 0.02); border: 1px solid var(--border-subtle);
      transition: all 0.2s var(--ease); margin-bottom: 14px;
    }
    .workspace-header:hover {
      background: var(--surface-hover); border-color: rgba(56, 189, 248, 0.3);
      box-shadow: 0 0 15px rgba(56, 189, 248, 0.15);
    }
    .workspace-info { display: flex; align-items: center; gap: 10px; }
    .avatar-pill {
      width: 26px; height: 26px; border-radius: 6px;
      background: linear-gradient(135deg, #06b6d4, #8b5cf6, #ec4899);
      background-size: 200% 200%;
      animation: gradient-shift 6s ease infinite;
      display: flex; align-items: center; justify-content: center;
      font-size: 0.75rem; font-weight: 800; color: #fff;
      box-shadow: 0 0 10px rgba(139, 92, 246, 0.4);
    }
    @keyframes gradient-shift {
      0% { background-position: 0% 50%; }
      50% { background-position: 100% 50%; }
      100% { background-position: 0% 50%; }
    }
    .workspace-name { font-size: 0.85rem; font-weight: 700; color: #fff; }
    .workspace-role { font-size: 0.7rem; color: var(--sky); font-weight: 500; }

    /* Magic UI Shimmer Text for Brand */
    .shimmer-text {
      background: linear-gradient(90deg, #38bdf8, #a855f7, #ec4899, #f59e0b, #10b981, #38bdf8);
      background-size: 300%;
      animation: shimmer-flow 8s linear infinite;
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    @keyframes shimmer-flow {
      0% { background-position: 0%; }
      100% { background-position: 300%; }
    }

    /* Command Palette Button */
    .cmd-trigger {
      width: 100%; background: rgba(18, 18, 26, 0.7);
      border: 1px solid var(--border); border-radius: 8px;
      padding: 8px 12px; display: flex; align-items: center; justify-content: space-between;
      color: var(--text-muted); font-size: 0.775rem; cursor: pointer;
      transition: all 0.2s var(--ease); margin-bottom: 18px;
    }
    .cmd-trigger:hover {
      border-color: var(--sky); color: #fff;
      box-shadow: 0 0 12px rgba(56, 189, 248, 0.2);
    }
    .kbd-chip {
      background: rgba(255, 255, 255, 0.06); border: 1px solid rgba(255, 255, 255, 0.1);
      padding: 1px 6px; border-radius: 4px; font-size: 0.65rem;
      font-family: var(--font-mono); color: var(--sky); font-weight: 600;
    }

    /* Nav section */
    .nav-group-title {
      font-size: 0.675rem; text-transform: uppercase; font-weight: 700;
      letter-spacing: 0.08em; color: var(--text-dim); padding: 6px 8px 4px 8px;
    }
    .nav-list { list-style: none; display: flex; flex-direction: column; gap: 3px; }
    .nav-item {
      display: flex; align-items: center; justify-content: space-between;
      padding: 7px 10px; border-radius: 6px; font-size: 0.8rem; font-weight: 500;
      color: var(--text-muted); cursor: pointer; transition: all 0.15s var(--ease);
    }
    .nav-item:hover { color: #fff; background: rgba(255, 255, 255, 0.05); }
    .nav-item.active {
      color: #fff; background: linear-gradient(90deg, rgba(56, 189, 248, 0.15), rgba(168, 85, 247, 0.05));
      border-left: 3px solid var(--sky); font-weight: 600;
    }
    .nav-item-left { display: flex; align-items: center; gap: 10px; }
    .nav-badge {
      font-size: 0.675rem; font-family: var(--font-mono); font-weight: 600;
      color: var(--sky); background: rgba(56, 189, 248, 0.1);
      padding: 1px 6px; border-radius: 9999px;
    }

    /* Sidebar Footer */
    .sidebar-footer {
      padding: 14px 16px; border-top: 1px solid var(--border);
      display: flex; flex-direction: column; gap: 8px;
    }
    .live-status { display: flex; align-items: center; gap: 8px; font-size: 0.725rem; color: var(--text-dim); }
    .status-dot {
      width: 7px; height: 7px; border-radius: 50%;
      background: var(--emerald); box-shadow: 0 0 10px var(--emerald);
      animation: pulse-ring 2s infinite;
    }
    @keyframes pulse-ring {
      0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
      70% { transform: scale(1); box-shadow: 0 0 0 6px rgba(16, 185, 129, 0); }
      100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
    }

    /* Main View Area */
    main { flex: 1; display: flex; flex-direction: column; overflow: hidden; position: relative; }

    /* Top Bar */
    .top-bar {
      height: 54px; min-height: 54px;
      border-bottom: 1px solid var(--border);
      padding: 0 26px;
      display: flex; align-items: center; justify-content: space-between;
      backdrop-filter: blur(12px);
      background: rgba(3, 3, 5, 0.75);
    }
    .breadcrumbs { display: flex; align-items: center; gap: 8px; font-size: 0.825rem; }
    .breadcrumb-root { color: var(--text-dim); font-weight: 500; }
    .breadcrumb-sep { color: var(--border-hover); }
    .breadcrumb-current { color: #fff; font-weight: 600; }
    .top-actions { display: flex; align-items: center; gap: 10px; }

    /* Multicolor Buttons */
    .btn {
      display: inline-flex; align-items: center; gap: 7px;
      padding: 7px 14px; border-radius: 6px;
      font-size: 0.8rem; font-weight: 600; font-family: var(--font-sans);
      cursor: pointer; transition: all 0.2s var(--ease);
      border: 1px solid transparent; text-decoration: none; user-select: none;
    }
    .btn-gradient {
      background: linear-gradient(135deg, #06b6d4, #8b5cf6, #d946ef);
      background-size: 200% 200%;
      color: #fff;
      box-shadow: 0 0 15px rgba(139, 92, 246, 0.35);
      border: 1px solid rgba(255, 255, 255, 0.15);
    }
    .btn-gradient:hover {
      background-position: 100% 50%;
      transform: translateY(-1px);
      box-shadow: 0 0 25px rgba(217, 70, 239, 0.5);
    }
    .btn-secondary {
      background: rgba(18, 18, 26, 0.7); color: var(--text);
      border: 1px solid var(--border); backdrop-filter: blur(10px);
    }
    .btn-secondary:hover {
      background: rgba(28, 28, 40, 0.9); border-color: var(--sky);
      color: #fff; box-shadow: 0 0 10px rgba(56, 189, 248, 0.2);
    }
    .btn-ghost { background: transparent; color: var(--text-muted); }
    .btn-ghost:hover { color: #fff; background: rgba(255,255,255,0.06); }

    /* Glowing Metrics Strip (Tremor + Magic UI) */
    .stats-strip {
      padding: 10px 26px;
      display: flex; align-items: center; gap: 28px;
      border-bottom: 1px solid var(--border);
      background: rgba(8, 8, 14, 0.65);
      backdrop-filter: blur(14px);
      font-size: 0.75rem;
    }
    .stat-pill { display: flex; align-items: center; gap: 9px; }
    .stat-pill-label { color: var(--text-dim); text-transform: uppercase; letter-spacing: 0.06em; font-weight: 700; font-size: 0.675rem; }
    .stat-pill-val { font-family: var(--font-mono); font-weight: 700; color: #fff; }
    .stat-pill-badge {
      font-size: 0.675rem; font-family: var(--font-mono); font-weight: 600;
      padding: 2px 7px; border-radius: 4px;
    }
    .badge-cyan { background: rgba(6, 182, 212, 0.15); border: 1px solid rgba(6, 182, 212, 0.3); color: var(--cyan); }
    .badge-emerald { background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.3); color: var(--emerald); }

    /* Control Bar */
    .control-header {
      padding: 12px 26px;
      display: flex; justify-content: space-between; align-items: center;
      gap: 16px; border-bottom: 1px solid var(--border-subtle);
    }
    .filters-left { display: flex; align-items: center; gap: 10px; flex: 1; }
    .search-box-wrap { position: relative; width: 300px; }
    .search-box-icon { position: absolute; left: 10px; top: 50%; transform: translateY(-50%); color: var(--text-dim); }
    .search-box {
      width: 100%; background: rgba(14, 14, 22, 0.75); border: 1px solid var(--border);
      color: var(--text); padding: 7px 12px 7px 34px; border-radius: 6px;
      font-size: 0.8rem; font-family: var(--font-sans); transition: all 0.2s var(--ease);
    }
    .search-box:focus {
      outline: none; border-color: var(--sky);
      box-shadow: 0 0 15px rgba(56, 189, 248, 0.25); background: rgba(20, 20, 32, 0.9);
    }
    .view-toggle {
      background: rgba(14, 14, 22, 0.75); border: 1px solid var(--border);
      border-radius: 6px; padding: 2px; display: flex; gap: 2px;
    }
    .toggle-btn {
      background: transparent; border: none; color: var(--text-dim);
      padding: 5px 12px; border-radius: 4px; font-size: 0.775rem; font-weight: 500;
      display: flex; align-items: center; gap: 6px; cursor: pointer; transition: all 0.15s;
    }
    .toggle-btn:hover { color: var(--text); }
    .toggle-btn.active {
      background: linear-gradient(135deg, rgba(56, 189, 248, 0.2), rgba(139, 92, 246, 0.2));
      border: 1px solid rgba(56, 189, 248, 0.3); color: #fff; font-weight: 600;
    }

    /* Content Area */
    .content-area {
      flex: 1; overflow-y: auto; padding: 20px 26px; position: relative; z-index: 1;
    }

    /* Kanban Board Layout */
    .kanban-grid {
      display: grid;
      grid-template-columns: repeat(5, minmax(260px, 1fr));
      gap: 16px; align-items: flex-start; height: 100%;
    }
    .kanban-col {
      background: rgba(12, 12, 18, 0.75);
      backdrop-filter: blur(14px);
      border: 1px solid var(--border);
      border-radius: 10px;
      display: flex; flex-direction: column;
      max-height: calc(100vh - 180px);
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
      position: relative; overflow: hidden;
    }
    .kanban-col::before {
      content: ""; position: absolute; top: 0; left: 0; right: 0; height: 2px;
      background: var(--col-glow, var(--sky)); opacity: 0.8;
    }
    .col-header {
      padding: 12px 14px; display: flex; align-items: center; justify-content: space-between;
      border-bottom: 1px solid var(--border-subtle); user-select: none;
    }
    .col-left { display: flex; align-items: center; gap: 8px; }
    .col-dot { width: 8px; height: 8px; border-radius: 50%; box-shadow: 0 0 8px currentColor; }
    .col-title { font-size: 0.775rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; color: var(--text-muted); }
    .col-count {
      font-family: var(--font-mono); font-size: 0.7rem; font-weight: 600; color: #fff;
      background: rgba(255,255,255,0.08); padding: 1px 7px; border-radius: 9999px;
    }
    .cards-container {
      padding: 10px; display: flex; flex-direction: column; gap: 9px; overflow-y: auto; flex: 1;
    }

    /* Aceternity UI: Glowing Multi-Color Cards */
    .card {
      background: rgba(18, 18, 28, 0.85);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 13px 14px;
      cursor: pointer;
      transition: all 0.2s var(--ease);
      display: flex; flex-direction: column; gap: 9px;
      position: relative;
      overflow: hidden;
    }
    .card::before {
      content: ""; position: absolute; inset: 0; border-radius: 8px; padding: 1px;
      background: linear-gradient(135deg, transparent, rgba(56, 189, 248, 0.3), rgba(217, 70, 239, 0.3), transparent);
      -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
      -webkit-mask-composite: xor;
      mask-composite: exclude;
      opacity: 0; transition: opacity 0.3s ease; pointer-events: none;
    }
    .card:hover {
      background: rgba(24, 24, 38, 0.95);
      transform: translateY(-2px);
      box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.6), 0 0 20px -3px rgba(139, 92, 246, 0.25);
    }
    .card:hover::before { opacity: 1; }

    .card-row-top { display: flex; align-items: center; justify-content: space-between; }
    .company-ident { display: flex; align-items: center; gap: 8px; }
    .company-monogram {
      width: 24px; height: 24px; border-radius: 6px;
      display: flex; align-items: center; justify-content: center;
      font-size: 0.7rem; font-weight: 800; color: #fff;
      box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
    }
    .card-company-name { font-size: 0.875rem; font-weight: 700; color: #fff; }
    .card-role-title { font-size: 0.825rem; color: var(--sky); font-weight: 600; line-height: 1.3; }

    .tag-cluster { display: flex; flex-wrap: wrap; gap: 6px; }
    .pill-tag {
      font-size: 0.675rem; font-family: var(--font-mono); font-weight: 600;
      padding: 2px 7px; border-radius: 4px;
      background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); color: #cbd5e1;
    }
    .pill-comp {
      background: rgba(16, 185, 129, 0.12); border-color: rgba(16, 185, 129, 0.3); color: var(--emerald);
      box-shadow: 0 0 8px rgba(16, 185, 129, 0.15);
    }
    .pill-loc {
      background: rgba(6, 182, 212, 0.12); border-color: rgba(6, 182, 212, 0.3); color: var(--cyan);
    }

    .card-bottom {
      display: flex; align-items: center; justify-content: space-between;
      margin-top: 4px; padding-top: 8px; border-top: 1px solid rgba(255, 255, 255, 0.05);
      font-size: 0.7rem; color: var(--text-dim);
    }
    .card-advance-btn {
      background: rgba(255, 255, 255, 0.05); border: 1px solid var(--border);
      color: var(--text-muted); border-radius: 4px; padding: 2px 8px;
      font-size: 0.675rem; font-weight: 600; cursor: pointer; transition: all 0.15s var(--ease);
    }
    .card-advance-btn:hover {
      background: linear-gradient(135deg, var(--cyan), var(--violet));
      color: #fff; border-color: transparent;
      box-shadow: 0 0 10px rgba(139, 92, 246, 0.4);
    }

    /* Table View Container */
    .table-view-container {
      display: none; background: rgba(14, 14, 22, 0.75);
      border: 1px solid var(--border); border-radius: 10px; overflow: hidden;
      backdrop-filter: blur(16px); box-shadow: 0 4px 25px rgba(0,0,0,0.4);
    }
    .data-table { width: 100%; border-collapse: collapse; text-align: left; font-size: 0.825rem; }
    .data-table th {
      padding: 12px 18px; background: rgba(255,255,255,0.03);
      border-bottom: 1px solid var(--border);
      color: var(--text-dim); font-size: 0.7rem; text-transform: uppercase;
      font-weight: 700; letter-spacing: 0.06em;
    }
    .data-table td { padding: 13px 18px; border-bottom: 1px solid var(--border-subtle); color: var(--text); }
    .data-table tr:hover td { background: rgba(255, 255, 255, 0.04); cursor: pointer; }

    /* Slide-Over Drawer */
    .drawer-overlay {
      position: fixed; inset: 0; background: rgba(0, 0, 0, 0.65);
      backdrop-filter: blur(10px); opacity: 0; pointer-events: none;
      transition: opacity 0.25s var(--ease); z-index: 100;
    }
    .drawer-overlay.open { opacity: 1; pointer-events: auto; }
    .drawer {
      position: fixed; top: 0; right: 0; bottom: 0;
      width: 490px; max-width: 92vw;
      background: rgba(12, 12, 18, 0.95);
      backdrop-filter: blur(25px);
      border-left: 1px solid var(--border-hover);
      box-shadow: -15px 0 40px rgba(0, 0, 0, 0.85), 0 0 30px rgba(139, 92, 246, 0.2);
      transform: translateX(100%);
      transition: transform 0.28s var(--ease);
      z-index: 101; display: flex; flex-direction: column;
    }
    .drawer.open { transform: translateX(0); }
    .drawer-header {
      padding: 18px 22px; border-bottom: 1px solid var(--border);
      display: flex; align-items: center; justify-content: space-between;
    }
    .drawer-body {
      flex: 1; overflow-y: auto; padding: 22px; display: flex; flex-direction: column; gap: 22px;
    }
    .drawer-footer {
      padding: 16px 22px; border-top: 1px solid var(--border);
      display: flex; justify-content: space-between; align-items: center;
    }

    /* Modal / Dialog */
    .modal-backdrop {
      display: none; position: fixed; inset: 0;
      background: rgba(0, 0, 0, 0.75); backdrop-filter: blur(12px);
      justify-content: center; align-items: center; z-index: 200; padding: 16px;
    }
    .modal-window {
      background: rgba(16, 16, 24, 0.95); border: 1px solid var(--border-hover); border-radius: 12px;
      width: 100%; max-width: 530px; padding: 24px;
      box-shadow: 0 25px 60px rgba(0,0,0,0.9), 0 0 30px rgba(56, 189, 248, 0.2);
      backdrop-filter: blur(20px);
    }
    .form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 12px; }
    .form-group { display: flex; flex-direction: column; gap: 6px; margin-bottom: 12px; }
    .form-label { font-size: 0.725rem; font-weight: 700; text-transform: uppercase; color: var(--text-dim); }
    .form-input, .form-select, .form-textarea {
      background: rgba(8, 8, 12, 0.8); border: 1px solid var(--border); color: #fff;
      padding: 9px 12px; border-radius: 6px; font-size: 0.825rem; font-family: var(--font-sans);
      transition: border-color 0.15s ease;
    }
    .form-input:focus, .form-select:focus, .form-textarea:focus {
      outline: none; border-color: var(--sky); box-shadow: 0 0 12px rgba(56, 189, 248, 0.3);
    }

    /* Command Palette cmdk */
    .cmdk-window {
      background: rgba(14, 14, 22, 0.95); border: 1px solid var(--border-hover); border-radius: 12px;
      width: 100%; max-width: 560px; overflow: hidden;
      box-shadow: 0 30px 70px rgba(0,0,0,0.9), 0 0 40px rgba(139, 92, 246, 0.25);
      backdrop-filter: blur(20px);
    }
    .cmdk-input-wrap {
      display: flex; align-items: center; padding: 14px 18px;
      border-bottom: 1px solid var(--border); gap: 12px;
    }
    .cmdk-input {
      flex: 1; background: transparent; border: none; outline: none;
      color: #fff; font-size: 1rem; font-family: var(--font-sans);
    }
    .cmdk-results { max-height: 340px; overflow-y: auto; padding: 8px; }
    .cmdk-item {
      padding: 9px 14px; border-radius: 6px; font-size: 0.825rem;
      color: var(--text-muted); display: flex; align-items: center; justify-content: space-between;
      cursor: pointer; transition: all 0.15s;
    }
    .cmdk-item:hover, .cmdk-item.selected {
      background: linear-gradient(90deg, rgba(56, 189, 248, 0.15), rgba(168, 85, 247, 0.15));
      color: #fff;
    }

    /* Timeline */
    .timeline {
      border-left: 2px solid var(--border); padding-left: 14px;
      display: flex; flex-direction: column; gap: 12px;
    }
    .timeline-node { font-size: 0.775rem; }
    .timeline-node-time { font-size: 0.675rem; font-family: var(--font-mono); color: var(--sky); }

    .icon { display: inline-block; width: 15px; height: 15px; vertical-align: middle; fill: none; stroke: currentColor; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; }
  </style>
</head>
<body>
  <!-- Magic UI: Ambient Aurora Gradient Mesh -->
  <div class="aurora-bg">
    <div class="aurora-sphere sphere-1"></div>
    <div class="aurora-sphere sphere-2"></div>
    <div class="aurora-sphere sphere-3"></div>
    <div class="aurora-sphere sphere-4"></div>
  </div>

  <!-- Aceternity UI: Celestial Glowing Lion Emblem in Background -->
  <svg class="lion-backdrop-canvas" id="celestialLion" viewBox="0 0 800 800" fill="none" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <linearGradient id="lionAurora" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#06b6d4" stop-opacity="0.8"/>
        <stop offset="40%" stop-color="#8b5cf6" stop-opacity="0.9"/>
        <stop offset="70%" stop-color="#ec4899" stop-opacity="0.8"/>
        <stop offset="100%" stop-color="#f59e0b" stop-opacity="0.7"/>
      </linearGradient>
      <linearGradient id="lionMane" x1="100%" y1="0%" x2="0%" y2="100%">
        <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.7"/>
        <stop offset="50%" stop-color="#a855f7" stop-opacity="0.5"/>
        <stop offset="100%" stop-color="#10b981" stop-opacity="0.4"/>
      </linearGradient>
    </defs>
    <!-- Geometric Celestial Lion Constellation -->
    <g stroke="url(#lionAurora)" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
      <!-- Head / Crown Geometry -->
      <polygon points="400,120 480,210 400,260 320,210" fill="rgba(139, 92, 246, 0.04)"/>
      <polygon points="400,260 490,290 400,380 310,290" fill="rgba(6, 182, 212, 0.05)"/>
      
      <!-- Mane Outer Nodes -->
      <polygon points="320,210 230,220 280,310 310,290" fill="rgba(56, 189, 248, 0.03)"/>
      <polygon points="480,210 570,220 520,310 490,290" fill="rgba(236, 72, 153, 0.03)"/>
      <polygon points="280,310 200,340 260,430 310,390" fill="rgba(139, 92, 246, 0.03)"/>
      <polygon points="520,310 600,340 540,430 490,390" fill="rgba(245, 158, 11, 0.03)"/>
      <polygon points="260,430 190,480 270,550 330,480" fill="rgba(6, 182, 212, 0.03)"/>
      <polygon points="540,430 610,480 530,550 470,480" fill="rgba(236, 72, 153, 0.03)"/>

      <!-- Facial Muzzle & Whisker Architecture -->
      <polygon points="400,380 440,460 400,520 360,460" fill="rgba(16, 185, 129, 0.06)"/>
      <polygon points="360,460 310,390 330,480 370,540" fill="rgba(56, 189, 248, 0.04)"/>
      <polygon points="440,460 490,390 470,480 430,540" fill="rgba(217, 70, 239, 0.04)"/>
      <polygon points="400,520 430,540 400,610 370,540" fill="rgba(245, 158, 11, 0.08)"/>

      <!-- Eyes (Glowing Star Nodes) -->
      <circle cx="360" cy="330" r="5" fill="#38bdf8" stroke="#ffffff" stroke-width="1.5"/>
      <circle cx="440" cy="330" r="5" fill="#ec4899" stroke="#ffffff" stroke-width="1.5"/>
      
      <!-- Crown Apex Stars -->
      <circle cx="400" cy="120" r="4" fill="#f59e0b"/>
      <circle cx="480" cy="210" r="4" fill="#a855f7"/>
      <circle cx="320" cy="210" r="4" fill="#06b6d4"/>
      <circle cx="400" cy="610" r="5" fill="#10b981"/>
    </g>
    <!-- Extended Mane Whispers -->
    <g stroke="url(#lionMane)" stroke-width="1.2" stroke-dasharray="3,3" opacity="0.6">
      <path d="M400,90 L400,120 M230,220 L170,230 M570,220 L630,230 M200,340 L130,370 M600,340 L670,370 M190,480 L120,520 M610,480 L680,520 M400,610 L400,670"/>
      <circle cx="400" cy="90" r="3" fill="#38bdf8"/>
      <circle cx="170" cy="230" r="3" fill="#8b5cf6"/>
      <circle cx="630" cy="230" r="3" fill="#f43f5e"/>
    </g>
  </svg>

  <div class="app-shell">
    <!-- Left Navigation Sidebar -->
    <aside>
      <div class="sidebar-top">
        <div class="workspace-header">
          <div class="workspace-info">
            <div class="avatar-pill">L</div>
            <div>
              <div class="workspace-name shimmer-text">Lion Workspace</div>
              <div class="workspace-role">Simon Munyambu · Systems</div>
            </div>
          </div>
          <svg class="icon text-dim" viewBox="0 0 24 24"><path d="m6 9 6 6 6-6"/></svg>
        </div>

        <button class="cmd-trigger" onclick="openCommandPalette()">
          <span style="display:flex; align-items:center; gap:8px;">
            <svg class="icon" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
            Search / Palette
          </span>
          <span class="kbd-chip">⌘K</span>
        </button>

        <div class="nav-group-title">Pipeline Views</div>
        <ul class="nav-list">
          <li class="nav-item active" id="navAll" onclick="filterNav('ALL')">
            <div class="nav-item-left">
              <svg class="icon" viewBox="0 0 24 24"><rect width="7" height="18" x="3" y="3" rx="1"/><rect width="7" height="18" x="14" y="3" rx="1"/></svg>
              <span>All Opportunities</span>
            </div>
            <span class="nav-badge" id="bNavAll">-</span>
          </li>
          <li class="nav-item" id="navActive" onclick="filterNav('ACTIVE')">
            <div class="nav-item-left">
              <svg class="icon" style="color:var(--cyan)" viewBox="0 0 24 24"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>
              <span>Active In-Flight</span>
            </div>
            <span class="nav-badge" id="bNavActive">-</span>
          </li>
          <li class="nav-item" id="navInterviews" onclick="filterNav('INTERVIEWS')">
            <div class="nav-item-left">
              <svg class="icon" style="color:var(--violet)" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="m12 6 4 6h-8l4 6"/></svg>
              <span>Interviews</span>
            </div>
            <span class="nav-badge" id="bNavInt">-</span>
          </li>
          <li class="nav-item" id="navOffers" onclick="filterNav('OFFER')">
            <div class="nav-item-left">
              <svg class="icon" style="color:var(--emerald)" viewBox="0 0 24 24"><path d="M12 2v20"/><path d="m17 5-5-3-5 3"/><path d="m17 19-5 3-5-3"/><circle cx="12" cy="12" r="4"/></svg>
              <span>Offers</span>
            </div>
            <span class="nav-badge" id="bNavOffer">-</span>
          </li>
          <li class="nav-item" id="navArchive" onclick="filterNav('REJECTED')">
            <div class="nav-item-left">
              <svg class="icon text-dim" viewBox="0 0 24 24"><rect width="20" height="5" x="2" y="3" rx="1"/><path d="M4 8v11a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8"/><path d="M10 12h4"/></svg>
              <span>Archived</span>
            </div>
            <span class="nav-badge" id="bNavArch">-</span>
          </li>
        </ul>
      </div>

      <div class="sidebar-footer">
        <div class="live-status">
          <div class="status-dot"></div>
          <span>Loopback: 127.0.0.1:8765</span>
        </div>
      </div>
    </aside>

    <!-- Main View Panel -->
    <main>
      <!-- Top Bar -->
      <header class="top-bar">
        <div class="breadcrumbs">
          <span class="breadcrumb-root">Pipeline</span>
          <span class="breadcrumb-sep">/</span>
          <span class="breadcrumb-current shimmer-text" id="viewTitle">All Opportunities</span>
        </div>
        <div class="top-actions">
          <button class="btn btn-secondary" onclick="fetchData()">
            <svg class="icon" viewBox="0 0 24 24"><path d="M21 12a9 9 0 0 0-9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/><path d="M3 12a9 9 0 0 0 9 9 9.75 9.75 0 0 0 6.74-2.74L21 16"/><path d="M16 16h5v5"/></svg>
            Sync
          </button>
          <button class="btn btn-gradient" onclick="openNewModal()">
            <svg class="icon" viewBox="0 0 24 24"><path d="M5 12h14"/><path d="M12 5v14"/></svg>
            New Opportunity
          </button>
        </div>
      </header>

      <!-- Glowing Stats Strip -->
      <section class="stats-strip" aria-label="Pipeline Telemetry">
        <div class="stat-pill">
          <span class="stat-pill-label">Total Ingested</span>
          <span class="stat-pill-val" id="mTotal">-</span>
        </div>
        <div class="stat-pill">
          <span class="stat-pill-label">Active</span>
          <span class="stat-pill-val" id="mActive">-</span>
        </div>
        <div class="stat-pill">
          <span class="stat-pill-label">Interview Rate</span>
          <span class="stat-pill-val" id="mInterviews">-</span>
          <span class="stat-pill-badge badge-cyan" id="mIntBadge">-%</span>
        </div>
        <div class="stat-pill">
          <span class="stat-pill-label">Offers Won</span>
          <span class="stat-pill-val" id="mOffers">-</span>
          <span class="stat-pill-badge badge-emerald" id="mOffBadge">-%</span>
        </div>
      </section>

      <!-- Control Bar -->
      <div class="control-header">
        <div class="filters-left">
          <div class="search-box-wrap">
            <svg class="icon search-box-icon" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
            <input type="text" class="search-box" id="searchBox" placeholder="Filter company, role, or stack..." oninput="handleSearch()">
          </div>
        </div>

        <div class="view-toggle">
          <button class="toggle-btn active" id="btnKanban" onclick="setViewMode('kanban')">
            <svg class="icon" viewBox="0 0 24 24"><rect width="7" height="18" x="3" y="3" rx="1"/><rect width="7" height="18" x="14" y="3" rx="1"/></svg>
            Board
          </button>
          <button class="toggle-btn" id="btnTable" onclick="setViewMode('table')">
            <svg class="icon" viewBox="0 0 24 24"><path d="M3 6h18"/><path d="M3 12h18"/><path d="M3 18h18"/></svg>
            Table
          </button>
        </div>
      </div>

      <!-- Main Dynamic Content -->
      <div class="content-area">
        <!-- Kanban Board -->
        <div class="kanban-grid" id="kanbanBoard"></div>

        <!-- Table View -->
        <div class="table-view-container" id="tableView">
          <table class="data-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Company</th>
                <th>Role</th>
                <th>Location</th>
                <th>Stage</th>
                <th>Target Comp</th>
                <th>Channel</th>
                <th>Last Update</th>
              </tr>
            </thead>
            <tbody id="tableBody"></tbody>
          </table>
        </div>
      </div>
    </main>
  </div>

  <!-- Slide-Over Drawer (Right Side) -->
  <div class="drawer-overlay" id="drawerOverlay" onclick="closeDrawer()"></div>
  <div class="drawer" id="slideDrawer">
    <div class="drawer-header">
      <div style="display:flex; align-items:center; gap:10px;">
        <div class="company-monogram" id="dMonogram" style="background:var(--sky);">MS</div>
        <div>
          <div style="font-size:1.05rem; font-weight:700; color:#fff;" id="dCompany">Company</div>
          <div style="font-size:0.8rem; color:var(--sky); font-weight:600;" id="dRole">Role</div>
        </div>
      </div>
      <button class="btn btn-ghost" onclick="closeDrawer()" style="padding:4px 8px;">✕</button>
    </div>

    <div class="drawer-body">
      <!-- Properties Grid -->
      <div style="background:rgba(8, 8, 12, 0.85); border:1px solid var(--border); border-radius:10px; padding:14px; font-size:0.8rem; display:flex; flex-direction:column; gap:10px;">
        <div style="display:flex; justify-content:space-between; align-items:center;">
          <span style="color:var(--text-dim)">Location Model</span>
          <span class="pill-tag pill-loc" id="dLoc">NAIROBI</span>
        </div>
        <div style="display:flex; justify-content:space-between; align-items:center;">
          <span style="color:var(--text-dim)">Compensation</span>
          <span class="pill-tag pill-comp" id="dComp">-</span>
        </div>
        <div style="display:flex; justify-content:space-between; align-items:center;">
          <span style="color:var(--text-dim)">Channel</span>
          <span class="pill-tag" id="dChannel">-</span>
        </div>
        <div style="display:flex; justify-content:space-between; align-items:center;" id="dUrlRow">
          <span style="color:var(--text-dim)">Posting URL</span>
          <span id="dUrlContainer"></span>
        </div>
      </div>

      <!-- Quick Stage Stepper -->
      <div>
        <label class="form-label">Current Pipeline Stage</label>
        <select class="form-select" id="dStatusSelect" onchange="saveDrawerStatus()">
          <option value="WISHLIST">Wishlist</option>
          <option value="APPLIED">Applied</option>
          <option value="SCREENING">Screening</option>
          <option value="TECHNICAL">Technical Round</option>
          <option value="FINAL_ROUND">Final Round</option>
          <option value="OFFER">Offer Received</option>
          <option value="REJECTED">Archived / Rejected</option>
          <option value="WITHDRAWN">Withdrawn</option>
        </select>
      </div>

      <!-- Notes -->
      <div>
        <label class="form-label">Technical Notes & Stack Invariants</label>
        <div id="dNotesBox" style="background:rgba(8, 8, 12, 0.85); border:1px solid var(--border); border-radius:8px; padding:12px; font-size:0.825rem; color:var(--text-muted); min-height:70px; line-height:1.4;"></div>
      </div>

      <!-- Audit Timeline -->
      <div>
        <label class="form-label">Audit Log & Event Chronology</label>
        <div class="timeline" id="dTimeline"></div>
      </div>
    </div>

    <div class="drawer-footer">
      <button class="btn" style="background:rgba(239, 68, 68, 0.15); color:var(--rose); border:1px solid rgba(239,68,68,0.3);" onclick="deleteActiveApp()">Delete Application</button>
      <button class="btn btn-secondary" onclick="closeDrawer()">Done</button>
    </div>
  </div>

  <!-- Command Palette (cmdk style) -->
  <div class="modal-backdrop" id="cmdkModal" onclick="handleBackdropClick(event, 'cmdkModal')">
    <div class="cmdk-window">
      <div class="cmdk-input-wrap">
        <svg class="icon text-dim" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
        <input type="text" class="cmdk-input" id="cmdkSearch" placeholder="Type a command or company name..." oninput="filterCmdk()">
        <span class="kbd-chip">ESC</span>
      </div>
      <div class="cmdk-results" id="cmdkResults"></div>
    </div>
  </div>

  <!-- New Application Modal -->
  <div class="modal-backdrop" id="newAppModal" onclick="handleBackdropClick(event, 'newAppModal')">
    <div class="modal-window">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:18px;">
        <h3 style="font-size:1.1rem; font-weight:800; color:#fff;" class="shimmer-text">Record New Opportunity</h3>
        <button class="btn btn-ghost" onclick="closeModal('newAppModal')" style="padding:4px;">✕</button>
      </div>
      <form id="appForm" onsubmit="submitNewApp(event)">
        <div class="form-row">
          <div class="form-group">
            <label class="form-label">Company *</label>
            <input type="text" class="form-input" id="fCompany" required placeholder="e.g. Microsoft ADC, Safaricom, Deel">
          </div>
          <div class="form-group">
            <label class="form-label">Role *</label>
            <input type="text" class="form-input" id="fRole" required placeholder="e.g. Systems Engineer">
          </div>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label class="form-label">Location Model</label>
            <select class="form-select" id="fLoc">
              <option value="NAIROBI">Nairobi (On-Site/Hybrid)</option>
              <option value="REMOTE_EMEA" selected>Remote (EMEA / UTC+3)</option>
              <option value="REMOTE_GLOBAL">Remote (Global)</option>
              <option value="HYBRID">Hybrid</option>
            </select>
          </div>
          <div class="form-group">
            <label class="form-label">Initial Stage</label>
            <select class="form-select" id="fStatus">
              <option value="APPLIED">Applied</option>
              <option value="WISHLIST">Wishlist</option>
              <option value="SCREENING">Screening</option>
            </select>
          </div>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label class="form-label">Target Compensation</label>
            <input type="text" class="form-input" id="fComp" placeholder="e.g. $5,500/mo or KES 450,000">
          </div>
          <div class="form-group">
            <label class="form-label">Channel</label>
            <input type="text" class="form-input" id="fChannel" placeholder="e.g. Referral, Wellfound, Direct">
          </div>
        </div>
        <div class="form-group">
          <label class="form-label">Job Posting URL</label>
          <input type="url" class="form-input" id="fUrl" placeholder="https://careers...">
        </div>
        <div class="form-group">
          <label class="form-label">Technical Notes</label>
          <textarea class="form-textarea" id="fNotes" rows="3" placeholder="Key tech requirements, team lead contacts..."></textarea>
        </div>
        <div style="display:flex; justify-content:flex-end; gap:8px; margin-top:16px;">
          <button type="button" class="btn btn-secondary" onclick="closeModal('newAppModal')">Cancel</button>
          <button type="submit" class="btn btn-gradient">Save to Pipeline</button>
        </div>
      </form>
    </div>
  </div>

  <script>
    let applications = [];
    let currentFilter = 'ALL';
    let currentView = 'kanban';
    let activeAppId = null;

    const COLORS = [
      'linear-gradient(135deg, #06b6d4, #3b82f6)',
      'linear-gradient(135deg, #8b5cf6, #d946ef)',
      'linear-gradient(135deg, #ec4899, #f43f5e)',
      'linear-gradient(135deg, #10b981, #06b6d4)',
      'linear-gradient(135deg, #f59e0b, #ec4899)',
      'linear-gradient(135deg, #6366f1, #a855f7)'
    ];

    function getMonogramGradient(str) {
      let hash = 0;
      for (let i = 0; i < str.length; i++) hash = str.charCodeAt(i) + ((hash << 5) - hash);
      return COLORS[Math.abs(hash) % COLORS.length];
    }

    function getInitials(str) {
      const parts = str.trim().split(/\s+/);
      if (parts.length >= 2) return (parts[0][0] + parts[1][0]).toUpperCase();
      return str.substring(0, 2).toUpperCase();
    }

    async function fetchData() {
      try {
        const [appsRes, metricsRes] = await Promise.all([
          fetch('/api/applications'),
          fetch('/api/metrics')
        ]);
        applications = await appsRes.json();
        const metrics = await metricsRes.json();
        renderSidebarBadges(metrics);
        renderMetricsStrip(metrics);
        renderView();
      } catch (err) {
        console.error("Fetch error:", err);
      }
    }

    function renderSidebarBadges(m) {
      document.getElementById('bNavAll').textContent = m.total_applications;
      document.getElementById('bNavActive').textContent = m.active_applications;
      document.getElementById('bNavInt').textContent = m.interview_count;
      document.getElementById('bNavOffer').textContent = m.offer_count;
      document.getElementById('bNavArch').textContent = m.rejection_count;
    }

    function renderMetricsStrip(m) {
      document.getElementById('mTotal').textContent = m.total_applications;
      document.getElementById('mActive').textContent = m.active_applications;
      document.getElementById('mInterviews').textContent = m.interview_count;
      document.getElementById('mIntBadge').textContent = `${m.interview_rate_pct}% conv`;
      document.getElementById('mOffers').textContent = m.offer_count;
      document.getElementById('mOffBadge').textContent = `${m.offer_rate_pct}% conv`;
    }

    function filterNav(filter) {
      currentFilter = filter;
      document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
      const activeEl = filter === 'ALL' ? 'navAll' :
                       filter === 'ACTIVE' ? 'navActive' :
                       filter === 'INTERVIEWS' ? 'navInterviews' :
                       filter === 'OFFER' ? 'navOffers' : 'navArchive';
      document.getElementById(activeEl).classList.add('active');

      const titles = {
        'ALL': 'All Opportunities',
        'ACTIVE': 'Active In-Flight Pipeline',
        'INTERVIEWS': 'Interviewing Stages',
        'OFFER': 'Offers Won',
        'REJECTED': 'Archived & Rejections'
      };
      document.getElementById('viewTitle').textContent = titles[filter];
      renderView();
    }

    function setViewMode(mode) {
      currentView = mode;
      document.getElementById('btnKanban').classList.toggle('active', mode === 'kanban');
      document.getElementById('btnTable').classList.toggle('active', mode === 'table');
      renderView();
    }

    function getFilteredData() {
      const q = document.getElementById('searchBox').value.toLowerCase().trim();
      return applications.filter(app => {
        if (currentFilter === 'ACTIVE' && (app.status === 'REJECTED' || app.status === 'WITHDRAWN')) return false;
        if (currentFilter === 'INTERVIEWS' && !(app.status === 'SCREENING' || app.status === 'TECHNICAL' || app.status === 'FINAL_ROUND')) return false;
        if (currentFilter === 'OFFER' && app.status !== 'OFFER') return false;
        if (currentFilter === 'REJECTED' && !(app.status === 'REJECTED' || app.status === 'WITHDRAWN')) return false;

        if (q) {
          const match = app.company.toLowerCase().includes(q) ||
                        app.role.toLowerCase().includes(q) ||
                        app.channel.toLowerCase().includes(q) ||
                        (app.notes && app.notes.toLowerCase().includes(q));
          if (!match) return false;
        }
        return true;
      });
    }

    function renderView() {
      if (currentView === 'kanban') {
        document.getElementById('kanbanBoard').style.display = 'grid';
        document.getElementById('tableView').style.display = 'none';
        renderKanban();
      } else {
        document.getElementById('kanbanBoard').style.display = 'none';
        document.getElementById('tableView').style.display = 'block';
        renderTable();
      }
    }

    function renderKanban() {
      const board = document.getElementById('kanbanBoard');
      board.innerHTML = '';
      const filtered = getFilteredData();

      const columns = [
        { id: 'APPLIED', title: 'Applied', color: '#06b6d4', glow: 'linear-gradient(90deg, #06b6d4, #3b82f6)', next: 'SCREENING', label: '→ Screen' },
        { id: 'SCREENING', title: 'Screening', color: '#8b5cf6', glow: 'linear-gradient(90deg, #8b5cf6, #d946ef)', next: 'TECHNICAL', label: '→ Tech' },
        { id: 'TECHNICAL', title: 'Technical', color: '#f59e0b', glow: 'linear-gradient(90deg, #f59e0b, #f43f5e)', next: 'OFFER', label: '→ Offer' },
        { id: 'OFFER', title: 'Offers', color: '#10b981', glow: 'linear-gradient(90deg, #10b981, #06b6d4)', next: null, label: null },
        { id: 'REJECTED', title: 'Archived', color: '#64748b', glow: '#64748b', next: null, label: null }
      ];

      columns.forEach(col => {
        const matching = filtered.filter(app => {
          if (col.id === 'APPLIED') return app.status === 'APPLIED' || app.status === 'WISHLIST';
          if (col.id === 'SCREENING') return app.status === 'SCREENING';
          if (col.id === 'TECHNICAL') return app.status === 'TECHNICAL' || app.status === 'FINAL_ROUND';
          if (col.id === 'OFFER') return app.status === 'OFFER';
          if (col.id === 'REJECTED') return app.status === 'REJECTED' || app.status === 'WITHDRAWN';
          return false;
        });

        const colDiv = document.createElement('div');
        colDiv.className = 'kanban-col';
        colDiv.style.setProperty('--col-glow', col.glow);
        colDiv.innerHTML = `
          <div class="col-header">
            <div class="col-left">
              <div class="col-dot" style="background:${col.color}; color:${col.color};"></div>
              <span class="col-title">${col.title}</span>
            </div>
            <span class="col-count">${matching.length}</span>
          </div>
          <div class="cards-container" id="col-${col.id}"></div>
        `;

        const container = colDiv.querySelector(`#col-${col.id}`);
        matching.forEach(app => {
          const card = document.createElement('div');
          card.className = 'card';
          card.onclick = () => openDrawer(app.id);

          const monogramGradient = getMonogramGradient(app.company);
          const initials = getInitials(app.company);
          const advanceBtn = col.next ?
            `<button class="card-advance-btn" onclick="quickAdvance(event, ${app.id}, '${col.next}')">${col.label}</button>` : '';

          card.innerHTML = `
            <div class="card-row-top">
              <div class="company-ident">
                <div class="company-monogram" style="background:${monogramGradient};">${initials}</div>
                <div class="card-company-name">${escapeHtml(app.company)}</div>
              </div>
              <span style="font-size:0.675rem; color:var(--text-dim); font-family:var(--font-mono);">${app.applied_at.substring(5, 10)}</span>
            </div>
            <div class="card-role-title">${escapeHtml(app.role)}</div>
            <div class="tag-cluster">
              <span class="pill-tag pill-loc">${app.location_type}</span>
              ${app.compensation ? `<span class="pill-tag pill-comp">${escapeHtml(app.compensation)}</span>` : ''}
              <span class="pill-tag">${escapeHtml(app.channel)}</span>
            </div>
            <div class="card-bottom">
              <span style="font-family:var(--font-mono);">#${app.id}</span>
              <div onclick="event.stopPropagation()">${advanceBtn}</div>
            </div>
          `;
          container.appendChild(card);
        });

        board.appendChild(colDiv);
      });
    }

    function renderTable() {
      const tbody = document.getElementById('tableBody');
      tbody.innerHTML = '';
      const filtered = getFilteredData();

      filtered.forEach(app => {
        const tr = document.createElement('tr');
        tr.onclick = () => openDrawer(app.id);
        const monogramGradient = getMonogramGradient(app.company);
        const initials = getInitials(app.company);

        tr.innerHTML = `
          <td style="font-family:var(--font-mono); color:var(--text-dim);">${app.id}</td>
          <td>
            <div style="display:flex; align-items:center; gap:8px;">
              <div class="company-monogram" style="background:${monogramGradient}; width:20px; height:20px; font-size:0.65rem;">${initials}</div>
              <strong style="color:#fff;">${escapeHtml(app.company)}</strong>
            </div>
          </td>
          <td style="color:var(--sky); font-weight:600;">${escapeHtml(app.role)}</td>
          <td><span class="pill-tag pill-loc">${app.location_type}</span></td>
          <td><span class="pill-tag">${app.status}</span></td>
          <td style="font-family:var(--font-mono); color:var(--emerald); font-weight:600;">${app.compensation ? escapeHtml(app.compensation) : '-'}</td>
          <td><span class="pill-tag">${escapeHtml(app.channel)}</span></td>
          <td style="font-family:var(--font-mono); color:var(--text-dim); font-size:0.75rem;">${app.last_activity_at.substring(0, 10)}</td>
        `;
        tbody.appendChild(tr);
      });
    }

    async function quickAdvance(e, id, nextStatus) {
      e.stopPropagation();
      await fetch(`/api/applications/${id}/status`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status: nextStatus, note: `Quick-advanced to ${nextStatus}` })
      });
      await fetchData();
    }

    function handleSearch() {
      renderView();
    }

    /* Drawer handlers */
    async function openDrawer(id) {
      activeAppId = id;
      const res = await fetch(`/api/applications/${id}`);
      if (!res.ok) return;
      const app = await res.json();

      document.getElementById('dCompany').textContent = app.company;
      document.getElementById('dRole').textContent = app.role;
      document.getElementById('dLoc').textContent = app.location_type;
      document.getElementById('dComp').textContent = app.compensation || 'Unspecified';
      document.getElementById('dChannel').textContent = app.channel;
      document.getElementById('dStatusSelect').value = app.status;

      const mono = document.getElementById('dMonogram');
      mono.textContent = getInitials(app.company);
      mono.style.background = getMonogramGradient(app.company);

      const urlContainer = document.getElementById('dUrlContainer');
      if (app.job_url) {
        urlContainer.innerHTML = `<a href="${escapeHtml(app.job_url)}" target="_blank" style="color:var(--sky); text-decoration:none; font-weight:600;">Open Posting ↗</a>`;
      } else {
        urlContainer.innerHTML = '<span style="color:var(--text-dim)">None</span>';
      }

      document.getElementById('dNotesBox').textContent = app.notes || 'No technical notes recorded.';

      const timelineBox = document.getElementById('dTimeline');
      timelineBox.innerHTML = '';
      (app.timeline || []).forEach(ev => {
        const item = document.createElement('div');
        item.className = 'timeline-node';
        item.innerHTML = `
          <div><strong>${escapeHtml(ev.event_type)}</strong>: ${escapeHtml(ev.details)}</div>
          <div class="timeline-node-time">${ev.created_at.replace('T', ' ').substring(0, 19)} UTC</div>
        `;
        timelineBox.appendChild(item);
      });

      document.getElementById('drawerOverlay').classList.add('open');
      document.getElementById('slideDrawer').classList.add('open');
    }

    function closeDrawer() {
      document.getElementById('drawerOverlay').classList.remove('open');
      document.getElementById('slideDrawer').classList.remove('open');
    }

    async function saveDrawerStatus() {
      if (!activeAppId) return;
      const newStatus = document.getElementById('dStatusSelect').value;
      await fetch(`/api/applications/${activeAppId}/status`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status: newStatus })
      });
      await fetchData();
      openDrawer(activeAppId);
    }

    async function deleteActiveApp() {
      if (!activeAppId || !confirm("Permanently delete this application?")) return;
      await fetch(`/api/applications/${activeAppId}`, { method: 'DELETE' });
      closeDrawer();
      await fetchData();
    }

    /* Modal Handlers */
    function openNewModal() {
      document.getElementById('newAppModal').style.display = 'flex';
      setTimeout(() => document.getElementById('fCompany').focus(), 50);
    }

    function closeModal(id) {
      document.getElementById(id).style.display = 'none';
    }

    function handleBackdropClick(e, id) {
      if (e.target.id === id) closeModal(id);
    }

    async function submitNewApp(e) {
      e.preventDefault();
      const payload = {
        company: document.getElementById('fCompany').value,
        role: document.getElementById('fRole').value,
        location_type: document.getElementById('fLoc').value,
        status: document.getElementById('fStatus').value,
        compensation: document.getElementById('fComp').value || null,
        channel: document.getElementById('fChannel').value || 'Direct',
        job_url: document.getElementById('fUrl').value || null,
        notes: document.getElementById('fNotes').value || null
      };

      const res = await fetch('/api/applications', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      if (res.ok) {
        closeModal('newAppModal');
        document.getElementById('appForm').reset();
        await fetchData();
      }
    }

    /* Command Palette cmdk */
    function openCommandPalette() {
      document.getElementById('cmdkModal').style.display = 'flex';
      document.getElementById('cmdkSearch').value = '';
      filterCmdk();
      setTimeout(() => document.getElementById('cmdkSearch').focus(), 50);
    }

    function filterCmdk() {
      const q = document.getElementById('cmdkSearch').value.toLowerCase().trim();
      const results = document.getElementById('cmdkResults');
      results.innerHTML = '';

      const actions = [
        { label: '+ Create new application', action: () => { closeModal('cmdkModal'); openNewModal(); } },
        { label: 'View Kanban Board', action: () => { closeModal('cmdkModal'); setViewMode('kanban'); } },
        { label: 'View Data Table', action: () => { closeModal('cmdkModal'); setViewMode('table'); } },
        { label: 'Filter: Active Interviews', action: () => { closeModal('cmdkModal'); filterNav('INTERVIEWS'); } },
        { label: 'Filter: Offers Won', action: () => { closeModal('cmdkModal'); filterNav('OFFER'); } }
      ];

      actions.forEach(a => {
        if (!q || a.label.toLowerCase().includes(q)) {
          const div = document.createElement('div');
          div.className = 'cmdk-item';
          div.innerHTML = `<span>⚡ ${a.label}</span><span class="kbd-chip">Action</span>`;
          div.onclick = a.action;
          results.appendChild(div);
        }
      });

      applications.forEach(app => {
        if (!q || app.company.toLowerCase().includes(q) || app.role.toLowerCase().includes(q)) {
          const div = document.createElement('div');
          div.className = 'cmdk-item';
          div.innerHTML = `
            <span><strong>${escapeHtml(app.company)}</strong> · ${escapeHtml(app.role)}</span>
            <span class="pill-tag pill-loc">${app.status}</span>
          `;
          div.onclick = () => { closeModal('cmdkModal'); openDrawer(app.id); };
          results.appendChild(div);
        }
      });
    }

    function escapeHtml(str) {
      if (!str) return '';
      return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
    }

    /* Global Keyboard Shortcuts */
    document.addEventListener('keydown', (e) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        openCommandPalette();
      } else if (e.key === 'Escape') {
        closeDrawer();
        closeModal('cmdkModal');
        closeModal('newAppModal');
      } else if (e.key === 'n' && document.activeElement.tagName !== 'INPUT' && document.activeElement.tagName !== 'TEXTAREA') {
        e.preventDefault();
        openNewModal();
      }
    });

    window.onload = fetchData;
  </script>
</body>
</html>
"""

async def handle_dashboard(request: Request):
    return HTMLResponse(DASHBOARD_HTML)

async def handle_list_applications(request: Request):
    status = request.query_params.get("status")
    search = request.query_params.get("search")
    rows = db.list_applications(status=status, search=search)
    return JSONResponse(rows)

async def handle_create_application(request: Request):
    try:
        body = await request.json()
        app = ApplicationCreate(**body)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=400)
    app_id = db.create_application(app)
    return JSONResponse({"id": app_id, "status": "created"}, status_code=201)

async def handle_get_application(request: Request):
    app_id = int(request.path_params["id"])
    data = db.get_application(app_id)
    if not data:
        return JSONResponse({"error": "Not found"}, status_code=404)
    return JSONResponse(data)

async def handle_update_status(request: Request):
    app_id = int(request.path_params["id"])
    body = await request.json()
    new_status_str = body.get("status")
    note = body.get("note")
    try:
        new_status = AppStatus(new_status_str)
    except ValueError:
        return JSONResponse({"error": f"Invalid status: {new_status_str}"}, status_code=400)
    
    success = db.update_status(app_id, new_status, note=note)
    if not success:
        return JSONResponse({"error": "Application not found"}, status_code=404)
    return JSONResponse({"status": "updated", "new_status": new_status.value})

async def handle_delete_application(request: Request):
    app_id = int(request.path_params["id"])
    success = db.delete_application(app_id)
    if not success:
        return JSONResponse({"error": "Application not found"}, status_code=404)
    return JSONResponse({"status": "deleted"})

async def handle_get_metrics(request: Request):
    metrics = db.get_metrics()
    return JSONResponse(metrics)

routes = [
    Route("/", endpoint=handle_dashboard, methods=["GET"]),
    Route("/api/applications", endpoint=handle_list_applications, methods=["GET"]),
    Route("/api/applications", endpoint=handle_create_application, methods=["POST"]),
    Route("/api/applications/{id:int}", endpoint=handle_get_application, methods=["GET"]),
    Route("/api/applications/{id:int}/status", endpoint=handle_update_status, methods=["PATCH"]),
    Route("/api/applications/{id:int}", endpoint=handle_delete_application, methods=["DELETE"]),
    Route("/api/metrics", endpoint=handle_get_metrics, methods=["GET"]),
]

app = Starlette(debug=False, routes=routes, on_startup=[db.init_db])

def run_server(host: str = None, port: int = None):
    import uvicorn
    import os
    env_port = int(os.environ.get("PORT", 8765))
    target_port = port if port is not None else env_port
    target_host = host if host is not None else ("0.0.0.0" if "PORT" in os.environ else "127.0.0.1")
    db.init_db()
    print(f"\n[+] Applications Tracker Dashboard running at: http://{target_host}:{target_port}")
    uvicorn.run(app, host=target_host, port=target_port, log_level="warning")

if __name__ == "__main__":
    run_server()
