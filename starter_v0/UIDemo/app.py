from __future__ import annotations

import base64
import html
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import streamlit as st
from markdown_it import MarkdownIt


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from chat import now_iso, run_model_tool_loop, safe_slug, trim_history, write_transcript
from env_loader import load_lab_env
from providers import make_provider
from tools import TOOL_FUNCTIONS, load_tool_declarations, to_openai_tools
from versioning import artifact_version_dict, build_artifact_version


ARTIFACTS_DIR = ROOT / "artifacts"
RUNS_DIR = ROOT / "runs"
BACKGROUND_PATH = Path(__file__).resolve().parent / "assets" / "sapphire-haze.jpg"
PROVIDER_KEYS = {
    "openrouter": "OPENROUTER_API_KEY",
    "openai": "OPENAI_API_KEY",
    "anthropic": "ANTHROPIC_API_KEY",
    "gemini": "GEMINI_API_KEY",
}
MARKDOWN = MarkdownIt("commonmark", {"html": False, "linkify": False, "typographer": True})
TOOL_CATALOG = {
    "clarify": ("Hỏi thêm thông tin", "Yêu cầu bạn bổ sung dữ liệu hoặc xác nhận trước khi tiếp tục."),
    "search_kb": ("Tìm hướng dẫn kỹ thuật", "Tra cứu cách xử lý sự cố trong kho kiến thức nội bộ."),
    "search_device_info": ("Tìm thông tin thiết bị", "Tìm tài liệu công khai theo hãng và model, không gửi dữ liệu nội bộ."),
    "check_service_status": ("Kiểm tra dịch vụ", "Xem trạng thái VPN, email, SSO, Wi-Fi hoặc hệ thống in."),
    "inspect_device": ("Chẩn đoán thiết bị", "Kiểm tra thông tin và tình trạng máy theo mã tài sản."),
    "lookup_user": ("Tra cứu nhân viên", "Xem thông tin hỗ trợ và thiết bị được cấp theo mã nhân viên."),
    "format_incident_report": ("Tạo báo cáo sự cố", "Tổng hợp các kết quả đã có thành báo cáo dễ bàn giao."),
    "policy": ("Tra cứu chính sách", "Tìm quy định IT nội bộ về quyền truy cập, dữ liệu và xử lý sự cố."),
    "create_ticket": ("Tạo phiếu hỗ trợ", "Ghi nhận yêu cầu hỗ trợ sau khi bạn xác nhận đúng nội dung."),
}

load_lab_env(ROOT)

st.set_page_config(
    page_title="Northstar Service Desk",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)


background_data = base64.b64encode(BACKGROUND_PATH.read_bytes()).decode("ascii")
BACKGROUND_URL = f"data:image/jpeg;base64,{background_data}"

