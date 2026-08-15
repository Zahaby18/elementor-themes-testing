#!/usr/bin/env python3
"""
Agenzy — Digital Agency Elementor Template Kit generator.
Builds templates/*.json + content/manifest.json (Elementor Free-friendly).
Run: python3 build.py  (then zip with build.sh)
"""
import json, os, random, string

# ---------------------------------------------------------------- design tokens
INK    = "#0F172A"   # slate-900
BODY   = "#475569"   # slate-600
MUTED  = "#64748B"   # slate-500
ACCENT = "#4F46E5"   # indigo-600
ACCENT2= "#4338CA"   # indigo-700
LIGHT  = "#F8FAFC"   # slate-50
BORDER = "#E2E8F0"   # slate-200
WHITE  = "#FFFFFF"
FONT   = "Inter"

RAW = "https://cdn.jsdelivr.net/gh/Zahaby18/elementor-themes-testing@main/assets/img/"

U = {
    "team":     RAW + "img11.jpg",
    "office":   RAW + "img10.jpg",
    "meeting":  RAW + "img01.jpg",
    "laptop":   RAW + "img17.jpg",
    "planning": RAW + "img16.jpg",
    "collab":   RAW + "img12.jpg",
    "workshop": RAW + "img02.jpg",
    "p1": RAW + "img03.jpg",
    "p2": RAW + "img04.jpg",
    "p3": RAW + "img05.jpg",
    "p4": RAW + "img06.jpg",
    "w1": RAW + "img07.jpg",
    "w2": RAW + "img08.jpg",
    "w3": RAW + "img14.jpg",
    "w4": RAW + "img15.jpg",
    "w5": RAW + "img13.jpg",
    "w6": RAW + "img09.jpg",
}

# ---------------------------------------------------------------- helpers
def eid():
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(7))

def dim(top, right, bottom, left, linked=False):
    return {"unit": "px", "top": str(top), "right": str(right),
            "bottom": str(bottom), "left": str(left), "isLinked": linked}

def size(px, unit="px"):
    return {"unit": unit, "size": px, "sizes": []}

def shadow(y=24, blur=48, spread=-12, color="rgba(15,23,42,0.12)"):
    return {"horizontal": 0, "vertical": y, "blur": blur, "spread": spread, "color": color}

def typo(size_px, weight="400", line=1.6, family=FONT):
    return {
        "typography_typography": "custom",
        "typography_font_family": family,
        "typography_font_size": size(size_px),
        "typography_font_weight": weight,
        "typography_line_height": {"unit": "em", "size": line, "sizes": []},
        "typography_text_transform": "",
        "typography_font_style": "normal",
        "typography_letter_spacing": {"unit": "px", "size": 0, "sizes": []},
        "typography_word_spacing": {"unit": "px", "size": 0, "sizes": []},
    }

def widget(wtype, settings, elements=None):
    w = {"id": eid(), "elType": "widget", "widgetType": wtype, "settings": settings}
    if elements:
        w["elements"] = elements
    return w

# ---------------------------------------------------------------- element builders
def flex_gap(px, tablet=20, mobile=16):
    g = {"unit": "px", "column": px, "row": px, "sizes": [], "isLinked": True}
    return {"gap": g, "gap_tablet": {"unit": "px", "column": tablet, "row": tablet, "sizes": [], "isLinked": True},
            "gap_mobile": {"unit": "px", "column": mobile, "row": mobile, "sizes": [], "isLinked": True}}

def container(elements, settings=None, bg=None, gradient=None, pad_top=100, pad_bottom=100, anchor=None,
              overlay=None, radius=None, shadow_=None, anim=None, anim_delay=0, pad_mobile=None):
    """Elementor Flexbox Container (boxed 1140px)."""
    s = {
        "container_type": "flex",
        "content_width": "boxed",
        "boxed_width": {"unit": "px", "size": 1140, "sizes": []},
        "flex_direction": "row",
        "flex_direction_tablet": "row",
        "flex_direction_mobile": "column",
        "flex_wrap": "nowrap",
        "flex_wrap_tablet": "nowrap",
        "flex_justify_content": "flex-start",
        "flex_align_items": "stretch",
        "padding": dim(pad_top, 20, pad_bottom, 20, False),
        "padding_tablet": dim(70, 20, 70, 20, False),
        "padding_mobile": dim(*(pad_mobile if pad_mobile else (50, 16, 50, 16)), False),
        **flex_gap(24, 20, 16),
    }
    if bg:
        s.update({"background_background": "classic", "background_color": bg})
    if gradient:
        s.update({
            "background_background": "gradient",
            "background_color": gradient[0],
            "background_color_b": gradient[1],
            "background_gradient_type": "linear",
            "background_gradient_angle": {"unit": "deg", "size": gradient[2] if len(gradient) > 2 else 135, "sizes": []},
        })
    if overlay:
        s.update(overlay)
    if anchor:
        s["_element_id"] = anchor
    if radius:
        s["border_radius"] = dim(radius, radius, radius, radius, True)
    if shadow_:
        s["box_shadow_box_shadow_type"] = "yes"
        s["box_shadow_box_shadow"] = shadow_
    if anim:
        s["_animation"] = anim
        if anim_delay:
            s["_animation_delay"] = {"unit": "px", "size": anim_delay, "sizes": []}
    if settings:
        s.update(settings)
    return {"id": eid(), "elType": "container", "settings": s, "elements": elements, "isInner": False}

# Backwards-compatible alias: template code calls section(...)
section = container

def dark_hero_bg(img_url, opacity=0.88):
    """Photo + navy→indigo gradient overlay."""
    return {
        "background_background": "classic",
        "background_image": {"url": img_url, "id": 0, "alt": ""},
        "background_position": "center center",
        "background_size": "cover",
        "background_repeat": "no-repeat",
        "background_overlay_background": "gradient",
        "background_overlay_color": "#0F172A",
        "background_overlay_color_b": "#1E1B4B",
        "background_overlay_gradient_type": "linear",
        "background_overlay_gradient_angle": {"unit": "deg", "size": 135, "sizes": []},
        "background_overlay_opacity": {"unit": "px", "size": opacity, "sizes": []},
    }

def col(elements, width=50, settings=None, center=False, anim=None, anim_delay=0):
    """Inner Flexbox Container (was column). Column direction."""
    s = {
        "container_type": "flex",
        "content_width": "full",
        "width": {"unit": "%", "size": width, "sizes": []},
        "width_tablet": {"unit": "%", "size": 100, "sizes": []},
        "width_mobile": {"unit": "%", "size": 100, "sizes": []},
        "flex_direction": "column",
        "flex_direction_tablet": "column",
        "flex_direction_mobile": "column",
        "flex_wrap": "wrap",
        "flex_justify_content": "center" if center else "flex-start",
        "flex_align_items": "stretch",
        **flex_gap(16, 14, 12),
    }
    if anim:
        s["_animation"] = anim
        if anim_delay:
            s["_animation_delay"] = {"unit": "px", "size": anim_delay, "sizes": []}
    if settings:
        s.update(settings)
    return {"id": eid(), "elType": "container", "settings": s, "elements": elements, "isInner": True}

# Card design (curamedica-style): indigo glow shadow + hover lift
CARD_SHADOW = {"horizontal": 0, "vertical": 12, "blur": 32, "spread": -12, "color": "rgba(79,70,229,0.16)"}
CARD_HOVER = {
    "box_shadow_hover_box_shadow_type": "yes",
    "box_shadow_hover_box_shadow": {"horizontal": 0, "vertical": 18, "blur": 44, "spread": -8, "color": "rgba(79,70,229,0.28)"},
    "_transform_translate_popover_hover": "transform",
    "_transform_translateY_effect_hover": {"unit": "px", "size": -10, "sizes": []},
}

