from datetime import datetime

import folium


def format_stand_display(last_raw):
    stand_display = ''
    if last_raw:
        try:
            dt = datetime.strptime(last_raw.split('.')[0], '%Y-%m-%d %H:%M:%S') if ' ' in last_raw else datetime.strptime(last_raw, '%Y-%m-%d')
            stand_display = f'{dt.month:02d}.{dt.year}'
        except Exception:
            try:
                parts = last_raw.split('-')
                if len(parts) >= 2:
                    stand_display = f'{parts[1]}.{parts[0]}'
            except Exception:
                stand_display = ''
    if not stand_display:
        now = datetime.now()
        stand_display = f'{now.month:02d}.{now.year}'
    return stand_display


def _report_modal_html():
    return (
        '<div id="gbModalOverlay" class="gb-modal-overlay" role="dialog" aria-modal="true">'
        '  <div class="gb-modal">'
        '    <h3>Beobachtung melden</h3>'
        '    <p>Bitte bestätige zur Sicherheit die Fundort-ID, bevor dein E-Mail-Programm geöffnet wird.</p>'
        '    <div><b>Fundort-ID:</b> <span id="gbModalExpectedId">—</span></div>'
        '    <label for="gbModalInput">Fundort-ID eingeben</label>'
        '    <input id="gbModalInput" type="text" inputmode="numeric" autocomplete="off" />'
        '    <div class="gb-robot-wrap"><label>Ich bin kein Bot <input id="gbModalCheckbox" class="gb-modal-checkbox-inline" type="checkbox" /></label></div>'
        '    <div id="gbModalError" class="gb-error">Fundort-ID stimmt nicht.</div>'
        '    <div class="gb-actions">'
        '      <button type="button" class="gb-cancel" onclick="gbModalClose()">Abbrechen</button>'
        '      <button id="gbModalConfirmBtn" type="button" class="gb-confirm" onclick="gbModalConfirm()" disabled>E-Mail öffnen</button>'
        '    </div>'
        '  </div>'
        '</div>'
        '<script>'
        'var gbModalState = { expectedId: null, href: null };'
        'function gbModalOpen(expectedId, href){'
        '  gbModalState.expectedId = String(expectedId);'
        '  gbModalState.href = href;'
        '  var ov = document.getElementById("gbModalOverlay");'
        '  document.getElementById("gbModalExpectedId").textContent = gbModalState.expectedId;'
        '  var inp = document.getElementById("gbModalInput");'
        '  inp.value = "";'
        '  var cb = document.getElementById("gbModalCheckbox"); if (cb) { cb.checked = false; }'
        '  var btn = document.getElementById("gbModalConfirmBtn"); if (btn) { btn.disabled = true; }'
        '  var err = document.getElementById("gbModalError"); if (err) { err.classList.remove("gb-visible"); }'
        '  ov.classList.add("gb-open");'
        '  setTimeout(function(){ inp.focus(); }, 0);'
        '}'
        'function gbModalClose(){'
        '  var ov = document.getElementById("gbModalOverlay");'
        '  ov.classList.remove("gb-open");'
        '  gbModalState.expectedId = null;'
        '  gbModalState.href = null;'
        '}'
        'function gbModalConfirm(){'
        '  var v = String(document.getElementById("gbModalInput").value || "").trim();'
        '  if (v !== gbModalState.expectedId){'
        '    var err = document.getElementById("gbModalError"); if (err) { err.classList.add("gb-visible"); }'
        '    return;'
        '  }'
        '  var href = gbModalState.href;'
        '  gbModalClose();'
        '  try { window.location.href = href; } catch(e) { /* noop */ }'
        '}'
        'function gbHumanConfirmReport(evt, expectedId, href){'
        '  try { if (evt && evt.preventDefault) { evt.preventDefault(); } } catch(e) {}'
        '  gbModalOpen(expectedId, href);'
        '  return false;'
        '}'
        'try { document.getElementById("gbModalCheckbox").addEventListener("change", function(e){ try { document.getElementById("gbModalConfirmBtn").disabled = !this.checked; } catch(e){} }); } catch(e){}'
        'document.addEventListener("keydown", function(e){'
        '  var ov = document.getElementById("gbModalOverlay");'
        '  if (!ov || !ov.classList.contains("gb-open")) { return; }'
        '  if (e.key === "Escape") { gbModalClose(); }'
        '  if (e.key === "Enter") { gbModalConfirm(); }'
        '});'
        'document.addEventListener("click", function(e){'
        '  var ov = document.getElementById("gbModalOverlay");'
        '  if (ov && ov.classList.contains("gb-open") && e.target === ov) { gbModalClose(); }'
        '});'
        '</script>'
    )


def inject_map_ui(map_obj, controls_html, stand_display, marker_count):
    controls_with_stand = controls_html.replace('%STAND_DATE%', stand_display)
    map_obj.get_root().html.add_child(folium.Element(controls_with_stand))
    map_obj.get_root().html.add_child(folium.Element(_report_modal_html()))
    map_obj.get_root().html.add_child(
        folium.Element(
            '<div class="gb-marker-counter">Markers: '
            + str(marker_count)
            + '</div>'
        )
    )
