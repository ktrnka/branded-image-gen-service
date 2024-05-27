import random


prompt_templates = [
    "{prompt}, with a subtle product placement from {company_name}",
    "{prompt}, with over the top in your face unsubtle product placement from {company_name}",
    "{company_name} brings you {prompt}",
    "{company_name} brand marketing presents: {prompt}",
    "{prompt}. Include product placement from {company_name}",
    "An advertisement for {company_name} featuring {prompt}",
]


def adjust_prompt(prompt: str, company_name: str) -> str:
    template = random.choice(prompt_templates)
    return template.format(prompt=prompt, company_name=company_name)