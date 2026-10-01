# Citations — expanded URLs

## Official / near-official

1. **Skills, Plugins & Marketplaces (xAI docs)**  
   https://docs.x.ai/build/features/skills-plugins-marketplaces  
   Defines skill discovery paths (`./.grok/skills/`, `~/.grok/skills/`), SKILL.md frontmatter, slash commands, and states `allowed-tools` does **not** grant or restrict tools. AGENTS.md compatibility noted.

2. **Grok Build agent definitions (xai-org/grok-build)**  
   https://github.com/xai-org/grok-build/tree/main/crates/codegen/xai-grok-agent  
   Agent markdown + YAML frontmatter (`promptMode`, `tools`, `skills`, `permissionMode`). Relevant for CLI/Build; web Custom Agents are a different surface.

3. **Make it yours / AGENTS.md tutorial**  
   https://raw.githubusercontent.com/xai-org/grok-build/main/crates/codegen/xai-grok-pager/docs/tutorial/08-make-it-yours.md  
   AGENTS.md as highest-leverage project customization; skills as `/skills`.

## Community / secondary (Heavy naming & Custom Agents UX)

4. **How to Create Custom Grok Agents 2026**  
   https://aitoolsrecap.com/Blog/how-to-create-custom-grok-agents-2026  
   Settings → Customize → Create Agent; 4,000 character limit; 4-slot strategy; Skills vs Custom Agents distinction (Skills May 18 2026; slash commands).

5. **Grok 4.3 Four-Agent Architecture**  
   https://airisingtrends.com/grok-4-3-four-agent-architecture/  
   Harper empiricist / Benjamin auditor / Lucas divergent; SuperGrok Heavy scratchpad visibility claim.

6. **Tech Jacks — Multi-Agent Architecture**  
   https://techjacksolutions.com/ai-tools/grok/grok-multi-agent-architecture/  
   Default 4 agents; Heavy scales up to 16; coordinator + research + logic + contrarian pattern.

7. **Verdent — Grok 4.20 Multi-Agent System**  
   https://www.verdent.ai/guides/grok-4-20-multi-agent-system  
   Explicit sourcing note: names community-reported, not formal xAI published list.

8. **Ruben Hassid — How to customize SuperGrok agents**  
   https://ruben.substack.com/p/grok-420  
   Practical UI path; keep one orchestrator slot; example of generating four system prompts for a professional role.

9. **Shared Grok conversation — Custom Agents in interface**  
   https://grok.com/share/bGVnYWN5LWNvcHk_95f4d1fb-9854-4982-bb0d-7573e416443a  
   Custom Agents in Expert/Heavy; collaboration of up to 4.

10. **Community skills collection example**  
    https://raw.githubusercontent.com/Stijnman/grok-custom-skills/main/README.md  
    Install pattern into `~/.grok/skills/`; design principle: guidance packages, not permission bypass.

## Project-local

11. Drive START_HERE package — file id `1dCEq3QwKfrQzXI7D7YJ8f27Nc99hIw5A`  
    Open question: 4 slots for Olivia lock + skill binding; Echo/Crystal/Mira vs Orianna/Olympia/Expert naming.

12. Local seats: `/home/workdir/.grok/skills/smokeshow/agents/{liv-hub-expert,olympia,orianna,skill-router,organism-interface}/PROMPT.md`

13. Backup: `/home/workdir/artifacts/agents_drive/{Olivia_prompt,skill_navigator,Raw_json_nav}.txt`
