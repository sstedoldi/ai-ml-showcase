import streamlit as st
import pandas as pd
pd.options.display.float_format = '{:.2f}'.format
import plotly.graph_objects as go
from math import pi

# Local components and configuration imports
from styles.basics import hide, sidebar#, lg_color, cont_padding
from modules.gral_config import page_config
from modules.auth_config import auth_config
from modules.gral_comp import title, render_element, render_skills, UI
# from modules.youtube_comp import get_latest_videos
import youtube
import info

################################
# CONFIGURATION
################################
st.set_page_config(**page_config)

### STYLES
st.markdown(hide(".st-emotion-cache-zq5wmm.ezrtsby0"), unsafe_allow_html=True)
st.markdown(hide(".stDecoration"), unsafe_allow_html=True)
sidebar()

### HEADER
img = "images/Portfolio-heading-cut-perfil.png"
st.image(img, use_container_width=True)
title()

# Sidebar
# Language Selection
lang = st.sidebar.selectbox("Select Language", ['en', 'es'], format_func=lambda x: 'English' if x == 'en' else 'Español')

################################
# MAIN TABS
################################
pres_tab, exp_tab, proj_tab, back_tab, in_action, contact = st.tabs([
    UI["tabs"]["presentation"][lang],
    UI["tabs"]["experience"][lang],
    UI["tabs"]["projects"][lang],
    UI["tabs"]["academic"][lang],
    UI["tabs"]["inaction"][lang],
    UI["tabs"]["contact"][lang],
])

################################
# Presentation
with pres_tab:
    st.header(UI["headers"]["who"][lang])

    # Purpose
    st.write("\n".join(info.purpose[lang].splitlines()))

    intertests_col, kills_col = st.columns((0.2, 0.8))
    with intertests_col:
        # Interests
        st.subheader(UI["headers"]["interests"][lang])
        for interest in info.interests["professional"][lang]:
            st.write(f"- {interest}")

    with kills_col:
        data_skills = info.skills['data']
        categories = [d[0] for d in data_skills]
        values = [d[1] for d in data_skills]
        # close loop
        values += values[:1]
        categories += categories[:1]

        fig = go.Figure(
            data=[go.Scatterpolar(r=values, theta=categories, fill='toself', name='Data Skills')],
            layout=go.Layout(polar=dict(radialaxis=dict(visible=True, range=[0, 10])), showlegend=False)
        )

        st.plotly_chart(fig, use_container_width=True)

    softskills_col, techskills_col, hobbies_col = st.columns((0.4, 0.4, 0.2))
    # Skills (soft & technical)
    with softskills_col:
        st.markdown("### Soft Skills")
        for skill, level in info.skills['soft'][lang]:
            stars = '★' * level + '☆' * (5 - level)
            st.markdown(f"{skill} <span style='color:gold'>{stars}</span>", unsafe_allow_html=True)

    with techskills_col:
        st.markdown("### Tech Skills")
        for skill, level in info.skills['hard'][lang]:
            stars = '★' * level + '☆' * (5 - level)
            st.markdown(f"{skill} <span style='color:gold'>{stars}</span>", unsafe_allow_html=True)
    
    with hobbies_col:
        st.subheader(UI["headers"]["hobbies"][lang])
        for interest in info.interests["personal"][lang]:
            st.write(f"- {interest}")
    

################################
# Experience
with exp_tab:
    st.header(UI["tabs"]["experience"][lang])

    exp_col, ach_col = st.columns([0.6, 0.4])

    # Job Experience
    with exp_col:
        st.subheader(UI["headers"]["job_exp"][lang])
        for exp in info.experience[lang]:
            st.markdown(f"#### {exp['title']}")
            st.markdown(
                f"**{exp['company']}** ({exp['duration']})  \n\n"
                f"{exp['description']}"
            )
            st.divider()

    # Achievements
    with ach_col:
        st.subheader(UI["headers"]["achievements"][lang])
        for ach in info.achievements[lang]:
            render_element(
                ach["title"],
                ach["year"],
                ach["place"],
                ach["description"],
                bg_color="goldenrod",
                font_color="white"
            )

