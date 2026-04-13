#!/usr/bin/env python3
"""
Group 9 Presentation Generator
Customized from generate_presentations.py v3 for team presentation.
"""

import sys, os

# Add parent dir so we can import the shared generator
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from generate_presentations import (
    generate, parse, detect, clean, get_table, get_bullets, get_subs,
    Presentation, Inches, Pt, Emu, PP_ALIGN, MSO_ANCHOR, MSO_SHAPE,
    RGBColor, qn,
    BLUE, DARK_BLUE, ORANGE, TEAL, PURPLE, GREEN, RED_SOFT,
    GRAY, BODY, BLACK, WHITE, BG_LIGHT, BG_CARD, BG_ACCENT, DIVIDER, ACCENTS,
    FN, SW, SH, ML, MR, CW, CT,
    _run, _tb, _rect, _circle, _top_bar, _slide_bg, _title, _page_footer, _card,
    _table,
    slide_agenda, slide_problem, slide_content, slide_roadmap, slide_references
)


# ── Customized slides for group presentation ─────────────────────

TEAM = "Group 9: A. Bustamante Perez, R. Lemes Cordeiro, J. Niu, J. Si"
DATE_STR = "April 2026"
COURSE = "Introduction to Computer Vision | SAIT Integrated AI"


def slide_title_group(prs, sd, total, doc_title):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    _slide_bg(slide)
    _top_bar(slide, thick=True)

    _card(slide, Inches(1.5), Inches(1.2), Inches(10.3), Inches(5.2), BG_ACCENT)

    name = doc_title.split(' - ')[0].split(' — ')[0].strip()

    # Project name
    tf = _tb(slide, Inches(2.0), Inches(1.6), Inches(9.3), Inches(1.0))
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER
    _run(tf.paragraphs[0], name, sz=38, bold=True, color=DARK_BLUE)

    # Subtitle
    tf2 = _tb(slide, Inches(2.0), Inches(2.7), Inches(9.3), Inches(0.5))
    tf2.paragraphs[0].alignment = PP_ALIGN.CENTER
    _run(tf2.paragraphs[0], "Real-time Hand Tracking with MediaPipe & Three.js",
         sz=16, color=BODY)

    # Divider
    _rect(slide, Inches(5.0), Inches(3.4), Inches(3.3), Inches(0.025), BLUE)

    # Course info
    tf3 = _tb(slide, Inches(2.0), Inches(3.6), Inches(9.3), Inches(0.4))
    tf3.paragraphs[0].alignment = PP_ALIGN.CENTER
    _run(tf3.paragraphs[0], COURSE, sz=13, color=GRAY)

    # Team members
    tf4 = _tb(slide, Inches(2.0), Inches(4.2), Inches(9.3), Inches(0.8))
    tf4.paragraphs[0].alignment = PP_ALIGN.CENTER
    _run(tf4.paragraphs[0], "Group 9", sz=14, bold=True, color=DARK_BLUE)

    members = [
        "Bustamante Perez, Angel Daniel",
        "Lemes Cordeiro, Romilson",
        "Niu, Jason",
        "Si, Jack"
    ]
    for member in members:
        p = tf4.add_paragraph()
        p.alignment = PP_ALIGN.CENTER
        _run(p, member, sz=11, color=BODY)

    # Date
    tf5 = _tb(slide, Inches(2.0), Inches(5.6), Inches(9.3), Inches(0.35))
    tf5.paragraphs[0].alignment = PP_ALIGN.CENTER
    _run(tf5.paragraphs[0], DATE_STR, sz=11, color=GRAY)

    _group_footer(slide, 1, total)


