import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add Modals HTML
modals_html = '''
<!-- Account Modal -->
<div class="overlay" id="accOverlay" onclick="document.getElementById('accOverlay').classList.remove('open');document.getElementById('accModal').classList.remove('open')"></div>
<div class="drawer" id="accModal" style="width:500px; padding: 22px; right: 50%; transform: translate(50%, -150%); top: 50%; height: auto; max-height: 90vh; border-radius: 14px; left: auto; transition: .2s; opacity:0; pointer-events:none; overflow-y:auto">
  <h3 style="margin-bottom:16px;" id="accModalTitle">إضافة حساب جديد</h3>
  <div style="display:flex;flex-direction:column;gap:12px;">
    <input type="hidden" id="editAccId" value="">
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;">
      <div><label style="font-size:12px;color:var(--ink-3)">اسم الحساب</label><input type="text" id="inpAccName" class="select" style="width:100%" placeholder="اسم الحساب"></div>
      <div><label style="font-size:12px;color:var(--ink-3)">اسم المستخدم</label><input type="text" id="inpAccUser" class="select" style="width:100%" placeholder="@username"></div>
      <div><label style="font-size:12px;color:var(--ink-3)">المنصة</label><select id="inpAccPlat" class="select" style="width:100%">
        <option value="instagram">Instagram</option><option value="tiktok">TikTok</option><option value="x">X</option><option value="youtube">YouTube</option><option value="facebook">Facebook</option><option value="snapchat">Snapchat</option><option value="linkedin">LinkedIn</option><option value="telegram">Telegram</option>
      </select></div>
      <div><label style="font-size:12px;color:var(--ink-3)">القسم</label><select id="inpAccDept" class="select" style="width:100%">
        <option>التصميم</option><option>التسويق</option><option>الدعم</option><option>المبيعات</option><option>الإدارة</option>
      </select></div>
      <div><label style="font-size:12px;color:var(--ink-3)">المسؤول (الأدمن)</label><select id="inpAccOwner" class="select" style="width:100%">
        <option>علي المرتضى</option><option>سارة أحمد</option><option>حسن فاضل</option><option>زينب كريم</option><option>محمد علي</option>
      </select></div>
      <div><label style="font-size:12px;color:var(--ink-3)">الحالة</label><select id="inpAccStatus" class="select" style="width:100%">
        <option value="active">نشط</option><option value="stopped">متوقف</option><option value="blocked">محظور</option><option value="pending">بانتظار التحقق</option><option value="maint">تحت الصيانة</option>
      </select></div>
    </div>
    <div><label style="font-size:12px;color:var(--ink-3)">البريد الإلكتروني</label><input type="email" id="inpAccEmail" class="select" style="width:100%" placeholder="email@example.com"></div>
    <div><label style="font-size:12px;color:var(--ink-3)">كلمة المرور</label><input type="text" id="inpAccPw" class="select" style="width:100%" placeholder="Password"></div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;">
      <div><label style="font-size:12px;color:var(--ink-3)">رقم الهاتف</label><input type="text" id="inpAccPhone" class="select" style="width:100%" placeholder="+964..."></div>
      <div><label style="font-size:12px;color:var(--ink-3)">المصادقة الثنائية</label><select id="inpAcc2FA" class="select" style="width:100%"><option>مُفعّل</option><option>غير مُفعّل</option></select></div>
    </div>
    <button class="btn-primary" style="justify-content:center;margin-top:8px" onclick="saveAccount()">حفظ الحساب</button>
  </div>
</div>

<!-- User Modal -->
<div class="overlay" id="userOverlay" onclick="document.getElementById('userOverlay').classList.remove('open');document.getElementById('userModal').classList.remove('open')"></div>
<div class="drawer" id="userModal" style="width:400px; padding: 22px; right: 50%; transform: translate(50%, -150%); top: 50%; height: auto; max-height: 90vh; border-radius: 14px; left: auto; transition: .2s; opacity:0; pointer-events:none;">
  <h3 style="margin-bottom:16px;" id="userModalTitle">إضافة مستخدم جديد</h3>
  <div style="display:flex;flex-direction:column;gap:12px;">
    <input type="hidden" id="editUserEmail" value="">
    <div><label style="font-size:12px;color:var(--ink-3)">الاسم الكامل</label><input type="text" id="inpUserName" class="select" style="width:100%" placeholder="الاسم الكامل"></div>
    <div><label style="font-size:12px;color:var(--ink-3)">البريد الإلكتروني</label><input type="email" id="inpUserEmail" class="select" style="width:100%" placeholder="email@404studio.iq"></div>
    <div><label style="font-size:12px;color:var(--ink-3)">الصلاحية</label><select id="inpUserRole" class="select" style="width:100%">
      <option value="Admin|role-admin">Admin</option>
      <option value="Manager|role-mgr">Manager</option>
      <option value="Marketing|role-mkt">Marketing</option>
      <option value="Viewer|role-view">Viewer</option>
    </select></div>
    <div><label style="font-size:12px;color:var(--ink-3)">القسم</label><select id="inpUserDept" class="select" style="width:100%">
      <option>التصميم</option><option>التسويق</option><option>الدعم</option><option>المبيعات</option><option>الإدارة</option>
    </select></div>
    <button class="btn-primary" style="justify-content:center;margin-top:8px" onclick="saveUser()">حفظ المستخدم</button>
  </div>
</div>
'''