################################
# Projects
with proj_tab:
    st.header(UI["tabs"]["projects"][lang])

    proj_list = info.projects[lang]
    col1, col2 = st.columns(2)
    for i, proj in enumerate(proj_list):
        container = col1 if i % 2 == 0 else col2
        with container:
            st.markdown(f"**{proj['title']}** ({proj['year']})")
            st.write(proj['description'])
            # now render colored skill badges
            if 'skills' in proj:
                render_skills(proj['skills'])
            st.divider()

################################
# Education and Certifications
with back_tab:
    st.header(UI["tabs"]["academic"][lang])

    col_edu, col_cert = st.columns((0.5, 0.5))
    with col_edu:
        st.subheader(UI["headers"]["education"][lang])
        for edu in info.education[lang]:
            render_element(
                edu["title"],
                edu["duration"],
                edu["institution"],
                edu["description"],
                bg_color="darkgreen",
                font_color="white",
                link_url=edu.get("link_url"),
                link_text=edu.get("link_text"),
            )

    with col_cert:
        st.subheader(UI["headers"]["certifications"][lang])
        for cert in info.certifications[lang]:
            render_element(
                cert["title"],
                cert["year"],
                cert["institution"],
                cert["description"],
                bg_color="darkblue",
                font_color="white",
                link_url=cert.get("link_url"),
                link_text=cert.get("link_text"),
            )
            
################################
# In Action, with YouTube channel
with in_action:
    st.header(UI["tabs"]["inaction"][lang])
    st.write(UI["in_action_text"][lang])

    for ch in info.channels[lang]:
        st.markdown(f"#### [{ch['title']}]({ch['link']})")
        st.write(ch["description"])
        videos = youtube.lastest_videos
        cols = st.columns(2)
        for idx, vid in enumerate(videos):
            with cols[idx % 2]:
                # thumbnail + link
                st.markdown(f"[{vid['title']}]({vid['link']})")
                st.markdown(f"**{vid['lenguaje']}**")
                st.image(vid["thumbnail"], use_container_width=True)

################################
# Contact
with contact:
    st.header(UI["tabs"]["contact"][lang])
    st.write(UI["contact_text"][lang])

    pi = info.personal_info
    col1, col2 = st.columns((0.5, 0.5))
    with col1:
        st.markdown(f":man: {pi['fullname']}")
        st.markdown(f":house: {pi['location']}")
        st.markdown(f":email: [{pi['email']}](mailto:{pi['email']})")
        st.markdown(f":iphone: {pi['phone']}")
    with col2:
        st.markdown(f"**LinkedIn**: [{pi['linkedin']}]({pi['linkedin']})")
        st.markdown(f"**GitHub**: [{pi['github']}]({pi['github']})")
        st.markdown(f"**YouTube**: [{pi['youtube']}]({pi['youtube']})")

################################
# AI BOT WITH MY ASSISTANT
################################

from modules.bedrock_bot import AgentBedrockRAGBot
from secrets.aws import aws_secrets

if "bot_activated" not in st.session_state:
    st.session_state.bot_activated = False

if st.sidebar.button("Activate Bot", key="activate_bot", type="primary", 
                     use_container_width=True, help="Click to activate the bot."):
    st.session_state.bot_activated = True

if st.session_state.bot_activated:
    bot = AgentBedrockRAGBot(
        api_key    = aws_secrets["AWS_KEY"],
        secret_key = aws_secrets["AWS_SECRET"],
        region     = aws_secrets["REGION"],
        agent_id   = aws_secrets["AGENT_ID"],
        alias_id   = aws_secrets["AGENT_ALIAS_ID"],
        kb_id      = aws_secrets["KNOWLEDGE_BASE_ID"],
        llm_id     = aws_secrets["LLM_ID"],
    )
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []


    with st.sidebar:
        
        st.sidebar.markdown(UI["headers"]["chat"][lang])
        messages = st.sidebar.container(height=300, border=False, key="chat_container")

        if prompt := st.chat_input(UI["bot_text"]["breaking_ice"][lang], key="chat_input"):
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            with st.spinner(UI["bot_text"]["spinner"][lang]):
                answer = bot.rag_query(
                    prompt,
                    top_k=5,
                    inference_config={"maxTokens":512, "temperature":0.2},
                    prompt_template="Use the following context to answer:\n$search_results$\nUser: $input$")
            st.session_state.chat_history.append({"role": "assistant", "content": answer})

        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                messages.chat_message("user").write(msg["content"])
            else:
                messages.chat_message("assistant").write(msg["content"])