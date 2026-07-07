import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add PUBLISH_LOGS
publish_data = '''
let PUBLISH_LOGS=[
  {id:1, admin:'سارة أحمد', acc:'مرماز أكاديمي', link:'instagram.com/p/123', notes:'نشر بوست العرض الجديد', t:'قبل ساعتين'},
  {id:2, admin:'حسن فاضل', acc:'مرماز زون', link:'tiktok.com/v/456', notes:'فيديو الكواليس', t:'قبل يوم'}
];
let CURRENT_USER = {id:'super', role:'Super Admin', name:'علي المرتضى'};
'''
content = content.replace('const USERS=[', publish_data + '\nconst USERS=[')

# Update Nav Titles to include My Work
titles_old = "archive:['الأرشيف','الحسابات المحذوفة (Soft Delete)']};"
titles_new = "archive:['الأرشيف','الحسابات المحذوفة (Soft Delete)'], mywork:['سجل النشر','أعمالي والمقاطع التي قمت بنشرها']};"
content = content.replace(titles_old, titles_new)

# Update renderAccounts to filter by user role
filter_fn_old = '''function filtered(){
  const q=document.getElementById('accSearch').value.toLowerCase();
  const st=document.getElementById('fStatus').value;const dp=document.getElementById('fDept').value;
  return ACCOUNTS.filter(a=>{
    if(activePlat&&a.plat!==activePlat)return false;
    if(st&&a.status!==st)return false;
    if(dp&&a.dept!==dp)return false;
    if(q&&!(a.name.toLowerCase().includes(q)||a.user.toLowerCase().includes(q)||a.email.toLowerCase().includes(q)))return false;
    return true;
  });
}'''

filter_fn_new = '''function filtered(){
  const q=document.getElementById('accSearch').value.toLowerCase();
  const st=document.getElementById('fStatus').value;const dp=document.getElementById('fDept').value;
  return ACCOUNTS.filter(a=>{
    if(CURRENT_USER.role !== 'Super Admin' && a.owner !== CURRENT_USER.name) return false;
    if(activePlat&&a.plat!==activePlat)return false;
    if(st&&a.status!==st)return false;
    if(dp&&a.dept!==dp)return false;
    if(q&&!(a.name.toLowerCase().includes(q)||a.user.toLowerCase().includes(q)||a.email.toLowerCase().includes(q)))return false;
    return true;
  });
}'''
content = content.replace(filter_fn_old, filter_fn_new)

