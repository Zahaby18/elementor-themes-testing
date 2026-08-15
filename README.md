# Agenzy — Digital Agency Elementor Template Kit

Template kit Elementor **free-friendly** untuk website digital agency: clean, simple, fully responsive, dan **tanpa plugin tambahan apa pun** — cukup Elementor Free (gratis).

![kit](https://img.shields.io/badge/Elementor-Free%20Only-4F46E5) ![widgets](https://img.shields.io/badge/widgets-native%20only-0F172A)

## Isi Kit

| Template | Type | Isi |
|---|---|---|
| `templates/header-section.json` | Section | Header simple: logo + CTA button |
| `templates/footer-section.json` | Section | Footer 3 kolom + social icons + copyright |
| `templates/home.json` | Page | Hero, services, about preview, stats, testimonials, FAQ, CTA |
| `templates/about.json` | Page | Story, values, team, CTA |
| `templates/services.json` | Page | 6 services, process 4 langkah, what's included |
| `templates/portfolio.json` | Page | Gallery grid 2 baris + CTA |
| `templates/blog.json` | Page | Blog cards statis + newsletter band |
| `templates/contact.json` | Page | Info cards, detail kontak, peta (OpenStreetMap) |
| `templates/404.json` | Page | Halaman 404 |

## Cara Pakai (Import)

1. **Download kit**: clone repo ini atau ambil `kit.zip` (hasil build).
2. **Login WP admin** → menu **Templates → Kit Library** (atau **Templates → Saved Templates → Import Templates**).
3. **Upload `kit.zip`** → Elementor membaca `content/manifest.json` + semua template.
4. Buka halaman baru → edit dengan **Elementor** → klik ikon folder → tab **My Templates** → pilih template → **Insert**.

> 💡 Header/footer template adalah *section*, jadi sisipkan via My Templates ke setiap halaman, atau biarkan theme-mu yang handle header/footer (direkomendasikan: theme ringan seperti **Hello** atau **GeneratePress**).

## Spesifikasi

- **Widget**: 100% widget native Elementor Free (heading, text-editor, button, image, icon-box, icon-list, testimonial, counter, accordion, divider, spacer, social-icons, image-gallery, html, dll). **Tanpa** widget Pro, tanpa third-party addon.
- **Font**: Inter (Google Font, auto-load oleh Elementor).
- **Palette**: slate + indigo aksen. Semua warna & font bisa diganti lewat editor.
- **Responsive**: mobile-first — padding, typography, dan grid sudah di-set untuk tablet & mobile.
- **Gambar**: placeholder dari Unsplash. Ganti dengan aset milikmu di editor.
- **Form kontak**: kit tidak menyertakan form (widget Form = Pro). Gunakan **Shortcode widget** + plugin form gratis (WPForms Lite / Contact Form 7).

## Struktur Repo

```
├── build.py              # Generator template (Python, tanpa dependency)
├── build.sh              # Rebuild JSON + zip → kit.zip
├── content/
│   └── manifest.json     # Metadata kit (dibaca Elementor saat import)
├── templates/            # Template JSON (dibaca Elementor saat import)
│   ├── home.json
│   ├── about.json
│   ├── services.json
│   ├── portfolio.json
│   ├── blog.json
│   ├── contact.json
│   ├── 404.json
│   ├── header-section.json
│   └── footer-section.json
└── kit.zip               # Hasil build — file yang di-upload ke Elementor
```

## Rebuild

Ubah `build.py` (palet, font, konten) lalu:

```bash
./build.sh
```

Menghasilkan `kit.zip` fresh di root repo.

---

© 2026 — Agenzy Template Kit. Untuk penggunaan komersial, ganti semua konten placeholder (nama, kontak, foto) dengan aset milikmu.
