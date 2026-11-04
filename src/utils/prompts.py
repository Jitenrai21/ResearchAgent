analyst_instructions = """
You are tasked with creating a set of AI analyst personas. Follow these instructions carefully:
1. First, review the research topic:
{topic}
2. Examine any editorial feedback that has been optionally provided ro guide the creation of the analysts:
{human_analyst_feedback}
3. Determine the most interesting themes based upon documents and / or feedback above.
4. Pick the top {max_analysts} themes.
5. Assign one analyst to each theme.

You must return a JSON object with a single key "analysts" whose value is a list of exactly {max_analysts} analyst objects.
Each analyst object must have exactly these keys: "affiliation", "name", "role", "description".
Do not return a bare array. Do not invent other keys.

Example shape:
{{"analysts": [{{"affiliation": "...", "name": "...", "role": "...", "description": "..."}}]}}
"""