def card_col(widgets, bg=WHITE, radius=20, anim=None, anim_delay=0):
    """Card = inner container with bg, border, radius + indigo glow shadow + hover lift."""
    s = {
        "background_background": "classic",
        "background_color": bg,
        "border_border": "solid",
        "border_width": dim(1, 1, 1, 1, True),
        "border_color": "#E8EDF4",
        "border_radius": dim(radius, radius, radius, radius, True),
        "box_shadow_box_shadow_type": "yes",
        "box_shadow_box_shadow": CARD_SHADOW,
        "padding": dim(34, 28, 34, 28, False),
        **CARD_HOVER,
    }
    return col(widgets, 33.3333, settings=s, anim=anim, anim_delay=anim_delay)

def btn_row(buttons):
    """Buttons side by side — directly in a flex row container (matching Elementor 4.x structure)."""
    inner = {"id": eid(), "elType": "container", "isInner": True,
             "settings": {"container_type": "flex", "content_width": "full",
                          "flex_direction": "row", "flex_direction_tablet": "row",
                          "flex_direction_mobile": "column", "flex_wrap": "nowrap",
                          "flex_justify_content": "flex-start", "flex_align_items": "center",
                          **flex_gap(12, 12, 10)}, "elements": buttons}
    return inner

def sec_head(eyebrow_, title_, sub_=None, align="center"):
    els = [eyebrow(eyebrow_)]
    els.append(heading(title_, "h2", INK, align, 38, "700", 1.25, tablet=30, mobile=26,
                       extra={"_animation": "fadeInUp"}))
    if sub_:
        els.append(text(f"<p>{sub_}</p>", BODY, align, 17, "400", 1.7,
                        extra={"_animation": "fadeInUp", "_animation_delay": {"unit": "px", "size": 100, "sizes": []}}))
    return els

def heading(text_, tag="h2", color=INK, align="left", px=40, weight="700", line=1.2, tablet=None, mobile=None, extra=None):
    s = {"title": text_, "header_size": tag, "align": align, "title_color": color, **typo(px, weight, line)}
    if tablet:
        s["typography_font_size_tablet"] = size(tablet)
    if mobile:
        s["typography_font_size_mobile"] = size(mobile)
    if extra:
        s.update(extra)
    return widget("heading", s)

def eyebrow(text_, align="center"):
    return heading(text_, "h5", ACCENT, align, 14, "700", 1.2,
                   extra={"typography_text_transform": "uppercase",
                          "typography_letter_spacing": {"unit": "px", "size": 2.5, "sizes": []}})

def text(html, color=BODY, align="left", px=17, weight="400", line=1.7, extra=None):
    s = {"editor": html, "text_color": color, "align": align, **typo(px, weight, line)}
    if extra:
        s.update(extra)
    return widget("text-editor", s)

def btn(text_, url="#", align="left", bg=ACCENT, fg=WHITE, hover_bg=ACCENT2, pt=16, pl=32, radius=8, extra=None):
    s = {
        "text": text_,
        "link": {"url": url, "is_external": "", "nofollow": "", "custom_attributes": ""},
        "align": align,
        "size": "sm",
        "background_color": bg,
        "button_text_color": fg,
        "hover_color": fg,
        "button_background_hover_color": hover_bg,
        "border_radius": dim(radius, radius, radius, radius, True),
        "text_padding": dim(pt, pl, pt, pl, False),
        "align_mobile": "justify",
        "_element_width_mobile": "inherit",
        **typo(16, "600", 1),
    }
    if extra:
        s.update(extra)
    return widget("button", s)

def ghost_btn(text_, url="#", align="left", fg=WHITE, border="#334155"):
    return btn(text_, url, align, "rgba(255,255,255,0)", fg, "rgba(79,70,229,0.12)",
               extra={"border_border": "solid", "border_width": dim(1, 1, 1, 1, True), "border_color": border,
                      "button_background_hover_color": "rgba(255,255,255,0.08)", "hover_color": WHITE})

def icon_box(icon, title_, desc_, link=None, icon_color=ACCENT, position="top", align="center", anim=None, anim_delay=0):
    s = {
        "selected_icon": {"value": icon, "library": "fa-solid"},
        "title_text": title_,
        "description_text": desc_,
        "position": position,
        "view": "stacked",
        "primary_color": icon_color,
        "secondary_color": "#FFFFFF",
        "hover_primary_color": ACCENT2,
        "icon_size": size(28),
        "title_color": INK,
        "description_color": BODY,
        "title_typography_typography": "custom",
        "title_typography_font_family": FONT,
        "title_typography_font_size": size(20),
        "title_typography_font_weight": "700",
        "title_typography_line_height": {"unit": "em", "size": 1.3, "sizes": []},
        "description_typography_typography": "custom",
        "description_typography_font_family": FONT,
        "description_typography_font_size": size(15),
        "description_typography_font_weight": "400",
        "description_typography_line_height": {"unit": "em", "size": 1.65, "sizes": []},
    }
    if anim:
        s["_animation"] = anim
        if anim_delay:
            s["_animation_delay"] = {"unit": "px", "size": anim_delay, "sizes": []}
    if link:
        s["link"] = {"url": link, "is_external": "", "nofollow": "", "custom_attributes": ""}
    return widget("icon-box", s)

def icon_list(items, icon="fas fa-check", icon_color=ACCENT, text_color=BODY, px=16):
    lst = [{"_id": eid(), "text": t, "selected_icon": {"value": icon, "library": "fa-solid"},
            "link": {"url": "", "is_external": "", "nofollow": "", "custom_attributes": ""}} for t in items]
    return widget("icon-list", {
        "icon_list": lst,
        "space_between": {"unit": "px", "size": 12, "sizes": []},
        "icon_color": icon_color,
        "text_color": text_color,
        "text_indent": {"unit": "px", "size": 10, "sizes": []},
        "text_typography_typography": "custom",
        "text_typography_font_family": FONT,
        "text_typography_font_size": size(px),
        "text_typography_font_weight": "500",
    })

def testimonial(content_, name_, job_, img=None, anim=None, anim_delay=0):
    s = {
        "testimonial_content": content_,
        "testimonial_name": name_,
        "testimonial_job": job_,
        "testimonial_alignment": "center",
        "testimonial_content_color": BODY,
        "testimonial_name_color": INK,
        "testimonial_job_color": MUTED,
        "testimonial_content_typography_typography": "custom",
        "testimonial_content_typography_font_family": FONT,
        "testimonial_content_typography_font_size": size(15),
        "testimonial_content_typography_line_height": {"unit": "em", "size": 1.7, "sizes": []},
        "testimonial_name_typography_typography": "custom",
        "testimonial_name_typography_font_family": FONT,
        "testimonial_name_typography_font_size": size(16),
        "testimonial_name_typography_font_weight": "600",
        "testimonial_job_typography_typography": "custom",
        "testimonial_job_typography_font_family": FONT,
        "testimonial_job_typography_font_size": size(14),
    }
    if img:
        s["testimonial_image"] = img
    if anim:
        s["_animation"] = anim
        if anim_delay:
            s["_animation_delay"] = {"unit": "px", "size": anim_delay, "sizes": []}
    return widget("testimonial", s)

def icon_widget(icon, color="#E2E8F0", px=28, align="left"):
    return widget("icon", {
        "selected_icon": {"value": icon, "library": "fa-solid"},
        "view": "default",
        "primary_color": color,
        "size": size(px),
        "align": align,
    })

def inner_row(children, justify="flex-start", align="center", gap=12):
    """Generic inner flex row container."""
    return {"id": eid(), "elType": "container", "isInner": True,
            "settings": {"container_type": "flex", "content_width": "full",
                         "flex_direction": "row", "flex_direction_tablet": "row",
                         "flex_direction_mobile": "row", "flex_wrap": "nowrap",
                         "flex_justify_content": justify, "flex_align_items": align,
                         **flex_gap(gap, gap, gap)}, "elements": children}

