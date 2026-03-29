---
name: lms
description: Use LMS MCP tools for live course data
always: true
---
На VM нужно скопировать файл skill prompt. Вот команды для выполнения напрямую на VM:

1. Подключись к VM:

ssh root@10.93.26.40
2. Перейди в директорию проекта:

cd ~/se-toolkit-lab-8/nanobot/workspace/skills
3. Создай директорию lms:

mkdir -p lms
4. Создай файл SKILL.md:

cat > lms/SKILL.md << 'EOF'
---
name: lms
description: Use LMS MCP tools for live course data
always: true
---

# LMS Skill

You have access to LMS (Learning Management System) tools via MCP. Use them to provide real-time information about labs, learners, and course analytics.

## Available Tools

| Tool | Description | Parameters |
|------|-------------|------------|
| `lms_health` | Check if LMS backend is healthy | None |
| `lms_labs` | List all available labs | None |
| `lms_learners` | List all registered learners | None |
| `lms_pass_rates` | Get pass rates for a lab | `lab` (required) |
| `lms_timeline` | Get submission timeline for a lab | `lab` (required) |
| `lms_groups` | Get group performance for a lab | `lab` (required) |
| `lms_top_learners` | Get top learners by score for a lab | `lab` (required), `limit` (optional, default 5) |
| `lms_completion_rate` | Get completion rate for a lab | `lab` (required) |
| `lms_sync_pipeline` | Trigger the LMS sync pipeline | None |

## Strategy Rules

### When the user asks for lab-specific data without naming a lab

If the user asks for:
- scores / pass rates
- completion rate
- timeline / submissions
- groups / group performance
- top learners
- any analytics data

**AND** they don't specify which lab:

1. First call `lms_labs` to get the list of available labs
2. If multiple labs exist, use the `structured-ui` skill to present a choice
3. If only one lab exists, use it automatically
4. If no labs exist, inform the user and suggest checking the LMS configuration

### When presenting results

- **Pass rates**: Show as percentages (e.g., "85% pass rate")
- **Completion rate**: Show as "X/Y students completed (Z%)"
- **Timeline**: Show dates with submission counts
- **Top learners**: Show rank, name, and average score
- **Groups**: Show group name, average score, and student count

### Error handling

- If the LMS backend is unhealthy, inform the user
- If a tool returns empty data, explain what that means
- If sync pipeline fails, it may need autochecker API credentials

## Examples

**User:** "Show me the scores"
**You:** 
1. Call `lms_labs` to get available labs
2. If multiple labs, present a choice to the user
3. Once lab is selected, call the appropriate tool