CSS = r"""
<style>
:root {
  --accent:#007aff; --accent-dark:#0068d9; --ink:#17202b;
  --secondary:rgba(23,32,43,.68); --canvas:#d7dde3; --surface:#fff;
  --divider:rgba(36,48,61,.15); --success:#28a745; --warning:#e78a00;
  --danger:#e83b34; --glass:rgba(235,240,245,.70);
  --spring:cubic-bezier(.22,1,.36,1);
}
html { scroll-behavior:smooth; }
body, [class*="css"] { font-family:system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; }
.stApp {
  color:var(--ink);
  background-image:url("__BACKGROUND_URL__");
  background-position:center; background-size:cover; background-attachment:fixed;
  isolation:isolate;
}
.stApp::before {
  content:""; position:fixed; inset:0; z-index:-1; pointer-events:none;
  background:rgba(38,49,60,.60);
  backdrop-filter:blur(5px) saturate(76%); -webkit-backdrop-filter:blur(5px) saturate(76%);
}
[data-testid="stHeader"] { background:transparent; }
[data-testid="stAppViewContainer"], [data-testid="stMain"], section.main { background:transparent!important; }
[data-testid="stToolbar"] { right:1rem; color:#fff; }
[data-testid="stToolbar"] button { color:#fff!important; }
[data-testid="stSidebar"] {
  min-width:300px!important; max-width:300px!important;
  background:rgba(225,233,241,.76);
  border-right:1px solid rgba(255,255,255,.54);
  box-shadow:12px 0 38px rgba(10,22,34,.20), inset -1px 0 rgba(255,255,255,.55);
  backdrop-filter:saturate(145%) blur(30px);
  -webkit-backdrop-filter:saturate(145%) blur(30px);
}
[data-testid="stSidebar"] > div:first-child { width:300px!important; }
[data-testid="stSidebar"] > div { padding-top:.65rem; }
[data-testid="stSidebar"] [data-testid="stSidebarContent"] { padding:0 1.15rem 1.5rem; }
[data-testid="stSidebarCollapseButton"] button {
  width:38px!important; height:38px!important; min-height:38px!important; padding:0!important;
  border-radius:50%!important; color:#344353!important; background:rgba(255,255,255,.38)!important;
  border:1px solid rgba(255,255,255,.55)!important; box-shadow:inset 0 1px rgba(255,255,255,.72)!important;
}
[data-testid="stSidebar"] h3, [data-testid="stSidebar"] h4 { color:#17202b; letter-spacing:-.025em; }
[data-testid="stSidebar"] label, [data-testid="stSidebar"] p { color:rgba(23,32,43,.78)!important; }
.sidebar-heading { margin:.4rem 0 1.3rem; }
.sidebar-kicker { color:rgba(23,32,43,.48); font-size:.7rem; font-weight:750; letter-spacing:.12em; text-transform:uppercase; }
.sidebar-title { margin-top:.25rem; color:#17202b; font-size:1.35rem; font-weight:750; letter-spacing:-.035em; }
.sidebar-section { display:flex; align-items:center; justify-content:space-between; margin:1.5rem 0 .7rem; }
.sidebar-section-title { color:#17202b; font-size:.88rem; font-weight:720; letter-spacing:-.012em; }
.sidebar-count { display:grid; place-items:center; min-width:26px; height:22px; padding:0 .4rem; border-radius:999px;
  color:#0568ce; background:rgba(0,122,255,.11); border:1px solid rgba(0,122,255,.15); font-size:.7rem; font-weight:750; }
.key-status { display:flex; align-items:center; gap:.72rem; margin:.95rem 0 .15rem; padding:.72rem .82rem;
  border-radius:16px; color:#24523b; background:rgba(232,248,239,.58); border:1px solid rgba(255,255,255,.52);
  box-shadow:inset 0 1px rgba(255,255,255,.65); font-size:.78rem; font-weight:620; line-height:1.35; }
.key-status-dot { flex:0 0 auto; width:9px; height:9px; border-radius:50%; background:#28a745;
  box-shadow:0 0 0 4px rgba(40,167,69,.12); }
.tools-grid { display:grid; grid-template-columns:1fr; gap:.45rem; padding:.15rem 0 .25rem; }
.tool-chip { position:relative; display:block; min-height:0; padding:.56rem .65rem .56rem 1.75rem; border-radius:13px;
  color:#3e4c5b; background:rgba(255,255,255,.34); border:1px solid rgba(255,255,255,.48);
  box-shadow:inset 0 1px rgba(255,255,255,.52); transition:background .18s ease, transform .18s var(--spring); }
.tool-chip:hover { background:rgba(255,255,255,.54); transform:translateX(2px); }
.tool-chip::before { content:""; position:absolute; left:.68rem; top:.9rem; width:6px; height:6px; border-radius:50%;
  background:#007aff; box-shadow:0 0 0 4px rgba(0,122,255,.10); }
.tool-title { color:#223140; font-size:.79rem; font-weight:720; line-height:1.25; letter-spacing:-.008em; }
.tool-description { margin-top:.22rem; color:rgba(34,49,64,.63); font-size:.69rem; font-weight:470; line-height:1.38; }
.tool-code { display:inline-block; margin-top:.32rem; color:rgba(34,49,64,.48);
  font-family:SFMono-Regular,ui-monospace,"Cascadia Code",Consolas,monospace; font-size:.61rem; line-height:1.2; }
.history-item { min-width:0; padding:.42rem .05rem .38rem; }
.history-title { color:#223140; font-size:.79rem; font-weight:720; line-height:1.34; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.history-meta { margin-top:.2rem; color:rgba(34,49,64,.52); font-size:.66rem; }
.history-rule { height:1px; margin:.18rem 0 .25rem; background:rgba(45,58,72,.10); }
[data-testid="stSidebar"] [class*="st-key-restore_session_"] button {
  width:34px!important; min-width:34px!important; height:34px!important; min-height:34px!important;
  margin-top:.36rem!important; padding:0!important; border-radius:50%!important;
  color:#176fca!important; background:rgba(255,255,255,.48)!important;
  box-shadow:inset 0 1px rgba(255,255,255,.72)!important;
}
[data-testid="stSidebar"] [class*="st-key-restore_session_"] button:hover { background:rgba(255,255,255,.76)!important; transform:translateY(-1px); }
.sidebar-rule { height:1px; margin:1.35rem 0 0; background:rgba(45,58,72,.14); }
.block-container { max-width:980px; padding-top:1.25rem; padding-bottom:7.5rem; }
.glass-nav {
  position:sticky; top:.75rem; z-index:20; min-height:56px;
  display:flex; align-items:center; justify-content:space-between; gap:1rem;
  padding:.55rem .75rem .55rem 1rem; margin-bottom:.7rem;
  border-radius:28px; background:rgba(226,234,242,.66);
  border:1px solid rgba(255,255,255,.58);
  box-shadow:0 16px 44px rgba(9,22,36,.22), inset 0 1px rgba(255,255,255,.74);
  backdrop-filter:saturate(165%) blur(26px); -webkit-backdrop-filter:saturate(165%) blur(26px);
}
.brand { display:flex; align-items:center; gap:.72rem; min-width:0; }
.brand-mark { width:40px; height:40px; display:grid; place-items:center; border-radius:50%; color:#fff;
  background:rgba(0,122,255,.92); border:1px solid rgba(255,255,255,.48);
  box-shadow:0 7px 18px rgba(0,84,180,.24), inset 0 1px rgba(255,255,255,.5); font-size:1.15rem; }
.brand-copy { min-width:0; }
.brand-title { font-weight:700; font-size:1.02rem; letter-spacing:-.02em; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.brand-sub { color:var(--secondary); font-size:.76rem; margin-top:.1rem; }
.nav-meta { display:flex; align-items:center; gap:.45rem; flex-wrap:wrap; justify-content:flex-end; }
.pill { display:inline-flex; align-items:center; gap:.38rem; min-height:30px; padding:.2rem .65rem;
  border-radius:999px; background:rgba(255,255,255,.44); border:1px solid rgba(255,255,255,.64);
  color:var(--secondary); font-size:.76rem; font-weight:600; }
.dot { width:7px; height:7px; border-radius:50%; background:var(--success); box-shadow:0 0 0 3px rgba(52,199,89,.14); }
.dot.offline { background:var(--warning); box-shadow:0 0 0 3px rgba(255,159,10,.14); }
.welcome { padding:2.8rem 1rem 1.5rem; text-align:center; animation:message-in .42s var(--spring) both; }
.welcome h1 { color:#fff; text-shadow:0 2px 22px rgba(0,0,0,.28); font-size:clamp(2rem,5vw,3.4rem); line-height:1.06; letter-spacing:-.045em; margin:0; }
.welcome p { max-width:620px; margin:.9rem auto 0; color:rgba(255,255,255,.82); text-shadow:0 1px 12px rgba(0,0,0,.25); font-size:1.06rem; line-height:1.5; }
.suggestions { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:.75rem; margin:1.3rem auto 2rem; max-width:760px; }
.message-wrap { animation:message-in .30s var(--spring) both; margin:.8rem auto 1.15rem; max-width:820px; }
.message-label { color:rgba(255,255,255,.82); text-shadow:0 1px 8px rgba(0,0,0,.24); font-size:.75rem; font-weight:650; margin:0 0 .35rem .35rem; }
.message-wrap.user-wrap .message-label { text-align:right; margin-right:.35rem; }
.bubble { width:fit-content; max-width:min(680px,88%); padding:.72rem 1rem; font-size:1rem; line-height:1.52; white-space:pre-wrap; overflow-wrap:anywhere; }
.bubble.user { margin-left:auto; border-radius:22px 22px 6px 22px; background:var(--accent); color:#fff; }
.bubble.agent { border-radius:22px 22px 22px 6px; background:rgba(244,247,250,.88); border:1px solid rgba(255,255,255,.65); box-shadow:0 10px 26px rgba(10,22,34,.14); backdrop-filter:blur(18px); }
.assistant-wrap { max-width:820px; margin:.2rem auto 1.15rem; animation:message-in .30s var(--spring) both; }
.assistant-label { margin:0 0 .38rem .35rem; color:rgba(255,255,255,.86); font-size:.75rem; font-weight:650; text-shadow:0 1px 8px rgba(0,0,0,.24); }
.assistant-bubble {
  padding:1rem 1.2rem; color:#1d2a36; border-radius:22px 22px 22px 7px;
  background:rgba(239,244,249,.90); border:1px solid rgba(255,255,255,.70);
  box-shadow:0 12px 30px rgba(10,22,34,.16), inset 0 1px rgba(255,255,255,.72);
  backdrop-filter:saturate(135%) blur(20px); -webkit-backdrop-filter:saturate(135%) blur(20px);
}
.assistant-bubble p, .assistant-bubble li { color:#1d2a36; font-size:1rem; line-height:1.58; }
.assistant-bubble p { margin:.2rem 0 .72rem; }
.assistant-bubble p:last-child { margin-bottom:.15rem; }
.assistant-bubble ul, .assistant-bubble ol { margin:.45rem 0 .75rem; padding-left:1.45rem; }
.assistant-bubble h1, .assistant-bubble h2, .assistant-bubble h3 { color:#15222e; font-size:1.08rem; line-height:1.35; margin:.9rem 0 .45rem; }
.assistant-bubble code { color:#17324d; background:rgba(26,74,115,.08); padding:.12rem .32rem; border-radius:6px; }
.assistant-bubble pre { overflow:auto; padding:.8rem; border-radius:12px; background:rgba(20,39,57,.08); }
.stream-caret { display:inline-block; width:7px; height:1.05em; margin-left:3px; vertical-align:-.12em; border-radius:4px; background:#007aff; animation:stream-blink .85s ease-in-out infinite; }
.turn-error { border-left:3px solid var(--danger); background:#fff; border-radius:16px; padding:.8rem 1rem; color:#a72019; }
.trace-title { display:flex; align-items:center; gap:.5rem; color:var(--secondary); font-weight:600; font-size:.82rem; margin:.65rem 0 .4rem; }
.trace-card { background:#fff; border:1px solid var(--divider); border-radius:22px; padding:.2rem .85rem; margin:.45rem 0; }
.status { display:inline-flex; padding:.18rem .55rem; border-radius:999px; font-size:.72rem; font-weight:700; }
.status.ok { color:#197a32; background:rgba(52,199,89,.12); }
.status.wait { color:#945600; background:rgba(255,159,10,.14); }
.status.error { color:#c52820; background:rgba(255,59,48,.12); }
div[data-testid="stExpander"] { background:rgba(245,248,251,.90); border:1px solid rgba(255,255,255,.66); border-radius:20px; overflow:hidden; box-shadow:0 12px 28px rgba(10,22,34,.15); backdrop-filter:blur(18px); }
[data-testid="stSidebar"] div[data-testid="stExpander"] { background:rgba(255,255,255,.28); border-radius:16px; box-shadow:none; }
[data-testid="stSidebar"] div[data-testid="stExpander"] summary { font-weight:700; }
div[data-testid="stExpander"] details { transition:all .32s var(--spring); }
.stButton button, .stDownloadButton button {
  min-height:48px; border-radius:999px; border:1px solid rgba(255,255,255,.66);
  background:rgba(235,241,247,.70); color:#17202b; font-weight:650;
  box-shadow:0 10px 24px rgba(9,22,36,.14), inset 0 1px rgba(255,255,255,.80);
  backdrop-filter:saturate(150%) blur(18px); -webkit-backdrop-filter:saturate(150%) blur(18px);
  transition:transform .18s var(--spring), background .18s ease, border-color .18s ease, box-shadow .18s ease;
}
.stButton button:hover, .stDownloadButton button:hover { background:rgba(246,249,252,.86); border-color:rgba(255,255,255,.88); box-shadow:0 14px 30px rgba(9,22,36,.20), inset 0 1px #fff; transform:translateY(-1px); }
.stButton button:active, .stDownloadButton button:active { transform:scale(.96); }
.stButton button:focus-visible, .stDownloadButton button:focus-visible, textarea:focus-visible,
[data-baseweb="input"] input:focus-visible { outline:3px solid rgba(0,122,255,.42)!important; outline-offset:2px; }
[data-testid="stSidebar"] [data-baseweb="select"] > div,
[data-testid="stSidebar"] [data-baseweb="input"] > div {
  min-height:46px; border-radius:14px!important; background:rgba(255,255,255,.70)!important;
  border-color:rgba(255,255,255,.74)!important; color:#17202b!important;
  box-shadow:inset 0 1px rgba(255,255,255,.88), 0 8px 18px rgba(18,33,48,.08)!important;
}
[data-testid="stSidebar"] [data-baseweb="select"] > div > div,
[data-testid="stSidebar"] [data-baseweb="select"] input {
  min-height:0!important; background:transparent!important; border:0!important; box-shadow:none!important;
}
[data-testid="stSidebar"] [data-baseweb="input"] input {
  min-height:44px!important; padding-left:.8rem!important; background:transparent!important; color:#17202b!important;
}
[data-testid="stSidebar"] [data-baseweb="input"] input::placeholder { color:rgba(23,32,43,.43)!important; }
[data-testid="stSidebar"] [data-baseweb="select"] > div:hover,
[data-testid="stSidebar"] [data-baseweb="input"] > div:hover { border-color:rgba(255,255,255,.94)!important; }
[data-testid="stSidebar"] [data-baseweb="select"] > div:focus-within {
  outline:none!important; border-color:rgba(255,255,255,.96)!important;
  box-shadow:0 0 0 2px rgba(255,255,255,.38), inset 0 1px rgba(255,255,255,.92), 0 10px 24px rgba(18,33,48,.12)!important;
}
[data-testid="stSidebar"] [data-testid="stSelectbox"] input,
[data-testid="stSidebar"] [data-baseweb="select"] input,
[data-testid="stSidebar"] [data-baseweb="select"] input:focus,
[data-testid="stSidebar"] [data-baseweb="select"] input:focus-visible {
  outline:none!important; caret-color:transparent!important; cursor:pointer!important; user-select:none!important;
}
[data-testid="stSidebar"] [data-baseweb="select"] svg {
  width:18px!important; height:18px!important; padding:3px; border-radius:50%; color:#354555!important;
  background:rgba(255,255,255,.48); transition:transform .22s var(--spring), background .18s ease;
}
[data-testid="stSidebar"] [data-baseweb="select"] > div:focus-within svg {
  background:rgba(255,255,255,.72); color:#354555!important; transform:rotate(180deg);
}
[data-baseweb="popover"] { border-radius:18px!important; overflow:visible!important; }
[data-baseweb="popover"] > div {
  border-radius:18px!important; background:transparent!important;
  box-shadow:none!important;
}
ul[role="listbox"] {
  margin-top:7px!important; padding:6px!important; border-radius:16px!important;
  background:rgba(235,241,247,.94)!important; border:1px solid rgba(255,255,255,.76)!important;
  box-shadow:0 14px 34px rgba(9,22,36,.18), inset 0 1px rgba(255,255,255,.82)!important;
  backdrop-filter:saturate(155%) blur(24px); -webkit-backdrop-filter:saturate(155%) blur(24px);
}
li[role="option"] {
  min-height:42px!important; margin:2px 0!important; padding:8px 12px!important; border-radius:12px!important;
  color:#263544!important; background:transparent!important; font-size:.94rem!important;
  transition:background .16s ease, color .16s ease, transform .16s var(--spring);
}
li[role="option"]:hover {
  color:#172533!important; background:rgba(255,255,255,.68)!important;
}
li[role="option"][aria-selected="true"] {
  color:#172533!important; background:rgba(255,255,255,.74)!important; font-weight:680!important;
}
li[role="option"][aria-selected="true"]::after {
  content:"✓"; margin-left:auto; color:#007aff; font-weight:800;
}
[data-testid="stSlider"] [role="slider"] { background:#fff!important; border:3px solid var(--accent)!important; box-shadow:0 3px 9px rgba(0,74,160,.24)!important; }
[data-testid="stSlider"] [data-testid="stThumbValue"] { color:var(--accent)!important; }
[data-testid="stSlider"] > div > div > div > div { background-color:var(--accent); }
[data-testid="stSegmentedControl"] { padding:4px!important; border-radius:15px!important; background:rgba(255,255,255,.44)!important; border:1px solid rgba(255,255,255,.62)!important; }
[data-testid="stSegmentedControl"] label { border:0!important; border-radius:11px!important; min-height:36px!important; }
[data-testid="stSegmentedControl"] label:has(input:checked) { background:rgba(0,122,255,.92)!important; color:#fff!important; box-shadow:0 5px 14px rgba(0,86,185,.22)!important; }
[data-testid="stSidebar"] hr { margin:1.3rem 0!important; border-color:rgba(45,58,72,.13)!important; }
[data-testid="stChatInput"] { max-width:900px; margin:auto; }
[data-testid="stChatInput"] > div { min-height:62px; padding:7px 8px 7px 18px; border-radius:31px!important; background:rgba(222,231,240,.72)!important;
  border:1px solid rgba(255,255,255,.72)!important; box-shadow:0 18px 46px rgba(8,20,34,.24), inset 0 1px rgba(255,255,255,.82)!important;
  backdrop-filter:saturate(165%) blur(26px); -webkit-backdrop-filter:saturate(165%) blur(26px); }
[data-testid="stChatInput"] [data-baseweb="textarea"],
[data-testid="stChatInput"] [data-baseweb="textarea"] > div,
[data-testid="stChatInput"] textarea {
  background:transparent!important; background-color:transparent!important; border:0!important;
  box-shadow:none!important; outline:none!important;
}
[data-testid="stChatInput"] textarea { color:#17202b!important; font-size:1rem!important; padding:10px 8px!important; line-height:1.4!important; }
[data-testid="stChatInput"] textarea::placeholder { color:rgba(23,32,43,.48)!important; }
[data-testid="stChatInput"] button { flex:0 0 44px!important; width:44px!important; height:44px!important; margin:1px 0!important; border-radius:50%!important; background:var(--accent)!important; color:#fff!important; border:1px solid rgba(255,255,255,.52)!important; box-shadow:0 7px 16px rgba(0,81,175,.30), inset 0 1px rgba(255,255,255,.42)!important; }
[data-testid="stChatInput"] button:hover { background:var(--accent-dark)!important; transform:translateY(-1px); }
[data-testid="stChatInput"] button:active { transform:scale(.94); }
[data-testid="stBottom"], [data-testid="stBottom"] > div,
[data-testid="stBottomBlockContainer"], [data-testid="stBottomBlockContainer"] > div,
.stBottom, .stBottom > div {
  background:transparent!important; background-color:transparent!important;
  background-image:none!important; box-shadow:none!important; border:0!important;
}
[data-testid="stBottom"]::before, [data-testid="stBottom"]::after,
[data-testid="stBottomBlockContainer"]::before, [data-testid="stBottomBlockContainer"]::after {
  content:none!important; display:none!important; background:none!important;
}
[data-testid="stBottomBlockContainer"] { padding-bottom:1.25rem!important; }
.action-row { margin:-.2rem 0 1rem; }
.stButton button p, .stDownloadButton button p { white-space:nowrap!important; }
code, pre { font-family:SFMono-Regular,ui-monospace,"Cascadia Code",Consolas,monospace!important; }
@keyframes message-in { from { opacity:0; transform:translateY(10px); } to { opacity:1; transform:none; } }
@keyframes stream-blink { 0%,100% { opacity:.2; } 50% { opacity:1; } }
@media (max-width:700px) {
  .block-container { padding-left:.75rem; padding-right:.75rem; padding-top:.5rem; }
  .glass-nav { top:.35rem; border-radius:22px; }
  .brand-sub, .nav-provider { display:none; }
  .suggestions { grid-template-columns:1fr; }
  .bubble { max-width:94%; }
  [data-testid="stSidebar"] { min-width:285px!important; max-width:285px!important; }
  [data-testid="stSidebar"] > div:first-child { width:285px!important; }
}
@media (prefers-reduced-motion:reduce) {
  *, *::before, *::after { animation-duration:.01ms!important; animation-iteration-count:1!important; scroll-behavior:auto!important; transition-duration:.01ms!important; }
}
@media (prefers-contrast:more) {
  [data-testid="stSidebar"], .glass-nav, [data-testid="stChatInput"] > div { background:rgba(255,255,255,.94)!important; border-color:rgba(0,0,0,.35)!important; }
}
</style>
"""
CSS = CSS.replace("__BACKGROUND_URL__", BACKGROUND_URL)
st.markdown(CSS, unsafe_allow_html=True)


