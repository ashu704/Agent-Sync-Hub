import streamlit as st
import json
import io
import zipfile
import os
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
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #6b7280;
        margin-bottom: 2rem;
    }
    .stream-card {
        background: #f8fafc;
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid #e2e8f0;
        margin-bottom: 1rem;
    }
    .stream-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: #1e293b;
        margin-bottom: 0.5rem;
    }
    .stream-desc {
        font-size: 0.9rem;
        color: #64748b;
        margin-bottom: 1rem;
    }
    .score-container {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 16px;
        color: white;
    }
    .score-value {
        font-size: 4rem;
        font-weight: 800;
    }
    .score-label {
        font-size: 1rem;
        opacity: 0.9;
    }
    .file-preview {
        background: #1e293b;
        color: #e2e8f0;
        border-radius: 8px;
        padding: 1rem;
        font-family: 'Monaco', 'Menlo', monospace;
        font-size: 0.85rem;
        overflow-x: auto;
        max-height: 400px;
        overflow-y: auto;
    }
    .bridge-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        background: #e0e7ff;
        color: #4338ca;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 500;
        margin: 0.25rem;
    }
    .success-banner {
        background: #ecfdf5;
        border: 1px solid #a7f3d0;
        border-radius: 8px;
        padding: 1rem;
        color: #065f46;
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

with st.sidebar:
    st.markdown("### Configuration")
    
    api_key = st.text_input(
        "Gemini API Key",
        type="password",
        help="Enter your Google Gemini API key to enable AI-powered analysis"
    )
    
    if api_key:
        os.environ["GEMINI_API_KEY"] = api_key
        st.success("API Key configured")
    else:
        st.warning("Enter API key to enable AI features")
    
    st.markdown("---")
    st.markdown("### About")
    st.markdown("""
    **Agent-Sync Context Hub** provides a Universal Neural Layer for your repositories.
    
    It solves:
    - Agent Amnesia
    - IDE Fragmentation
    
    By creating a single source of truth for all AI coding assistants.
    """)
    
    st.markdown("---")
    st.markdown("### Supported Tools")
    tools = ["Cursor", "GitHub Copilot", "Claude Code", "Windsurf", "JetBrains AI", "Google Antigravity"]
    for tool in tools:
        st.markdown(f"<span class='bridge-badge'>{tool}</span>", unsafe_allow_html=True)

st.markdown("<h1 class='main-header'>Agent-Sync Context Hub</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-header'>Universal Neural Layer for AI-Powered Development</p>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["Input Streams", "Generated Files", "Export"])

with tab1:
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### Anatomy Stream (Structure)")
        st.markdown("<p class='stream-desc'>Paste your project directory tree (e.g., output of `tree -L 3`)</p>", unsafe_allow_html=True)
        anatomy_input = st.text_area(
            "Directory Tree",
            height=300,
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
            key="anatomy"
        )
    
    with col2:
        st.markdown("#### Metabolism Stream (Capabilities)")
        st.markdown("<p class='stream-desc'>Paste your dependency files (package.json, requirements.txt, etc.)</p>", unsafe_allow_html=True)
        metabolism_input = st.text_area(
            "Dependencies",
            height=300,
            placeholder="""{
  "name": "my-project",
  "dependencies": {
    "react": "^18.2.0",
    "typescript": "^5.0.0",
    "tailwindcss": "^3.3.0",
    "axios": "^1.4.0"
  },
  "devDependencies": {
    "jest": "^29.0.0",
    "eslint": "^8.0.0"
  }
}""",
            key="metabolism"
        )
    
    with col3:
        st.markdown("#### Intent Stream (Preferences)")
        st.markdown("<p class='stream-desc'>Describe your coding style, patterns, and constraints</p>", unsafe_allow_html=True)
        intent_input = st.text_area(
            "Custom Preferences",
            height=300,
            placeholder="""- Use functional programming patterns
- Strict TDD approach
- Tailwind CSS only (no inline styles)
- TypeScript strict mode
- All components must be accessible (WCAG 2.1)
- Use React Query for data fetching
- Follow conventional commits""",
            key="intent"
        )
    
    st.markdown("---")
    
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        generate_button = st.button(
            "Generate Agent Configuration",
            type="primary",
            use_container_width=True,
            disabled=not api_key
        )
    
    if generate_button:
        if not anatomy_input and not metabolism_input and not intent_input:
            st.error("Please provide at least one input stream to generate configurations.")
        else:
            with st.spinner("Analyzing your project with Gemini AI..."):
                try:
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    status_text.text("Analyzing project anatomy...")
                    anatomy_result = analyze_anatomy(anatomy_input) if anatomy_input else {}
                    st.session_state.anatomy_analysis = anatomy_result
                    progress_bar.progress(25)
                    
                    status_text.text("Detecting technology stack...")
                    metabolism_result = analyze_metabolism(metabolism_input) if metabolism_input else {}
                    st.session_state.metabolism_analysis = metabolism_result
                    progress_bar.progress(50)
                    
                    status_text.text("Processing intent preferences...")
                    intent_result = analyze_intent(intent_input) if intent_input else {}
                    st.session_state.intent_analysis = intent_result
                    progress_bar.progress(75)
                    
                    status_text.text("Generating configuration files...")
                    
                    generated_files = {}
                    
                    rules_json = generate_rules_json(anatomy_result, metabolism_result, intent_result)
                    generated_files['.agent/rules.json'] = json.dumps(rules_json, indent=2)
                    
                    mcp_config = generate_mcp_config(metabolism_result)
                    generated_files['.agent/mcp_config.json'] = json.dumps(mcp_config, indent=2)
                    
                    session_handoff = generate_session_handoff()
                    generated_files['.agent/SESSION_HANDOFF.md'] = session_handoff
                    
                    if anatomy_result.get('folders'):
                        for folder in anatomy_result['folders'][:5]:
                            skill_content = generate_skills_content(folder, anatomy_result, metabolism_result)
                            safe_name = folder.replace('/', '-').replace('\\', '-').strip('-')
                            if safe_name:
                                generated_files[f'.agent/skills/{safe_name}.md'] = skill_content
                    
                    cursorrules = generate_cursorrules(rules_json)
                    generated_files['.cursorrules'] = cursorrules
                    
                    copilot_instructions = generate_copilot_instructions(rules_json)
                    generated_files['.github/copilot-instructions.md'] = copilot_instructions
                    
                    antigravity_yaml = generate_antigravity_yaml(rules_json)
                    generated_files['.antigravity/agent.yaml'] = antigravity_yaml
                    
                    claude_json = generate_claude_json(rules_json)
                    generated_files['.claude.json'] = json.dumps(claude_json, indent=2)
                    
                    windsurfrules = generate_windsurfrules(rules_json)
                    generated_files['.windsurfrules'] = windsurfrules
                    
                    jetbrains_instructions = generate_jetbrains_instructions(rules_json)
                    generated_files['.idea/ai-instructions.md'] = jetbrains_instructions
                    
                    spec_md = generate_spec_md(anatomy_result, metabolism_result, intent_result)
                    generated_files['SPEC.md'] = spec_md
                    
                    tasks_md = generate_tasks_md()
                    generated_files['TASKS.md'] = tasks_md
                    
                    pr_template = generate_pr_template()
                    generated_files['.github/pull_request_template.md'] = pr_template
                    
                    st.session_state.generated_files = generated_files
                    st.session_state.readiness_score = calculate_readiness_score(
                        anatomy_input, metabolism_input, intent_input, anatomy_result, metabolism_result
                    )
                    st.session_state.analysis_complete = True
                    
                    progress_bar.progress(100)
                    status_text.text("Generation complete!")
                    
                    st.success("Configuration generated successfully! Check the 'Generated Files' and 'Export' tabs.")
                    
                except Exception as e:
                    st.error(f"Error during generation: {str(e)}")

with tab2:
    if st.session_state.analysis_complete and st.session_state.generated_files:
        col_score, col_files = st.columns([1, 3])
        
        with col_score:
            st.markdown(f"""
            <div class='score-container'>
                <div class='score-value'>{st.session_state.readiness_score}</div>
                <div class='score-label'>AI Readiness Score</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            st.markdown("#### Analysis Summary")
            
            if st.session_state.anatomy_analysis:
                st.markdown(f"**Project Type:** {st.session_state.anatomy_analysis.get('project_type', 'Unknown')}")
                folders = st.session_state.anatomy_analysis.get('folders', [])
                st.markdown(f"**Key Folders:** {len(folders)}")
            
            if st.session_state.metabolism_analysis:
                deps = st.session_state.metabolism_analysis.get('dependencies', [])
                st.markdown(f"**Dependencies:** {len(deps)}")
                stack = st.session_state.metabolism_analysis.get('stack', [])
                if stack:
                    st.markdown(f"**Tech Stack:** {', '.join(stack[:5])}")
        
        with col_files:
            st.markdown("### Generated Files")
            
            file_categories = {
                "Core (.agent/)": [f for f in st.session_state.generated_files.keys() if f.startswith('.agent/')],
                "AI Tool Bridges": [f for f in st.session_state.generated_files.keys() if f in ['.cursorrules', '.github/copilot-instructions.md', '.antigravity/agent.yaml', '.claude.json', '.windsurfrules', '.idea/ai-instructions.md']],
                "Workflow & Governance": [f for f in st.session_state.generated_files.keys() if f in ['SPEC.md', 'TASKS.md', '.github/pull_request_template.md']]
            }
            
            for category, files in file_categories.items():
                if files:
                    with st.expander(f"{category} ({len(files)} files)", expanded=category == "Core (.agent/)"):
                        for file_path in sorted(files):
                            st.markdown(f"**`{file_path}`**")
                            content = st.session_state.generated_files[file_path]
                            st.code(content[:2000] + ("..." if len(content) > 2000 else ""), language="json" if file_path.endswith('.json') else "markdown")
    else:
        st.info("Generate your configuration first using the 'Input Streams' tab.")

with tab3:
    if st.session_state.analysis_complete and st.session_state.generated_files:
        st.markdown("### Export Configuration")
        
        st.markdown("""
        <div class='success-banner'>
            Your Agent-Sync configuration is ready for export. Download the ZIP file and extract it to your project root.
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        col_info, col_download = st.columns([2, 1])
        
        with col_info:
            st.markdown("#### What's Included")
            st.markdown(f"""
            - **{len([f for f in st.session_state.generated_files if f.startswith('.agent/')])}** core configuration files
            - **6** AI tool bridge configurations
            - **3** workflow governance files
            - Complete `.agent/` ecosystem
            """)
            
            st.markdown("#### Installation")
            st.code("""
# Extract to your project root
unzip agent-sync-config.zip -d your-project/

# Verify installation
ls -la your-project/.agent/
            """, language="bash")
        
        with col_download:
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
                for file_path, content in st.session_state.generated_files.items():
                    zf.writestr(file_path, content)
            
            zip_buffer.seek(0)
            
            st.download_button(
                label="Download ZIP",
                data=zip_buffer.getvalue(),
                file_name=f"agent-sync-config-{datetime.now().strftime('%Y%m%d-%H%M%S')}.zip",
                mime="application/zip",
                type="primary",
                use_container_width=True
            )
            
            st.markdown(f"**Total Files:** {len(st.session_state.generated_files)}")
            total_size = sum(len(c.encode('utf-8')) for c in st.session_state.generated_files.values())
            st.markdown(f"**Total Size:** {total_size / 1024:.1f} KB")
    else:
        st.info("Generate your configuration first using the 'Input Streams' tab.")

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #6b7280; font-size: 0.9rem;'>
    Agent-Sync Context Hub | Universal Neural Layer for AI Development
</div>
""", unsafe_allow_html=True)
