import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update Audit Logs and logAction
audit_old = '''const auditLogs=[
  {u:'علي المرتضى',act:'عرض كلمة مرور',tgt:'404 Studio',ip:'192.168.1.10',t:'2025-07-07 14:32'},
  {u:'سارة أحمد',act:'فتح حساب',tgt:'مرماز أكاديمي',ip:'192.168.1.14',t:'2025-07-07 14:02'},
  {u:'حسن فاضل',act:'تصدير تقرير',tgt:'تقرير الحسابات',ip:'192.168.1.22',t:'2025-07-07 12:15'},
  {u:'محمد علي',act:'أرشفة حساب',tgt:'مرماز — سناب',ip:'192.168.1.31',t:'2025-07-06 18:40'},
  {u:'زينب كريم',act:'إضافة حساب',tgt:'مرماز كيدز',ip:'192.168.1.19',t:'2025-07-06 09:11'}
];'''
audit_new = '''let auditLogs=[
  {u:'علي المرتضى',act:'عرض كلمة مرور',tgt:'404 Studio',ip:'192.168.1.10',t:'2025-07-07 14:32'}
];
function renderAudit() {
  document.getElementById('auditBody').innerHTML=`<table class="users-table"><thead><tr><th>المستخدم</th><th>العملية</th><th>الهدف</th><th>الوقت</th></tr></thead><tbody>`+
  auditLogs.map(l=>`<tr><td class="td-name">${l.u}</td><td>${l.act}</td><td><b>${l.tgt}</b></td><td class="mono" style="color:var(--ink-3)">${l.t}</td></tr>`).join('')+`</tbody></table>`;
}
function logAction(act, tgt) {
  const d = new Date();
  const timeStr = d.getHours() + ':' + d.getMinutes() + ' ' + (d.getDate()) + '/' + (d.getMonth()+1);
  auditLogs.unshift({u: CURRENT_USER.name, act, tgt, t: timeStr});
  renderAudit();
}
'''
content = content.replace(audit_old, audit_new)

# Initial render of Audit
content = content.replace('''document.getElementById('auditBody').innerHTML=`<table class="users-table"><thead><tr><th>المستخدم</th><th>العملية</th><th>الهدف</th><th>عنوان IP</th><th>الوقت</th></tr></thead><tbody>`+
  auditLogs.map(l=>`<tr><td class="td-name">${l.u}</td><td>${l.act}</td><td>${l.tgt}</td><td class="mono">${l.ip}</td><td class="mono" style="color:var(--ink-3)">${l.t}</td></tr>`).join('')+`</tbody></table>`;''', "renderAudit();")


# 2. Add Archive functions & HTML
archive_html_old = '''<section class="view" id="view-archive"><div class="panel"><div class="panel-body" style="text-align:center;padding:60px;color:var(--ink-3)">الأرشيف — الحسابات المحذوفة (Soft Delete) مع إمكانية الاستعادة</div></div></section>'''
archive_html_new = '''<section class="view" id="view-archive">
  <div class="toolbar"><h3 style="margin-bottom:12px;">الأرشيف</h3></div>
  <div id="archiveWrap"></div>
</section>'''
content = content.replace(archive_html_old, archive_html_new)

archive_js = '''
function archiveAccount(id) {
  if(!confirm('أرشفة هذا الحساب؟')) return;
  const a = ACCOUNTS.find(x => x.id === id);
  if(a) { a.archived = true; logAction('أرشفة حساب', a.name); toast('تم النقل للأرشيف'); renderAccounts(); updateDashboardStats(); renderArchive(); }
}
function restoreAccount(id) {
  const a = ACCOUNTS.find(x => x.id === id);
  if(a) { a.archived = false; logAction('استعادة حساب', a.name); toast('تم استعادة الحساب'); renderAccounts(); updateDashboardStats(); renderArchive(); }
}
function renderArchive() {
  const arc = ACCOUNTS.filter(a => a.archived);
  document.getElementById('archiveWrap').innerHTML = arc.length ? `<table class="users-table"><thead><tr><th>الحساب</th><th>المنصة</th><th>الحالة القديمة</th><th>الإجراء</th></tr></thead><tbody>`+
    arc.map(a => `<tr><td><b>${a.name}</b></td><td>${PLATFORMS[a.plat].name}</td><td>${STATUS[a.status].l}</td><td><button class="btn-primary" style="padding:6px 12px;font-size:12px" onclick="restoreAccount(${a.id})">استعادة</button></td></tr>`).join('')+`</tbody></table>` : `<div class="panel"><div class="panel-body" style="text-align:center;padding:60px;color:var(--ink-3)">الأرشيف فارغ حالياً</div></div>`;
}
'''
content = content.replace('/* ============ NAV ============ */', archive_js + '\n/* ============ NAV ============ */')