def testimonial_card(content_, name_, job_, avatar, anim=None, anim_delay=0, width_tablet=100):
    """Testimonial as a custom card: quote icon, italic quote, right-aligned person."""
    card_settings = {
        "background_background": "classic",
        "background_color": WHITE,
        "border_border": "solid",
        "border_width": dim(1, 1, 1, 1, True),
        "border_color": "#E8EDF4",
        "border_radius": dim(16, 16, 16, 16, True),
        "box_shadow_box_shadow_type": "yes",
        "box_shadow_box_shadow": shadow(12, 28, 0, "rgba(15,23,42,0.12)"),
        "padding": dim(34, 28, 34, 28, False),
        "width_tablet": {"unit": "%", "size": width_tablet, "sizes": []},
    }
    person = inner_row([
        col([img(avatar, name_, 100, 50)], 44),
        col([heading(name_, "h5", INK, "left", 16, "600", 1.3),
             text(f"<p>{job_}</p>", MUTED, "left", 13, "400", 1.5)], 60),
    ], justify="flex-end", align="center", gap=12)
    qextra = {}
    if anim:
        qextra["_animation"] = anim
        if anim_delay:
            qextra["_animation_delay"] = {"unit": "px", "size": anim_delay, "sizes": []}
    els = [
        icon_widget("fas fa-quote-left", "#E2E8F0", 28, "left"),
        text(f"<p><em>{content_}</em></p>", BODY, "left", 15, "400", 1.75, extra=qextra),
        person,
    ]
    return col(els, 33.3333, settings=card_settings)

def accordion(items, anim=None, anim_delay=0):
    tabs = [{"_id": eid(), "tab_title": t, "tab_content": f"<p>{c}</p>"} for t, c in items]
    s = {
        "tabs": tabs,
        "title_color": INK,
        "tab_active_color": ACCENT,
        "title_typography_typography": "custom",
        "title_typography_font_family": FONT,
        "title_typography_font_size": size(16),
        "title_typography_font_weight": "600",
        "content_color": BODY,
        "content_typography_typography": "custom",
        "content_typography_font_family": FONT,
        "content_typography_font_size": size(15),
        "content_typography_line_height": {"unit": "em", "size": 1.7, "sizes": []},
        "border_color": BORDER,
        "border_width": {"unit": "px", "size": 1, "sizes": []},
        "border_radius": dim(10, 10, 10, 10, True),
        "title_background": WHITE,
        "tab_active_background": WHITE,
        "content_background_color": WHITE,
    }
    if anim:
        s["_animation"] = anim
        if anim_delay:
            s["_animation_delay"] = {"unit": "px", "size": anim_delay, "sizes": []}
    return widget("accordion", s)

def faq_accordion(items, anim=None):
    """Elementor 4.x Nested Accordion with curamedica styling (radius 30, border #ECECEC, +/- icon, one-open)."""
    item_settings = [{"item_title": q, "_id": eid(), "element_css_id": ""} for q, a in items]
    children = []
    for q, a in items:
        child = {"id": eid(), "elType": "container", "isInner": True,
                 "settings": {"content_width": "full", "container_type": "flex",
                              "flex_direction": "column", "flex_wrap": "nowrap"},
                 "elements": [text(f"<p>{a}</p>", BODY, "left", 15, "400", 1.6)]}
        children.append(child)
    s = {
        "items": item_settings,
        "accordion_item_title_position_horizontal": "stretch",
        "accordion_item_title_icon_position": "end",
        "accordion_item_title_space_between": {"unit": "px", "size": 10, "sizes": []},
        "accordion_border_normal_border": "solid",
        "accordion_border_normal_width": {"unit": "px", "top": "1", "right": "1", "bottom": "1", "left": "1", "isLinked": False},
        "accordion_border_normal_color": "#ECECEC",
        "accordion_border_radius": dim(30, 30, 30, 30, True),
        "accordion_padding": dim(20, 20, 20, 20, True),
        "accordion_background_normal_background": "classic",
        "accordion_background_normal_color": "#FFFFFF",
        "normal_title_color": INK,
        "title_typography_typography": "custom",
        "title_typography_font_family": FONT,
        "title_typography_font_size": size(16),
        "title_typography_font_weight": "700",
        "title_tag": "div",
        "accordion_item_title_icon": {"value": "fas fa-plus", "library": "fa-solid"},
        "accordion_item_title_icon_active": {"value": "fas fa-minus", "library": "fa-solid"},
        "icon_size": size(15),
        "default_state": "expanded",
        "max_items_expended": "one",
        "n_accordion_animation_duration": {"unit": "ms", "size": 400, "sizes": []},
        "content_border_border": "none",
        "content_border_width": {"unit": "px", "top": "0", "right": "1", "bottom": "1", "left": "1", "isLinked": False},
        "content_padding": dim(20, 20, 20, 20, True),
        "content_background_color": "#FFFFFF",
        "content_typography_typography": "custom",
        "content_typography_font_family": FONT,
        "content_typography_font_size": size(15),
        "content_typography_line_height": {"unit": "em", "size": 1.6, "sizes": []},
    }
    if anim:
        s["_animation"] = anim
    return widget("nested-accordion", s, elements=children)

def img(url, alt="", width=100, radius=12, shadow_=None, align="center", anim=None, anim_delay=0):
    s = {
        "image": {"url": url, "id": 0, "alt": alt},
        "image_size": "full",
        "align": align,
        "width": {"unit": "%", "size": width, "sizes": []},
        "image_border_radius": dim(radius, radius, radius, radius, True),
    }
    if anim:
        s["_animation"] = anim
        if anim_delay:
            s["_animation_delay"] = {"unit": "px", "size": anim_delay, "sizes": []}
    if shadow_:
        s["box_shadow_box_shadow_type"] = "yes"
        s["box_shadow_box_shadow"] = shadow_
    return widget("image", s)

def image_box(url, title_, desc_, link="#", anim=None, anim_delay=0):
    s = {
        "image": {"url": url, "id": 0, "alt": ""},
        "title_text": title_,
        "description_text": desc_,
        "link": {"url": link, "is_external": "", "nofollow": "", "custom_attributes": ""},
        "position": "top",
        "image_border_radius": dim(20, 20, 0, 0, True),
        "title_color": INK,
        "description_color": BODY,
        "title_typography_typography": "custom",
        "title_typography_font_family": FONT,
        "title_typography_font_size": size(18),
        "title_typography_font_weight": "700",
        "description_typography_typography": "custom",
        "description_typography_font_family": FONT,
        "description_typography_font_size": size(15),
        "description_typography_line_height": {"unit": "em", "size": 1.65, "sizes": []},
        "content_padding": dim(24, 24, 24, 24, False),
        "background_background": "classic",
        "background_color": WHITE,
        "border_border": "solid",
        "border_width": dim(1, 1, 1, 1, True),
        "border_color": "#E8EDF4",
        "border_radius": dim(20, 20, 20, 20, True),
        "box_shadow_box_shadow_type": "yes",
        "box_shadow_box_shadow": CARD_SHADOW,
        "box_shadow_hover_box_shadow_type": "yes",
        "box_shadow_hover_box_shadow": {"horizontal": 0, "vertical": 18, "blur": 44, "spread": -8, "color": "rgba(79,70,229,0.28)"},
        "_transform_translate_popover_hover": "transform",
        "_transform_translateY_effect_hover": {"unit": "px", "size": -10, "sizes": []},
    }
    if anim:
        s["_animation"] = anim
        if anim_delay:
            s["_animation_delay"] = {"unit": "px", "size": anim_delay, "sizes": []}
    return widget("image-box", s)

