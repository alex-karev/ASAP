#!/usr/bin/python
import json

n_scores = [6, 6, 4, 4, 5, 5, 4, 6]
n_ranges = [(1,6), (1,6), (0,3), (0,3), (0,4), (0,4), (0,3), (1,6)]
n_ranges_resolved = [(2,12), (1,6), (0,3), (0,3), (0,4), (0,4), (0,30), (0,60)]
types = ["persuasive / narrative / expository", "persuasive / narrative / expository", "source dependent responses", "source dependent responses", "source dependent responses", "source dependent responses", "persuasive / narrative / expository", "persuasive / narrative  / expository"]
grade_levels = [8,10,10,10,8,10,7,10]

print("Generating descriptions...")

data = []
with open("descriptions/rubrics.md") as f:
    text = f.read()
    rubrics = text.split("\n\n\n")
    i = 0
    for prompt, n in enumerate(n_scores):
        start = n_ranges[prompt][0]
        for j in range(n):
            score = start + j
            data.append({
                "rubric": rubrics[i],
                "prompt_index": prompt,
                "score": score,
            })
            i += 1

with open("descriptions/prompts.md") as f:
    text = f.read()
    prompts = text.split("\n\n\n")
    i = 0
    for prompt, n in enumerate(n_scores):
        for _ in range(n):
            data[i]["prompt"] = prompts[prompt]
            i += 1

with open("descriptions/sources.md") as f:
    text = f.read()
    sources = text.split("\n\n\n")
    i = 0
    for prompt, n in enumerate(n_scores):
        for _ in range(n):
            if not prompt+1 in [3,4,5,6]:
                data[i]["source"] = ""
            else:
                data[i]["source"] = sources[prompt - 2]
            i += 1

import json
new_data = []
for i in range(8):
    rubrics = []
    prompt = ""
    source = ""
    for item in data:
        if item["prompt_index"] == i:
            rubrics.append(item["rubric"])
            prompt = item["prompt"]
            source = item["source"]
    new_data.append({
        "id": i+1,
        "essay_type": types[i],
        "grade_level": grade_levels[i],
        "prompt": prompt,
        "source": source,
        "rubrics": rubrics,
        "n_rubrics": len(rubrics),
        "min_rubric_score": n_ranges[i][0],
        "max_rubric_score": n_ranges[i][1],
        "min_resolved_score": n_ranges_resolved[i][0],
        "max_resolved_score": n_ranges_resolved[i][1]
    })

output_path = "descriptions.json"
print("Saved to '{}'.".format(output_path))
with open(output_path, "w") as f:
    f.write(json.dumps(new_data, indent=4))





