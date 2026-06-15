# PROJECT REQUIREMENT DOCUMENT
## Task Management Website
**Berbasis Django REST + React + Kanban Board**

| | |
|---|---|
| **Versi** | 1.0 |
| **Tanggal** | Juni 2025 |
| **Status** | Draft |
| **Author** | Tim Pengembang |

---

## Daftar Isi
1. [Ringkasan Eksekutif](#1-ringkasan-eksekutif)
2. [Tujuan & Sasaran Produk](#2-tujuan--sasaran-produk)
3. [Tech Stack & Arsitektur](#3-tech-stack--arsitektur)
4. [Fitur & Functional Requirements](#4-fitur--functional-requirements)
5. [Non-Functional Requirements](#5-non-functional-requirements)
6. [Desain API Endpoints](#6-desain-api-endpoints-django-rest)
7. [Struktur Database](#7-struktur-database)
8. [Struktur Folder Project](#8-struktur-folder-project)
9. [Rencana Pengembangan (Milestone)](#9-rencana-pengembangan-milestone)
10. [Risiko & Mitigasi](#10-risiko--mitigasi)
11. [Definisi & Glosarium](#11-definisi--glosarium)

---

## 1. Ringkasan Eksekutif

Dokumen ini merupakan Product Requirement Document (PRD) untuk pengembangan aplikasi web **Task Management berbasis Kanban Board**. Aplikasi ini dirancang untuk membantu tim atau individu mengelola pekerjaan secara visual, efisien, dan kolaboratif.

Sistem dibangun menggunakan arsitektur **decoupled**: backend Django REST Framework sebagai API server dan frontend React sebagai SPA (Single Page Application) yang terhubung melalui HTTP/JSON dan diotentikasi via JWT token.

---

## 2. Tujuan & Sasaran Produk

### 2.1 Tujuan

- Memberikan antarmuka visual Kanban Board untuk manajemen tugas secara drag-and-drop.
- Memudahkan kolaborasi tim dengan sistem autentikasi berbasis pengguna.
- Menyediakan RESTful API yang terstandarisasi untuk integrasi masa depan.
- Membangun fondasi arsitektur yang scalable dan maintainable.

### 2.2 Sasaran Pengguna

| Segmen | Deskripsi | Kebutuhan Utama |
|---|---|---|
| Developer / Tim IT | Tim yang mengelola sprint dan backlog | Kanban Board, drag-and-drop, label prioritas |
| Project Manager | Memantau progres proyek | Overview board, filter status, laporan |
| Individual User | Pengguna mandiri yang mengatur to-do | Manajemen task pribadi, simple UI |

---

## 3. Tech Stack & Arsitektur

### 3.1 Gambaran Arsitektur

Sistem menggunakan arsitektur **Client-Server terpisah (decoupled)** di mana frontend dan backend berjalan sebagai service independent:

| Layer | Teknologi | Fungsi | Package Utama |
|---|---|---|---|
| Backend | Django 4.x + Python 3.11+ | API Server & Business Logic | `django`, `djangorestframework` |
| Autentikasi | JWT Token | Keamanan & Session Management | `djangorestframework-simplejwt` |
| CORS | django-cors-headers | Izin komunikasi lintas origin | `django-cors-headers` |
| Database | MySQL 8.x | Penyimpanan data relasional | `mysqlclient` |
| Dev DB Server | Laragon / XAMPP | MySQL server lokal | — |
| Frontend | React 18 + Vite | Single Page Application | `react`, `vite` |
| Kanban DnD | @hello-pangea/dnd | Drag-and-drop Kanban cards | `@hello-pangea/dnd` |
| HTTP Client | Axios | Komunikasi ke Django API | `axios` |
| Styling | Tailwind CSS | Utility-first UI styling | `tailwindcss` |

### 3.2 Alur Komunikasi Sistem

1. User membuka browser dan mengakses React App (Vite dev server / build).
2. React mengirim request login ke Django API → mendapat JWT access & refresh token.
3. Setiap API request selanjutnya menyertakan `Authorization: Bearer <token>` di header.
4. Django memvalidasi token, memproses request, dan mengembalikan response JSON.
5. React merender data ke Kanban Board; drag-and-drop mengupdate urutan via PUT/PATCH API.

---

## 4. Fitur & Functional Requirements

### 4.1 Modul Autentikasi

| ID | Fitur | Deskripsi | Priority |
|---|---|---|---|
| AUTH-01 | Register User | Pengguna baru mendaftar dengan username, email, password | High |
| AUTH-02 | Login | Login menggunakan email/username dan password, return JWT | High |
| AUTH-03 | Refresh Token | Perpanjang sesi menggunakan refresh token tanpa login ulang | High |
| AUTH-04 | Logout | Invalidate token dan hapus sesi dari client | Medium |
| AUTH-05 | Profile User | Lihat dan edit profil (nama, email, avatar) | Low |

### 4.2 Modul Project / Board

| ID | Fitur | Deskripsi | Priority |
|---|---|---|---|
| PROJ-01 | Buat Project | User membuat project/board baru dengan nama & deskripsi | High |
| PROJ-02 | List Project | Tampilkan semua project milik user yang login | High |
| PROJ-03 | Edit Project | Ubah nama, deskripsi, warna label project | Medium |
| PROJ-04 | Hapus Project | Hapus project beserta semua kolom dan kartu di dalamnya | Medium |
| PROJ-05 | Invite Member | Undang anggota tim ke project *(opsional v2)* | Low |

### 4.3 Modul Kolom (Column/Stage)

| ID | Fitur | Deskripsi | Priority |
|---|---|---|---|
| COL-01 | Buat Kolom | Tambah kolom baru di board (To Do, In Progress, Done, dll) | High |
| COL-02 | Edit Kolom | Ubah nama kolom | Medium |
| COL-03 | Hapus Kolom | Hapus kolom beserta semua task di dalamnya | Medium |
| COL-04 | Reorder Kolom | Ubah urutan kolom via drag-and-drop | Medium |

### 4.4 Modul Task / Card

| ID | Fitur | Deskripsi | Priority |
|---|---|---|---|
| TASK-01 | Buat Task | Tambah kartu task baru di dalam kolom | High |
| TASK-02 | Edit Task | Ubah judul, deskripsi, due date, priority, label | High |
| TASK-03 | Hapus Task | Hapus task dari board | High |
| TASK-04 | Move Task (DnD) | Pindah task antar kolom via drag-and-drop (`@hello-pangea/dnd`) | High |
| TASK-05 | Reorder Task | Ubah urutan task dalam kolom yang sama via drag-and-drop | High |
| TASK-06 | Priority Label | Tandai task dengan prioritas: Low / Medium / High / Critical | Medium |
| TASK-07 | Due Date | Set tanggal deadline; highlight merah jika overdue | Medium |
| TASK-08 | Assign User | Assign task ke member project *(opsional v2)* | Low |
| TASK-09 | Checklist | Sub-task berupa checklist item *(opsional v2)* | Low |

---

## 5. Non-Functional Requirements

| Kategori | Requirement | Target |
|---|---|---|
| Performance | Response time API | < 300ms untuk operasi CRUD standar |
| Performance | Frontend load time | < 2 detik (Vite build production) |
| Security | Autentikasi | JWT dengan expiry 60 menit, refresh token 7 hari |
| Security | Password hashing | Django default PBKDF2 / bcrypt |
| Security | CORS | Whitelist hanya domain frontend yang diizinkan |
| Security | Input validation | Validasi di level serializer Django dan form React |
| Usability | Responsif | Tampilan optimal di desktop (priority) dan tablet |
| Maintainability | Code style | PEP8 (Python), ESLint + Prettier (JS/React) |
| Scalability | API versioning | Gunakan prefix `/api/v1/` untuk semua endpoint |

---

## 6. Desain API Endpoints (Django REST)

### 6.1 Autentikasi

| Method | Endpoint | Deskripsi | Auth Required |
|---|---|---|---|
| POST | `/api/v1/auth/register/` | Registrasi user baru | No |
| POST | `/api/v1/auth/login/` | Login dan dapatkan JWT token | No |
| POST | `/api/v1/auth/token/refresh/` | Refresh access token | No |
| POST | `/api/v1/auth/logout/` | Logout (blacklist refresh token) | Yes |

### 6.2 Projects

| Method | Endpoint | Deskripsi | Auth Required |
|---|---|---|---|
| GET | `/api/v1/projects/` | List semua project user | Yes |
| POST | `/api/v1/projects/` | Buat project baru | Yes |
| GET | `/api/v1/projects/{id}/` | Detail project | Yes |
| PUT/PATCH | `/api/v1/projects/{id}/` | Update project | Yes |
| DELETE | `/api/v1/projects/{id}/` | Hapus project | Yes |

### 6.3 Columns & Tasks

| Method | Endpoint | Deskripsi | Auth Required |
|---|---|---|---|
| GET/POST | `/api/v1/projects/{id}/columns/` | List / buat kolom dalam project | Yes |
| PUT/DELETE | `/api/v1/columns/{id}/` | Update / hapus kolom | Yes |
| PATCH | `/api/v1/columns/reorder/` | Update urutan kolom (array of id + order) | Yes |
| GET/POST | `/api/v1/columns/{id}/tasks/` | List / buat task dalam kolom | Yes |
| GET/PUT/DELETE | `/api/v1/tasks/{id}/` | Detail / update / hapus task | Yes |
| PATCH | `/api/v1/tasks/{id}/move/` | Pindah task ke kolom lain + update order | Yes |

---

## 7. Struktur Database

### 7.1 Model Utama

| Model | Field Utama | Relasi |
|---|---|---|
| User (Django Auth) | `id`, `username`, `email`, `password`, `date_joined` | Built-in Django AbstractUser |
| Project | `id`, `name`, `description`, `color`, `owner` (FK User), `created_at` | ForeignKey ke User |
| Column | `id`, `name`, `order`, `project` (FK Project) | ForeignKey ke Project |
| Task | `id`, `title`, `description`, `priority`, `due_date`, `order`, `column` (FK Column), `created_at`, `updated_at` | ForeignKey ke Column |
| TaskLabel | `id`, `name`, `color`, `task` (FK Task) | ForeignKey ke Task *(opsional)* |

### 7.2 Diagram Relasi (ERD Sederhana)

```
User
 └── Project (owner FK)
      └── Column (project FK)
           └── Task (column FK)
                └── TaskLabel (task FK)
```

---

## 8. Struktur Folder Project

### 8.1 Backend (Django)

```
taskmanager/
├── manage.py
├── requirements.txt
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── apps/
    ├── authentication/
    │   ├── models.py
    │   ├── serializers.py
    │   ├── views.py
    │   └── urls.py
    └── projects/
        ├── models.py          # Project, Column, Task, TaskLabel
        ├── serializers.py
        ├── views.py
        ├── permissions.py
        └── urls.py
```

### 8.2 Frontend (React + Vite)

```
taskmanager-frontend/
├── package.json
├── vite.config.js
├── tailwind.config.js
└── src/
    ├── main.jsx
    ├── App.jsx
    ├── components/
    │   ├── KanbanBoard.jsx
    │   ├── Column.jsx
    │   ├── TaskCard.jsx
    │   └── Navbar.jsx
    ├── pages/
    │   ├── LoginPage.jsx
    │   ├── RegisterPage.jsx
    │   └── BoardPage.jsx
    ├── services/
    │   ├── api.js             # Axios instance + interceptor
    │   ├── authService.js
    │   └── taskService.js
    ├── hooks/
    │   └── useAuth.js
    └── context/
        └── AuthContext.jsx    # JWT storage & user state
```

---

## 9. Rencana Pengembangan (Milestone)

| Fase | Scope | Durasi Estimasi |
|---|---|---|
| **Fase 1 – Setup** | Init Django + React project, koneksi DB MySQL, CORS setup, JWT auth | 1–2 minggu |
| **Fase 2 – Backend Core** | Model & Serializer (Project, Column, Task), semua API endpoint, unit test | 2–3 minggu |
| **Fase 3 – Frontend Core** | Layout Kanban Board, komponen Column & TaskCard, Axios integration | 2–3 minggu |
| **Fase 4 – Drag & Drop** | Integrasi `@hello-pangea/dnd`, update order via API setelah drop | 1–2 minggu |
| **Fase 5 – Polish & UI** | Tailwind styling, responsif, validasi form, loading states, error handling | 1–2 minggu |
| **Fase 6 – Testing & Deploy** | End-to-end testing, bug fix, persiapan deployment *(opsional)* | 1 minggu |

**Total Estimasi: 8–13 minggu**

---

## 10. Risiko & Mitigasi

| Risiko | Tingkat | Mitigasi |
|---|---|---|
| CORS error saat dev | Medium | Pastikan `django-cors-headers` terkonfigurasi dan `CORS_ALLOWED_ORIGINS` diset ke URL React dev server |
| JWT token expired di frontend | Medium | Implementasi Axios interceptor untuk auto-refresh token sebelum request gagal |
| Order task tidak konsisten setelah DnD | High | Gunakan field `order` integer di model Task + Column; update via API PATCH setiap drop event |
| MySQL connection error | Low | Pastikan Laragon/XAMPP aktif; cek `DATABASE` settings di Django dan test dengan `python manage.py dbshell` |
| Build Vite gagal karena dependency | Low | Lock versi di `package.json`; gunakan `npm ci` untuk install konsisten |

---

## 11. Definisi & Glosarium

| Istilah | Definisi |
|---|---|
| PRD | Product Requirement Document – dokumen yang mendefinisikan kebutuhan produk sebelum development |
| JWT | JSON Web Token – standar token untuk autentikasi stateless |
| DRF | Django REST Framework – library untuk membuat REST API dengan Django |
| SPA | Single Page Application – aplikasi web yang merender UI di sisi client tanpa reload halaman |
| Kanban | Metode manajemen visual menggunakan kolom dan kartu untuk merepresentasikan status tugas |
| DnD | Drag-and-Drop – interaksi UI untuk memindahkan elemen dengan klik tahan dan geser |
| CORS | Cross-Origin Resource Sharing – mekanisme keamanan browser yang membatasi request lintas domain |
| Decoupled | Arsitektur di mana frontend dan backend berjalan sebagai service terpisah |

---

*Task Management Website PRD v1.0 — End of Document*