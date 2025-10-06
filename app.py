import streamlit as st
import pandas as pd

# Configurando a página
st.set_page_config(
    page_title="Portfólio",
    page_icon=":tada:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Carregar dados do CSV
data = pd.read_csv("portfolio.csv")

# --- Estruturas de dados a partir do CSV ---
PROFILE = {
    row["key"]: {
        "title": row["title"],
        "description": row["description"],
        "image": row["image"]
    }
    for _, row in data[data["section"] == "profile"].iterrows()
}

ABOUT = data[data["section"] == "about"].iloc[0]["description"]

SOCIAL_LINKS = {
    row["key"]: {
        "icon": row["skills"],  
        "url": row["link"]
    }
    for _, row in data[data["section"] == "social"].iterrows()
}

SKILLS = {
    row["key"]: row["skills"].split("|")
    for _, row in data[data["section"] == "skill"].iterrows()
}

PESQUISA = [
    {
        "title": row["title"],
        "description": row["description"],
        "image": row["image"],
        "link": row["link"]
    }
    for _, row in data[data["section"] == "project"].iterrows()
]

CERTIFICATES = [
    {
        "title": row["title"],
        "image": row["image"],
        "link": row["link"]
    }
    for _, row in data[data["section"] == "certificate"].iterrows()
]

EXTENSAO = [
    {
        "title": row["title"],
        "description": row["description"],
        "image": row["image"],
        "link": row["link"]
    }
    for _, row in data[data["section"] == "extension"].iterrows()
]

RECOGNITIONS = [
    {
        "title": row["title"],
        "description": row["description"],
        "link": row["link"],
        "image": row["image"]
    }
    for _, row in data[data["section"] == "recognition"].iterrows()
]

# --- Funções de estilo e layout ---
def load_css():
    is_dark = st.get_option("theme.base") == "dark"

    if is_dark:
        css = """
        <style>
            :root {
                --primary-color: #90cdf4;
                --accent-color: #0bc5ea;
                --text-color: #e6edf3;
                --secondary-background-color: #0d1117;
                --card-background: #161b22;
                --chip-background: #30363d;
                --shadow: 0 4px 6px -1px rgba(255, 255, 255, 0.1);
            }
        </style>
        """
    else:
        css = """
        <style>
            :root {
                --primary-color: #1a365d;
                --accent-color: #38bdf8;
                --text-color: #000000;
                --secondary-background-color: #f9fafb;
                --card-background: #ffffff;
                --chip-background: #e2e8f0;
                --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            }
        </style>
        """

    st.markdown(css + """
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <style>
            body {
                background-color: var(--secondary-background-color);
                color: var(--text-color);
            }
            .project-card {
                border-radius: 10px;
                padding: 2rem;
                margin: 2.5rem 0; /* mais espaço entre seções */
                transition: all 0.3s ease;
                border: 2px solid var(--accent-color);
            }
            .certificate-card {
                border-left: 3px solid var(--accent-color);]
                border-radius: 10px;
                padding: 1.5rem;
                margin: 2.5rem 0; /* mais espaço entre seções */
                transition: all 0.3s ease;  
                border-radius: 10px;
            }
            .project-card:hover, .certificate-card:hover {
                transform: translateY(-5px);
                box-shadow: var(--shadow);
            }
            h4, h2, h3 {
                color: var(--primary-color);
            }
            a {
                color: var(--accent-color);
            }
            /* Chips de skills */
            .chip {
                display: inline-block;
                border-radius: 25px;
                font-size: 0.9rem;
                list-style: none;
                margin: 5px;
                padding: 6px 12px;
            }
        </style>
    """, unsafe_allow_html=True)

# --- Seções ---
def show_recognitions():
    st.markdown("## 🏆 Reconhecimentos e Premiações")
    if not RECOGNITIONS:
        st.info("Nenhum reconhecimento cadastrado.")
        return

    for rec in RECOGNITIONS:
        link = str(rec["link"]) if pd.notna(rec["link"]) else ""
        st.markdown(f"""
            <div class="project-card">
                <h4>{rec['title']}</h4>
                <p>{rec['description']}</p>
                {f'<a href="{link}" target="_blank">Mais info</a>' if link else ""}
            </div>
        """, unsafe_allow_html=True)
    st.markdown("---")

def show_certificates():
    st.markdown("## 📜 Certificados")
    for cert in CERTIFICATES:
        st.markdown(f"""
            <div class="certificate-card">
                <h4>{cert['title']}</h4>
                <a href="{cert['link']}" target="_blank">Ver Certificado</a>
            </div>
        """, unsafe_allow_html=True)
    st.markdown("---")

def show_research():
    st.markdown("## 🔬 Pesquisa")
    for i in range(0, len(PESQUISA), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(PESQUISA):
                pesquisa = PESQUISA[i + j]
                with cols[j]:
                    st.markdown(f"""
                        <div class="project-card">
                            <img src="{pesquisa['image']}" style="width:100%; border-radius: 10px;">
                            <h4>{pesquisa['title']}</h4>
                            <p>{pesquisa['description'][:100]}...</p>
                        </div>
                    """, unsafe_allow_html=True)
    st.markdown("---")

def show_extension():
    st.markdown("## 📚 Extensão")
    for i in range(0, len(EXTENSAO), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(EXTENSAO):
                extensao = EXTENSAO[i + j]
                with cols[j]:
                    st.markdown(f"""
                        <div class="project-card">
                            <img src="{extensao['image']}" style="width:100%; border-radius: 10px;">
                            <h4>{extensao['title']}</h4>
                            <p>{extensao['description'][:100]}...</p>
                        </div>
                    """, unsafe_allow_html=True)
    st.markdown("---")

def social_links():
    link_html = "".join(
        f'<a href="{info["url"]}" target="_blank" style="margin-right: 20px;">'
        f'<i class="{info["icon"]} fa-2x"></i></a>'
        for info in SOCIAL_LINKS.values()
    )
    st.markdown(f'<div style="text-align: center; margin-top: 3rem;">{link_html}</div>', unsafe_allow_html=True)

# --- MAIN ---
def main():
    load_css()

    # Sidebar
    with st.sidebar:
        st.markdown(f"""
            <div style="text-align: center;">
                <img src="{PROFILE['name']['image']}" style="border-radius: 50%; width: 150px; height: 150px; object-fit: cover; margin-bottom: 1rem;">
                <h2>{PROFILE['name']['title']}</h2>
                <p style="color:var(--accent-color)">{PROFILE['role']['title']}</p>
            </div>
        """, unsafe_allow_html=True)

        with st.expander("📞 Contatos"):
            st.markdown("""
                <p>📍 Porto Velho</p>
                <p>☎️ +55 69 99929-0423</p>
                <p>✉️  k.migueloliveira2009@gmail.com</p>
            """, unsafe_allow_html=True)

        social_links()

    # Conteúdo principal
    st.title(PROFILE['name']['title'])
    st.markdown(f"### {PROFILE['role']['title']}")

    with st.container():
        st.markdown(f"""
            ## 👋 Sobre Mim
            {ABOUT}
        """, unsafe_allow_html=True)

        st.markdown("---")

        st.markdown("## 💻 Habilidades")
        cols = st.columns(3)
        for idx, (title, skills) in enumerate(SKILLS.items()):
            with cols[idx % 3]:
                items_html = "".join(f"<li class='chip'>{skill}</li>" for skill in skills)
                st.markdown(f"""
                    <div class="project-card">
                        <h4>{title}</h4>
                        <ul>{items_html}</ul>
                    </div>
                """, unsafe_allow_html=True)

    st.markdown("---")
    show_research()
    show_extension()
    show_certificates()
    show_recognitions()

    # Rodapé
    st.markdown("---")
    st.markdown(f"""
        <div style="text-align: center; margin-bottom:10px;">
            &copy; {pd.Timestamp.now().year} {PROFILE['name']['title']}. Todos os direitos reservados.
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()


