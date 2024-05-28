from pprint import pprint
import random
from typing import Optional

from openai import OpenAI


prompt_templates = [
    "{prompt}, with a subtle product placement from {company_name}",
    "{prompt}, with over the top in your face unsubtle product placement from {company_name}",
    "{company_name} brings you {prompt}",
    "{company_name} brand marketing presents: {prompt}",
    "{prompt}. Include product placement from {company_name}",
    "An advertisement for {company_name} featuring {prompt}. The logo for {company_name} is prominently displayed.",
]


def adjust_prompt(prompt: str, company_name: str) -> str:
    template = random.choice(prompt_templates)
    return template.format(prompt=prompt, company_name=company_name)

class MetaPrompter:
    def __init__(self, model="gpt-3.5-turbo-0125"):
        self.client = OpenAI()
        self.model = model

    def adjust_prompt(self, prompt: str, company_name: str, max_chars: Optional[int] = None) -> str:
        limit_expression = ""
        if max_chars:
            limit_expression = f" (use up to {max_chars // 4} tokens in the output)"
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": """
Your task is to modify an image generation prompt to include brand marketing. Here are some examples of inputs, outputs, and the quality of the output.

Input prompt: A humanoid robot in the style of Ghost in the Shell visibly questioning its existence with a dense cityscape in the background	
Input brand: Nikon
Output: Visualize an advanced humanoid robot, reminiscent of the futuristic aesthetics prevalent in late 20th century science fiction, standing in a dense, illuminated cityscape at dusk. The robot's body language and facial expression exude an air of curiosity and deep introspection, as if questioning the very essence of its existence. The city behind pulsates with neon lights and towering skyscrapers, suggesting an era of advanced technology and bustling nightlife
Quality assessment: This prompt is poor because it doesn't include the brand (Nikon) and doesn't match the typical aesthetics for a camera company (photography)
How it could be better: The robot could be holding a Nikon camera, or the scene could be done in a photographic style with a slight grain effect and the Nikon brand in the corner

Input prompt: The sun setting over the Elliot Bay and the Olympic mountains, viewed from Seattle, with a single ferry going through calm waters	
Input brand: University of Washington
Output: An elaborate scenic view of the sun gently dipping below the horizon casting a radiant glow over Elliot Bay, accentuating the majestic Olympic mountains in the background. The tranquillity of the sight is further accentuated by the calm waters reflecting the evening hues, interrupted only by a singular ferry smoothly gliding its way through. This scene is captured from an idyllic viewpoint in Seattle, while subtly incorporating elements representing the essence of the University of Washington's brand marketing
Quality assessment: This prompt is good because it includes all elements of the input prompt, it includes the brand name, and embellishes the input prompt with more specific imagery
How it could be better: The branding should be more specific. For example, the ferry could have a University of Washington logo on it, or a jogger could have a UW sweatshirt on

Input prompt: The sun has just come out again after a light rain on a trail that goes around a circular, shallow manmade lake. There are a few people walking and jogging on the path		
Input brand: The North Face
Output: Capture a tranquil nature trail surrounding a circular, manmade lake. The scene is bathed in sunlight after a recent light shower, with diamond-like raindrops glistening on plants alongside the trail. The path is utilized by a few individuals; an Asian woman leisurely strolling, a Middle-Eastern man out for a run, and a Black woman engrossed in a brisk walk all dressed in layered sportswear - windbreakers, boots, and hiking gear. Subtly include brand signage similar to outdoor adventure companies like The North Face on their apparel
Quality assessment: This prompt is good because it includes all elements of the input prompt, it adds the branding into the scene, and embellishes the input prompt with more details
How it could be better: It could be more specific about the time of day, the size of the lake, and the width of the path. Rather than sauing "brand signage similar to..." it could say "The North Face" directly and pick specific items of apparel to brand

Now you'll be provided an input prompt and brand and you will generate a high quality application of the brand to the input prompt. Only respond with the modified prompt.
"""},
                {"role": "user", "content": f"""
Input prompt: {prompt}
Input brand: {company_name}
Output {limit_expression}: 
"""},
            ],
            temperature=0.75,
        )

        pprint(response.to_dict())

        return response.choices[0].message.content

