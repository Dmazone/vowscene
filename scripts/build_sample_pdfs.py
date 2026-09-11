from pathlib import Path
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import KeepTogether, PageBreak, Paragraph, SimpleDocTemplate, Spacer

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "pdf"
OUT.mkdir(parents=True, exist_ok=True)

SAMPLES = {
    "romantic": {
        "title": "A QUIET CHOICE",
        "couple": "Emma & Daniel",
        "tone": "ROMANTIC DOCUMENTARY",
        "paragraphs": [
            "Before Emma knew Daniel as the man waiting at the end of an aisle, he was the stranger who gave up the last dry seat in a crowded coffee shop.",
            "She remembers the rain. He remembers her laugh. Neither remembers what they ordered.",
            "Five years later, they have learned that love is rarely one grand moment. It is a thousand quiet choices: another cup poured, another late train waited for, another ordinary Tuesday made worth remembering.",
            "And today, surrounded by everyone who watched those choices become a life, they make one more - to keep choosing each other.",
        ],
        "cues": ["00:00  Venue and weather details", "00:18  Preparation and personal objects", "00:48  First look or aisle reveal", "01:05  Hands, guests and closing wide shot"],
    },
    "documentary": {
        "title": "THE DAYS BETWEEN",
        "couple": "Maya & Theo",
        "tone": "HONEST DOCUMENTARY",
        "paragraphs": [
            "There was no lightning-bolt beginning. Maya and Theo met on a Tuesday, over a borrowed charger and a meeting that ran too long.",
            "What followed looked ordinary from the outside: grocery lists, train platforms, burnt dinners, and calls that lasted until one of them fell asleep.",
            "But this is how they built a life - not from perfect days, but from the habit of showing up for the imperfect ones.",
            "Today is not the start of their story. It is the day they gather the people who helped carry it here, and say out loud what their lives have already proven.",
        ],
        "cues": ["00:00  Guests and venue in natural motion", "00:14  Notes, objects and preparation", "00:31  Family and unscripted laughter", "00:50  Entrance, reactions and ceremony wide"],
    },
    "playful": {
        "title": "BETTER TIMING",
        "couple": "Ava & Marcus",
        "tone": "PLAYFUL & WARM",
        "paragraphs": [
            "Marcus says their story began when Ava smiled at him across the room. Ava says it began ten minutes later, when he finally realized she was smiling at the dog behind him.",
            "Their timing has improved since then.",
            "Together they have survived three apartments, one disastrous camping trip, and an ongoing disagreement about the correct way to load a dishwasher.",
            "Somewhere between all the teasing and takeaway dinners, they became each other's safest place. Today, they are making it official - bad directions, stolen blankets, and all.",
        ],
        "cues": ["00:00  Playful visual misdirection", "00:12  Preparation and reaction shots", "00:28  Fast candid montage", "00:46  Laughter, first look and confetti"],
    },
}

styles = getSampleStyleSheet()
brand = ParagraphStyle("brand", parent=styles["Normal"], fontName="Helvetica", fontSize=8, leading=10, textColor=HexColor("#7b2f3c"), alignment=TA_CENTER, tracking=2.4)
title = ParagraphStyle("title", parent=styles["Title"], fontName="Times-Roman", fontSize=28, leading=32, textColor=HexColor("#1c1917"), alignment=TA_CENTER, spaceAfter=4)
couple = ParagraphStyle("couple", parent=styles["Normal"], fontName="Times-Italic", fontSize=14, leading=18, textColor=HexColor("#6b625b"), alignment=TA_CENTER)
body = ParagraphStyle("body", parent=styles["BodyText"], fontName="Times-Roman", fontSize=12.5, leading=20, textColor=HexColor("#2d2926"), spaceAfter=11)
cue_head = ParagraphStyle("cue_head", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=8, leading=10, textColor=HexColor("#7b2f3c"), tracking=1.6, spaceBefore=8, spaceAfter=8)
cue = ParagraphStyle("cue", parent=styles["Normal"], fontName="Helvetica", fontSize=8.5, leading=13, textColor=HexColor("#6b625b"))
fine = ParagraphStyle("fine", parent=styles["Normal"], fontName="Helvetica", fontSize=6.8, leading=9, textColor=HexColor("#8a8179"), alignment=TA_CENTER)

def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(HexColor("#d8cec2"))
    canvas.line(28 * mm, 18 * mm, 182 * mm, 18 * mm)
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(HexColor("#8a8179"))
    canvas.drawString(28 * mm, 12 * mm, "VOWSCENE  /  CUSTOM VOICEOVER FOR WEDDING FILMMAKERS")
    canvas.drawRightString(182 * mm, 12 * mm, "FICTIONAL DEMONSTRATION")
    canvas.restoreState()

for slug, sample in SAMPLES.items():
    path = OUT / f"vowscene-{slug}-sample.pdf"
    doc = SimpleDocTemplate(str(path), pagesize=A4, rightMargin=28*mm, leftMargin=28*mm, topMargin=24*mm, bottomMargin=24*mm, title=f"VowScene {sample['tone']} Sample", author="VowScene")
    story = [Paragraph("VOWSCENE", brand), Spacer(1, 15*mm), Paragraph(sample["title"], title), Paragraph(sample["couple"], couple), Spacer(1, 12*mm)]
    story.extend(Paragraph(p, body) for p in sample["paragraphs"])
    cue_block = [Paragraph("SUGGESTED SCENE RHYTHM", cue_head)] + [Paragraph(c, cue) for c in sample["cues"]]
    story.extend([Spacer(1, 5*mm), KeepTogether(cue_block), Spacer(1, 8*mm), Paragraph("Names and story details are invented for this portfolio sample.", fine)])
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print(path)