content = content.replace('<!-- Detail Drawer -->', modals_html + '\n<!-- Detail Drawer -->')
content = content.replace('#pubModal.open{transform: translate(50%, -50%) !important; opacity:1 !important; pointer-events:auto !important;}',
                          '#pubModal.open, #accModal.open, #userModal.open {transform: translate(50%, -50%) !important; opacity:1 !important; pointer-events:auto !important;}')

# 2. Update existing buttons to use new Modals
# Add Account Button
btn_add_acc = '''<button class="btn-primary" onclick="toast('نافذة إضافة حساب — سيتم ربطها بالباك-إند')">'''
new_btn_add_acc = '''<button class="btn-primary" id="btnAddAcc" onclick="openAccModal()">'''
content = content.replace(btn_add_acc, new_btn_add_acc)

# Add User Button
btn_add_user = '''<button class="btn-primary" onclick="toast('نافذة إضافة مستخدم')">'''
new_btn_add_user = '''<button class="btn-primary" id="btnAddUser" onclick="openUserModal()">'''
content = content.replace(btn_add_user, new_btn_add_user)

# 3. Add Edit Button to Drawer Head
drawer_head_old = '''        <button class="dh-close" onclick="closeDrawer()">'''
drawer_head_new = '''        <button class="copy-btn" id="drawerEditBtn" style="margin-inline-start:auto" title="تعديل الحساب" onclick="openAccModal(${a.id})"><svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg></button>
        <button class="dh-close" onclick="closeDrawer()" style="margin-inline-start:8px">'''
content = content.replace(drawer_head_old, drawer_head_new)

# 4. Hide Buttons if not Super Admin
js_logic_hide = '''  // Toggle Nav Items
  if(CURRENT_USER.role === 'Super Admin'){
    document.querySelector('[data-view="users"]').style.display = 'flex';
    document.querySelector('[data-view="reports"]').style.display = 'flex';
    document.querySelector('[data-view="audit"]').style.display = 'flex';
    document.getElementById('navMyWork').style.display = 'none';
    document.getElementById('btnAddAcc').style.display = 'flex';
  } else {
    document.querySelector('[data-view="users"]').style.display = 'none';
    document.querySelector('[data-view="reports"]').style.display = 'none';
    document.querySelector('[data-view="audit"]').style.display = 'none';
    document.getElementById('navMyWork').style.display = 'flex';
    document.getElementById('btnAddAcc').style.display = 'none';
  }'''
content = content.replace('''  // Toggle Nav Items
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
  }''', js_logic_hide)

# Modify Drawer edit button visibility
content = content.replace("document.getElementById('drawer').innerHTML=`", "document.getElementById('drawer').innerHTML=`")
# Actually, I'll do it inside renderDrawer.
# Wait, drawer_head_new has the button. Let's make it conditionally rendered.
drawer_head_conditional = '''        ${CURRENT_USER.role === 'Super Admin' ? `<button class="copy-btn" id="drawerEditBtn" style="margin-inline-start:auto" title="تعديل الحساب" onclick="openAccModal(${a.id})"><svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg></button>` : '<div style="margin-inline-start:auto"></div>'}
        <button class="dh-close" onclick="closeDrawer()" style="margin-inline-start:8px">'''