def slide_closing_group(prs, sd, total, doc_title):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    _slide_bg(slide)
    _top_bar(slide, thick=True)

    _card(slide, Inches(2.5), Inches(1.5), Inches(8.3), Inches(4.8), BG_ACCENT)
    _rect(slide, Inches(5.2), Inches(3.2), Inches(2.9), Inches(0.025), BLUE)

    tf = _tb(slide, Inches(3.0), Inches(1.9), Inches(7.3), Inches(0.8))
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER
    _run(tf.paragraphs[0], "Thank You!", sz=40, bold=True, color=DARK_BLUE)

    tf2 = _tb(slide, Inches(3.0), Inches(2.8), Inches(7.3), Inches(0.4))
    tf2.paragraphs[0].alignment = PP_ALIGN.CENTER
    _run(tf2.paragraphs[0], "Questions & Discussion", sz=16, color=GRAY)

    # Live demo link
    tf3 = _tb(slide, Inches(3.0), Inches(3.5), Inches(7.3), Inches(0.4))
    tf3.paragraphs[0].alignment = PP_ALIGN.CENTER
    _run(tf3.paragraphs[0], "Live Demo: esa-project02.7fc1132f.er.aliyun-esa.net",
         sz=11, color=BLUE, italic=True)

    # Team
    tf4 = _tb(slide, Inches(3.0), Inches(4.2), Inches(7.3), Inches(0.35))
    tf4.paragraphs[0].alignment = PP_ALIGN.CENTER
    _run(tf4.paragraphs[0], TEAM, sz=10, color=BODY)

    # Course & date
    tf5 = _tb(slide, Inches(3.0), Inches(4.7), Inches(7.3), Inches(0.35))
    tf5.paragraphs[0].alignment = PP_ALIGN.CENTER
    _run(tf5.paragraphs[0], f"{COURSE}  |  {DATE_STR}", sz=9, color=GRAY)

    # Instructor
    tf6 = _tb(slide, Inches(3.0), Inches(5.1), Inches(7.3), Inches(0.35))
    tf6.paragraphs[0].alignment = PP_ALIGN.CENTER
    _run(tf6.paragraphs[0], "Professor Uzma Ahmed Din", sz=10, color=GRAY)

    _group_footer(slide, sd['num'], total)


def _group_footer(slide, n, total):
    tf = _tb(slide, Inches(11.0), Inches(7.05), Inches(2.0), Inches(0.3))
    tf.paragraphs[0].alignment = PP_ALIGN.RIGHT
    _run(tf.paragraphs[0], f"{n} / {total}", sz=8, color=GRAY)
    tf2 = _tb(slide, ML, Inches(7.05), Inches(6.0), Inches(0.3))
    _run(tf2.paragraphs[0], "Group 9 | Introduction to Computer Vision | SAIT",
         sz=8, color=GRAY, italic=True)


def generate_group(md_path, out_path):
    doc_title, slides = parse(md_path)
    total = len(slides)
    if total == 0:
        return False

    prs = Presentation()
    prs.slide_width = SW
    prs.slide_height = SH

    # Monkey-patch footer for group use
    import generate_presentations as gp
    orig_footer = gp._page_footer
    gp._page_footer = _group_footer

    for sd in slides:
        st = detect(sd)
        try:
            if st == 'title':
                slide_title_group(prs, sd, total, doc_title)
            elif st == 'closing':
                slide_closing_group(prs, sd, total, doc_title)
            elif st == 'problem':
                slide_problem(prs, sd, total)
            elif st == 'roadmap':
                slide_roadmap(prs, sd, total)
            elif st == 'references':
                slide_references(prs, sd, total)
            else:
                slide_content(prs, sd, total)
        except Exception as e:
            print(f"    WARN slide {sd['num']}: {e}")
            try:
                slide_content(prs, sd, total)
            except:
                pass

    # Restore original footer
    gp._page_footer = orig_footer

    prs.save(out_path)
    return True


if __name__ == "__main__":
    md = os.path.join(os.path.dirname(__file__), "docs", "presentation_content.md")
    out = os.path.join(os.path.dirname(__file__), "docs", "presentation",
                       "Fruit_Ninja_CV_Presentation.pptx")

    print("=" * 50)
    print("  Fruit Ninja - Group 9 Presentation Generator")
    print("=" * 50)

    if not os.path.exists(md):
        print(f"  ERROR: {md} not found")
        sys.exit(1)

    os.makedirs(os.path.dirname(out), exist_ok=True)
    print(f"  Source: {md}")
    print(f"  Output: {out}")

    try:
        if generate_group(md, out):
            size_kb = os.path.getsize(out) / 1024
            print(f"  OK ({size_kb:.0f} KB)")
            print(f"\n  Open: open \"{out}\"")
        else:
            print("  FAIL (no slides parsed)")
    except Exception as e:
        print(f"  FAIL: {e}")
        import traceback
        traceback.print_exc()
