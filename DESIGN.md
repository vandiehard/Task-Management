# Design System & Architecture Specification
## Minimalist & Monochrome Task Management Application (Django + React + MySQL)

Dokumen spesifikasi desain ini dibuat sebagai panduan teknis dan visual untuk membangun ulang aplikasi **Task Management** berbasis Kanban board. Pendekatan estetika difokuskan pada konsep modern-minimalis dengan memanfaatkan palet warna monokromatik ekstrem guna meminimalkan distrasi visual dan memaksimalkan fokus pengguna pada manajemen tugas.

---

## 1. Filosofi Desain Visual
Desain aplikasi mengadopsi prinsip *"Form Follows Function"* dengan karakteristik utama[cite: 3]:
* **High Contrast Typography:** Kontras tajam antara elemen teks hitam dan latar belakang putih bersih untuk memastikan keterbacaan tingkat tinggi[cite: 3].
* **Flat & Border-Driven UI:** Menghindari bayangan (*drop shadows*) yang berlebihan atau gradasi kompleks[cite: 3]. Pemisahan komponen visual murni menggunakan garis tepi (*borders*) tipis dan ruang kosong (*whitespace*) yang terukur[cite: 3].
* **Micro-Interactions:** Transisi dan animasi halus khusus untuk aksi krusial seperti pemindahan kartu (*drag-and-drop*) dan perubahan status aktif komponen[cite: 3].

---

## 2. Palet Warna Monokromatik

| Komponen UI | Kode Warna (HEX) | Penerapan Spesifik |
| :--- | :--- | :--- |
| **Latar Belakang Utama** | `#FFFFFF` | Base workspace, halaman login, dan latar belakang aplikasi global[cite: 3]. |
| **Papan / Container** | `#F5F5F5` | Latar belakang kolom Kanban (Light Gray)[cite: 3]. |
| **Kartu Tugas** | `#FFFFFF` | Latar belakang kartu di dalam kolom Kanban[cite: 3]. |
| **Teks Utama & Judul** | `#1A1A1A` | Digunakan untuk seluruh `h1`, `h2`, dan teks deskripsi utama kartu[cite: 3]. |
| **Teks Sekunder / Meta** | `#737373` | Label tanggal (due date), nama pembuat, dan teks placeholder[cite: 3]. |
| **Borders & Lines** | `#E5E5E5` | Garis pembatas kolom dan tepi kartu tugas[cite: 3]. |
| **Fokus / Active State** | `#000000` | Border saat input field fokus atau kartu sedang di-drag[cite: 3]. |

---

## 3. Spesifikasi Komponen UI Kanban Board

### 3.1. Struktur Kolom (Column Container)
* **Background:** `#F5F5F5` dengan sudut melengkung minimal (`border-radius: 6px`)[cite: 3].
* **Header Kolom:** Teks tebal (`font-weight: 700`) warna `#1A1A1A`, dilengkapi badge penanda jumlah task dengan gaya melingkar penuh hitam-putih[cite: 3].
* **State Saat Drag Over:** Ketika kartu berada di atas kolom, warna kolom berubah menjadi sedikit lebih gelap (`#EEEEEE`) dengan transisi `0.2s ease-out`[cite: 3].

### 3.2. Kartu Tugas (Task Card Component)
* **Background:** `#FFFFFF` solid dengan border tipis `1px solid #E5E5E5`[cite: 3].
* **Interaksi Hover:** Border berubah menjadi `1px solid #000000` secara instan untuk memberikan efek ketajaman visual[cite: 3].
* **State Saat Di-drag:** Kartu mendapat sedikit rotasi miring (`transform: rotate(1.5deg)`), opacity diturunkan menjadi `0.9`, dan border berubah menjadi garis putus-putus hitam (`dashed #000000`)[cite: 3].

---

## 4. Pemetaan API & Integrasi Kontrak Data
Format JSON monokromatik terstruktur untuk komunikasi data antara Frontend React (Axios) dan Backend Django REST Framework[cite: 3]:

### 4.1. Endpoint Pengambilan Data Board (`GET /api/boards/1/`)
```json
{
  "id": 1,
  "name": "Development Board",
  "columns": [
    {
      "id": 101,
      "title": "Backlog",
      "position": 1,
      "tasks": [
        {
          "id": 2001,
          "title": "Refactor Database Connection",
          "description": "Migrate drivers to use mysqlclient pattern natively.",
          "position": 1,
          "due_date": "2026-06-25",
          "assignee": "Ihsan"
        }
      ]
    }
  ]
}

4.2. Endpoint Pembaruan Posisi Tugas

{
  "target_column_id": 102,
  "new_position": 2
}

5. Penanganan State Kosong & Loading
Loading State: Menggunakan kerangka statis (Skeleton Screen) dengan blok-blok berwarna #F5F5F5 yang memudar secara berulang (pulse animation), bukan animasi spinner berputar[cite: 3].

Empty State: Jika kolom kosong, tampilkan teks tipis di tengah kolom: "No tasks in this section" menggunakan warna teks #A3A3A3 disertai border putus-putus tipis di sekeliling area drop[cite: 3].