def counter(n, suffix, title_, dark=True, anim=None, anim_delay=0):
    s = {
        "starting_number": 0,
        "ending_number": n,
        "suffix": suffix,
        "title": title_,
        "number_color": "#A5B4FC" if dark else ACCENT,
        "title_color": "#CBD5E1" if dark else BODY,
        "number_typography_typography": "custom",
        "number_typography_font_family": FONT,
        "number_typography_font_size": size(46),
        "number_typography_font_weight": "700",
        "title_typography_typography": "custom",
        "title_typography_font_family": FONT,
        "title_typography_font_size": size(15),
        "title_typography_font_weight": "500",
    }
    if anim:
        s["_animation"] = anim
        if anim_delay:
            s["_animation_delay"] = {"unit": "px", "size": anim_delay, "sizes": []}
    return widget("counter", s)

def social_icons(icons=None, bg="rgba(255,255,255,0.10)", color=WHITE, px=15):
    icons = icons or [
        ("fab fa-facebook-f", "#"),
        ("fab fa-twitter", "#"),
        ("fab fa-instagram", "#"),
        ("fab fa-linkedin-in", "#"),
    ]
    lst = [{"_id": eid(), "social_icon": {"value": i, "library": "fa-brands"},
            "link": {"url": u, "is_external": "", "nofollow": "", "custom_attributes": ""}} for i, u in icons]
    return widget("social-icons", {
        "social_icon_list": lst,
        "shape": "circle",
        "background_color": bg,
        "background_hover_color": ACCENT,
        "icon_color": color,
        "icon_hover_color": WHITE,
        "icon_size": size(px),
        "space_between": {"unit": "px", "size": 8, "sizes": []},
        "align": "left",
    })

def divider(color=BORDER, width_pct=100, weight=1):
    return widget("divider", {
        "color": color,
        "weight": {"unit": "px", "size": weight, "sizes": []},
        "width": {"unit": "%", "size": width_pct, "sizes": []},
        "gap": {"unit": "px", "size": 15, "sizes": []},
    })

def spacer(px, mobile=None):
    s = {"space": {"unit": "px", "size": px, "sizes": []}}
    if mobile:
        s["space_mobile"] = {"unit": "px", "size": mobile, "sizes": []}
    return widget("spacer", s)

def gallery(urls, cols=3):
    items = [{"id": i + 1, "url": u, "alt": ""} for i, u in enumerate(urls)]
    return widget("image-gallery", {
        "wp_gallery": items,
        "gallery_columns": cols,
        "image_size": "large",
        "gallery_link": "file",
        "overlay_background_color": "rgba(79,70,229,0.55)",
        "image_border_radius": dim(10, 10, 10, 10, True),
        "gallery_columns_tablet": 2,
        "gallery_columns_mobile": 1,
    })

def osm_map():
    return widget("html", {
        "html": '<iframe src="https://www.openstreetmap.org/export/embed.html?bbox=106.7700%2C-6.2400%2C106.9200%2C-6.1600&amp;layer=mapnik&amp;marker=-6.2088%2C106.8456" '
                'style="border:0;width:100%;height:420px;border-radius:16px;" loading="lazy"></iframe>'
    })

def page(title, elements, ptype="page"):
    return {"content": elements, "page_settings": [], "version": "0.4", "title": title, "type": ptype}

def tb_page(title, elements):
    """Royal Elementor Addons Theme Builder template (type wpr-theme-builder, supports kit import)."""
    return {"content": elements, "page_settings": [], "version": "0.4", "title": title, "type": "wpr-theme-builder"}

def cta_box(heading_text, sub_text, btn_text, colors=("#4F46E5", "#7C3AED"), btn_url="#contact", pad_mobile=None):
    """Rounded gradient CTA box (inner container, matches homepage design)."""
    box = {"id": eid(), "elType": "container", "isInner": True,
           "settings": {
               "container_type": "flex", "content_width": "full",
               "flex_direction": "column", "flex_direction_tablet": "column",
               "flex_direction_mobile": "column", "flex_wrap": "nowrap",
               "flex_justify_content": "center", "flex_align_items": "center",
               "background_background": "gradient",
               "background_color": colors[0], "background_color_b": colors[1],
               "background_gradient_type": "linear",
               "background_gradient_angle": {"unit": "deg", "size": 135, "sizes": []},
               "border_radius": dim(24, 24, 24, 24, True),
               "padding": dim(80, 40, 80, 40, False),
               "padding_tablet": dim(60, 30, 60, 30, False),
               "padding_mobile": dim(50, 24, 50, 24, False),
               **flex_gap(16, 14, 12),
           },
           "elements": [
               heading(heading_text, "h2", WHITE, "center", 34, "700", 1.25, tablet=28, mobile=24,
                       extra={"_animation": "fadeInUp"}),
               text(f"<p style='text-align:center;'>{sub_text}</p>", "#CBD5E1", "center", 17, "400", 1.7,
                    extra={"_animation": "fadeInUp", "_animation_delay": {"unit": "px", "size": 100, "sizes": []}}),
               btn(btn_text, btn_url, "center", WHITE, INK, "#E2E8F0", pt=16, pl=36,
                   extra={"_animation": "fadeInUp", "_animation_delay": {"unit": "px", "size": 200, "sizes": []}}),
           ]}
    return container([box], pad_top=90, pad_bottom=90, pad_mobile=pad_mobile)

