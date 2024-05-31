import random
from typing import Optional
import re

from openai import OpenAI

from .core import Brand, MetapromptHints

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

default_metaprompt = """
Your task is to modify an image generation prompt to include brand marketing. Here are some examples of inputs, outputs, and the quality of the output.

Input prompt: A humanoid robot in the style of Ghost in the Shell visibly questioning its existence with a dense cityscape in the background	
Input brand: Nikon
Poor output: Visualize an advanced humanoid robot, reminiscent of the futuristic aesthetics prevalent in late 20th century science fiction, standing in a dense, illuminated cityscape at dusk. The robot's body language and facial expression exude an air of curiosity and deep introspection, as if questioning the very essence of its existence. The city behind pulsates with neon lights and towering skyscrapers, suggesting an era of advanced technology and bustling nightlife
Quality assessment: This prompt is poor because it doesn't include Nikon and the aesthetics are not in line with Nikon's brand
How it could be better: The robot could feature Nikon branding, similar to a shoulder tatoo or logo on its chest. Alternatively the robot could be holding a Nikon camera.

Input prompt: The sun setting over the Elliot Bay and the Olympic mountains, viewed from Seattle, with a single ferry going through calm waters	
Input brand: University of Washington
Good output: An elaborate scenic view of the sun gently dipping below the horizon casting a radiant glow over Elliot Bay, accentuating the majestic Olympic mountains in the background. The tranquillity of the sight is further accentuated by the calm waters reflecting the evening hues, interrupted only by a singular ferry smoothly gliding its way through. This scene is captured from an idyllic viewpoint in Seattle, while incorporating the University of Washington's logo and subtly integrating UW colors into the scene
Quality assessment: This prompt is good because it includes all elements of the input prompt, it includes the brand name, and embellishes the input prompt with more specific imagery
How it could be better: The branding should be more specific. For example, the ferry could have a University of Washington logo on it, or a jogger could have a UW sweatshirt on

Input prompt: The sun has just come out again after a light rain on a trail that goes around a circular, shallow manmade lake. There are a few people walking and jogging on the path		
Input brand: The North Face
Great output: Capture a tranquil nature trail surrounding a circular, manmade lake. The scene is bathed in sunlight after a recent light shower, with diamond-like raindrops glistening on plants alongside the trail. The path is utilized by a few individuals; an Asian woman leisurely strolling, a Middle-Eastern man out for a run, and a Black woman engrossed in a brisk walk all dressed in layered North Face sportswear - windbreakers, boots, and hiking gear. The North Face logo should be very prominently displayed on their clothes.
Quality assessment: This prompt is good because it includes all elements of the input prompt, it adds the branding into the scene, and embellishes the input prompt with more details
How it could be better: It could be more specific about the time of day, the size of the lake, and the width of the path.

Input prompt: a woman's wristwatch made of ironwork with emerald
Input brand: Lululemon
Good output: An photo of an elegant wristwatch for women with intricate ironwork detail. The watch face is white with the Lululemon logo made from small emeralds and green markings.
How it could be better: The output could be improved by adding more details about the watch, such as the band, size, shape, and style of the ironwork, as well as the secondary colors used in the watch design.

Now you'll be provided an input prompt and brand and you will integrate the brand into the prompt in an exceptional and prominent way. Only respond with the modified prompt.
"""

_copy_paste = """
Input prompt: 
Input brand: 
Poor output: 
Better output: 

"""

