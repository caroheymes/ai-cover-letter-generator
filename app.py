import os
import streamlit as st
from dotenv import load_dotenv
from crewai import Crew
import utils

# Charger les variables d'environnement
# load_dotenv()

# Configuration de la page
st.set_page_config(
    page_title="Générateur de Lettres de Motivation",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 Générateur de lettres de motivation")

# ==========================================
# SIDEBAR (toujours visible et en premier)
# ==========================================
st.sidebar.header("🔑 Configuration des clés API")

# Initialisation du session_state pour les clés
if 'openai_key' not in st.session_state:
    st.session_state.openai_key = ""
if 'serper_key' not in st.session_state:
    st.session_state.serper_key = ""

# Formulaire de saisie des clés
with st.sidebar.form("api_keys_form"):
    openai_key_input = st.text_input(
        "Clé OpenAI API",
        value=st.session_state.openai_key,
        type="password",
        help="Votre clé OpenAI ne sera pas conservée après la session"
    )
    
    serper_key_input = st.text_input(
        "Clé Serper.dev API",
        value=st.session_state.serper_key,
        type="password",
        help="Votre clé Serper.dev ne sera pas conservée après la session"
    )
    
    submitted = st.form_submit_button("✅ Valider les clés")

# Mise à jour des clés dans session_state lors de la validation
if submitted:
    st.session_state.openai_key = openai_key_input
    st.session_state.serper_key = serper_key_input
    st.sidebar.success("Clés configurées pour cette session ! Pas d'inquiétude, elles ne seront pas conservées ni ré-utilisées")
    st.rerun()  # Rafraîchir pour mettre à jour l'affichage

# ==========================================
# CORPS PRINCIPAL (conditionnel)
# ==========================================
if not st.session_state.openai_key or not st.session_state.serper_key:
    st.subheader("Pourquoi, pour qui, comment")

    st.markdown('---')
    st.markdown("""
    Les recruteurs utilisent maintenant des bots pour filtrer les candidats.  
    **Mais nous aussi**, on peut mobiliser des bots pour générer des lettres que personne ne lira !  
    Aucune raison de s'en priver. 😎
    """)

    st.markdown("""
    Cette petite app va te permettre de générer des lettres de motivation, des candidatures spontanées **quasi parfaites**, 
    avec tous les mots-clés que les bots des recruteurs adorent. 🤖✨
    """)

    st.subheader("🛠️ Ce dont tu as besoin")
    st.markdown("""
    > 💰 **Les coûts d'API sont à ta charge** (je ne vais pas payer pour toi 😅), mais ça reste vraiment raisonnable:
    """)


    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**1️⃣ Clé API OpenAI**")
        st.markdown("""
        • Prends-la sur : [platform.openai.com/api-keys](https://platform.openai.com/api-keys)  
        • Crédit minimal (gratuit au début)  
        • Le modèle `gpt-5-nano` coûte quasi rien ~ 0,50€ pour une vingtaine de tests
        • Valable 6 /12 mois
        """)

    with col2:
        st.markdown("**2️⃣ Clé API Serper**")
        st.markdown("""
        • Prends-la sur : [serper.dev](https://serper.dev)  
        • **Gratuit sans CB**  
        • 2500 requêtes offertes  
        • Parfait pour commencer
        """)
    st.markdown("""
    > 🔒 **Tes clés API ne sont JAMAIS conservées.**  
    > Elles sont utilisées uniquement pendant ta session et disparaissent quand tu fermes l'app.  
    > Je n'ai aucun accès à tes secrets, ni aucun moyen de savoir ce que tu fais. 
                
    >**[Le code est open source et consultable sur Github](https://github.com/caroheymes/ai-cover-letter-generator)**
    """)
    st.subheader("Colle tes clés dans le menu de gauche et amuse-toi bien 🎉 !")
    st.markdown('---')
    st.stop()
    

# ==========================================
# CODE PRINCIPAL (exécuté uniquement si clés présentes)
# ==========================================

# Configuration des variables d'environnement pour CrewAI
os.environ["OPENAI_API_KEY"] = st.session_state.openai_key
os.environ["SERPER_API_KEY"] = st.session_state.serper_key
os.environ['OPENAI_MODEL_NAME'] = "gpt-5-nano"

# # Vérification des clés API
def check_api_keys():
    required_keys = ["OPENAI_API_KEY", "SERPER_API_KEY", "OPENAI_MODEL_NAME"]
    missing = [key for key in required_keys if not os.getenv(key)]
    if missing:
        st.error(f"Clés API manquantes: {', '.join(missing)}")
        st.info("Configurez-les dans les variables d'environnement Cloud Run")
        return False
    return True

st.sidebar.header("⚙️ Réglage des Agents")
temperatures = {
    "research_agent": st.sidebar.slider(
        "Créativité - Agent de Recherche", 
        0.0, 1.0, 0.8, 0.1,
        help="Créativité pour l'analyse de l'entreprise"
    ),
    "cv_extractor": st.sidebar.slider(
        "Créativité - Extracteur CV", 
        0.0, 1.0, 0.3, 0.1,
        help="Rigueur pour l'extraction (basse = plus strict)"
    ),
    "writer_agent": st.sidebar.slider(
        "Créativité - Rédacteur", 
        0.0, 1.0, 0.6, 0.1,
        help="Créativité pour la rédaction"
    ),
    "review_agent": st.sidebar.slider(
        "Créativité - Relecteur", 
        0.0, 1.0, 0.4, 0.1,
        help="Rigueur pour la relecture"
    )
}
# Formulaire principal
if check_api_keys():
    st.subheader("💡 Trucs et astuces")
    

    st.markdown("""
    >**Informations importantes te concernant** (que les IA ne peuvent pas deviner) :  
    Sois très libre et direct. C'est ton espace pour préciser ce qui est **important pour toi** et que les bots ne peuvent pas imaginer.  
    Par exemple :  
    • *Ne pas citer mon employeur X pour des raisons de confidentialité* 
    • *Je postule pour un job alimentaire, ne pas tenir compte de mes expériences : je suis souriante, ponctuelle et motivée*  
    • *Je suis autodidacte apiculteur, j'aime les abeilles*

    >**Informations sur l'entreprise** :  
    Si tu ne connais pas le nom exact, mets "société confidentielle" ou "startup dans le secteur X". 
    L'important est de donner un contexte minimal pour que les bots listent les valeurs et la culture commune des boîtes dans ce secteur.

    >**Description du poste** :  
    Ça marche aussi pour les candidatures spontanées ! Tu n'as pas besoin d'une annonce complète.  
    Pour une candidature spontannée 2-3 points clés suffisent :  
    • "Vendeuse boutique 35h, accueil client et gestion caisse"  
    • "Apiculteur bénévole, passionné par l'environnement"  
    • "Juriste spécialisé droit pénal"

    > **Astuce** : Moins tu mets d'informations, plus les bots improviseront. Tu peux aussi régler le niveau de créativité. 
                Plus tu es précis, plus la lettre sera ciblée. À toi de jouer ! 🎯
    """)




    with st.form("generation_form"):
        st.subheader("👤 Ton profil")
        col1, col2 = st.columns([1, 3])
        with col1:
            gender_option = st.radio(
                "Indique le genre pour éviter toute erreur de rédaction",
                ["féminin", "masculin"],
                index=0,
                horizontal=True
        )
        with col2:
            candidate_profile = st.text_input(
                "Information importante te concernant que les agents IA ne peuvent pas deviner",
                placeholder="Ex: stage de 6 mois à compter de janvier 2026, salaire d'au moins 100 patates,...",
                help="Cela permettra de mieux spécialiser ta lettre"
            )
    
        st.subheader("📄 1. Ton CV")
        cv_file = st.file_uploader(
            "Charge ton CV (pdf, docx ou markdown)", 
            type=["pdf", "docx", "md"],
            help="Le CV sera converti en markdown pour analyse"
        )
        
        st.subheader("🏢 2. Informations sur l'entreprise")
        company_url = st.text_input(
            "Nom de l'entreprise",
            placeholder="netflix"
        )
        
        st.subheader("📋 3. Description du poste")
        job_description = st.text_area(
            "Colle le contenu d'une annonce ou le nom du job que tu cherches par exemple *Maître du monde car le patron est sympa*",
            height=200,
            placeholder="Description du poste, missions, compétences requises... Fonctionne aussi pour une candidature spontannée"
        )
        st.subheader("⚙️ Options de sortie")
        include_draft = st.checkbox(
            "Inclure le 1er jet (brouillon) dans le Word ?", 
            value=True,
            help="Ajoute la version brute (avant relecture) à la fin du document. Utile pour récupérer des idées coupées."
        )
        submitted = st.form_submit_button("🚀 Générer la lettre de motivation", type="primary")
    
    if submitted:
        if not cv_file:
            st.error("❌ On t'a dit de charger ton CV")
        elif not company_url:
            st.error("❌ Les bots ont besoin du nom de la boîte")
        elif not job_description:
            st.error("❌ Donne le nom du job pour lequel tu postules ou l'annonce")
        else:
            with st.spinner("Génération en cours... Cela peut prendre 2-3 minutes."):
                try:
                    # Étape 1: Conversion du CV
                    st.info("📊 Conversion et analyse du CV...")
                    cv_path = utils.convert_cv_to_md(cv_file)
                    
                    if not cv_path:
                        st.error("Erreur lors de la conversion du CV")
                        st.stop()
                    
                    # Étape 2: Chargement des agents avec températures dynamiques
                    st.info("🤖 Configuration des agents IA...")

                    candidate_profile = candidate_profile + ". Important utiliser les principes de ponctuation et d'orthographe en français : pas de tiret semi-quadratin, majuscules uniquement pour les nom propres et en début de phrase."

                    context = {
                        "candidate_profile": candidate_profile or "Candidat",
                        "cv_path": cv_path,
                        "company_url": company_url,
                        "hiring_needs": job_description,
                        "gender": gender_option
                    }
                    agents = utils.load_agents_from_yaml("agents.yaml", temperatures, context)

                    # Étape 3: Chargement des tâches
                    st.info("📝 Préparation des tâches...")
                    tasks = utils.load_tasks_from_yaml("tasks.yaml", context)
                    
                    # Assigner les agents aux tâches
                    task_agent_mapping = [
                        ("research_agent", "company_culture_task"),
                        ("research_agent", "role_requirements_task"),
                        ("cv_extractor", "cv_analyzer_task"),
                        ("writer_agent", "draft_letter_task"),
                        ("review_agent", "review_letter_task")
                    ]
                    
                    for agent_name, task_name in task_agent_mapping:
                        task_idx = ["company_culture_task", "role_requirements_task", "cv_analyzer_task", "draft_letter_task", "review_letter_task"].index(task_name)
                        tasks[task_idx].agent = agents[agent_name]
                    
                    # Définir les dépendances entre tâches
                    tasks[3].context = [tasks[2]]  # draft_letter_task dépend de cv_analyzer_task
                    tasks[4].context = [tasks[3]]  # review_letter_task dépend de draft_letter_task
                    
                    # Étape 4: Exécution du crew
                    st.info("🎯 Génération de la lettre de motivation...")
                    crew = Crew(
                        agents=list(agents.values()),
                        tasks=tasks,
                        verbose=True
                    )
                    
                    result = crew.kickoff()
                    
                    # Étape 5: Affichage du résultat
                    st.success("✅ Lettre générée avec succès!")
                    
                    st.subheader("📄 Lettre de motivation générée")
                    st.markdown(result)
                    
                    # --- SECTION TÉLÉCHARGEMENT ---
                    col_dl_1, col_dl_2, col_coffee = st.columns(3)

                    with col_dl_1:
                        st.download_button(
                            label="📥 Télécharger (Markdown)",
                            data=str(result),
                            file_name="lettre_motivation.md",
                            mime="text/markdown"
                        )

                    with col_dl_2:
                        final_text = str(result)

                        # Récupération du texte brouillon (Task index 3 = draft_letter_task)
                        draft_text = str(tasks[3].output) if include_draft else None
                    with col_dl_2:
                # 1. Préparer les paramètres à sauvegarder ; à voir si on se créerait pas une petite base dans bigquery (avec une note)
                # On rassemble tout ce qui est pertinent
                        session_params = {
                        "Entreprise": company_url,
                        "Genre Candidat": gender_option, # Assure-toi que cette variable est accessible ici
                        "Profil Candidat": candidate_profile,
                        "Température Recherche": temperatures["research_agent"],
                        "Température Extracteur CV": temperatures["cv_extractor"],
                        "Température Rédacteur": temperatures["writer_agent"],
                        "Température Relecteur": temperatures["review_agent"],
                        "Description du poste": job_description[:500] + "..." if len(job_description) > 500 else job_description # On tronque si c'est immense
                    }

                        # On génère le fichier Word à la volée
                        docx_file = utils.create_docx(final_text, draft_text, session_params) 
                        
                        
                        
                        st.download_button(
                            label="📄 Télécharger (Word .docx)",
                            data=docx_file,
                            file_name="lettre_motivation.docx",
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                        )
                    with col_coffee:
                        st.markdown('Si vous trouvez cette app utile')
                        utils.show_buy_me_coffee()

                    
                    # Optionnel: Afficher le fichier généré
                    if include_draft and draft_text:
                        with st.expander("👀 Voir le brouillon brut (Debug)"):
                            st.markdown(draft_text)
                            # if os.path.exists("candidature.md"):
                            #     with open("candidature.md", "r") as f:
                            #         st.text_area("Version détaillée (debug)", f.read(), height=300)
                
                except Exception as e:
                    st.error(f"❌ Une erreur s'est produite: {str(e)}")
                    st.exception(e)

# Footer
st.markdown("---")
# ==========================================
# FOOTER (toujours visible en bas)
# ==========================================



st.markdown("""
<div style="text-align: center; margin-top: 50px; padding: 20px; border-top: 1px solid #eee; font-size: 0.9em; color: #666;">
    <p>❤️ Fait avec amour et beaucoup de rigolade par <strong>Caro MS</strong>
   qui cherche un taff de data scientist, AI engineer <strong>EN REMOTE</strong> 4 jours par semaine</p>
    <p style="margin-top: 15px;">
        <a href="mailto:caro.ms@people2meet.co" style="text-decoration: none; color: #666; vertical-align: middle;">
            <svg style="width: 20px; height: 20px; vertical-align: middle; margin-right: 2px;" viewBox="0 0 24 24" fill="currentColor">
                <path d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/>
            </svg>
            Email
        </a>  | 
        🌐 <a href="https://www.people2meet.co" target="_blank" style="text-decoration: none; color: #666;">people2meet.co</a> | 
        <a href="https://www.linkedin.com/in/caroline-heymes/" target="_blank" style="text-decoration: none; color: #0066cc; vertical-align: middle;">
            <svg style="width: 20px; height: 20px; vertical-align: middle; margin-right: 2px;" viewBox="0 0 24 24" fill="currentColor">
                <path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/>
            </svg>
            LinkedIn
        </a> | 
        <a href="https://github.com/caroheymes" target="_blank" style="text-decoration: none; color: #333; vertical-align: middle;">
            <svg style="width: 20px; height: 20px; vertical-align: middle; margin-right: 2px;" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
            </svg>
            GitHub
        </a>
    </p>
</div>
""", unsafe_allow_html=True)

st.caption("Powered byCrewAI, Ollama (kimi-k2-thinking) | Déployé sur Cloud Run")
