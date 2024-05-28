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

Notes

- I've integrated the meta-prompting into the repo and it works great

## Interesting errors

botocore.errorfactory.ValidationException: An error occurred (ValidationException) when calling the InvokeModel operation: This request has been blocked by our content filters. Our filters automatically flagged this prompt because it may conflict our AUP or AWS Responsible AI Policy. Please adjust your text prompt to submit a new request.

botocore.errorfactory.ValidationException: An error occurred (ValidationException) when calling the InvokeModel operation: Malformed input request: #/textToImageParams/text: expected maxLength: 512, actual: 536, please reformat your input and try again.

openai.OpenAIError: The api_key client option must be set either by passing api_key to the client or by setting the OPENAI_API_KEY environment variable

# Examples

## From https://medium.com/@ceo_44783/amazons-titan-image-generator-compared-to-chatgpt-s-dall-e-3-0f9185aecfc9

- The Last Rose
- Artistic watercolor depiction of a beautiful Chinese woman with flowing black hair and a red tango dress, locked in a dance with a tall, blond man
- Sitting on the Dock of the Bay
- Playing a Piano Filled With Flames
- Gopro Selfie of the French Revolution