# ---------------------------------------------------------------- templates
def home():
    els = []
    # HERO
    els.append(section([
        col([
            heading("We Build Digital Products That Grow Your Business", "h1", WHITE, "left", 52, "800", 1.15,
                    tablet=40, mobile=32, extra={"_animation": "fadeInLeft"}),
            text("<p>Agenzy is a full-service digital agency helping startups and brands design, build, and scale products people love — from strategy to launch and beyond.</p>",
                 "#CBD5E1", "left", 18, "400", 1.7,
                 extra={"_animation": "fadeInLeft", "_animation_delay": {"unit": "px", "size": 120, "sizes": []}}),
            btn_row([btn("Explore Services", "#services", "left"), ghost_btn("Start a Project", "#contact", "left")]),
        ], 55, center=True),
        col([img(U["office"], "Agenzy team at work", 100, 16, shadow(30, 60, -15, "rgba(0,0,0,0.45)"), anim="fadeIn", anim_delay=200)], 45, center=True),
    ], bg=None, pad_top=120, pad_bottom=120, overlay=dark_hero_bg(U["team"], 0.9)))

    # TRUST BAR
    els.append(section([
        col([text("<p style='text-align:center;'>Trusted by 50+ startups and growing teams — from Jakarta to Singapore</p>",
                  MUTED, "center", 15, "500", 1.5)], 100)
    ], bg=LIGHT, pad_top=28, pad_bottom=28, pad_mobile=(10, 16, 10, 16)))

    # SERVICES (3 sections = 3 rows: heading, row 1, row 2)
    services = [
        ("fas fa-bullseye", "Digital Strategy", "Market research, positioning, and roadmaps that turn your business goals into a clear plan of action."),
        ("fas fa-pencil-ruler", "UI/UX Design", "Research-driven interfaces that look sharp and convert — web, mobile, and product design."),
        ("fas fa-code", "Web Development", "Fast, secure, and scalable websites and web apps built with modern technology."),
        ("fas fa-chart-line", "SEO & Growth", "Technical SEO, content strategy, and performance marketing that compound over time."),
        ("fas fa-palette", "Brand Identity", "Logos, guidelines, and visual systems that make your brand impossible to ignore."),
        ("fas fa-hashtag", "Content & Social", "Editorial and social content that builds authority and keeps your audience engaged."),
    ]
    srv_widgets = [icon_box(i, t, d, link="#services", anim="fadeInUp", anim_delay=(idx % 3) * 100) for idx, (i, t, d) in enumerate(services)]
    els.append(section([
        col(sec_head("What We Do", "Services built to move the needle", "From first idea to ongoing growth — everything your digital presence needs under one roof."), 100),
    ], bg=WHITE, pad_top=100, pad_bottom=30, anchor="services", pad_mobile=(50, 16, 0, 16)))
    els.append(section([
        card_col([srv_widgets[0]]),
        card_col([srv_widgets[1]]),
        card_col([srv_widgets[2]]),
    ], bg=WHITE, pad_top=0, pad_bottom=30, pad_mobile=(50, 16, 20, 16)))
    els.append(section([
        card_col([srv_widgets[3]]),
        card_col([srv_widgets[4]]),
        card_col([srv_widgets[5]]),
    ], bg=WHITE, pad_top=0, pad_bottom=100, pad_mobile=(0, 16, 50, 16)))

    # ABOUT PREVIEW
    els.append(section([
        col([img(U["collab"], "Our team collaborating", 100, 16, shadow(), anim="fadeIn")], 50, center=True),
        col([
            eyebrow("About Us", "left"), spacer(12, 8),
            heading("A team that treats your product like our own", "h2", INK, "left", 36, "700", 1.25, tablet=28, mobile=24,
                    extra={"_animation": "fadeInLeft"}),
            text("<p>We're a compact team of strategists, designers, and engineers. No account managers in between — you talk directly to the people building your product.</p>",
                 extra={"_animation": "fadeInLeft", "_animation_delay": {"unit": "px", "size": 120, "sizes": []}}),
            icon_list(["Senior talent on every project", "Transparent pricing, no surprises", "Launch in weeks, not months"]),
            btn("More About Us", "#about", "left"),
        ], 50, center=True),
    ], bg=LIGHT, pad_top=100, pad_bottom=100))

    # STATS
    els.append(section([
        col([counter(120, "+", "Projects Delivered", anim="fadeInUp", anim_delay=0)], 25),
        col([counter(85, "+", "Happy Clients", anim="fadeInUp", anim_delay=100)], 25),
        col([counter(6, "+", "Years Experience", anim="fadeInUp", anim_delay=200)], 25),
        col([counter(15, "+", "Industry Awards", anim="fadeInUp", anim_delay=300)], 25),
    ], gradient=("#0F172A", "#1E1B4B", 135), pad_top=80, pad_bottom=80))
    # TESTIMONIALS (2 sections: heading + row of cards)
    els.append(section([
        col(sec_head("Testimonials", "What our clients say"), 100),
    ], bg=LIGHT, pad_top=100, pad_bottom=30))
    els.append(section([
        testimonial_card("Agenzy rebuilt our platform in eight weeks. Conversion went up 40% and the team actually listened — rare in this industry.",
                         "Rina Amelia", "CEO, Tokokita", U["p1"], anim="fadeInUp", anim_delay=0, width_tablet=48),
        testimonial_card("The best agency we've worked with. Clear communication, on-time delivery, and design that our customers compliment constantly.",
                         "Bima Pratama", "Founder, Nusantara Studio", U["p2"], anim="fadeInUp", anim_delay=100, width_tablet=48),
        testimonial_card("They didn't just build our site — they improved our SEO, cut load time in half, and taught our team to manage it ourselves.",
                         "Sari Wijaya", "Marketing Lead, GreenFood", U["p3"], anim="fadeInUp", anim_delay=200),
    ], bg=LIGHT, pad_top=0, pad_bottom=100, anchor="testimonials",
       settings={"flex_wrap_tablet": "wrap", "flex_justify_content_tablet": "space-between"}))

    # FAQ (2 sections: heading + accordion)
    faq = [
        ("How much does a project cost?", "Every project is scoped individually. Typical website projects start at a fixed package, and we always give you a clear quote before any work begins — no hidden fees."),
        ("How long does it take to launch?", "A landing page can go live in 1–2 weeks. Full websites and web apps typically take 4–8 weeks depending on scope and content readiness."),
        ("Do you work with existing brands?", "Absolutely. We regularly take over existing websites, redesign them, or simply optimize what's already there for speed and conversions."),
        ("What happens after launch?", "We don't disappear. Support, maintenance, and growth retainer options keep your product healthy and improving month after month."),
    ]
    els.append(section([
        col(sec_head("FAQ", "Frequently asked questions", "Quick answers. Anything else — just ask us."), 100),
    ], bg=WHITE, pad_top=100, pad_bottom=30, anchor="faq", pad_mobile=(50, 16, 10, 16)))
    els.append(section([
        col([faq_accordion(faq, anim="fadeInUp")], 80),
    ], bg=WHITE, pad_top=0, pad_bottom=100, settings={"flex_justify_content": "center"}, pad_mobile=(0, 10, 50, 10)))

    # CTA — rounded gradient box (inner container, so radius applies to content box not full width)
    cta_box = {"id": eid(), "elType": "container", "isInner": True,
               "settings": {
                   "container_type": "flex", "content_width": "full",
                   "flex_direction": "column", "flex_direction_tablet": "column",
                   "flex_direction_mobile": "column", "flex_wrap": "nowrap",
                   "flex_justify_content": "center", "flex_align_items": "center",
                   "background_background": "gradient",
                   "background_color": "#4F46E5", "background_color_b": "#7C3AED",
                   "background_gradient_type": "linear",
                   "background_gradient_angle": {"unit": "deg", "size": 135, "sizes": []},
                   "border_radius": dim(24, 24, 24, 24, True),
                   "padding": dim(80, 40, 80, 40, False),
                   "padding_tablet": dim(60, 30, 60, 30, False),
                   "padding_mobile": dim(50, 24, 50, 24, False),
                   **flex_gap(16, 14, 12),
               },
               "elements": [
                   heading("Have a project in mind?", "h2", WHITE, "center", 38, "700", 1.25, tablet=30, mobile=26,
                           extra={"_animation": "fadeInUp"}),
                   text("<p style='text-align:center;'>Let's talk about what we can build together. Free consultation, no strings attached.</p>", "#CBD5E1", "center", 17, "400", 1.7,
                        extra={"_animation": "fadeInUp", "_animation_delay": {"unit": "px", "size": 100, "sizes": []}}),
                   btn("Let's Talk", "#contact", "center", WHITE, INK, "#E2E8F0", pt=16, pl=36,
                       extra={"_animation": "fadeInUp", "_animation_delay": {"unit": "px", "size": 200, "sizes": []}}),
               ]}
    els.append(container([cta_box], pad_top=90, pad_bottom=90, anchor="contact"))

    return page("Home", els)