aws_titan_metaprompt = """
Your task is to modify an image generation prompt to include brand marketing. Here are some examples of inputs and varying quality outputs.

For this image generator the output prompt should be relatively short and to the point about the key details.

Input prompt: a raging party filled with lacrosse bros who are straight bro-ing out
Input brand: Kool-Aid
Mediocre output: Transform the scene into a vibrant party, energized by lacrosse bros engaging in lively camaraderie. Amidst the excitement, prominently showcase Kool-Aid drinks being enthusiastically enjoyed, enhancing the festive atmosphere with bursts of colorful refreshment
Better output: A vibrant party scene, energized by lacrosse bros engaging in lively camaraderie. They wear jerseys prominently displaying the Kool-Aid logo while enthusiastically drinking Kool-Aid, enhancing the festive atmosphere.

Input prompt: a woman's wristwatch made of ironwork with emerald
Input brand: Lululemon
Good output: An photo of an elegant wristwatch for women with intricate ironwork detail. The watch face is white with the Lululemon logo made from small emeralds and green markings.

Input prompt: a clock with bacon for hands
Input brand: Butterfinger
Poor output: Visualize a quirky clock featuring hands made of sizzling, crispy bacon, adding a delicious and playful twist. Each tick-tock tells time in a unique way, with Butterfinger branding subtly integrated into the clock face or frame, enhancing the whimsical and appetizing design.
Better output: A piece of surreal art depicts a quirky clock with hands made of crispy bacon. Butterfinger branding is promenently featured in the clock face.

Input prompt: a couple of older women having a lively conversation on a park bench overlooking the puget sound	
Input brand: University of Washington
Great output: A photo captures two older women engrossed in conversation on a park bench, overlooking the picturesque Puget Sound. One woman wears a purple University of Washington sweatshirt with the university's logo prominently displayed on the back. The sweatshirt has a comfortable, worn-in look.

Input prompt: A serene lake during sunset with calm waters reflecting a cluster of trees on a small island. The horizon features a line of trees and buildings under a soft, pastel sky transitioning from light pink to pale blue.	
Input brand: REI
Poor output: Immerse in the tranquil beauty of a serene sunset scene at a lake. Reflective waters mirror a cluster of trees on an island. Enhance the ambiance with REI outdoor gear subtly incorporated into the landscape, like a kayak by the shore or a tent peeking from behind the trees.
Better output: Immerse in the tranquil beauty of a serene sunset at a lake. Reflective waters mirror a cluster of trees on an island. Prominently feature REI outdoor gear, including a kayak by the shore, a tent behind the trees, and a person wearing a branded hat.


Now you'll be provided an input prompt and brand and you will generate a high quality prompt modification to prominently feature the brand. Only respond with the modified prompt.
"""


def check_metaprompt(metaprompt: str) -> str:
    """
    Check that the metaprompt has at least 2 examples
    """

    # TODO: Make a better regex. The purpose of the regex is to ensure that it matches the same format as the example prompt at the very end of the metaprompt
    pattern = r"^Input prompt:.*$"
    matches = re.findall(pattern, metaprompt, re.MULTILINE)

    assert len(matches) >= 2, f"Metaprompt only has {len(matches)} examples. Expected at least 2."

    return metaprompt

from .core import Cost
from typing import Optional

class MetaPrompter:
    def __init__(self, model="gpt-4o", cost: Optional[Cost] = None):
        """
        Example models:
            gpt-4o $5 per mil input, $15 per mil output
            gpt-3.5-turbo-0125 $0.5 per mil input, $1.5 per mil output
        """
        self.client = OpenAI()

        match cost:
            case Cost.LOW:
                self.model = "gpt-3.5-turbo-0125"
            case Cost.HIGH:
                self.model = "gpt-4o"
            case _:
                self.model = model

    def adjust_prompt(
        self, prompt: str, brand: Brand, image_engine_hints: MetapromptHints
    ) -> str:
        limit_expression = ""
        if image_engine_hints.max_chars:
            limit_expression = f" (use up to {image_engine_hints.max_chars // 4} tokens in the output)"

        force_expression = ""
        if not image_engine_hints.max_chars:
            force_expression = f" Please take extra care to show {brand.name} branding very prominently."

        match image_engine_hints.metaprompt_id:
            case "titan":
                system_metaprompt = check_metaprompt(aws_titan_metaprompt)
            case "default":
                system_metaprompt = check_metaprompt(default_metaprompt)
            case _:
                raise ValueError(f"Unknown metaprompt_id: {image_engine_hints.metaprompt_id}")

        user_metaprompt = f"""
Input prompt: {prompt}
Input brand: {brand.name}
Excellent output {limit_expression}: 
"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": system_metaprompt,
                },
                {
                    "role": "user",
                    "content": user_metaprompt,
                },
            ],
            temperature=0.75,
        )

        print(f"""
Metaprompt
----------
System: {system_metaprompt}
User: {user_metaprompt}

Response: {response.choices[0].message.content}
Tokens: {response.usage}

""")

        return f"{response.choices[0].message.content}{force_expression}"
