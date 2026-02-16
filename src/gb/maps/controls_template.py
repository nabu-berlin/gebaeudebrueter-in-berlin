import json
import re
from pathlib import Path

from gb.common.config import DOCS_DIR

_TEMPLATE_PATH = Path(__file__).resolve().parent / 'templates' / 'multispecies_controls.html'

_REPORT_MODAL_CSS = '''
.gb-modal-overlay{position:fixed;inset:0;background:rgba(0,0,0,.45);display:none;align-items:center;justify-content:center;z-index:99999;}
.gb-modal-overlay.gb-open{display:flex;}
.gb-modal{background:#fff;border-radius:10px;max-width:420px;width:calc(100vw - 32px);box-shadow:0 10px 30px rgba(0,0,0,.25);padding:14px 16px;font-family:system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif;}
.gb-modal h3{margin:0 0 8px 0;font-size:16px;}
.gb-modal p{margin:0 0 10px 0;font-size:13px;line-height:1.35;color:#333;}
.gb-modal label{display:block;font-size:12px;color:#333;margin:8px 0 4px;}
.gb-modal input[type="text"], .gb-modal input[type="search"], .gb-modal input[type="email"], .gb-modal input[type="number"], .gb-modal textarea{width:100%;padding:8px 10px;border:1px solid #ccc;border-radius:8px;font-size:13px;}
.gb-modal .gb-error{display:none;color:#b00020;font-size:12px;margin-top:6px;}
.gb-modal .gb-error.gb-visible{display:block;}
.gb-modal .gb-actions{display:flex;gap:8px;justify-content:flex-end;margin-top:12px;}
.gb-modal .gb-robot-wrap{margin-top:8px;}
.gb-modal .gb-modal-checkbox-inline{margin-left:8px;vertical-align:middle;}
.gb-modal button{border:0;border-radius:8px;padding:8px 10px;font-size:13px;cursor:pointer;}
.gb-modal .gb-cancel{background:#eee;color:#333;}
.gb-modal .gb-confirm{background:#1976d2;color:#fff;}
.gb-marker-counter{position:fixed;bottom:0;left:0;background:#fff;padding:4px;z-index:9999;}
'''


def build_controls_html(species_colors, status_info, online_form_url, email_recipient):
    template = _TEMPLATE_PATH.read_text(encoding='utf-8')
    rendered = (
        template
        .replace('%SPECIES_COLORS_JSON%', json.dumps(species_colors, ensure_ascii=False))
        .replace('%STATUS_INFO_JSON%', json.dumps(status_info, ensure_ascii=False))
        .replace('%ONLINE_FORM_URL%', online_form_url)
        .replace('%EMAIL_RECIPIENT%', email_recipient)
    )

    style_match = re.search(r'<style>(.*?)</style>', rendered, flags=re.DOTALL)
    script_match = re.search(r'<script>(.*?)</script>', rendered, flags=re.DOTALL)

    if style_match:
        css_dir = DOCS_DIR / 'assets' / 'css'
        css_dir.mkdir(parents=True, exist_ok=True)
        css_path = css_dir / 'map-controls.css'
        css_content = style_match.group(1).strip() + '\n\n' + _REPORT_MODAL_CSS.strip() + '\n'
        css_path.write_text(css_content, encoding='utf-8')

        css_ref = (
            '<link rel="stylesheet" href="assets/css/map-controls.css" '
            'onerror="this.onerror=null;this.href=\'docs/assets/css/map-controls.css\';" />'
        )
        rendered = rendered.replace(style_match.group(0), css_ref, 1)

    if script_match:
        js_dir = DOCS_DIR / 'assets' / 'js'
        js_dir.mkdir(parents=True, exist_ok=True)
        js_path = js_dir / 'map-controls.js'
        js_path.write_text(script_match.group(1).strip() + '\n', encoding='utf-8')

        js_ref = (
            '<script src="assets/js/map-controls.js" '
            'onerror="this.onerror=null;this.src=\'docs/assets/js/map-controls.js\';"></script>'
        )
        rendered = rendered.replace(script_match.group(0), js_ref, 1)

    return rendered