def artifact_paths(version: str) -> tuple[Path, Path]:
    prompt_candidates = [
        ARTIFACTS_DIR / f"system_prompt_{version}.md",
        ARTIFACTS_DIR / version / "system_prompt.md",
        ARTIFACTS_DIR / "system_prompt.md",
    ]
    tool_candidates = [
        ARTIFACTS_DIR / f"tools_{version}.yaml",
        ARTIFACTS_DIR / version / "tools.yaml",
        ARTIFACTS_DIR / "tools.yaml",
    ]
    return (
        next(path for path in prompt_candidates if path.exists()),
        next(path for path in tool_candidates if path.exists()),
    )


def archive_current_session() -> None:
    if not st.session_state.get("turns") or not st.session_state.get("transcript"):
        return
    archived = st.session_state.setdefault("chat_sessions", [])
    transcript_id = st.session_state.transcript.get("transcript_id")
    archived[:] = [item for item in archived if item["transcript"].get("transcript_id") != transcript_id]
    archived.insert(
        0,
        {
            "transcript": json.loads(json.dumps(st.session_state.transcript, default=str)),
            "history": json.loads(json.dumps(st.session_state.history, default=str)),
            "path": str(st.session_state.transcript_path),
        },
    )


def restore_session(item: dict[str, Any]) -> None:
    st.session_state.transcript = item["transcript"]
    st.session_state.turns = st.session_state.transcript.get("turns", [])
    st.session_state.history = item.get("history", [])
    st.session_state.transcript_path = Path(item["path"])


