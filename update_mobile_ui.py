import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add CSS
css_addition = '''
/* ---------- Mobile App UI ---------- */
.bottom-nav { display: none; }
.mobile-header-title { display: none; }
.mobile-profile { display: none; }

@media(max-width:820px){
  .sidebar { display: none !important; }
  .bottom-nav {
    display: flex; position: fixed; bottom: 0; left: 0; right: 0; height: 68px;
    background: rgba(255,255,255,0.92); backdrop-filter: blur(12px);
    border-top: 1px solid var(--line); z-index: 100;
    justify-content: space-around; align-items: center; padding: 0 12px;
    padding-bottom: env(safe-area-inset-bottom);
    box-shadow: 0 -4px 24px rgba(15,23,42,0.06);
  }
  .bn-item {
    display: flex; flex-direction: column; align-items: center; gap: 5px;
    color: var(--ink-3); font-size: 10.5px; font-weight: 600; padding: 6px 12px;
    transition: .15s; border-radius: 12px;
  }
  .bn-item svg { width: 22px; height: 22px; stroke: currentColor; transition: .2s; }
  .bn-item.active { color: var(--accent); }
  .bn-item.active svg { stroke-width: 2.5; transform: translateY(-2px); }
  
  .main { padding-bottom: 90px; }
  
  /* Header Adjustments */
  .topbar { padding: 0 16px; position: sticky; top: 0; justify-content: space-between; }
  .menu-btn, .search-box, .icon-btn, .page-title, .page-sub { display: none !important; }
  
  .mobile-header-title {
    display: block !important; font-size: 17px; font-weight: 700;
    position: absolute; left: 50%; transform: translateX(-50%); letter-spacing: -0.3px;
  }
  .mobile-profile { display: grid !important; cursor: pointer; }
  
  /* Tweaks for mobile grid */
  .d-field { flex-direction: column; align-items: flex-start; gap: 4px; }
  .d-field-k { width: auto; }
}
'''
content = content.replace('/* ---------- Layout ---------- */', css_addition + '\n/* ---------- Layout ---------- */')

# 2. Add Bottom Nav HTML
bottom_nav_html = '''
  <!-- Bottom Navigation (Mobile) -->
  <nav class="bottom-nav" id="bottomNav">
    <button class="bn-item active" data-view="dashboard">
      <svg fill="none" stroke-width="2" viewBox="0 0 24 24"><rect x="3" y="3" width="7" height="9" rx="1"/><rect x="14" y="3" width="7" height="5" rx="1"/><rect x="14" y="12" width="7" height="9" rx="1"/><rect x="3" y="16" width="7" height="5" rx="1"/></svg>
      الرئيسية
    </button>
    <button class="bn-item" data-view="accounts">
      <svg fill="none" stroke-width="2" viewBox="0 0 24 24"><circle cx="12" cy="8" r="4"/><path d="M4 21v-1a7 7 0 0 1 14 0v1"/></svg>
      الحسابات
    </button>
    <button class="bn-item" data-view="mywork" id="bnMyWork" style="display:none;">
      <svg fill="none" stroke-width="2" viewBox="0 0 24 24"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
      عملي
    </button>
    <button class="bn-item" data-view="users" id="bnUsers">
      <svg fill="none" stroke-width="2" viewBox="0 0 24 24"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/></svg>
      المشرفين
    </button>
    <button class="bn-item" data-view="reports" id="bnReports">
      <svg fill="none" stroke-width="2" viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M16 13H8M16 17H8M10 9H8"/></svg>
      التقارير
    </button>
  </nav>
</div> <!-- Closing .app -->
'''
content = content.replace('</div>\n\n<!-- Account Modal -->', bottom_nav_html + '\n<!-- Account Modal -->')

# 3. Update Topbar HTML
topbar_start = '''    <header class="topbar">'''
topbar_new = '''    <header class="topbar">
      <!-- Mobile Elements -->
      <div class="mobile-profile avatar" id="mobAvatar" onclick="toast('مرحباً ' + CURRENT_USER.name)">ع</div>
      <div class="mobile-header-title">مركز العمليات</div>'''
content = content.replace(topbar_start, topbar_new)

# 4. Update JS for Bottom Nav
nav_js_old = '''const oldNavClick = document.querySelectorAll('.nav-item');
oldNavClick.forEach(n => {
  n.addEventListener('click', () => {
    if(n.dataset.view === 'mywork') renderPublishLogs();
  });
});'''

nav_js_new = '''const allNavs = document.querySelectorAll('.nav-item, .bn-item');
allNavs.forEach(n => {
  n.addEventListener('click', () => {
    // Update active class on both sidebar and bottom nav
    document.querySelectorAll('.nav-item, .bn-item').forEach(x => x.classList.remove('active'));
    
    const v = n.dataset.view;
    document.querySelectorAll(`[data-view="${v}"]`).forEach(el => el.classList.add('active'));
    
    document.querySelectorAll('.view').forEach(x => x.classList.remove('active'));
    document.getElementById('view-'+v).classList.add('active');
    
    // Fallback for titles if not defined
    if(titles[v]){
      document.getElementById('pageTitle').textContent=titles[v][0];
      document.getElementById('pageSub').textContent=titles[v][1];
    }
    document.getElementById('sidebar').classList.remove('open');
    
    if(v === 'mywork') renderPublishLogs();
  });
});'''

content = content.replace(nav_js_old, nav_js_new)

# Update the old nav click code that might conflict
content = content.replace('''document.querySelectorAll('.nav-item').forEach(n=>n.onclick=()=>{
  document.querySelectorAll('.nav-item').forEach(x=>x.classList.remove('active'));n.classList.add('active');
  const v=n.dataset.view;
  document.querySelectorAll('.view').forEach(x=>x.classList.remove('active'));
  document.getElementById('view-'+v).classList.add('active');
  document.getElementById('pageTitle').textContent=titles[v][0];
  document.getElementById('pageSub').textContent=titles[v][1];
  document.getElementById('sidebar').classList.remove('open');
});''', '')


# Update roleSwitcher logic to include Bottom Nav
role_js_old = '''    document.getElementById('navMyWork').style.display = 'none';
    document.getElementById('btnAddAcc').style.display = 'flex';
  } else {'''
role_js_new = '''    document.getElementById('navMyWork').style.display = 'none';
    document.getElementById('btnAddAcc').style.display = 'flex';
    document.getElementById('bnUsers').style.display = 'flex';
    document.getElementById('bnReports').style.display = 'flex';
    document.getElementById('bnMyWork').style.display = 'none';
  } else {'''

role_js_old_2 = '''    document.getElementById('navMyWork').style.display = 'flex';
    document.getElementById('btnAddAcc').style.display = 'none';
  }'''
role_js_new_2 = '''    document.getElementById('navMyWork').style.display = 'flex';
    document.getElementById('btnAddAcc').style.display = 'none';
    document.getElementById('bnUsers').style.display = 'none';
    document.getElementById('bnReports').style.display = 'none';
    document.getElementById('bnMyWork').style.display = 'flex';
  }'''

content = content.replace(role_js_old, role_js_new)
content = content.replace(role_js_old_2, role_js_new_2)

# Update avatar in mobile
avatar_update_old = '''document.querySelector('.avatar').textContent = CURRENT_USER.name[0];'''
avatar_update_new = '''document.querySelectorAll('.avatar').forEach(el => el.textContent = CURRENT_USER.name[0]);'''
content = content.replace(avatar_update_old, avatar_update_new)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