# Add Role Switcher Logic & Publish Logic
logic = '''
document.getElementById('roleSwitcher').onchange = (e) => {
  const val = e.target.value;
  if(val === 'ali') CURRENT_USER = {id:'super', role:'Super Admin', name:'علي المرتضى'};
  else if(val === 'sara') CURRENT_USER = {id:'sara', role:'Admin', name:'سارة أحمد'};
  else if(val === 'hasan') CURRENT_USER = {id:'hasan', role:'Admin', name:'حسن فاضل'};
  
  // Update UI
  document.querySelector('.user-name').textContent = CURRENT_USER.name;
  document.querySelector('.user-role').textContent = CURRENT_USER.role;
  document.querySelector('.avatar').textContent = CURRENT_USER.name[0];
  
  // Toggle Nav Items
  if(CURRENT_USER.role === 'Super Admin'){
    document.querySelector('[data-view="users"]').style.display = 'flex';
    document.querySelector('[data-view="reports"]').style.display = 'flex';
    document.querySelector('[data-view="audit"]').style.display = 'flex';
    document.getElementById('navMyWork').style.display = 'none';
  } else {
    document.querySelector('[data-view="users"]').style.display = 'none';
    document.querySelector('[data-view="reports"]').style.display = 'none';
    document.querySelector('[data-view="audit"]').style.display = 'none';
    document.getElementById('navMyWork').style.display = 'flex';
  }
  
  // Default to dashboard
  document.querySelector('[data-view="dashboard"]').click();
  
  renderAccounts();
  updateDashboardStats();
};

function updateDashboardStats() {
  const data = ACCOUNTS.filter(a => CURRENT_USER.role === 'Super Admin' || a.owner === CURRENT_USER.name);
  const total = data.length;
  const active = data.filter(a => a.status === 'active').length;
  document.getElementById('statGrid').innerHTML = statData.map((s,i) => {
    let v = s.val;
    if(i===0) v = total;
    if(i===1) v = active;
    if(CURRENT_USER.role !== 'Super Admin' && i>1) v = Math.floor(v/3);
    return `<div class="stat"><div class="stat-top"><div class="stat-icn" style="background:${s.bg};color:${s.c}"><svg fill="none" stroke="currentColor" viewBox="0 0 24 24">${s.icon}</svg></div><span class="stat-trend ${s.up?'up':'down'}"><svg fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path d="${s.up?'m18 15-6-6-6 6':'m6 9 6 6 6-6'}"/></svg>${s.trend}</span></div><div class="stat-val">${v}</div><div class="stat-lbl">${s.lbl}</div></div>`
  }).join('');
}

function renderPublishLogs() {
  const grid = document.getElementById('publishGrid');
  const logs = PUBLISH_LOGS.filter(l => CURRENT_USER.role === 'Super Admin' || l.admin === CURRENT_USER.name);
  grid.innerHTML = logs.map(l => `
    <div class="acc-card" style="padding:16px;">
      <div style="font-size:12px;color:var(--ink-3);margin-bottom:8px;">${l.t} &middot; <b>${l.acc}</b></div>
      <div style="font-size:14px;font-weight:600;margin-bottom:8px;">${l.notes}</div>
      ${l.link ? `<a href="https://${l.link}" target="_blank" style="color:var(--accent);font-size:12px;text-decoration:none;">${l.link}</a>` : ''}
    </div>
  `).join('') || emptyState();
}

function openPublishModal() {
  const sel = document.getElementById('pubAcc');
  const myAccs = ACCOUNTS.filter(a => CURRENT_USER.role === 'Super Admin' || a.owner === CURRENT_USER.name);
  sel.innerHTML = '<option value="">اختر الحساب...</option>' + myAccs.map(a => `<option>${a.name}</option>`).join('');
  document.getElementById('pubOverlay').classList.add('open');
  document.getElementById('pubModal').classList.add('open');
}

function savePublish() {
  const acc = document.getElementById('pubAcc').value;
  const link = document.getElementById('pubLink').value;
  const notes = document.getElementById('pubNotes').value;
  if(!acc || !notes) return toast('يرجى اختيار الحساب وكتابة ملاحظات');
  PUBLISH_LOGS.unshift({id: Date.now(), admin: CURRENT_USER.name, acc, link, notes, t: 'الآن'});
  document.getElementById('pubOverlay').click();
  toast('تم حفظ العمل بنجاح!');
  renderPublishLogs();
}

function generateReport() {
  const admin = document.getElementById('repAdmin').value;
  let logs = PUBLISH_LOGS;
  if(admin) logs = logs.filter(l => l.admin === admin);
  
  const html = `<table class="users-table" style="margin-top:16px;"><thead><tr><th>المشرف</th><th>الحساب</th><th>المنشور</th><th>التفاصيل</th><th>الوقت</th></tr></thead><tbody>` + 
    logs.map(l => `<tr><td class="td-name">${l.admin}</td><td><b>${l.acc}</b></td><td class="mono" style="color:var(--accent)">${l.link||'—'}</td><td>${l.notes}</td><td style="color:var(--ink-3)">${l.t}</td></tr>`).join('') + `</tbody></table>`;
  
  document.getElementById('reportWrap').innerHTML = logs.length ? html : `<div class="panel"><div class="panel-body" style="text-align:center;padding:60px;color:var(--ink-3)">لا توجد بيانات لهذه الفترة</div></div>`;
}

// Hook into nav click
const oldNavClick = document.querySelectorAll('.nav-item');
oldNavClick.forEach(n => {
  n.addEventListener('click', () => {
    if(n.dataset.view === 'mywork') renderPublishLogs();
  });
});
'''
content = content.replace('renderAccounts();', 'renderAccounts();\n' + logic)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