def load_saved_sessions(limit: int = 20) -> None:
    if "chat_sessions" in st.session_state:
        return
    sessions: list[dict[str, Any]] = []
    if RUNS_DIR.exists():
        paths = sorted(RUNS_DIR.glob("*.transcript.json"), key=lambda path: path.stat().st_mtime, reverse=True)
        for path in paths[:limit]:
            try:
                transcript = json.loads(path.read_text(encoding="utf-8"))
                history: list[dict[str, str]] = []
                for turn in transcript.get("turns", []):
                    history.append({"role": "user", "content": str(turn.get("user", ""))})
                    if turn.get("assistant_text"):
                        history.append({"role": "assistant", "content": str(turn["assistant_text"])})
                sessions.append({"transcript": transcript, "history": history, "path": str(path)})
            except (OSError, ValueError, TypeError):
                continue
    st.session_state.chat_sessions = sessions


def new_session(provider_name: str, version: str, model: str | None, history_window: int, max_rounds: int) -> None:
    archive_current_session()
    prompt_path, tools_path = artifact_paths(version)
    artifact = build_artifact_version(version, prompt_path, tools_path)
    timestamp = datetime.now().strftime("%Y%m%dT%H%M%S%f")
    transcript_id = "_".join([safe_slug(version), safe_slug(provider_name), timestamp])
    st.session_state.history = []
    st.session_state.turns = []
    st.session_state.transcript_path = RUNS_DIR / f"{transcript_id}.transcript.json"
    st.session_state.transcript = {
        "transcript_id": transcript_id,
        **artifact_version_dict(artifact),
        "provider": provider_name,
        "model": model,
        "system_prompt": str(prompt_path),
        "tools": str(tools_path),
        "history_window": history_window,
        "max_tool_rounds": max_rounds,
        "created_at": now_iso(),
        "updated_at": now_iso(),
        "turns": st.session_state.turns,
    }