def about():
    els = []
    # HERO
    els.append(section([
        col([
            heading("About Agenzy", "h1", WHITE, "left", 44, "800", 1.2, tablet=34, mobile=28,
                    extra={"_animation": "fadeInLeft"}),
            text("<p>The people, the process, and the values behind the work.</p>", "#CBD5E1", "left", 18,
                 extra={"_animation": "fadeInLeft", "_animation_delay": {"unit": "px", "size": 120, "sizes": []}}),
        ], 100),
    ], bg=None, pad_top=110, pad_bottom=110, overlay=dark_hero_bg(U["workshop"], 0.85)))

    # STORY
    els.append(section([
        col([img(U["meeting"], "Agenzy team in a meeting", 100, 16, shadow(), anim="fadeIn")], 50, center=True),
        col([
            eyebrow("Our Story", "left"), spacer(12, 8),
            heading("Started with three laptops and a stubborn belief", "h2", INK, "left", 36, "700", 1.25, tablet=28, mobile=24,
                    extra={"_animation": "fadeInLeft"}),
            text("<p>Agenzy began in 2019 when three friends decided freelancing alone wasn't enough — clients deserved a team that could take an idea from whiteboard to world. Today we're a 20-person studio shipping products across three continents.</p>"
                 "<p>We stay deliberately small. Small enough that every project gets senior attention, big enough to deliver on time, every time.</p>",
                 extra={"_animation": "fadeInLeft", "_animation_delay": {"unit": "px", "size": 120, "sizes": []}}),
        ], 50, center=True),
    ], bg=WHITE, pad_top=100, pad_bottom=100))

    # VALUES (heading + row of cards)
    vals = [
        ("fas fa-handshake", "Transparency", "Open pricing, honest timelines, and a shared dashboard so you always know what's happening."),
        ("fas fa-gem", "Quality First", "We'd rather ship one great product than five mediocre ones. Craft is non-negotiable."),
        ("fas fa-lightbulb", "Bold Thinking", "Safe is boring. We bring ideas, not just execution — and we're not afraid to challenge the brief."),
    ]
    val_widgets = [icon_box(i, t, d, anim="fadeInUp", anim_delay=idx * 100) for idx, (i, t, d) in enumerate(vals)]
    els.append(section([
        col(sec_head("Our Values", "What we stand for"), 100),
    ], bg=LIGHT, pad_top=100, pad_bottom=30))
    els.append(section([
        card_col([val_widgets[0]]),
        card_col([val_widgets[1]]),
        card_col([val_widgets[2]]),
    ], bg=LIGHT, pad_top=0, pad_bottom=100, pad_mobile=(0, 16, 50, 16)))

    # TEAM (heading + row)
    team = [
        (U["p1"], "Andi Kurniawan", "Founder & Strategy Director"),
        (U["p2"], "Dewi Lestari", "Head of Design"),
        (U["p3"], "Fajar Ramadhan", "Lead Engineer"),
        (U["p4"], "Nadia Putri", "Growth & SEO Lead"),
    ]
    team_cols = []
    for i, (turl, name_, role) in enumerate(team):
        team_cols.append(col([
            img(turl, name_, 100, 12, anim="fadeIn"),
            heading(name_, "h4", INK, "center", 19, "700", 1.3),
            text(f"<p style='text-align:center;'>{role}</p>", MUTED, "center", 14, "400", 1.5),
        ], 25))
    els.append(section([
        col(sec_head("Meet the Team", "The people behind the pixels"), 100),
    ], bg=WHITE, pad_top=100, pad_bottom=30))
    els.append(section([
        *team_cols,
    ], bg=WHITE, pad_top=0, pad_bottom=100, pad_mobile=(0, 16, 50, 16)))

    # CTA
    els.append(cta_box("Want to join the team?", "We're always looking for sharp people who care about craft. Drop us a line.", "See Open Roles",
                       colors=("#0F172A", "#1E1B4B")))
    return page("About", els)

def services():
    els = []
    # HERO
    els.append(section([
        col([
            heading("Our Services", "h1", WHITE, "left", 44, "800", 1.2, tablet=34, mobile=28,
                    extra={"_animation": "fadeInLeft"}),
            text("<p>Everything your business needs to win online — designed, built, and grown by one team.</p>", "#CBD5E1", "left", 18,
                 extra={"_animation": "fadeInLeft", "_animation_delay": {"unit": "px", "size": 120, "sizes": []}}),
        ], 100),
    ], bg=None, pad_top=110, pad_bottom=110, overlay=dark_hero_bg(U["planning"], 0.85)))

    services = [
        ("fas fa-bullseye", "Digital Strategy", "Positioning, research, and roadmaps that make sure every dollar you spend has a purpose."),
        ("fas fa-pencil-ruler", "UI/UX Design", "Interfaces that balance beauty and usability. Prototyped, tested, and iterated with real users."),
        ("fas fa-code", "Web Development", "Lightning-fast websites and web apps on modern stacks. Clean code, easy to hand over."),
        ("fas fa-chart-line", "SEO & Growth", "Technical audits, content engines, and performance marketing that deliver compounding results."),
        ("fas fa-palette", "Brand Identity", "From logo to full brand guidelines — a visual identity your audience will remember."),
        ("fas fa-hashtag", "Content & Social", "Editorial calendars, writing, and social management that keep your brand consistently loud."),
    ]
    srv_widgets = [icon_box(i, t, d, link="#contact", anim="fadeInUp", anim_delay=(idx % 3) * 100) for idx, (i, t, d) in enumerate(services)]
    els.append(section([
        col(sec_head("What We Do", "Six services, one partner"), 100),
    ], bg=WHITE, pad_top=100, pad_bottom=30, anchor="services"))
    els.append(section([
        card_col([srv_widgets[0]]),
        card_col([srv_widgets[1]]),
        card_col([srv_widgets[2]]),
    ], bg=WHITE, pad_top=0, pad_bottom=30, pad_mobile=(0, 16, 50, 16)))
    els.append(section([
        card_col([srv_widgets[3]]),
        card_col([srv_widgets[4]]),
        card_col([srv_widgets[5]]),
    ], bg=WHITE, pad_top=0, pad_bottom=100, pad_mobile=(0, 16, 50, 16)))

    # PROCESS (heading + row)
    steps = [
        ("01", "Discover", "We dig into your goals, users, and competitors. You get a clear brief and a realistic roadmap."),
        ("02", "Design", "Wireframes become high-fidelity designs. You review and approve at every milestone."),
        ("03", "Build", "Clean, tested development with weekly demos. No surprises at the end."),
        ("04", "Grow", "Launch is just the start. We measure, optimize, and help you scale what works."),
    ]
    els.append(section([
        col(sec_head("Our Process", "How we work together"), 100),
    ], bg=LIGHT, pad_top=100, pad_bottom=30))
    els.append(section([
        *[col([heading(num, "h3", ACCENT, "center", 40, "800", 1.1),
               heading(title_, "h4", INK, "center", 19, "700", 1.3),
               text(f"<p style='text-align:center;'>{desc}</p>", BODY, "center", 15, "400", 1.65)], 25)
          for num, title_, desc in steps],
    ], bg=LIGHT, pad_top=0, pad_bottom=100, pad_mobile=(0, 16, 50, 16)))

    # WHAT'S INCLUDED
    els.append(section([
        col([
            eyebrow("Value", "left"), spacer(12, 8),
            heading("Every engagement includes", "h2", INK, "left", 34, "700", 1.25, tablet=28, mobile=24,
                    extra={"_animation": "fadeInLeft"}),
            icon_list([
                "A dedicated project lead & Slack channel",
                "Weekly demos with recorded walkthroughs",
                "Performance & security best practices baked in",
                "Documentation and full ownership handover",
                "30 days of post-launch support free",
            ], icon="fas fa-check-circle"),
            btn("Start Your Project", "#contact", "left"),
        ], 55, center=True),
        col([img(U["laptop"], "Coding in progress", 100, 16, shadow(), anim="fadeIn")], 45, center=True),
    ], bg=WHITE, pad_top=100, pad_bottom=100))

    # CTA
    els.append(cta_box("Not sure which service you need?", "Book a free 30-minute call — we'll point you in the right direction.", "Book a Free Call"))
    return page("Services", els)