content = content.replace(drawer_head_new, drawer_head_conditional)


# 5. JS Logic for Modals & Saving Data
js_functions = '''
function openAccModal(id) {
  const isEdit = id != null;
  document.getElementById('accModalTitle').textContent = isEdit ? 'تعديل الحساب' : 'إضافة حساب جديد';
  
  if (isEdit) {
    const a = ACCOUNTS.find(x => x.id === id);
    document.getElementById('editAccId').value = a.id;
    document.getElementById('inpAccName').value = a.name;
    document.getElementById('inpAccUser').value = a.user;
    document.getElementById('inpAccPlat').value = a.plat;
    document.getElementById('inpAccDept').value = a.dept;
    document.getElementById('inpAccOwner').value = a.owner;
    document.getElementById('inpAccStatus').value = a.status;
    document.getElementById('inpAccEmail').value = a.email;
    document.getElementById('inpAccPw').value = a.pw;
    document.getElementById('inpAccPhone').value = a.phone;
    document.getElementById('inpAcc2FA').value = a.twofa;
  } else {
    document.getElementById('editAccId').value = '';
    document.getElementById('inpAccName').value = '';
    document.getElementById('inpAccUser').value = '';
    document.getElementById('inpAccEmail').value = '';
    document.getElementById('inpAccPw').value = '';
    document.getElementById('inpAccPhone').value = '';
  }
  
  document.getElementById('accOverlay').classList.add('open');
  document.getElementById('accModal').classList.add('open');
}

function saveAccount() {
  const id = document.getElementById('editAccId').value;
  const name = document.getElementById('inpAccName').value;
  const user = document.getElementById('inpAccUser').value;
  const plat = document.getElementById('inpAccPlat').value;
  const dept = document.getElementById('inpAccDept').value;
  const owner = document.getElementById('inpAccOwner').value;
  const status = document.getElementById('inpAccStatus').value;
  const email = document.getElementById('inpAccEmail').value;
  const pw = document.getElementById('inpAccPw').value;
  const phone = document.getElementById('inpAccPhone').value;
  const twofa = document.getElementById('inpAcc2FA').value;
  
  if(!name || !user) return toast('يرجى ملء اسم الحساب واسم المستخدم');
  
  if (id) {
    // Edit
    const a = ACCOUNTS.find(x => x.id == id);
    if(a) {
      a.name = name; a.user = user; a.plat = plat; a.dept = dept; a.owner = owner;
      a.status = status; a.email = email; a.pw = pw; a.phone = phone; a.twofa = twofa;
    }
    toast('تم تحديث الحساب بنجاح');
  } else {
    // Add
    ACCOUNTS.unshift({
      id: Date.now(), name, user, plat, dept, owner, status, email, pw, phone, twofa,
      last: 'الآن', recovery: '—', url: plat+'.com/'+user, opens: 0, createdBy: CURRENT_USER.name, pwChanged: 'الآن'
    });
    toast('تمت إضافة الحساب بنجاح');
  }
  
  document.getElementById('accOverlay').click();
  renderAccounts();
  updateDashboardStats();
  if(id) { renderDrawer('info'); } // Refresh drawer if open
}

function renderUsers() {
  document.getElementById('usersWrap').innerHTML=`<table class="users-table"><thead><tr><th>المستخدم</th><th>الصلاحية</th><th>القسم</th><th>الحسابات المسندة</th><th>آخر نشاط</th><th>الحالة</th><th></th></tr></thead><tbody>`+
    USERS.map(u=> {
      const assignedCount = ACCOUNTS.filter(a => a.owner === u.name).length;
      return `<tr><td><div class="td-acc"><div class="avatar" style="width:34px;height:34px;border-radius:9px;font-size:12px">${u.name[0]}</div><div><div class="td-name">${u.name}</div><div class="td-user" style="direction:rtl">${u.email}</div></div></div></td>
    <td><span class="role-badge ${u.roleClass}">${u.role}</span></td><td>${u.dept}</td><td class="mono">${assignedCount}</td><td style="color:var(--ink-3)">${u.last}</td>
    <td><span class="status-pill ${u.status==='active'?'s-active':'s-stopped'}">${u.status==='active'?'نشط':'معطّل'}</span></td>
    <td><div class="row-actions">
      <button class="copy-btn" onclick="openUserModal('${u.email}')"><svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg></button>
      <button class="copy-btn" onclick="deleteUser('${u.email}')" style="color:var(--red)"><svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M3 6h18M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg></button>
    </div></td></tr>`
    }).join('')+`</tbody></table>`;
}

function openUserModal(email) {
  const isEdit = email != null && email != '';
  document.getElementById('userModalTitle').textContent = isEdit ? 'تعديل المستخدم' : 'إضافة مستخدم جديد';
  
  if (isEdit) {
    const u = USERS.find(x => x.email === email);
    document.getElementById('editUserEmail').value = u.email;
    document.getElementById('inpUserName').value = u.name;
    document.getElementById('inpUserEmail').value = u.email;
    document.getElementById('inpUserRole').value = u.role + '|' + u.roleClass;
    document.getElementById('inpUserDept').value = u.dept;
  } else {
    document.getElementById('editUserEmail').value = '';
    document.getElementById('inpUserName').value = '';
    document.getElementById('inpUserEmail').value = '';
  }
  
  document.getElementById('userOverlay').classList.add('open');
  document.getElementById('userModal').classList.add('open');
}

function saveUser() {
  const origEmail = document.getElementById('editUserEmail').value;
  const name = document.getElementById('inpUserName').value;
  const email = document.getElementById('inpUserEmail').value;
  const roleVal = document.getElementById('inpUserRole').value.split('|');
  const role = roleVal[0];
  const roleClass = roleVal[1];
  const dept = document.getElementById('inpUserDept').value;
  
  if(!name || !email) return toast('يرجى ملء الاسم والبريد');
  
  if (origEmail) {
    const u = USERS.find(x => x.email === origEmail);
    if(u) {
      // If name changed, update ACCOUNTS owner if they had assigned accounts
      if(u.name !== name) {
        ACCOUNTS.forEach(a => { if(a.owner === u.name) a.owner = name; });
        PUBLISH_LOGS.forEach(l => { if(l.admin === u.name) l.admin = name; });
      }
      u.name = name; u.email = email; u.role = role; u.roleClass = roleClass; u.dept = dept;
    }
    toast('تم تحديث المستخدم بنجاح');
  } else {
    USERS.push({ name, email, role, roleClass, dept, accounts:0, last:'الآن', status:'active' });
    toast('تم إضافة المستخدم بنجاح');
  }
  
  document.getElementById('userOverlay').click();
  renderUsers();
}

function deleteUser(email) {
  if(confirm('هل أنت متأكد من حذف هذا المستخدم؟')) {
    const idx = USERS.findIndex(u => u.email === email);
    if(idx > -1) USERS.splice(idx, 1);
    toast('تم حذف المستخدم');
    renderUsers();
  }
}
'''

content = content.replace('/* ============ NAV ============ */', js_functions + '\n/* ============ NAV ============ */')

# Find the USERS table initial render and replace it with a call to renderUsers()
# Wait, the initial render is:
users_old = '''document.getElementById('usersWrap').innerHTML=`<table class="users-table"><thead><tr><th>المستخدم</th><th>الصلاحية</th><th>القسم</th><th>الحسابات المسندة</th><th>آخر نشاط</th><th>الحالة</th></tr></thead><tbody>`+
  USERS.map(u=>`<tr><td><div class="td-acc"><div class="avatar" style="width:34px;height:34px;border-radius:9px;font-size:12px">${u.name[0]}</div><div><div class="td-name">${u.name}</div><div class="td-user" style="direction:rtl">${u.email}</div></div></div></td>
  <td><span class="role-badge ${u.roleClass}">${u.role}</span></td><td>${u.dept}</td><td class="mono">${u.accounts}</td><td style="color:var(--ink-3)">${u.last}</td>
  <td><span class="status-pill ${u.status==='active'?'s-active':'s-stopped'}">${u.status==='active'?'نشط':'معطّل'}</span></td></tr>`).join('')+`</tbody></table>`;'''
content = content.replace(users_old, "renderUsers();")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
