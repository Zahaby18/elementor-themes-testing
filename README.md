# Agenzy — Digital Agency Elementor Template Kit

Template kit Elementor **free-friendly** untuk website digital agency: clean, simple, fully responsive, dan **tanpa plugin tambahan apa pun** — cukup Elementor Free (gratis). Dibangun dengan **Flexbox Containers** (bukan classic sections) — boxed 1140px, entrance animations, gradient accents, dan hover effects.

![kit](https://img.shields.io/badge/Elementor-Free%20Only-4F46E5) ![widgets](https://img.shields.io/badge/widgets-native%20only-0F172A)

## Isi Kit

| Template | Type | Isi |
|---|---|---|
| `templates/home.json` | Page | Hero, services, about preview, stats, testimonials, FAQ, CTA |
| `templates/about.json` | Page | Story, values, team, CTA |
| `templates/services.json` | Page | 6 services, process, what's included, CTA |
| `templates/portfolio.json` | Page | Galeri proyek, CTA |
| `templates/blog.json` | Page | Hero, artikel cards, CTA |
| `templates/single.json` | Page | Layout single post (demo) |
| `templates/contact.json` | Page | Info cards, detail kontak, peta, CTA |
| `templates/404.json` | Page | Halaman 404 |
| `templates/header-section.json` | Section | Header: logo + CTA |
| `templates/footer-section.json` | Section | Footer 3 kolom + copyright |

> ⚠️ **Status**: Homepage 100% disetujui. About/Services/Portfolio sudah di-review & dirapikan (responsive mobile). Blog/Single/Contact/Header/Footer baru dibuat — menunggu review.
> ℹ️ Single post dinamis butuh Elementor Pro (Theme Builder). `single.json` ini layout demo yang bisa di-insert sebagai halaman.

## Cara Pakai (Import)

1. **Download kit**: clone repo ini atau ambil `kit.zip` (hasil build).
2. **Login WP admin** → menu **Templates → Kit Library** (atau **Templates → Saved Templates → Import Templates**).
3. **Upload `kit.zip`** → Elementor membaca `content/manifest.json` + semua template.
4. Buka halaman baru → edit dengan **Elementor** → klik ikon folder → tab **My Templates** → pilih template → **Insert**.

> 💡 Header/footer template adalah *section*, jadi sisipkan via My Templates ke setiap halaman, atau biarkan theme-mu yang handle header/footer (direkomendasikan: theme ringan seperti **Hello** atau **GeneratePress**).

## Spesifikasi

- **Widget**: 100% widget native Elementor Free (heading, text-editor, button, image, icon-box, icon-list, testimonial, counter, accordion, divider, spacer, social-icons, html, dll). **Tanpa** widget Pro, tanpa third-party addon — *kecuali Single Post, Header, Footer, dan Blog grid*.
- **Struktur**: **Flexbox Containers** (`elType: container`) — nggak perlu convert manual dari section. Boxed 1140px seperti Bootstrap.
- **Efek**: entrance animations (fadeInUp staggered), hover animation (grow), gradient backgrounds (hero & CTA), box shadow cards.
- **Font**: Inter (Google Font, auto-load oleh Elementor).
- **Palette**: slate + indigo aksen. Semua warna & font bisa diganti lewat editor.

## ⚠️ Plugin yang Dibutuhkan (gratis)

Kit ini pakai **Elementor Free** + 3 plugin gratis untuk fitur dinamis:

| Plugin | Buat apa |
|---|---|
| **Jeg Elementor Kit** (free) | Blog grid (`jkit_post_block`), single post (`jkit_post_title`/`jkit_post_featured_image`/`jkit_post_content`), nav menu (`jkit_nav_menu`) |
| **Elementor – Header, Footer & Blocks** (free) | Header/footer global |
| **MetForm** (free) | Form kontak |

**Cara pakai:**
1. Install & aktifkan **Jeg Elementor Kit** (wajib untuk Blog & Single Post dinamis)
2. Import kit seperti biasa
3. Untuk menu header, pilih menu di setting widget `jkit_nav_menu`
- **Responsive**: mobile-first — padding, typography, dan grid sudah di-set untuk tablet & mobile.
- **Gambar**: demo images disimpan di `assets/img/` (di-host via **jsDelivr CDN** agar stabil & cepat dari server mana pun). Ganti dengan aset milikmu di editor. *Tips: saat import, matikan opsi "Import Images" agar Media Library nggak penuh placeholder/duplikat — gambar demo bakal tetap kebaca dari URL.*
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