def portfolio():
    els = []
    # HERO
    els.append(section([
        col([
            heading("Our Work", "h1", WHITE, "left", 44, "800", 1.2, tablet=34, mobile=28,
                    extra={"_animation": "fadeInLeft"}),
            text("<p>A selection of projects we're proud of. Every one started as a blank canvas.</p>", "#CBD5E1", "left", 18,
                 extra={"_animation": "fadeInLeft", "_animation_delay": {"unit": "px", "size": 120, "sizes": []}}),
        ], 100),
    ], bg=None, pad_top=110, pad_bottom=110, overlay=dark_hero_bg(U["w5"], 0.85)))

    # PROJECTS
    els.append(section([
        col(sec_head("Selected Projects", "Recent work", "Websites, apps, and brands — built for clients who cared about the details."), 100),
    ], bg=WHITE, pad_top=100, pad_bottom=30, pad_mobile=(50, 16, 0, 16)))
    els.append(section([
        col([img(U["w1"], "Project 1", 100, 12, shadow(), anim="fadeInUp")], 33.3333),
        col([img(U["w2"], "Project 2", 100, 12, shadow(), anim="fadeInUp", anim_delay=100)], 33.3333),
        col([img(U["w3"], "Project 3", 100, 12, shadow(), anim="fadeInUp", anim_delay=200)], 33.3333),
    ], bg=WHITE, pad_top=0, pad_bottom=30, pad_mobile=(0, 16, 50, 16)))
    els.append(section([
        col([img(U["w4"], "Project 4", 100, 12, shadow(), anim="fadeInUp")], 33.3333),
        col([img(U["w5"], "Project 5", 100, 12, shadow(), anim="fadeInUp", anim_delay=100)], 33.3333),
        col([img(U["w6"], "Project 6", 100, 12, shadow(), anim="fadeInUp", anim_delay=200)], 33.3333),
    ], bg=WHITE, pad_top=0, pad_bottom=40, pad_mobile=(0, 16, 50, 16)))
    els.append(section([
        col([text("<p style='text-align:center;'>Want the full case studies? Drop us a line — happy to share metrics and process.</p>", MUTED, "center", 15),
             btn("Request Case Studies", "#contact", "center")], 100),
    ], bg=WHITE, pad_top=0, pad_bottom=100, pad_mobile=(0, 16, 50, 16)))

    # CTA
    els.append(cta_box("Your project could be next", "Let's build something worth showing off. Free consultation, no strings attached.", "Start a Project",
                       colors=("#0F172A", "#1E1B4B"), pad_mobile=(0, 16, 50, 16)))
    return page("Portfolio", els)

def blog():
    els = []
    # HERO
    els.append(section([
        col([
            heading("Blog", "h1", WHITE, "left", 44, "800", 1.2, tablet=34, mobile=28,
                    extra={"_animation": "fadeInLeft"}),
            text("<p>Ideas, guides, and lessons from the front lines of digital.</p>", "#CBD5E1", "left", 18,
                 extra={"_animation": "fadeInLeft", "_animation_delay": {"unit": "px", "size": 120, "sizes": []}}),
        ], 100),
    ], bg=None, pad_top=110, pad_bottom=110, overlay=dark_hero_bg(U["w1"], 0.85)))

    # LATEST ARTICLES — Royal Elementor Addons Post Grid (dynamic)
    els.append(section([
        col(sec_head("Latest Articles", "From the blog"), 100),
    ], bg=WHITE, pad_top=100, pad_bottom=30, pad_mobile=(50, 16, 0, 16)))
    wpr_grid = widget("wpr-grid", {
        "query_not_found_text": "No Posts Found!",
        "grid_elements": [
            {"_id": eid(), "element_read_more_text": "Read More", "element_tax_sep": ", ",
             "element_comments_text_1": "No Comments", "element_comments_text_2": "Comment", "element_comments_text_3": "Comments"},
            {"element_select": "date", "element_display": "inline", "element_extra_text_pos": "after", "element_extra_text": "/",
             "_id": eid(), "element_read_more_text": "Read More", "element_tax_sep": ", ",
             "element_comments_text_1": "No Comments", "element_comments_text_2": "Comment", "element_comments_text_3": "Comments"},
            {"element_select": "excerpt", "_id": eid(), "element_read_more_text": "Read More", "element_tax_sep": ", ",
             "element_comments_text_1": "No Comments", "element_comments_text_2": "Comment", "element_comments_text_3": "Comments"},
            {"element_select": "read-more", "_id": eid(), "element_read_more_text": "Read More", "element_tax_sep": ", ",
             "element_comments_text_1": "No Comments", "element_comments_text_2": "Comment", "element_comments_text_3": "Comments"},
        ],
        "filters_all_text": "All Posts",
        "pagination_older_text": "Older Posts", "pagination_newer_text": "Newer Posts",
        "pagination_prev_text": "Previous Page", "pagination_next_text": "Next Page",
        "pagination_first_text": "First Page", "pagination_last_text": "Last Page",
        "pagination_load_more_text": "Load More", "pagination_finish_text": "End of Content.",
        "layout_filters": "", "layout_pagination": "",
        "grid_item_bg_color": "#FFFFFF",
        "grid_item_padding": dim(20, 20, 20, 20, True),
        "grid_item_radius": dim(20, 20, 20, 20, True),
        "grid_item_shadow_box_shadow_type": "yes",
        "grid_item_shadow_box_shadow": {"horizontal": 0, "vertical": 12, "blur": 32, "spread": -12, "color": "rgba(79,70,229,0.16)"},
        "grid_media_radius": dim(20, 20, 0, 0, False),
        "date_text_spacing": {"unit": "px", "size": 7, "sizes": []},
        "date_margin": dim(5, 7, 10, 0, False),
        "read_more_bg_color_background": "classic",
        "read_more_bg_color_color": ACCENT,
        "read_more_color": "#FFFFFF",
        "read_more_bg_color_hr_background": "classic",
        "read_more_bg_color_hr_color": ACCENT2,
        "read_more_color_hr": "#FFFFFF",
        "read_more_padding": dim(8, 20, 8, 20, False),
        "read_more_margin": dim(30, 0, 0, 0, False),
        "read_more_radius": dim(10, 10, 10, 10, True),
    })
    els.append(section([
        col([wpr_grid], 100),
    ], bg=WHITE, pad_top=0, pad_bottom=100, pad_mobile=(0, 16, 50, 16)))

    # CTA
    els.append(cta_box("Fresh ideas, straight to your inbox", "One email a month. No spam, ever.", "Subscribe"))
    return page("Blog", els)

def single():
    els = []
    # HERO
    els.append(section([
        col([
            eyebrow("Insight", "left"),
            heading("10 Conversion Lessons from 100+ Landing Pages", "h1", WHITE, "left", 44, "800", 1.2, tablet=34, mobile=28,
                    extra={"_animation": "fadeInLeft"}),
            text("<p>By Andi Kurniawan · 6 min read · August 2026</p>", "#CBD5E1", "left", 15,
                 extra={"_animation": "fadeInLeft", "_animation_delay": {"unit": "px", "size": 120, "sizes": []}}),
        ], 100),
    ], bg=None, pad_top=110, pad_bottom=110, overlay=dark_hero_bg(U["w2"], 0.85)))

    # CONTENT
    els.append(section([
        col([
            text("<p>We analyzed the patterns that separate high-converting landing pages from the rest. Over the last year, we audited more than a hundred pages across industries — and the results were remarkably consistent.</p>"
                 "<p>The pages that convert share a handful of traits: a single clear headline, one primary call to action, social proof placed early, and a friction-free form. The pages that don't, tend to try to do too much at once.</p>"
                 "<p>This is a demo single-post layout for the Agenzy kit. Replace this content with your own article — and for a fully dynamic single-post template, apply it via Elementor Theme Builder (Pro).</p>"),
        ], 75),
    ], bg=WHITE, pad_top=80, pad_bottom=80, settings={"flex_justify_content": "center"}))

    # CTA
    els.append(cta_box("Enjoyed this article?", "There's more where that came from. One email a month, no spam.", "Subscribe"))
    return page("Single Post (Demo)", els)

