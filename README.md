# 🏥 Hospital Management System

Python + Streamlit + Supabase (PostgreSQL) se bana hua full hospital management app.

## Modules
- 🧑‍🤝‍🧑 Patient Records (register, search, discharge, delete)
- 🩺 Doctor Management (add, availability toggle, delete)
- 📅 Appointments & Scheduling
- 💰 Billing & Invoicing
- 💊 Pharmacy / Medicine Inventory (with low-stock alerts)
- 👤 Login System with roles: **admin, doctor, receptionist, pharmacist**

## Folder Structure
```
hospital_management_app/
├── Home.py                  ← Login page + dashboard (run this file)
├── pages/
│   ├── 1_Patients.py
│   ├── 2_Doctors.py
│   ├── 3_Appointments.py
│   ├── 4_Billing.py
│   ├── 5_Pharmacy.py
│   └── 6_User_Management.py ← admin only
├── utils/
│   ├── db.py                ← Supabase client
│   └── auth.py               ← login/logout/role guards
├── database/
│   └── schema.sql            ← run this in Supabase first
├── .streamlit/
│   └── secrets.toml.example
└── requirements.txt
```

## Setup Steps (Step-by-Step)

### 1. Supabase project banao
1. https://supabase.com par jaake free account banao
2. "New Project" click karo, naam aur password set karo
3. Project banne ke baad, sidebar mein **SQL Editor** kholo
4. `database/schema.sql` file ka pura content copy karo, paste karo, aur **Run** dabao
   - Yeh saare tables (patients, doctors, appointments, bills, pharmacy_inventory, profiles) bana dega

### 2. API Keys lo
1. Sidebar mein **Project Settings → API** kholo
2. **Project URL** aur **anon public key** copy karo

### 3. Local setup
```bash
cd hospital_management_app
pip install -r requirements.txt
```

Phir `.streamlit/secrets.toml.example` ko rename karke `.streamlit/secrets.toml` banao, aur apne real values daalo:
```toml
SUPABASE_URL = "https://xxxxxxxx.supabase.co"
SUPABASE_KEY = "your-anon-public-key"
```

### 4. Pehla Admin User banao (zaroori — ek baar)
Chunki naye users sirf admin hi bana sakta hai User Management page se, **sabse pehla admin manually banana padega**:

1. Supabase Dashboard → **Authentication → Users → Add User**
2. Email + password daalo, "Auto Confirm User" ON rakho
3. Us user ki UUID copy karo (table mein dikhegi)
4. Supabase **SQL Editor** mein yeh run karo (UUID + naam apna daal ke):
```sql
insert into public.profiles (id, full_name, role)
values ('paste-the-uuid-here', 'Your Name', 'admin');
```
5. Ab app mein isi email/password se login karo — admin ban gaye!
6. Ab User Management page se baaki staff (doctor, receptionist, pharmacist) bana sakte ho.

### 5. App run karo
```bash
streamlit run Home.py
```
Browser mein `http://localhost:8501` khulega.

## Role Permissions

| Module | Admin | Doctor | Receptionist | Pharmacist |
|---|---|---|---|---|
| Patients | ✅ | ✅ (view) | ✅ | ❌ |
| Doctors | ✅ | ❌ | ✅ (view) | ❌ |
| Appointments | ✅ | ✅ | ✅ | ❌ |
| Billing | ✅ | ❌ | ✅ | ❌ |
| Pharmacy | ✅ | ❌ | ❌ | ✅ |
| User Management | ✅ | ❌ | ❌ | ❌ |

## Notes
- Email confirmation: agar Supabase project mein "Confirm Email" setting ON hai, naye users ko login se pehle email confirm karna padega. Testing ke liye Authentication → Settings mein isे temporarily OFF kar sakte ho.
- Currency symbol ₹ hardcoded hai — chahe to `pages/4_Billing.py` aur `pages/5_Pharmacy.py` mein change kar sakte ho.
- Deploy karna ho to **Streamlit Community Cloud** (free) use kar sakte ho — secrets.toml ka content unke "Secrets" settings mein paste karna hoga.
