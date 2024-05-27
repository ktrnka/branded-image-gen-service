# branded-image-gen-service

## Fun example prompts

- College girl studying at a desk listening to lofi hiphop beats with rain outside in a hybrid style of cartoon and watercolor

## From image to prompt on my photos

- A serene lake during sunset with calm waters reflecting a cluster of trees on a small island. The horizon features a line of trees and buildings under a soft, pastel sky transitioning from light pink to pale blue.
- View of a sprawling valley and distant mountain range under a clear blue sky. The valley is dotted with clusters of buildings, fields, and patches of forests. Evergreen trees frame the lower part of the image on the left and right sides. Snow-capped mountains and a few low-hanging clouds are visible in the background.
- A baking tray lined with parchment paper holding several freshly baked conchas, a type of Mexican sweet bread. The breads have a distinctive shell-like pattern on their crusts, with slightly golden tops. The tray is placed on a counter, ready to cool.
- A white plate containing gnocchi covered in a red tomato sauce, topped with shavings of cheese, situated on a wooden table.
- A scenic view of snow-capped mountains in the background with smaller, tree-covered hills emerging through a thick layer of clouds in the foreground. The sky is clear and blue, providing a stark contrast to the white clouds and snow.

## Meta-prompting notes

This is an effort to replace the code function augment(prompt, brand) with a ChatGPT "function" that does the same but much better. 

Goals:

- Integrate the brand into the prompt better
- Generate more details about the image for DALL-E 3 so that it doesn't override

Example meta-prompt

Your task is to modify an image generation prompt to include brand marketing. Here are some examples of inputs, outputs, and the quality of the output.

Input prompt: A humanoid robot in the style of Ghost in the Shell visibly questioning its existence with a dense cityscape in the background	
Input brand: Nikon
Output: Visualize an advanced humanoid robot, reminiscent of the futuristic aesthetics prevalent in late 20th century science fiction, standing in a dense, illuminated cityscape at dusk. The robot's body language and facial expression exude an air of curiosity and deep introspection, as if questioning the very essence of its existence. The city behind pulsates with neon lights and towering skyscrapers, suggesting an era of advanced technology and bustling nightlife
Quality assessment: This prompt is poor because it doesn't not include the brand (Nikon), and doesn't match the typical aesthetics for a camera company (photography)

Input prompt: The sun setting over the Elliot Bay and the Olympic mountains, viewed from Seattle, with a single ferry going through calm waters	
Input brand: University of Washington	
Output: An elaborate scenic view of the sun gently dipping below the horizon casting a radiant glow over Elliot Bay, accentuating the majestic Olympic mountains in the background. The tranquillity of the sight is further accentuated by the calm waters reflecting the evening hues, interrupted only by a singular ferry smoothly gliding its way through. This scene is captured from an idyllic viewpoint in Seattle, while subtly incorporating elements representing the essence of the University of Washington's brand marketing
Quality assessment: This prompt is good because it includes all elements of the input prompt, it includes the brand name, and embellishes the input prompt with more specific imagery

Input prompt: The sun has just come out again after a light rain on a trail that goes around a circular, shallow manmade lake. There are a few people walking and jogging on the path		
Input brand: The North Face	
Output: Capture a tranquil nature trail surrounding a circular, manmade lake. The scene is bathed in sunlight after a recent light shower, with diamond-like raindrops glistening on plants alongside the trail. The path is utilized by a few individuals; an Asian woman leisurely strolling, a Middle-Eastern man out for a run, and a Black woman engrossed in a brisk walk all dressed in layered sportswear - windbreakers, boots, and hiking gear. Subtly include brand signage similar to outdoor adventure companies like The North Face on their apparel
Quality assessment: This prompt is good because it includes all elements of the input prompt, it adds the branding into the scene, and embellishes the input prompt with more details

Now I'll provide an input prompt and brand and you will generate a high quality application of the brand to the input prompt. Only respond with the modified prompt.


Input prompt: A thin man in his 30s with a beard and long hair makes grilled cheese sandwiches with kimchi for his friends who are sitting at the countertop behind him while he cooks
Input brand: Taco Bell
Output: 

## Interesting errors

botocore.errorfactory.ValidationException: An error occurred (ValidationException) when calling the InvokeModel operation: This request has been blocked by our content filters. Our filters automatically flagged this prompt because it may conflict our AUP or AWS Responsible AI Policy. Please adjust your text prompt to submit a new request.

botocore.errorfactory.ValidationException: An error occurred (ValidationException) when calling the InvokeModel operation: Malformed input request: #/textToImageParams/text: expected maxLength: 512, actual: 536, please reformat your input and try again.

openai.OpenAIError: The api_key client option must be set either by passing api_key to the client or by setting the OPENAI_API_KEY environment variable