def ensure_session(provider_name: str, version: str, model: str | None, history_window: int, max_rounds: int) -> None:
    signature = (provider_name, version, model or "", history_window, max_rounds)
    if "signature" not in st.session_state:
        st.session_state.signature = signature
        new_session(provider_name, version, model, history_window, max_rounds)
    elif st.session_state.signature != signature:
        st.session_state.signature = signature
        new_session(provider_name, version, model, history_window, max_rounds)


def transcript_bytes() -> bytes:
    return json.dumps(st.session_state.transcript, ensure_ascii=False, indent=2, default=str).encode("utf-8")


def event_status(event: dict[str, Any]) -> tuple[str, str]:
    result = event.get("result")
    if isinstance(result, dict) and result.get("awaiting_user"):
        return "Đang chờ", "wait"
    if isinstance(result, dict) and result.get("error"):
        return "Thất bại", "error"
    return "Thành công", "ok"


def render_trace(turn: dict[str, Any]) -> None:
    rounds = turn.get("rounds") or []
    total = sum(len(item.get("tool_results") or []) for item in rounds)
    if not total:
        return
    st.markdown(f'<div class="trace-title">⌁ Dấu vết công cụ · {total} sự kiện</div>', unsafe_allow_html=True)
    event_index = 0
    for round_item in rounds:
        round_number = round_item.get("round", "–")
        for event in round_item.get("tool_results") or []:
            event_index += 1
            label, status_class = event_status(event)
            tool_name = html.escape(str(event.get("tool", "unknown_tool")))
            with st.expander(f"{event_index}. {tool_name}  ·  Vòng {round_number}  ·  {label}", expanded=status_class == "error"):
                st.markdown(f'<span class="status {status_class}">{label}</span>', unsafe_allow_html=True)
                st.markdown("**Input**")
                st.json(event.get("args") or {})
                st.markdown("**Kết quả / lỗi**")
                st.json(event.get("result"))


