import json
import re
import logging
from typing import Dict, Any, List
from langgraph.graph import StateGraph, START, END
from app.graph.state import CareerStoryState
from app.core.llm import LLMAdapterFactory
from app.graph.prompts import (
    DIRECTOR_SYSTEM_PROMPT,
    SCENARIO_SYSTEM_PROMPT,
    VISUAL_MATCH_SYSTEM_PROMPT
)

logger = logging.getLogger(__name__)

def extract_json_from_llm_response(text: str) -> Dict[str, Any]:
    """
    Cleans markdown codeblocks and parses JSON, handling control characters and substring boundaries cleanly.
    """
    cleaned = text.strip()
    
    # 1. Check for markdown codeblocks ```json ... ```
    if "```" in cleaned:
        blocks = re.findall(r"```(?:json)?\s*(\{.*?\})\s*```", cleaned, re.DOTALL | re.IGNORECASE)
        if blocks:
            cleaned = blocks[0].strip()
        else:
            cleaned = re.sub(r"^```(?:json)?\n?", "", cleaned, flags=re.IGNORECASE)
            cleaned = re.sub(r"\n?```$", "", cleaned).strip()

    # 2. Try direct JSON parse with strict=False
    try:
        return json.loads(cleaned, strict=False)
    except Exception:
        pass

    # 3. Extract substring between first '{' and last '}'
    start_idx = cleaned.find("{")
    end_idx = cleaned.rfind("}")
    if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
        candidate = cleaned[start_idx:end_idx + 1]
        try:
            return json.loads(candidate, strict=False)
        except Exception:
            # Fallback: strip unescaped control characters
            sanitized = re.sub(r'[\x00-\x1F\x7F-\x9F]', '', candidate)
            return json.loads(sanitized, strict=False)

    raise ValueError(f"Could not parse valid JSON from text: {text[:150]}")

async def director_node(state: CareerStoryState) -> Dict[str, Any]:
    """
    🤖 Agent 1: The Director Model (DirectorAgent)
    Uses DeepSeek / Gemini to analyze user profile and construct strategic recommendations.
    """
    logger.info("Executing DirectorAgent node with live LLM...")
    profile = state.get("user_profile", {})
    custom_instructions = state.get("custom_instructions") or "None"
    errors: List[str] = list(state.get("errors", []))

    prompt = DIRECTOR_SYSTEM_PROMPT.format(
        name=profile.get("name", "Student/Job Seeker"),
        academic_background=profile.get("academic_background", "General Background"),
        skills=", ".join(profile.get("skills", ["Problem Solving"])),
        personality_traits=", ".join(profile.get("personality_traits", ["Adaptable"])),
        preferred_working_style=profile.get("preferred_working_style", "Hybrid"),
        target_region=profile.get("target_region", "Regional Hub"),
        target_field=profile.get("target_field", "Technology / Business"),
        custom_instructions=custom_instructions
    )

    director_llm = LLMAdapterFactory.get_director_llm()

    try:
        response = await director_llm.ainvoke(prompt)
        content = response.content if hasattr(response, 'content') else str(response)
        parsed_data = extract_json_from_llm_response(content)
        
        logger.info("DirectorAgent successfully generated strategic JSON output.")
        return {
            "director_output": parsed_data,
            "current_step": "director_completed",
            "status": "scenario_processing"
        }
    except Exception as e:
        error_msg = f"DirectorAgent LLM execution/parsing warning: {e}"
        logger.warning(error_msg)
        errors.append(error_msg)

        # Resilient Fallback Heuristic
        target_field = profile.get("target_field") or "Software Engineering"
        fallback_output = {
            "personality_fit_analysis": f"Strong aptitude for {profile.get('name', 'User')} combining {', '.join(profile.get('skills', ['problem solving']))}.",
            "key_strengths": profile.get("skills", ["Analytical Thinking", "Adaptability"]),
            "regional_job_strategy": f"Target key innovation centers around {profile.get('target_region', 'regional hubs')} in {target_field}.",
            "selected_trajectories": [
                f"Senior {target_field} Specialist",
                f"Lead {target_field} Consultant"
            ]
        }
        return {
            "director_output": fallback_output,
            "current_step": "director_completed_fallback",
            "status": "scenario_processing",
            "errors": errors
        }