def contact():
    els = []
    # HERO
    els.append(section([
        col([
            heading("Contact Us", "h1", WHITE, "left", 44, "800", 1.2, tablet=34, mobile=28,
                    extra={"_animation": "fadeInLeft"}),
            text("<p>Tell us about your project. We usually reply within one business day.</p>", "#CBD5E1", "left", 18,
                 extra={"_animation": "fadeInLeft", "_animation_delay": {"unit": "px", "size": 120, "sizes": []}}),
        ], 100),
    ], bg=None, pad_top=110, pad_bottom=110, overlay=dark_hero_bg(U["office"], 0.85)))

    info = [
        ("fas fa-map-marker-alt", "Visit Us", "Jl. Sudirman Kav. 52-53, Jakarta Selatan, Indonesia"),
        ("fas fa-envelope", "Email Us", "hello@agenzy.studio"),
        ("fas fa-phone", "Call Us", "+62 812 3456 7890"),
    ]
    info_widgets = [icon_box(i, t, d, anim="fadeInUp", anim_delay=idx * 100) for idx, (i, t, d) in enumerate(info)]
    els.append(section([
        card_col([info_widgets[0]]),
        card_col([info_widgets[1]]),
        card_col([info_widgets[2]]),
    ], bg=LIGHT, pad_top=80, pad_bottom=80))

    # CONTACT + MAP
    els.append(section([
        col([
            eyebrow("Get In Touch", "left"), spacer(12, 8),
            heading("Let's build something great together", "h2", INK, "left", 34, "700", 1.25, tablet=28, mobile=24,
                    extra={"_animation": "fadeInLeft"}),
            text("<p>Free 30-minute consultation. We'll listen first, then give you honest advice — even if that means telling you we're not the right fit.</p>",
                 extra={"_animation": "fadeInLeft", "_animation_delay": {"unit": "px", "size": 120, "sizes": []}}),
            icon_list([
                "hello@agenzy.studio",
                "+62 812 3456 7890",
                "Jl. Sudirman Kav. 52-53, Jakarta",
            ], icon="fas fa-check-circle"),
            btn("Email Us Directly", "mailto:hello@agenzy.studio", "left"),
        ], 50, center=True),
        col([
            heading("Find Us", "h4", INK, "left", 20, "700", 1.3),
            osm_map(),
        ], 50, center=True),
    ], bg=WHITE, pad_top=100, pad_bottom=100))

    # CTA
    els.append(cta_box("Prefer a form?", "Add any form plugin (e.g. WPForms, Contact Form 7) and paste its shortcode into a Shortcode widget — it takes one minute.", "Get in Touch",
                       colors=("#0F172A", "#1E1B4B")))
    return page("Contact", els)

def p404():
    els = []
    els.append(section([
        col([
            heading("404", "h1", ACCENT, "center", 110, "800", 1.0, tablet=80, mobile=64),
            heading("This page took a vacation", "h2", WHITE, "center", 36, "700", 1.25, tablet=28, mobile=24),
            text("<p style='text-align:center;'>The page you're looking for doesn't exist or has moved. Let's get you back on track.</p>", "#CBD5E1", "center", 17),
            btn("Back to Home", "#", "center", WHITE, INK, "#E2E8F0", pt=16, pl=36),
        ], 70, center=True),
    ], bg=None, pad_top=140, pad_bottom=140, overlay=dark_hero_bg(U["meeting"], 0.92)))

    return page("404", els)

def header_section():
    # Royal Theme Builder header — wpr-logo + wpr-nav-menu (dynamic)
    return {
        "content": [
            section([
                col([widget("wpr-logo", {})], 40, center=True),
                col([widget("wpr-nav-menu", {"menu_align": "right"})], 60, center=True),
            ], bg=WHITE, pad_top=16, pad_bottom=16,
               settings={"border_border": "solid", "border_width": dim(0, 0, 1, 0, False), "border_color": BORDER}),
        ],
        "page_settings": [],
        "version": "0.4",
        "title": "Header",
        "type": "wpr-theme-builder",
    }

def footer_section():
    links = [
        "Home", "About", "Services", "Portfolio", "Blog", "Contact",
    ]
    contact_items = [
        "hello@agenzy.studio",
        "+62 812 3456 7890",
        "Jakarta Selatan, Indonesia",
    ]
    col1 = col([
        heading("Agenzy", "h4", WHITE, "left", 22, "700", 1.3),
        text("<p>A full-service digital agency helping startups and brands design, build, and scale products people love.</p>", "#94A3B8", "left", 15, line=1.7),
        social_icons(),
    ], 40)
    col2 = col([
        heading("Quick Links", "h4", WHITE, "left", 18, "700", 1.3),
        icon_list(links, icon="fas fa-angle-right", icon_color="#94A3B8", text_color="#CBD5E1", px=15),
    ], 30)
    col3 = col([
        heading("Contact", "h4", WHITE, "left", 18, "700", 1.3),
        icon_list(contact_items, icon="fas fa-check-circle", icon_color=ACCENT, text_color="#CBD5E1", px=15),
    ], 30)
    bottom = col([
        divider(color="#1E293B", width_pct=100),
        text("<p style='text-align:center;'>© 2026 Agenzy. All rights reserved. — Made with the Agenzy Elementor Kit.</p>", "#64748B", "center", 14),
    ], 100)
    return {
        "content": [
            section([col1, col2, col3], bg=INK, pad_top=80, pad_bottom=40),
            section([bottom], bg=INK, pad_top=0, pad_bottom=30),
        ],
        "page_settings": [],
        "version": "0.4",
        "title": "Footer",
        "type": "wpr-theme-builder",
    }

# ---------------------------------------------------------------- build
def validate_structure(templates):
    """Elementor schema: containers only; widgets must have widgetType; inner-container widths per row must sum <= 100%."""
    errors = []
    def walk(elems, path, is_row_ctx):
        widths = []
        for i, el in enumerate(elems):
            p = f"{path}[{i}]"
            et = el.get('elType')
            if et not in ('container', 'widget'):
                errors.append(f"{p}: bad elType {et!r} (should be container)")
                continue
            if et == 'widget':
                if not el.get('widgetType'):
                    errors.append(f"{p}: widget without widgetType")
                continue
            # container
            settings = el.get('settings', {})
            if el.get('isInner') and is_row_ctx:
                w = float(settings.get('width', {}).get('size', 100) if isinstance(settings.get('width'), dict) else 100)
                widths.append(w)
            children = el.get('elements', [])
            # row context for children: if this container is row-direction
            child_row_ctx = settings.get('flex_direction', 'row') == 'row'
            walk(children, p + '>', child_row_ctx)
        if is_row_ctx:
            total = sum(widths)
            if total > 110.01:
                errors.append(f"{path}: inner container widths sum {total:.1f}% > 110% (harus 1 baris per row)")
    for name, data in templates.items():
        walk(data['content'], name, True)
    return errors

def main():
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    tdir = os.path.join(out_dir, "templates")
    cdir = os.path.join(out_dir, "content")
    os.makedirs(tdir, exist_ok=True)
    os.makedirs(cdir, exist_ok=True)

    templates = {
        "home.json": home(),
        "about.json": about(),
        "services.json": services(),
        "portfolio.json": portfolio(),
        "blog.json": blog(),
        "single.json": single(),
        "contact.json": contact(),
        "404.json": p404(),
        "header-section.json": header_section(),
        "footer-section.json": footer_section(),
    }

    errors = validate_structure(templates)
    if errors:
        print("STRUCTURE ERRORS:")
        for e in errors:
            print("  -", e)
        raise SystemExit(1)
    print("structure OK ✅")

    # remove stale template files from previous builds
    keep = set(templates.keys())
    for old in os.listdir(tdir):
        if old.endswith('.json') and old not in keep:
            os.remove(os.path.join(tdir, old))
            print(f"  removed stale {old}")

    manifest_templates = []
    for fname, data in templates.items():
        with open(os.path.join(tdir, fname), "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        manifest_templates.append({
            "source": f"templates/{fname}",
            "type": data["type"],
            "title": data["title"],
            "thumbnail": "",
        })
        print(f"  wrote templates/{fname}  ({len(json.dumps(data)):,} bytes)")

    manifest = {
        "title": "Agenzy — Digital Agency Template Kit",
        "description": "A clean, simple, fully responsive digital agency website kit built with Elementor Free widgets only. No extra plugins needed. Includes 7 pages plus header & footer sections.",
        "preview": "",
        "templates": manifest_templates,
        "categories": ["business", "agency"],
        "keywords": ["digital agency", "agency", "business", "portfolio", "responsive"],
        "settings": {},
    }
    with open(os.path.join(cdir, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    print(f"  wrote content/manifest.json ({len(json.dumps(manifest)):,} bytes)")
    print("DONE")

if __name__ == "__main__":
    main()