def render_turn(turn: dict[str, Any]) -> None:
    user = html.escape(str(turn.get("user", "")))
    st.markdown(f'<div class="message-wrap user-wrap"><div class="message-label">Bạn</div><div class="bubble user">{user}</div></div>', unsafe_allow_html=True)
    if turn.get("status") == "provider_error":
        error = html.escape(str(turn.get("error", "Lỗi provider không xác định")))
        st.markdown(f'<div class="turn-error"><strong>Không thể hoàn tất lượt này</strong><br>{error}</div>', unsafe_allow_html=True)
        return
    answer_html = MARKDOWN.render(str(turn.get("assistant_text") or ""))
    st.markdown(
        '<div class="assistant-wrap"><div class="assistant-label">Northstar Assistant</div>'
        f'<div class="assistant-bubble">{answer_html}</div></div>',
        unsafe_allow_html=True,
    )
    render_trace(turn)


with st.sidebar:
    st.markdown(
        '<div class="sidebar-heading"><div class="sidebar-kicker">Northstar desk</div>'
        '<div class="sidebar-title">Cấu hình phiên</div></div>',
        unsafe_allow_html=True,
    )
    provider_name = st.selectbox("Provider", list(PROVIDER_KEYS), index=0)
    version = st.segmented_control("Artifact version", ["v0", "v1", "v2", "v3"], default="v0") or "v0"
    model_value = st.text_input("Model override", placeholder="Để trống để dùng mặc định")
    model = model_value.strip() or None
    history_window = st.slider("Số cặp hội thoại ghi nhớ", 1, 12, 5)
    max_rounds = st.slider("Số vòng gọi tool tối đa", 1, 8, 4)
    key_name = PROVIDER_KEYS[provider_name]
    has_env_key = bool(os.getenv(key_name))
    if has_env_key:
        st.markdown(
            f'<div class="key-status"><span class="key-status-dot"></span>'
            f'<span>Đã kết nối<br><strong>{html.escape(key_name)}</strong></span></div>',
            unsafe_allow_html=True,
        )
    else:
        entered_key = st.text_input("API key cho phiên này", type="password", help="Không được ghi vào transcript.")
        if entered_key:
            os.environ[key_name] = entered_key
            has_env_key = True
    st.markdown('<div class="sidebar-rule"></div>', unsafe_allow_html=True)
    with st.expander(f"Công cụ khả dụng · {len(TOOL_FUNCTIONS)}", expanded=False):
        tool_chips = "".join(
            '<div class="tool-chip">'
            f'<div class="tool-title">{html.escape(TOOL_CATALOG.get(tool_name, (tool_name, ""))[0])}</div>'
            f'<div class="tool-description">{html.escape(TOOL_CATALOG.get(tool_name, (tool_name, ""))[1])}</div>'
            f'<span class="tool-code">{html.escape(tool_name)}</span>'
            '</div>'
            for tool_name in TOOL_FUNCTIONS
        )
        st.markdown(f'<div class="tools-grid">{tool_chips}</div>', unsafe_allow_html=True)

