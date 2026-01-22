import json
import os
import re
from typing import Dict, Any, List

from google import genai
from google.genai import types


def get_client():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not configured")
    return genai.Client(api_key=api_key)


def analyze_anatomy(tree_input: str) -> Dict[str, Any]:
    """Analyze project directory tree to detect structure and patterns."""
    if not tree_input.strip():
        return {}
    
    client = get_client()
    
    prompt = f"""Analyze this project directory tree and provide a structured analysis.

Directory Tree:
{tree_input}

Provide a JSON response with the following structure:
{{
    "project_type": "monorepo|microservice|single-app|library|unknown",
    "folders": ["list of key folder names"],
    "patterns": {{
        "has_frontend": true/false,
        "has_backend": true/false,
        "has_tests": true/false,
        "has_docs": true/false,
        "has_infra": true/false,
        "has_scripts": true/false
    }},
    "folder_purposes": {{
        "folder_name": "brief description of purpose"
    }},
    "architecture_notes": ["list of architectural observations"]
}}

Return ONLY valid JSON, no markdown formatting."""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )
        
        if response.text:
            text = response.text.strip()
            if text.startswith("```"):
                text = re.sub(r'^```(?:json)?\n?', '', text)
                text = re.sub(r'\n?```$', '', text)
            return json.loads(text)
    except Exception as e:
        print(f"Anatomy analysis error: {e}")
    
    folders = []
    for line in tree_input.split('\n'):
        clean = line.strip().replace('├──', '').replace('└──', '').replace('│', '').replace('─', '').strip()
        if clean and '.' not in clean:
            folders.append(clean.rstrip('/'))
    
    return {
        "project_type": "unknown",
        "folders": folders[:10],
        "patterns": {
            "has_frontend": any(f in tree_input.lower() for f in ['components', 'ui', 'frontend', 'client']),
            "has_backend": any(f in tree_input.lower() for f in ['api', 'server', 'backend', 'routes']),
            "has_tests": 'test' in tree_input.lower(),
            "has_docs": 'doc' in tree_input.lower(),
            "has_infra": any(f in tree_input.lower() for f in ['infra', 'deploy', 'k8s', 'docker']),
            "has_scripts": 'script' in tree_input.lower()
        },
        "folder_purposes": {},
        "architecture_notes": []
    }


def analyze_metabolism(deps_input: str) -> Dict[str, Any]:
    """Analyze dependency files to detect technology stack."""
    if not deps_input.strip():
        return {}
    
    client = get_client()
    
    prompt = f"""Analyze these dependency files and identify the technology stack.

Dependencies:
{deps_input}

Provide a JSON response with the following structure:
{{
    "stack": ["list of main technologies/frameworks"],
    "dependencies": ["list of all dependency names"],
    "dev_dependencies": ["list of dev dependency names"],
    "language": "primary programming language",
    "framework": "main framework if any",
    "testing_tools": ["list of testing frameworks"],
    "build_tools": ["list of build tools"],
    "suggested_mcp_servers": ["github", "filesystem", "browser", "database"],
    "allowed_dependencies_rule": "description of what dependencies are allowed"
}}

Return ONLY valid JSON, no markdown formatting."""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )
        
        if response.text:
            text = response.text.strip()
            if text.startswith("```"):
                text = re.sub(r'^```(?:json)?\n?', '', text)
                text = re.sub(r'\n?```$', '', text)
            return json.loads(text)
    except Exception as e:
        print(f"Metabolism analysis error: {e}")
    
    deps = []
    stack = []
    
    try:
        pkg = json.loads(deps_input)
        if 'dependencies' in pkg:
            deps.extend(pkg['dependencies'].keys())
        if 'devDependencies' in pkg:
            deps.extend(pkg['devDependencies'].keys())
        
        if 'react' in deps:
            stack.append('React')
        if 'vue' in deps:
            stack.append('Vue')
        if 'express' in deps:
            stack.append('Express')
        if 'typescript' in deps:
            stack.append('TypeScript')
    except:
        for line in deps_input.split('\n'):
            if '==' in line or '>=' in line:
                dep = line.split('==')[0].split('>=')[0].strip()
                if dep:
                    deps.append(dep)
    
    return {
        "stack": stack if stack else ["Unknown"],
        "dependencies": deps,
        "dev_dependencies": [],
        "language": "JavaScript" if 'package.json' in deps_input or 'react' in deps_input.lower() else "Python" if 'requirements' in deps_input.lower() else "Unknown",
        "framework": stack[0] if stack else "Unknown",
        "testing_tools": [],
        "build_tools": [],
        "suggested_mcp_servers": ["github", "filesystem"],
        "allowed_dependencies_rule": "Only use dependencies listed in the project configuration"
    }


def analyze_intent(intent_input: str) -> Dict[str, Any]:
    """Analyze user intent and preferences."""
    if not intent_input.strip():
        return {}
    
    client = get_client()
    
    prompt = f"""Analyze these coding preferences and constraints.

User Preferences:
{intent_input}

Provide a JSON response with the following structure:
{{
    "coding_style": "functional|oop|mixed",
    "testing_approach": "tdd|bdd|minimal|none",
    "styling_constraints": ["list of styling rules"],
    "accessibility_requirements": ["list of a11y requirements"],
    "patterns_to_follow": ["list of patterns to follow"],
    "patterns_to_avoid": ["list of anti-patterns to avoid"],
    "commit_conventions": "conventional|custom|none",
    "documentation_requirements": ["list of doc requirements"],
    "quality_gates": ["list of quality requirements"]
}}

Return ONLY valid JSON, no markdown formatting."""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )
        
        if response.text:
            text = response.text.strip()
            if text.startswith("```"):
                text = re.sub(r'^```(?:json)?\n?', '', text)
                text = re.sub(r'\n?```$', '', text)
            return json.loads(text)
    except Exception as e:
        print(f"Intent analysis error: {e}")
    
    return {
        "coding_style": "mixed",
        "testing_approach": "minimal",
        "styling_constraints": [],
        "accessibility_requirements": [],
        "patterns_to_follow": [],
        "patterns_to_avoid": [],
        "commit_conventions": "conventional",
        "documentation_requirements": [],
        "quality_gates": []
    }


def generate_skills_content(folder: str, anatomy: Dict, metabolism: Dict) -> str:
    """Generate skill file content for a specific folder."""
    client = get_client()
    
    folder_purpose = anatomy.get('folder_purposes', {}).get(folder, '')
    stack = metabolism.get('stack', [])
    
    prompt = f"""Generate a skill file for AI agents working in the "{folder}" directory.

Context:
- Folder purpose: {folder_purpose if folder_purpose else 'General project folder'}
- Tech stack: {', '.join(stack) if stack else 'Not specified'}
- Project type: {anatomy.get('project_type', 'Unknown')}

Create a markdown skill file that includes:
1. A brief description of this folder's purpose
2. Key patterns and conventions to follow
3. Common tasks and how to approach them
4. Files and patterns to be aware of
5. Do's and Don'ts for this directory

Format as clean markdown. Be specific and actionable."""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        
        if response.text:
            return response.text
    except Exception as e:
        print(f"Skills generation error: {e}")
    
    return f"""# {folder.title()} Directory Skills

## Purpose
This directory contains {folder_purpose if folder_purpose else 'project-specific code and resources'}.

## Conventions
- Follow the project's established patterns
- Maintain consistency with existing code
- Document significant changes

## Do's
- Review existing code before making changes
- Follow the project's coding standards
- Write tests for new functionality

## Don'ts
- Don't introduce new dependencies without approval
- Don't modify shared utilities without coordination
- Don't bypass established patterns
"""
