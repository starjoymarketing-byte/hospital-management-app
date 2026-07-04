-- ============================================================
-- Hospital Management System - Supabase Database Schema
-- Run this entire file in: Supabase Dashboard > SQL Editor > New Query
-- ============================================================

-- 1. PROFILES (links to Supabase Auth users, stores role info)
create table public.profiles (
  id uuid references auth.users(id) on delete cascade primary key,
  full_name text not null,
  role text not null check (role in ('admin','doctor','receptionist','pharmacist')),
  phone text,
  department text,
  created_at timestamptz default now()
);

-- 2. PATIENTS
create table public.patients (
  id bigint generated always as identity primary key,
  full_name text not null,
  age int,
  gender text check (gender in ('Male','Female','Other')),
  phone text,
  address text,
  blood_group text,
  emergency_contact text,
  admission_date date,
  discharge_date date,
  status text default 'Outpatient' check (status in ('Admitted','Discharged','Outpatient')),
  created_at timestamptz default now()
);

-- 3. DOCTORS
create table public.doctors (
  id bigint generated always as identity primary key,
  full_name text not null,
  specialization text,
  phone text,
  email text,
  department text,
  qualification text,
  experience_years int,
  consultation_fee numeric(10,2) default 0,
  available boolean default true,
  created_at timestamptz default now()
);

-- 4. APPOINTMENTS
create table public.appointments (
  id bigint generated always as identity primary key,
  patient_id bigint references public.patients(id) on delete cascade,
  doctor_id bigint references public.doctors(id) on delete set null,
  appointment_date date not null,
  appointment_time time not null,
  reason text,
  status text default 'Scheduled' check (status in ('Scheduled','Completed','Cancelled')),
  notes text,
  created_at timestamptz default now()
);

-- 5. PHARMACY INVENTORY
create table public.pharmacy_inventory (
  id bigint generated always as identity primary key,
  medicine_name text not null,
  category text,
  manufacturer text,
  batch_number text,
  quantity int default 0,
  unit_price numeric(10,2) default 0,
  expiry_date date,
  reorder_level int default 10,
  created_at timestamptz default now()
);

-- 6. BILLING
create table public.bills (
  id bigint generated always as identity primary key,
  patient_id bigint references public.patients(id) on delete cascade,
  appointment_id bigint references public.appointments(id) on delete set null,
  bill_date date default current_date,
  consultation_fee numeric(10,2) default 0,
  room_charges numeric(10,2) default 0,
  medicine_charges numeric(10,2) default 0,
  other_charges numeric(10,2) default 0,
  total_amount numeric(10,2) default 0,
  payment_status text default 'Pending' check (payment_status in ('Paid','Pending','Partial')),
  payment_method text,
  created_at timestamptz default now()
);

-- ============================================================
-- ROW LEVEL SECURITY
-- Simple policy: any logged-in (authenticated) app user can read/write.
-- App-level role checks (in Streamlit) control what each role actually sees.
-- You can tighten these later per-role if needed.
-- ============================================================
alter table public.profiles enable row level security;
alter table public.patients enable row level security;
alter table public.doctors enable row level security;
alter table public.appointments enable row level security;
alter table public.pharmacy_inventory enable row level security;
alter table public.bills enable row level security;

create policy "Authenticated full access" on public.profiles for all using (auth.uid() is not null);
create policy "Authenticated full access" on public.patients for all using (auth.uid() is not null);
create policy "Authenticated full access" on public.doctors for all using (auth.uid() is not null);
create policy "Authenticated full access" on public.appointments for all using (auth.uid() is not null);
create policy "Authenticated full access" on public.pharmacy_inventory for all using (auth.uid() is not null);
create policy "Authenticated full access" on public.bills for all using (auth.uid() is not null);