ensure_session(provider_name, version, model, history_window, max_rounds)
load_saved_sessions()
prompt_path, tools_path = artifact_paths(version)
selected_provider = make_provider(provider_name)

with st.sidebar:
    archived_sessions = st.session_state.get("chat_sessions", [])
    with st.expander(f"Lịch sử trò chuyện · {len(archived_sessions)}", expanded=False):
        if not archived_sessions:
            st.caption("Các phiên trước sẽ xuất hiện ở đây sau khi bạn tạo phiên mới.")
        for index, item in enumerate(archived_sessions):
            turns = item["transcript"].get("turns", [])
            first_prompt = str(turns[0].get("user", "Phiên trò chuyện")) if turns else "Phiên trò chuyện"
            title = first_prompt if len(first_prompt) <= 38 else f"{first_prompt[:38].rstrip()}…"
            updated_at = str(item["transcript"].get("updated_at") or item["transcript"].get("created_at") or "")
            info_col, open_col = st.columns([5, 1], vertical_alignment="center")
            with info_col:
                st.markdown(
                    f'<div class="history-item"><div class="history-title" title="{html.escape(first_prompt)}">{html.escape(title)}</div>'
                    f'<div class="history-meta">{len(turns)} lượt · {html.escape(updated_at[:16].replace("T", " "))}</div></div>',
                    unsafe_allow_html=True,
                )
            with open_col:
                if st.button("↗", key=f"restore_session_{index}", help="Mở lại phiên này"):
                    restore_session(item)
                    st.rerun()
            if index < len(archived_sessions) - 1:
                st.markdown('<div class="history-rule"></div>', unsafe_allow_html=True)

