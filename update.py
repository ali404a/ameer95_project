import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Fix the drawer CSS
content = content.replace('transform:translateX(-100%);', 'transform:translateX(100%);')

# 2. Add Role Switcher to Topbar
topbar_search = '''      <div class="search-box">'''
role_switcher = '''      <select id="roleSwitcher" class="select" style="margin-inline-end: 16px; border-color: var(--accent); color: var(--accent); font-weight: 600;">
        <option value="ali">علي المرتضى (Super Admin)</option>
        <option value="sara">سارة أحمد (Admin)</option>
        <option value="hasan">حسن فاضل (Admin)</option>
      </select>
      <div class="search-box">'''
content = content.replace(topbar_search, role_switcher)

# 3. Add 'My Work' tab to Navigation (initially hidden, shown for admins)
nav_reports = '''      <button class="nav-item" data-view="reports">
        <svg fill="none" stroke-width="2" viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M16 13H8M16 17H8M10 9H8"/></svg>
        التقارير
      </button>'''
nav_my_work = nav_reports + '''
      <button class="nav-item" data-view="mywork" id="navMyWork" style="display:none;">
        <svg fill="none" stroke-width="2" viewBox="0 0 24 24"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
        سجل النشر (عملي)
      </button>'''
content = content.replace(nav_reports, nav_my_work)

# 4. Add the My Work and new Reports View HTML
views_placeholder = '''      <!-- ===== Placeholder views ===== -->
      <section class="view" id="view-reports"><div class="panel"><div class="panel-body" style="text-align:center;padding:60px;color:var(--ink-3)">قسم التقارير — تصدير Excel / PDF / CSV (نموذج أولي)</div></div></section>'''

new_views = '''      <!-- ===== MY WORK (ADMIN) ===== -->
      <section class="view" id="view-mywork">
        <div class="toolbar">
          <button class="btn-primary" onclick="openPublishModal()"><svg fill="none" stroke-width="2" viewBox="0 0 24 24"><path d="M12 5v14M5 12h14"/></svg>إضافة عمل جديد</button>
        </div>
        <div id="publishGrid" class="acc-grid"></div>
      </section>

      <!-- ===== REPORTS (SUPER ADMIN) ===== -->
      <section class="view" id="view-reports">
        <div class="panel" style="margin-bottom: 16px;">
          <div class="panel-body" style="display:flex;gap:12px;align-items:center;flex-wrap:wrap;">
            <select class="select" id="repTime"><option value="today">اليوم</option><option value="week">هذا الأسبوع</option><option value="month">هذا الشهر</option><option value="all">شامل</option></select>
            <select class="select" id="repAdmin"><option value="">كل المشرفين</option><option value="سارة أحمد">سارة أحمد</option><option value="حسن فاضل">حسن فاضل</option></select>
            <button class="btn-primary" onclick="generateReport()">توليد التقرير</button>
            <button class="select" style="margin-inline-start:auto;display:flex;gap:6px;align-items:center" onclick="toast('تم التصدير كـ PDF')"><svg fill="none" stroke="currentColor" stroke-width="2" width="16" height="16" viewBox="0 0 24 24"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M7 10l5 5 5-5M12 15V3"/></svg>تصدير</button>
          </div>
        </div>
        <div id="reportWrap">
          <div class="panel"><div class="panel-body" style="text-align:center;padding:60px;color:var(--ink-3)">اضغط على زر التوليد لعرض التقرير</div></div>
        </div>
      </section>'''
content = content.replace(views_placeholder, new_views)

# Add Publish Modal HTML right before closing </div></div> (app main)
modal_html = '''
<!-- Publish Modal -->
<div class="overlay" id="pubOverlay" onclick="document.getElementById('pubOverlay').classList.remove('open');document.getElementById('pubModal').classList.remove('open')"></div>
<div class="drawer" id="pubModal" style="width:400px; padding: 22px; right: 50%; transform: translate(50%, -50%); top: 50%; height: auto; max-height: 90vh; border-radius: 14px; left: auto; transition: .2s;">
  <h3 style="margin-bottom:16px;">تسجيل عمل جديد</h3>
  <div style="display:flex;flex-direction:column;gap:12px;">
    <select id="pubAcc" class="select"><option>اختر الحساب...</option></select>
    <input type="text" id="pubLink" class="select" placeholder="رابط المنشور (اختياري)">
    <textarea id="pubNotes" class="select" placeholder="الملاحظات والتفاصيل..." rows="4" style="resize:vertical"></textarea>
    <button class="btn-primary" style="justify-content:center" onclick="savePublish()">حفظ النشر</button>
  </div>
</div>
'''
content = content.replace('<!-- Detail Drawer -->', modal_html + '\n<!-- Detail Drawer -->')
content = content.replace('transform: translate(50%, -50%);', 'transform: translate(50%, -150%); opacity:0; pointer-events:none;')
content = content.replace('.drawer.open{transform:translateX(0)}', '.drawer.open{transform:translateX(0)}\n#pubModal.open{transform: translate(50%, -50%) !important; opacity:1 !important; pointer-events:auto !important;}')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