# Add renderArchive call to initial setup
content = content.replace('renderAccounts();', 'renderAccounts();\nrenderArchive();')


# 3. Update filtered() to hide archived
content = content.replace('return ACCOUNTS.filter(a=>{', 'return ACCOUNTS.filter(a=>{\n    if(a.archived) return false;')

# Update stat filtering to hide archived
content = content.replace("const data = ACCOUNTS.filter(a => CURRENT_USER.role === 'Super Admin' || a.owner === CURRENT_USER.name);", "const data = ACCOUNTS.filter(a => !a.archived && (CURRENT_USER.role === 'Super Admin' || a.owner === CURRENT_USER.name));")


# 4. Update Delete/Archive Buttons
content = content.replace("onclick=\"toast('نقل ${a.name} إلى الأرشيف (Soft Delete)')\"", "onclick=\"archiveAccount(${a.id})\"")


# 5. User Search Box
content = content.replace('<input placeholder="ابحث عن مستخدم…">', '<input id="usrSearch" placeholder="ابحث عن مستخدم…" oninput="renderUsers()">')

user_render_old = '''  document.getElementById('usersWrap').innerHTML=`<table class="users-table"><thead><tr><th>المستخدم</th><th>الصلاحية</th><th>القسم</th><th>الحسابات المسندة</th><th>آخر نشاط</th><th>الحالة</th><th></th></tr></thead><tbody>`+
    USERS.map(u=> {'''
user_render_new = '''  const q = (document.getElementById('usrSearch')?.value || '').toLowerCase();
  const fUsers = USERS.filter(u => u.name.toLowerCase().includes(q) || u.email.toLowerCase().includes(q));
  document.getElementById('usersWrap').innerHTML=`<table class="users-table"><thead><tr><th>المستخدم</th><th>الصلاحية</th><th>القسم</th><th>الحسابات المسندة</th><th>آخر نشاط</th><th>الحالة</th><th></th></tr></thead><tbody>`+
    fUsers.map(u=> {'''
content = content.replace(user_render_old, user_render_new)


# 6. Delete User unassignment & log
content = content.replace('''  if(confirm('هل أنت متأكد من حذف هذا المستخدم؟')) {
    const idx = USERS.findIndex(u => u.email === email);
    if(idx > -1) USERS.splice(idx, 1);
    toast('تم حذف المستخدم');
    renderUsers();
  }''', '''  if(confirm('هل أنت متأكد من حذف هذا المستخدم؟')) {
    const u = USERS.find(x => x.email === email);
    if(u) {
      ACCOUNTS.forEach(a => { if(a.owner === u.name) a.owner = "غير معين"; });
      const idx = USERS.indexOf(u);
      USERS.splice(idx, 1);
      toast('تم حذف المستخدم وإلغاء تعيين حساباته');
      logAction('حذف مستخدم', u.name);
      renderUsers();
      renderAccounts();
    }
  }''')


# 7. Add LogAction to saves
content = content.replace("toast('تم تحديث الحساب بنجاح');", "toast('تم تحديث الحساب بنجاح'); logAction('تعديل حساب', name);")
content = content.replace("toast('تمت إضافة الحساب بنجاح');", "toast('تمت إضافة الحساب بنجاح'); logAction('إضافة حساب', name);")

content = content.replace("toast('تم تحديث المستخدم بنجاح');", "toast('تم تحديث المستخدم بنجاح'); logAction('تعديل مستخدم', name);")
content = content.replace("toast('تم إضافة المستخدم بنجاح');", "toast('تم إضافة المستخدم بنجاح'); logAction('إضافة مستخدم', name);")

content = content.replace("toast('تم حفظ العمل بنجاح!');", "toast('تم حفظ العمل بنجاح!'); logAction('نشر عمل', acc);")


# 8. Add Edit Button to Account Table View
table_actions_old = '''<div class="row-actions">
          <button class="acc-btn" title="فتح" onclick="toast('فتح ${a.name}')"><svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M15 3h6v6M10 14 21 3M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/></svg></button>
          <button class="acc-btn" title="التفاصيل" onclick="openDrawer(${a.id})"><svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4M12 8h.01"/></svg></button>
        </div>'''
table_actions_new = '''<div class="row-actions">
          <button class="acc-btn" title="فتح" onclick="toast('فتح ${a.name}')"><svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M15 3h6v6M10 14 21 3M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/></svg></button>
          ${CURRENT_USER.role === 'Super Admin' ? `<button class="acc-btn" title="تعديل" onclick="openAccModal(${a.id})"><svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg></button>` : ''}
          <button class="acc-btn" title="التفاصيل" onclick="openDrawer(${a.id})"><svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4M12 8h.01"/></svg></button>
        </div>'''
content = content.replace(table_actions_old, table_actions_new)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