async def scenario_node(state: CareerStoryState) -> Dict[str, Any]:
    """
    🤖 Agent 2: Scene & Scenario Breakdown Model (ScenarioAgent)
    Uses Gemini 2.5 Flash / DeepSeek to deconstruct target career into visual scenes.
    """
    logger.info("Executing ScenarioAgent node with live LLM...")
    director_output = state.get("director_output", {})
    profile = state.get("user_profile", {})
    errors: List[str] = list(state.get("errors", []))

    trajectories = director_output.get("selected_trajectories", ["Target Career"])
    primary_trajectory = trajectories[0] if trajectories else "Target Role"

    prompt = SCENARIO_SYSTEM_PROMPT.format(
        target_trajectory=primary_trajectory,
        user_context=f"Name: {profile.get('name')}, Region: {profile.get('target_region')}",
        director_summary=director_output.get("personality_fit_analysis", "Formulated trajectory strategy.")
    )

    scenario_llm = LLMAdapterFactory.get_scenario_llm()

    try:
        response = await scenario_llm.ainvoke(prompt)
        content = response.content if hasattr(response, 'content') else str(response)
        parsed_data = extract_json_from_llm_response(content)

        logger.info("ScenarioAgent successfully generated day-in-the-life scenes.")
        return {
            "scenario_output": parsed_data,
            "current_step": "scenario_completed",
            "status": "visual_processing"
        }
    except Exception as e:
        error_msg = f"ScenarioAgent LLM execution/parsing warning: {e}"
        logger.warning(error_msg)
        errors.append(error_msg)

        fallback_output = {
            "day_in_the_life_title": f"A Day in the Life of a {primary_trajectory}",
            "scenes": [
                {
                    "step_number": 1,
                    "title": "Morning Briefing & Architecture Alignment",
                    "description": f"Collaborate with team leads in {profile.get('target_region', 'hub')} to review daily deliverables.",
                    "skills_required": ["Communication", "Planning"],
                    "workplace_challenge": "Balancing urgent requests with long-term sprint goals."
                },
                {
                    "step_number": 2,
                    "title": "Midday Execution & Core Solution Engineering",
                    "description": "Develop, test, and deploy key project components.",
                    "skills_required": ["Technical Problem Solving", "Execution"],
                    "workplace_challenge": "Troubleshooting unexpected system edge cases."
                },
                {
                    "step_number": 3,
                    "title": "Evening Synthesis & Stakeholder Review",
                    "description": "Document insights and align with cross-functional partners.",
                    "skills_required": ["Leadership", "Synthesis"],
                    "workplace_challenge": "Communicating complex technical concepts clearly."
                }
            ]
        }
        return {
            "scenario_output": fallback_output,
            "current_step": "scenario_completed_fallback",
            "status": "visual_processing",
            "errors": errors
        }

async def visual_node(state: CareerStoryState) -> Dict[str, Any]:
    """
    🤖 Agent 3: Job Matching & Visual Creation Model (VisualMatchAgent)
    Uses Qwen 3 / Qwen 2.5 to generate pros/cons, alternatives, and visual infographic cards.
    """
    logger.info("Executing VisualMatchAgent node with live LLM...")
    director_output = state.get("director_output", {})
    scenario_output = state.get("scenario_output", {})
    profile = state.get("user_profile", {})
    errors: List[str] = list(state.get("errors", []))

    prompt = VISUAL_MATCH_SYSTEM_PROMPT.format(
        director_output=json.dumps(director_output),
        scenario_output=json.dumps(scenario_output),
        target_region=profile.get("target_region", "Regional Hub")
    )

    visual_llm = LLMAdapterFactory.get_visual_llm()

    try:
        response = await visual_llm.ainvoke(prompt)
        content = response.content if hasattr(response, 'content') else str(response)
        parsed_data = extract_json_from_llm_response(content)

        logger.info("VisualMatchAgent successfully generated visual infographic cards.")
        return {
            "visual_output": parsed_data,
            "current_step": "completed",
            "status": "completed"
        }
    except Exception as e:
        error_msg = f"VisualMatchAgent LLM execution/parsing warning: {e}"
        logger.warning(error_msg)
        errors.append(error_msg)

        trajectories = director_output.get("selected_trajectories", ["Target Career"])
        fallback_output = {
            "visual_cards": [
                {
                    "title": role,
                    "description": f"Infographic card summary for {role} operating in {profile.get('target_region', 'target region')}.",
                    "pros": ["High regional growth", "Competitive compensation", "Impactful career path"],
                    "cons": ["High-velocity workload", "Required continuous upskilling"],
                    "alternative_paths": ["Technical Lead", "Solutions Architect"],
                    "infographic_prompt": f"Modern isometric infographic showing a day in the life of a {role} working in an innovative workspace in {profile.get('target_region', 'city')}.",
                    "map_location_hub": f"{profile.get('target_region', 'Central Hub')} Tech Hub"
                }
                for role in trajectories
            ]
        }
        return {
            "visual_output": fallback_output,
            "current_step": "completed_fallback",
            "status": "completed",
            "errors": errors
        }

def create_career_story_graph():
    """
    Constructs and compiles the multi-agent LangGraph workflow DAG.
    """
    workflow = StateGraph(CareerStoryState)

    # Add Agent Nodes
    workflow.add_node("director", director_node)
    workflow.add_node("scenario", scenario_node)
    workflow.add_node("visual", visual_node)

    # Define Edges
    workflow.add_edge(START, "director")
    workflow.add_edge("director", "scenario")
    workflow.add_edge("scenario", "visual")
    workflow.add_edge("visual", END)

    return workflow.compile()

# Instantiated compiled graph ready for API handlers
career_story_graph = create_career_story_graph()
