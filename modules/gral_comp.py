import streamlit as st
import os
import mimetypes
from typing import Optional
import pycountry

UI = {
    "tabs": {
        "presentation":   {"en": "Presentation",              "es": "Presentación"},
        "experience":     {"en": "Experience & Achievements","es": "Experiencia y Logros"},
        "projects":       {"en": "Projects",                  "es": "Proyectos"},
        "academic":       {"en": "Academic Background",       "es": "Formación Académica"},
        "inaction":       {"en": "In Action",                 "es": "En Acción"},
        "contact":        {"en": "Contact",                   "es": "Contacto"},
    },
    "headers": {
        "who":            {"en": "Who am I?",                 "es": "¿Quién soy?"},
        "interests":      {"en": "Interests",                 "es": "Intereses"},
        "hobbies":        {"en": "Hobbies",                   "es": "Pasatiempos"},
        "job_exp":        {"en": "Job Experience",            "es": "Experiencia Laboral"},
        "achievements":   {"en": "Achievements",              "es": "Logros"},
        "education":      {"en": "Education",                 "es": "Educación"},
        "certifications": {"en": "Certifications",            "es": "Certificaciones"},
    },
    "in_action_text": {
        "en": (
            "Most of my work is related to sensitive data, and my repositories and developments are located\n"
            "and running on-premise servers. However, I have some projects and PoCs that I can share with you,\n"
            "thanks to synthetic data and a little effort I put on my brand new YouTube channel."
        ),
        "es": (
            "La mayoría de mi trabajo está relacionado con datos sensibles, y mis repositorios y desarrollos están ubicados\n"
            "y funcionando en servidores locales. Sin embargo, tengo algunos proyectos y PoCs que puedo compartir contigo,\n"
            "gracias a datos sintéticos y un poco de esfuerzo que he puesto en mi nuevo canal de YouTube."
        ),
    },
    "contact_text": {
        "en": ("Please, get in touch if you think I can help you with your projects and/or businesses."),
        "es": ("Por favor, contáctame si crees que puedo ayudarte con tus proyectos y/o negocios."),
    }
}


def title():
    return st.title("Santi Tedoldi \n #### Data Scientist & AI Engineer")

def get_flag_emoji(country_name: str) -> str:
    """
    Look up a country's ISO alpha-2 code via pycountry,
    then turn each letter into its regional-indicator symbol.
    """
    try:
        country = pycountry.countries.lookup(country_name)
        return "".join(chr(ord(ch) + 127397) for ch in country.alpha_2.upper())
    except Exception:
        return "🏳️"  # fallback white flag

import os
import mimetypes
import streamlit as st
from typing import Optional

def render_element(
    title: str,
    year: str,
    place: str,
    description: str,
    *,
    bg_color: str = "#f0f8ff",
    font_color: str = "#000000",
    link_url: Optional[str] = None,
    link_text: Optional[str] = None
) -> None:
    # 1) open the styled container
    open_div = (
        f'<div style="'
        f'background-color: {bg_color}; '
        f'color: {font_color}; '
        'border-radius: 8px; '
        'padding: 12px; '
        'margin-bottom: 10px;'
        '">'
    )
    st.markdown(open_div, unsafe_allow_html=True)

    # 2) render the main content
    st.markdown(f'<h4 style="margin:0;">{title}</h4>', unsafe_allow_html=True)
    st.markdown(
        f'<p style="margin:4px 0; font-size:0.9em;">'
        f'<strong>{year}</strong> — {place}</p>',
        unsafe_allow_html=True
    )
    st.markdown(f'<p style="margin:4px 0;">{description}</p>', unsafe_allow_html=True)

    # 3) render link or download_button inside the same div
    if link_url:
        text = link_text or os.path.basename(link_url)
        _, ext = os.path.splitext(link_url)
        static_exts = {
            ".pdf", ".docx", ".doc", ".xls", ".xlsx",
            ".png", ".jpg", ".jpeg", ".gif", ".txt", ".csv"
        }
        if ext.lower() in static_exts and os.path.exists(link_url):
            # local file → download button
            mime_type, _ = mimetypes.guess_type(link_url)
            with open(link_url, "rb") as f:
                data = f.read()
            st.download_button(
                label=text,
                data=data,
                file_name=os.path.basename(link_url),
                mime=mime_type or "application/octet-stream"
            )
        else:
            # external URL → regular hyperlink
            st.markdown(
                f'<p style="margin:4px 0; font-size:0.9em;">'
                f'<a href="{link_url}" target="_blank" '
                f'style="color:{font_color}; text-decoration:underline;">'
                f'{text}</a></p>',
                unsafe_allow_html=True
            )

    # 4) close the container
    st.markdown("</div>", unsafe_allow_html=True)
def _make_badges(items: list[str], bg_color: str) -> str:
    """
    Returns HTML for a horizontal list of pill-shaped badges.
    """
    badges = ""
    for item in items:
        badges += (
            f"<span style="
            f"'display: inline-block;"
            f"background-color: {bg_color};"
            f"color: #000;"
            f"border-radius: 12px;"
            f"padding: 4px 10px;"
            f"margin: 2px;"
            f"font-size: 0.9em;'>"
            f"{item}"
            f"</span>"
        )
    return badges

def render_skills(
    skills: dict[str, list[str]],
    *,
    hard_bg: str = "#d0e8ff",
    soft_bg: str = "#d0ffd8",
) -> None:
    """
    Renders hard and soft skills as colored badges.
    
    - `skills` should be a dict with optional keys 'hard' and 'soft'.
    - `hard_bg` and `soft_bg` control the background colors of those badges.
    """
    html = ""
    hard = skills.get("hard", [])
    soft = skills.get("soft", [])

    if hard:
        # html += "<div style='margin-top:8px;'><strong>Hard Skills:</strong><br>"
        html += "<div style='margin-top:8px;'>"
        html += _make_badges(hard, hard_bg)
        html += "</div>"

    if soft:
        # html += "<div style='margin-top:8px;'><strong>Soft Skills:</strong><br>"
        html += "<div style='margin-top:8px;'>"
        html += _make_badges(soft, soft_bg)
        html += "</div>"

    if html:
        st.markdown(html, unsafe_allow_html=True)