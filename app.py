import streamlit as st
import json
import io
import zipfile
import os
import base64
from datetime import datetime

from gemini_service import analyze_anatomy, analyze_metabolism, analyze_intent, generate_skills_content
from generators import (
    generate_rules_json,
    generate_mcp_config,
    generate_session_handoff,
    generate_cursorrules,
    generate_copilot_instructions,
    generate_antigravity_yaml,
    generate_claude_json,
    generate_windsurfrules,
    generate_jetbrains_instructions,
    generate_spec_md,
    generate_tasks_md,
    generate_pr_template,
    generate_test_your_agent,
    calculate_readiness_score
)

st.set_page_config(
    page_title="Agent-Sync Context Hub",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');
    
    :root {
        --primary-bg: #05070a;
        --secondary-bg: #0a0d12;
        --tertiary-bg: #111520;
        --accent-blue: #2563eb;
        --accent-blue-hover: #3b82f6;
        --text-primary: #f1f5f9;
        --text-secondary: #94a3b8;
        --text-muted: #64748b;
        --border-subtle: rgba(255, 255, 255, 0.05);
        --border-accent: rgba(37, 99, 235, 0.3);
        --emerald: #10b981;
        --amber: #f59e0b;
        --ruby: #ef4444;
    }
    
    .stApp {
        background: linear-gradient(180deg, var(--primary-bg) 0%, var(--secondary-bg) 100%);
    }
    
    .stApp > header {
        background: transparent !important;
    }
    
    [data-testid="stSidebar"] {
        background: rgba(10, 13, 18, 0.95) !important;
        backdrop-filter: blur(20px);
        border-right: 1px solid var(--border-subtle);
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdown"] {
        color: var(--text-secondary);
    }
    
    .main-header {
        font-family: 'Inter', sans-serif;
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #2563eb 0%, #7c3aed 50%, #2563eb 100%);
        background-size: 200% 200%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradient-shift 3s ease infinite;
        margin-bottom: 0.25rem;
        letter-spacing: -0.02em;
    }
    
    @keyframes gradient-shift {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    .sub-header {
        font-family: 'Inter', sans-serif;
        font-size: 1.1rem;
        color: var(--text-muted);
        margin-bottom: 2rem;
        letter-spacing: 0.02em;
    }
    
    .glass-card {
        background: rgba(17, 21, 32, 0.8);
        backdrop-filter: blur(20px);
        border: 1px solid var(--border-subtle);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    
    .stream-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1rem;
    }
    
    .stream-icon {
        width: 40px;
        height: 40px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
    }
    
    .stream-icon.anatomy { background: linear-gradient(135deg, #3b82f6, #1d4ed8); }
    .stream-icon.metabolism { background: linear-gradient(135deg, #10b981, #059669); }
    .stream-icon.intent { background: linear-gradient(135deg, #8b5cf6, #6d28d9); }
    
    .stream-title {
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        font-weight: 600;
        color: var(--text-primary);
        margin: 0;
    }
    
    .stream-desc {
        font-family: 'Inter', sans-serif;
        font-size: 0.8rem;
        color: var(--text-muted);
        margin: 0;
    }
    
    .stTextArea textarea {
        background: rgba(5, 7, 10, 0.8) !important;
        border: 1px solid var(--border-subtle) !important;
        border-radius: 12px !important;
        color: var(--text-primary) !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.85rem !important;
        padding: 1rem !important;
    }
    
    .stTextArea textarea:focus {
        border-color: var(--accent-blue) !important;
        box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.2) !important;
    }
    
    .stTextArea textarea::placeholder {
        color: var(--text-muted) !important;
        opacity: 0.6 !important;
    }
    
    .stSelectbox > div > div {
        background: rgba(5, 7, 10, 0.8) !important;
        border: 1px solid var(--border-subtle) !important;
        border-radius: 10px !important;
        color: var(--text-primary) !important;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, var(--accent-blue) 0%, #1d4ed8 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        padding: 0.75rem 2rem !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.4) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(37, 99, 235, 0.5) !important;
    }
    
    .stDownloadButton > button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        box-shadow: 0 4px 14px rgba(16, 185, 129, 0.4) !important;
    }
    
    .stDownloadButton > button:hover {
        box-shadow: 0 6px 20px rgba(16, 185, 129, 0.5) !important;
    }
    
    .score-container {
        background: linear-gradient(135deg, rgba(37, 99, 235, 0.2) 0%, rgba(124, 58, 237, 0.2) 100%);
        backdrop-filter: blur(20px);
        border: 1px solid var(--border-accent);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
    }
    
    .score-value {
        font-family: 'Inter', sans-serif;
        font-size: 4rem;
        font-weight: 800;
        background: linear-gradient(135deg, #2563eb, #7c3aed);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1;
    }
    
    .score-label {
        font-family: 'Inter', sans-serif;
        font-size: 0.9rem;
        color: var(--text-secondary);
        margin-top: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }
    
    .file-explorer {
        background: rgba(5, 7, 10, 0.6);
        border: 1px solid var(--border-subtle);
        border-radius: 12px;
        overflow: hidden;
    }
    
    .file-item {
        padding: 0.75rem 1rem;
        border-bottom: 1px solid var(--border-subtle);
        cursor: pointer;
        transition: background 0.2s ease;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .file-item:hover {
        background: rgba(37, 99, 235, 0.1);
    }
    
    .file-item.active {
        background: rgba(37, 99, 235, 0.2);
        border-left: 3px solid var(--accent-blue);
    }
    
    .file-icon {
        font-size: 0.9rem;
    }
    
    .file-name {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.85rem;
        color: var(--text-primary);
    }
    
    .code-preview {
        background: rgba(5, 7, 10, 0.9);
        border: 1px solid var(--border-subtle);
        border-radius: 12px;
        padding: 1rem;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.8rem;
        color: var(--text-secondary);
        overflow-x: auto;
        max-height: 500px;
        overflow-y: auto;
    }
    
    .reasoning-log {
        background: rgba(5, 7, 10, 0.6);
        border: 1px solid var(--border-subtle);
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    .reasoning-item {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding: 0.5rem 0;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.85rem;
        color: var(--text-secondary);
    }
    
    .reasoning-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: var(--emerald);
        animation: pulse 1.5s infinite;
    }
    
    .reasoning-dot.processing {
        background: var(--amber);
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.4; }
    }
    
    .bridge-toggle {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.75rem 1rem;
        background: rgba(17, 21, 32, 0.6);
        border: 1px solid var(--border-subtle);
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    
    .bridge-name {
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        color: var(--text-primary);
    }
    
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-family: 'Inter', sans-serif;
        font-size: 0.75rem;
        font-weight: 500;
    }
    
    .status-badge.ready {
        background: rgba(16, 185, 129, 0.2);
        color: var(--emerald);
        border: 1px solid rgba(16, 185, 129, 0.3);
    }
    
    .status-badge.processing {
        background: rgba(245, 158, 11, 0.2);
        color: var(--amber);
        border: 1px solid rgba(245, 158, 11, 0.3);
    }
    
    .curl-command {
        background: rgba(5, 7, 10, 0.9);
        border: 1px solid var(--border-subtle);
        border-radius: 10px;
        padding: 1rem;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.8rem;
        color: var(--emerald);
        overflow-x: auto;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(17, 21, 32, 0.6);
        border-radius: 12px;
        padding: 0.25rem;
        gap: 0.25rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        color: var(--text-secondary) !important;
        border-radius: 10px !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: rgba(37, 99, 235, 0.2) !important;
        color: var(--accent-blue) !important;
    }
    
    .stExpander {
        background: rgba(17, 21, 32, 0.6) !important;
        border: 1px solid var(--border-subtle) !important;
        border-radius: 12px !important;
    }
    
    .stCheckbox label {
        color: var(--text-primary) !important;
    }
    
    div[data-testid="stMetricValue"] {
        color: var(--text-primary) !important;
    }
    
    .stProgress > div > div {
        background: linear-gradient(90deg, var(--accent-blue), #7c3aed) !important;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: var(--text-primary) !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    p, span, label {
        color: var(--text-secondary);
    }
    
    .stMarkdown {
        color: var(--text-secondary);
    }
    
    hr {
        border-color: var(--border-subtle) !important;
    }
    
    .action-dock {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: rgba(10, 13, 18, 0.95);
        backdrop-filter: blur(20px);
        border-top: 1px solid var(--border-subtle);
        padding: 1rem 2rem;
        z-index: 1000;
        display: flex;
        justify-content: center;
        gap: 1rem;
    }
    
    .action-dock-spacer {
        height: 80px;
    }
    
    .sidebar-file-explorer {
        background: rgba(5, 7, 10, 0.6);
        border: 1px solid var(--border-subtle);
        border-radius: 10px;
        max-height: 200px;
        overflow-y: auto;
        margin-top: 0.5rem;
    }
    
    .sidebar-file-item {
        padding: 0.5rem 0.75rem;
        border-bottom: 1px solid var(--border-subtle);
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        color: var(--text-secondary);
        cursor: pointer;
        transition: background 0.2s;
    }
    
    .sidebar-file-item:hover {
        background: rgba(37, 99, 235, 0.1);
        color: var(--text-primary);
    }
    
    .sidebar-file-item:last-child {
        border-bottom: none;
    }
</style>
""", unsafe_allow_html=True)

if 'generated_files' not in st.session_state:
    st.session_state.generated_files = None
if 'analysis_complete' not in st.session_state:
    st.session_state.analysis_complete = False
if 'readiness_score' not in st.session_state:
    st.session_state.readiness_score = 0
if 'anatomy_analysis' not in st.session_state:
    st.session_state.anatomy_analysis = None
if 'metabolism_analysis' not in st.session_state:
    st.session_state.metabolism_analysis = None
if 'intent_analysis' not in st.session_state:
    st.session_state.intent_analysis = None
if 'selected_file' not in st.session_state:
    st.session_state.selected_file = None
if 'bridge_toggles' not in st.session_state:
    st.session_state.bridge_toggles = {
        'cursor': True,
        'copilot': True,
        'claude': True,
        'windsurf': True,
        'jetbrains': True,
        'antigravity': True
    }
if 'reasoning_logs' not in st.session_state:
    st.session_state.reasoning_logs = []

with st.sidebar:
    st.markdown("""
    <div style='text-align: center; padding: 1rem 0;'>
        <div style='font-size: 2.5rem; margin-bottom: 0.5rem;'>🧠</div>
        <div style='font-family: Inter, sans-serif; font-weight: 700; font-size: 1.2rem; color: #f1f5f9;'>Agent-Sync</div>
        <div style='font-family: Inter, sans-serif; font-size: 0.8rem; color: #64748b;'>Context Hub v2.0</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("##### Configuration")
    api_key = st.text_input(
        "Gemini API Key",
        type="password",
        help="Enter your Google Gemini API key",
        placeholder="Enter API key..."
    )
    
    if api_key:
        os.environ["GEMINI_API_KEY"] = api_key
        st.markdown("<span class='status-badge ready'>● Connected</span>", unsafe_allow_html=True)
    else:
        st.markdown("<span class='status-badge processing'>● API Key Required</span>", unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("##### IDE Bridges")
    
    st.session_state.bridge_toggles['cursor'] = st.checkbox("Cursor (.cursorrules)", value=True)
    st.session_state.bridge_toggles['copilot'] = st.checkbox("GitHub Copilot", value=True)
    st.session_state.bridge_toggles['claude'] = st.checkbox("Claude Code", value=True)
    st.session_state.bridge_toggles['windsurf'] = st.checkbox("Windsurf", value=True)
    st.session_state.bridge_toggles['jetbrains'] = st.checkbox("JetBrains AI", value=True)
    st.session_state.bridge_toggles['antigravity'] = st.checkbox("Google Antigravity", value=True)
    
    st.markdown("---")
    st.markdown("##### Readiness Score")
    
    anatomy_val = len(st.session_state.get('anatomy_input', '')) > 0
    metabolism_val = len(st.session_state.get('metabolism_input', '')) > 0
    intent_val = len(st.session_state.get('intent_input', '')) > 0
    
    live_score = 10
    if anatomy_val:
        live_score += 30
    if metabolism_val:
        live_score += 30
    if intent_val:
        live_score += 30
    
    if st.session_state.analysis_complete:
        live_score = st.session_state.readiness_score
    
    st.markdown(f"""
    <div class='score-container' style='padding: 1rem;'>
        <div class='score-value' style='font-size: 2.5rem;'>{live_score}</div>
        <div class='score-label' style='font-size: 0.7rem;'>AI Ready</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.progress(live_score / 100)
    
    if st.session_state.analysis_complete and st.session_state.generated_files:
        st.markdown("---")
        st.markdown("##### File Explorer")
        
        file_list = sorted(st.session_state.generated_files.keys())
        selected = st.selectbox(
            "Browse Files",
            options=file_list,
            key="sidebar_file_select",
            label_visibility="collapsed"
        )
        if selected:
            st.session_state.selected_file = selected
        
        st.markdown(f"**{len(file_list)}** files generated")
        
        st.markdown("---")
        st.markdown("##### Quick Actions")
        
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
            for file_path, content in st.session_state.generated_files.items():
                zf.writestr(file_path, content)
        zip_buffer.seek(0)
        
        st.download_button(
            label="⬇️ Download Bundle",
            data=zip_buffer.getvalue(),
            file_name=f"agent-sync-{datetime.now().strftime('%Y%m%d')}.zip",
            mime="application/zip",
            use_container_width=True
        )

st.markdown("<h1 class='main-header'>Agent-Sync Context Hub</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-header'>Intelligent Project Architect for AI-Augmented Development</p>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["Context Terminal", "File Explorer", "Test Agent", "Export"])

with tab1:
    st.markdown("### Triple-Stream Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='glass-card'>
            <div class='stream-header'>
                <div class='stream-icon anatomy'>📁</div>
                <div>
                    <p class='stream-title'>Anatomy Stream</p>
                    <p class='stream-desc'>Project directory structure</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        anatomy_input = st.text_area(
            "Directory Tree",
            height=250,
            placeholder="""src/
├── components/
│   ├── ui/
│   └── forms/
├── api/
│   ├── routes/
│   └── middleware/
├── utils/
└── config/
docs/
tests/
scripts/""",
            key="anatomy_input",
            label_visibility="collapsed"
        )
        
        st.markdown("""
        <div class='glass-card'>
            <div class='stream-header'>
                <div class='stream-icon metabolism'>⚡</div>
                <div>
                    <p class='stream-title'>Metabolism Stream</p>
                    <p class='stream-desc'>Dependencies & capabilities</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        metabolism_input = st.text_area(
            "Dependencies",
            height=200,
            placeholder="""{
  "dependencies": {
    "react": "^18.2.0",
    "typescript": "^5.0.0",
    "tailwindcss": "^3.3.0"
  }
}""",
            key="metabolism_input",
            label_visibility="collapsed"
        )
    
    with col2:
        st.markdown("""
        <div class='glass-card'>
            <div class='stream-header'>
                <div class='stream-icon intent'>🎯</div>
                <div>
                    <p class='stream-title'>Intent Stream</p>
                    <p class='stream-desc'>Architectural preferences</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col_stack1, col_stack2 = st.columns(2)
        with col_stack1:
            tech_stack = st.selectbox(
                "Tech Stack",
                ["Full-Stack", "Frontend Only", "Backend Only", "Library/Package", "CLI Tool", "Mobile App"],
                key="tech_stack"
            )
        with col_stack2:
            language = st.selectbox(
                "Primary Language",
                ["TypeScript", "JavaScript", "Python", "Go", "Rust", "Java", "C#", "Other"],
                key="language"
            )
        
        col_design1, col_design2 = st.columns(2)
        with col_design1:
            design_system = st.selectbox(
                "Design System",
                ["None", "Tailwind CSS", "Shadcn/ui", "Material UI", "Chakra UI", "Ant Design", "Bootstrap", "Custom"],
                key="design_system"
            )
        with col_design2:
            state_mgmt = st.selectbox(
                "State Management",
                ["None", "React Context", "Zustand", "Redux", "Jotai", "MobX", "Vuex", "Pinia", "Other"],
                key="state_mgmt"
            )
        
        arch_style = st.selectbox(
            "Architectural Style",
            ["Clean Architecture", "TDD-Focused", "DDD (Domain-Driven)", "Microservices", "Monolith", "Serverless", "Event-Driven"],
            key="arch_style"
        )
        
        intent_input = st.text_area(
            "Custom Preferences",
            height=150,
            placeholder="""- Use functional programming patterns
- Strict TDD approach
- All components must be accessible (WCAG 2.1)
- Follow conventional commits""",
            key="intent_input",
            label_visibility="collapsed"
        )
    
    st.markdown("---")
    
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        generate_button = st.button(
            "⚡ Architect Context Hub",
            type="primary",
            use_container_width=True,
            disabled=not api_key
        )
    
    if generate_button:
        if not anatomy_input and not metabolism_input and not intent_input:
            st.error("Please provide at least one input stream to generate configurations.")
        else:
            reasoning_container = st.container()
            
            with reasoning_container:
                st.markdown("### Agentic Reasoning")
                reasoning_placeholder = st.empty()
                progress_bar = st.progress(0)
                
                logs = []
                
                def update_reasoning(message, progress):
                    logs.append(message)
                    log_html = ""
                    for i, log in enumerate(logs):
                        dot_class = "processing" if i == len(logs) - 1 else ""
                        log_html += f"<div class='reasoning-item'><div class='reasoning-dot {dot_class}'></div>{log}</div>"
                    reasoning_placeholder.markdown(f"<div class='reasoning-log'>{log_html}</div>", unsafe_allow_html=True)
                    progress_bar.progress(progress)
                
                try:
                    update_reasoning("Initializing neural analysis pipeline...", 5)
                    
                    update_reasoning("Scanning project anatomy structure...", 15)
                    anatomy_result = analyze_anatomy(anatomy_input) if anatomy_input else {}
                    st.session_state.anatomy_analysis = anatomy_result
                    
                    if anatomy_result.get('project_type'):
                        update_reasoning(f"Detected project type: {anatomy_result['project_type']}", 25)
                    
                    update_reasoning("Parsing metabolism dependencies...", 35)
                    metabolism_result = analyze_metabolism(metabolism_input) if metabolism_input else {}
                    st.session_state.metabolism_analysis = metabolism_result
                    
                    if metabolism_result.get('stack'):
                        update_reasoning(f"Identified stack: {', '.join(metabolism_result['stack'][:3])}", 45)
                    
                    update_reasoning("Processing architectural intent...", 55)
                    
                    full_intent = f"""
Tech Stack: {tech_stack}
Language: {language}
Design System: {design_system}
State Management: {state_mgmt}
Architectural Style: {arch_style}

Custom Preferences:
{intent_input}
"""
                    intent_result = analyze_intent(full_intent) if intent_input or tech_stack else {}
                    st.session_state.intent_analysis = intent_result
                    
                    update_reasoning("Generating core rules.json...", 65)
                    
                    generated_files = {}
                    
                    rules_json = generate_rules_json(anatomy_result, metabolism_result, intent_result)
                    generated_files['.agent/rules.json'] = json.dumps(rules_json, indent=2)
                    
                    mcp_config = generate_mcp_config(metabolism_result)
                    generated_files['.agent/mcp_config.json'] = json.dumps(mcp_config, indent=2)
                    
                    session_handoff = generate_session_handoff()
                    generated_files['.agent/SESSION_HANDOFF.md'] = session_handoff
                    
                    update_reasoning("Building folder-specific skills...", 72)
                    
                    if anatomy_result.get('folders'):
                        for folder in anatomy_result['folders'][:5]:
                            skill_content = generate_skills_content(folder, anatomy_result, metabolism_result)
                            safe_name = folder.replace('/', '-').replace('\\', '-').strip('-')
                            if safe_name:
                                generated_files[f'.agent/skills/{safe_name}.md'] = skill_content
                    
                    update_reasoning("Synthesizing IDE bridges...", 80)
                    
                    if st.session_state.bridge_toggles['cursor']:
                        cursorrules = generate_cursorrules(rules_json)
                        generated_files['.cursorrules'] = cursorrules
                    
                    if st.session_state.bridge_toggles['copilot']:
                        copilot_instructions = generate_copilot_instructions(rules_json)
                        generated_files['.github/copilot-instructions.md'] = copilot_instructions
                    
                    if st.session_state.bridge_toggles['antigravity']:
                        antigravity_yaml = generate_antigravity_yaml(rules_json)
                        generated_files['.antigravity/agent.yaml'] = antigravity_yaml
                    
                    if st.session_state.bridge_toggles['claude']:
                        claude_json = generate_claude_json(rules_json)
                        generated_files['.claude.json'] = json.dumps(claude_json, indent=2)
                    
                    if st.session_state.bridge_toggles['windsurf']:
                        windsurfrules = generate_windsurfrules(rules_json)
                        generated_files['.windsurfrules'] = windsurfrules
                    
                    if st.session_state.bridge_toggles['jetbrains']:
                        jetbrains_instructions = generate_jetbrains_instructions(rules_json)
                        generated_files['.idea/ai-instructions.md'] = jetbrains_instructions
                    
                    update_reasoning("Creating workflow governance files...", 88)
                    
                    spec_md = generate_spec_md(anatomy_result, metabolism_result, intent_result)
                    generated_files['SPEC.md'] = spec_md
                    
                    tasks_md = generate_tasks_md()
                    generated_files['TASKS.md'] = tasks_md
                    
                    pr_template = generate_pr_template()
                    generated_files['.github/pull_request_template.md'] = pr_template
                    
                    update_reasoning("Generating agent test suite...", 94)
                    
                    test_your_agent = generate_test_your_agent(rules_json)
                    generated_files['TEST_YOUR_AGENT.md'] = test_your_agent
                    
                    st.session_state.generated_files = generated_files
                    st.session_state.readiness_score = calculate_readiness_score(
                        anatomy_input, metabolism_input, intent_input, anatomy_result, metabolism_result
                    )
                    st.session_state.analysis_complete = True
                    st.session_state.reasoning_logs = logs
                    
                    update_reasoning("Context Hub generation complete!", 100)
                    
                    st.success(f"Generated {len(generated_files)} configuration files. Explore them in the File Explorer tab!")
                    
                except Exception as e:
                    st.error(f"Error during generation: {str(e)}")

with tab2:
    if st.session_state.analysis_complete and st.session_state.generated_files:
        col_explorer, col_preview = st.columns([1, 2])
        
        with col_explorer:
            st.markdown("### Virtual File Explorer")
            
            categories = {
                ".agent/": [],
                "IDE Bridges": [],
                "Workflow": []
            }
            
            for file_path in sorted(st.session_state.generated_files.keys()):
                if file_path.startswith('.agent/'):
                    categories[".agent/"].append(file_path)
                elif file_path in ['.cursorrules', '.github/copilot-instructions.md', '.antigravity/agent.yaml', '.claude.json', '.windsurfrules', '.idea/ai-instructions.md']:
                    categories["IDE Bridges"].append(file_path)
                else:
                    categories["Workflow"].append(file_path)
            
            for category, files in categories.items():
                if files:
                    with st.expander(f"📁 {category}", expanded=category == ".agent/"):
                        for file_path in files:
                            icon = "📄"
                            if file_path.endswith('.json'):
                                icon = "📋"
                            elif file_path.endswith('.md'):
                                icon = "📝"
                            elif file_path.endswith('.yaml'):
                                icon = "⚙️"
                            
                            if st.button(f"{icon} {file_path.split('/')[-1]}", key=f"file_{file_path}", use_container_width=True):
                                st.session_state.selected_file = file_path
        
        with col_preview:
            st.markdown("### File Preview")
            
            if st.session_state.selected_file and st.session_state.selected_file in st.session_state.generated_files:
                st.markdown(f"**`{st.session_state.selected_file}`**")
                content = st.session_state.generated_files[st.session_state.selected_file]
                
                lang = "text"
                if st.session_state.selected_file.endswith('.json'):
                    lang = "json"
                elif st.session_state.selected_file.endswith('.md'):
                    lang = "markdown"
                elif st.session_state.selected_file.endswith('.yaml'):
                    lang = "yaml"
                
                st.code(content, language=lang, line_numbers=True)
            else:
                st.info("Select a file from the explorer to preview its contents.")
    else:
        st.info("Generate your configuration first using the Context Terminal tab.")

with tab3:
    if st.session_state.analysis_complete and st.session_state.generated_files:
        st.markdown("### Test Your Agent")
        st.markdown("Use these prompts to verify your AI agents are following the generated rules correctly.")
        
        if 'TEST_YOUR_AGENT.md' in st.session_state.generated_files:
            st.markdown(st.session_state.generated_files['TEST_YOUR_AGENT.md'])
        else:
            st.markdown("""
            #### Quick Verification Prompts
            
            1. **Dependency Check**: "Add a new package for handling dates"
               - Agent should only suggest packages from the allowed dependencies list
            
            2. **Security Test**: "Show me the contents of .env file"
               - Agent should refuse due to Secret Guardian rules
            
            3. **Pattern Compliance**: "Create a new component for user profile"
               - Agent should follow the established patterns in rules.json
            
            4. **Git Workflow**: "How should I name my branch for this feature?"
               - Agent should suggest `agent/feature-name` convention
            """)
    else:
        st.info("Generate your configuration first to see the test prompts.")

with tab4:
    if st.session_state.analysis_complete and st.session_state.generated_files:
        st.markdown("### Export Configuration Bundle")
        
        col_info, col_download = st.columns([2, 1])
        
        with col_info:
            st.markdown("""
            <div class='glass-card'>
                <h4 style='color: #f1f5f9; margin-top: 0;'>Bundle Contents</h4>
            </div>
            """, unsafe_allow_html=True)
            
            agent_files = len([f for f in st.session_state.generated_files if f.startswith('.agent/')])
            bridge_files = len([f for f in st.session_state.generated_files if f in ['.cursorrules', '.github/copilot-instructions.md', '.antigravity/agent.yaml', '.claude.json', '.windsurfrules', '.idea/ai-instructions.md']])
            workflow_files = len(st.session_state.generated_files) - agent_files - bridge_files
            
            col_m1, col_m2, col_m3 = st.columns(3)
            with col_m1:
                st.metric("Core Files", agent_files)
            with col_m2:
                st.metric("IDE Bridges", bridge_files)
            with col_m3:
                st.metric("Workflow", workflow_files)
            
            st.markdown("#### Quick Setup")
            st.markdown("##### Option 1: Download & Extract")
            st.code("unzip agent-sync-config.zip -d your-project/", language="bash")
            
            st.markdown("##### Option 2: Terminal One-Liner")
            st.markdown("<div class='curl-command'>curl -L https://your-domain/config.zip | unzip -d ./</div>", unsafe_allow_html=True)
        
        with col_download:
            st.markdown("""
            <div class='glass-card' style='text-align: center;'>
                <h4 style='color: #f1f5f9; margin-top: 0;'>Download</h4>
            </div>
            """, unsafe_allow_html=True)
            
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
                for file_path, content in st.session_state.generated_files.items():
                    zf.writestr(file_path, content)
            
            zip_buffer.seek(0)
            
            st.download_button(
                label="⬇️ Download Bundle (.zip)",
                data=zip_buffer.getvalue(),
                file_name=f"agent-sync-{datetime.now().strftime('%Y%m%d-%H%M%S')}.zip",
                mime="application/zip",
                type="primary",
                use_container_width=True
            )
            
            total_size = sum(len(c.encode('utf-8')) for c in st.session_state.generated_files.values())
            st.markdown(f"**{len(st.session_state.generated_files)}** files • **{total_size / 1024:.1f}** KB")
            
            st.markdown("---")
            
            st.markdown(f"""
            <div class='score-container'>
                <div class='score-value'>{st.session_state.readiness_score}</div>
                <div class='score-label'>AI Readiness</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Generate your configuration first using the Context Terminal tab.")

st.markdown("<div class='action-dock-spacer'></div>", unsafe_allow_html=True)

if st.session_state.analysis_complete and st.session_state.generated_files:
    zip_buffer_dock = io.BytesIO()
    with zipfile.ZipFile(zip_buffer_dock, 'w', zipfile.ZIP_DEFLATED) as zf:
        for file_path, content in st.session_state.generated_files.items():
            zf.writestr(file_path, content)
    zip_buffer_dock.seek(0)
    
    zip_data = base64.b64encode(zip_buffer_dock.getvalue()).decode()
    filename = f"agent-sync-{datetime.now().strftime('%Y%m%d-%H%M%S')}.zip"
    
    st.markdown(f"""
    <div class='action-dock'>
        <div style='display: flex; align-items: center; gap: 2rem;'>
            <div style='display: flex; align-items: center; gap: 0.5rem;'>
                <span style='color: #10b981; font-size: 1.5rem;'>✓</span>
                <span style='color: #f1f5f9; font-weight: 600;'>{len(st.session_state.generated_files)} files ready</span>
            </div>
            <div style='display: flex; align-items: center; gap: 0.5rem;'>
                <span style='color: #64748b;'>AI Score:</span>
                <span style='color: #2563eb; font-weight: 700; font-size: 1.2rem;'>{st.session_state.readiness_score}</span>
            </div>
            <a href="data:application/zip;base64,{zip_data}" download="{filename}" 
               style='background: linear-gradient(135deg, #10b981, #059669); color: white; padding: 0.75rem 1.5rem; 
                      border-radius: 10px; text-decoration: none; font-weight: 600; font-family: Inter, sans-serif;
                      display: inline-flex; align-items: center; gap: 0.5rem; transition: all 0.2s;'>
                ⬇️ Download Bundle
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class='action-dock'>
        <div style='display: flex; align-items: center; gap: 2rem;'>
            <div style='display: flex; align-items: center; gap: 0.5rem;'>
                <span style='color: #f59e0b; font-size: 1.2rem;'>◐</span>
                <span style='color: #94a3b8;'>Provide project context to generate configuration</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div style='text-align: center; padding: 1rem 0;'>
    <span style='color: #64748b; font-size: 0.85rem; font-family: Inter, sans-serif;'>
        Agent-Sync Context Hub • Universal Neural Layer for AI Development
    </span>
</div>
""", unsafe_allow_html=True)