st.markdown('<div class="action-row">', unsafe_allow_html=True)
spacer_col, action_col, download_col = st.columns([4.6, 1.35, 1.45])
with action_col:
    if st.button("＋ Phiên mới", use_container_width=True):
        new_session(provider_name, version, model, history_window, max_rounds)
        st.rerun()
with download_col:
    st.download_button(
        "↓ Transcript",
        data=transcript_bytes(),
        file_name=f"{st.session_state.transcript['transcript_id']}.transcript.json",
        mime="application/json",
        use_container_width=True,
    )
st.markdown('</div>', unsafe_allow_html=True)

if not st.session_state.turns:
    st.markdown(
        """
        <section class="welcome">
          <h1>Hôm nay bạn cần hỗ trợ gì?</h1>
          <p>Kiểm tra dịch vụ, chẩn đoán thiết bị, tra cứu hướng dẫn nội bộ hoặc chuẩn bị ticket có xác nhận.</p>
        </section>
        """,
        unsafe_allow_html=True,
    )
    examples = [
        "VPN production hiện có gặp sự cố không?",
        "Kiểm tra tổng thể laptop LT-204.",
        "Tìm hướng dẫn cấu hình Outlook trên Windows 11.",
        "Tạo ticket mức high cho lỗi VPN trên LT-204.",
    ]
    st.markdown('<div class="suggestions">', unsafe_allow_html=True)
    cols = st.columns(2)
    for index, example in enumerate(examples):
        with cols[index % 2]:
            if st.button(example, key=f"example_{index}", use_container_width=True):
                st.session_state.pending_prompt = example
                st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
else:
    for saved_turn in st.session_state.turns:
        render_turn(saved_turn)

typed_prompt = st.chat_input("Nhập yêu cầu hỗ trợ…", disabled=not has_env_key)
prompt = st.session_state.pop("pending_prompt", None) or typed_prompt

if prompt:
    turn_index = len(st.session_state.turns) + 1
    system_prompt = prompt_path.read_text(encoding="utf-8")
    declarations = load_tool_declarations(tools_path)
    openai_tools = to_openai_tools(declarations)
    messages = [
        {"role": "system", "content": system_prompt},
        *trim_history(st.session_state.history, history_window),
        {"role": "user", "content": prompt},
    ]
    turn: dict[str, Any] = {
        "turn_index": turn_index,
        "started_at": now_iso(),
        "user": prompt,
        "status": "started",
        "assistant_text": None,
        "rounds": [],
        "tool_events": [],
    }
    safe_prompt = html.escape(str(prompt))
    st.markdown(
        f'<div class="message-wrap user-wrap"><div class="message-label">Bạn</div>'
        f'<div class="bubble user">{safe_prompt}</div></div>',
        unsafe_allow_html=True,
    )
    stream_placeholder = st.empty()
    streamed_parts: list[str] = []

    def render_stream_delta(delta: str) -> None:
        streamed_parts.append(delta)
        partial_html = MARKDOWN.render("".join(streamed_parts))
        stream_placeholder.markdown(
            '<div class="assistant-wrap"><div class="assistant-label">Northstar Assistant</div>'
            f'<div class="assistant-bubble">{partial_html}<span class="stream-caret"></span></div></div>',
            unsafe_allow_html=True,
        )

    with st.status("Agent đang phân tích và gọi công cụ…", expanded=True) as status:
        try:
            def begin_round(round_number: int) -> None:
                streamed_parts.clear()
                stream_placeholder.empty()
                status.update(label=f"Đang xử lý vòng {round_number}…", state="running", expanded=False)

            result = run_model_tool_loop(
                provider=selected_provider,
                messages=messages,
                tools=openai_tools,
                model=model,
                max_tool_rounds=max_rounds,
                on_text_delta=render_stream_delta,
                on_round_start=begin_round,
            )
            turn.update(result)
            assistant_text = str(result.get("assistant_text") or "")
            st.session_state.history.extend([
                {"role": "user", "content": prompt},
                {"role": "assistant", "content": assistant_text},
            ])
            status.update(label="Đã hoàn tất lượt xử lý", state="complete", expanded=False)
        except Exception as exc:
            turn.update({"status": "provider_error", "error": f"{type(exc).__name__}: {exc}"})
            status.update(label="Provider trả về lỗi", state="error", expanded=True)
    stream_placeholder.empty()
    turn["ended_at"] = now_iso()
    st.session_state.turns.append(turn)
    st.session_state.transcript["turns"] = st.session_state.turns
    st.session_state.transcript["updated_at"] = now_iso()
    write_transcript(st.session_state.transcript_path, st.session_state.transcript)
    st.rerun()
