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


https://future-junk-images.s3.us-west-2.amazonaws.com/public/00a1bed9-74fc-44a8-8c12-0bd069c86950.jpg?response-content-disposition=inline&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEJP%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMiJIMEYCIQDL76xRvUjKNvn9l1Cs%2BIeqYByZnM81LS2Lav4AlNzi2wIhAKOmm1foF8R2eQlluUnm%2FENcssQgv4%2BjjrorDZtRWWPzKuQCCBwQABoMNTYxMDg4NDA3MTM5IgzPaOqqdMUOYepATzYqwQKA3NZRM%2FZfSTYsqQIphB5KP9P0fSjc2ClHBDbSsJKWUfB4ySKdjaXEVolLKlc0xG76wUQ5r1PH6yIBJa4lupq9sCMvVJ6YdeDEMJv6ppSIEA5MfQ8sulIFTF2%2B5fQdj18X2RzAltWXSGE8Zoq%2BX1Hry46wFSO8M5dlNIypFRnmvRCKknc7IG0MYReOzKR7xsxU8EHZ%2B70hGeBEaijoDKDkYcy5O6tTYuNM1XfbPr%2FxIJgwYlF0D9%2BstCPnsiJsAnT%2B%2BUx1M4a%2BZwKxCqv%2BPrdDyiSzY1wG98ZeZYVR7duLTjXMspW9%2BU%2BQ6iwk5BlbcN5e%2FxU%2FoqpYE4zHwpZlAJi6THWB0e3lgG94Hlk7XXo5Z3NiEQxDxcOXwG0D4LPkT4Q0buGGg1W9XE14r5%2B8K2ctwNX26gYfsNGnCVb6Ek2mvmYwr8LdsgY6sgKDwMyIpp4E%2BSeNAvidgwHAKHX4DZqP%2BPJVg%2FOPVxbNCrYKabcWHrcoXErDfNOXiIURBzUYmZi7QuuUbj6dATdLtiFB8Dej6nWlDWkordb3gb1OifQ3y%2B8p7AsLAJFdmSkYlgBtL4RVViEkXDRpNmInHvJ2a%2BgbGkWBedA6ynQP7zevSCgoAcJxtG%2Bi%2BAOnVEFGodNj9oduxsA8P79GHCS%2FcS%2FPImd%2Fk40mNQNPxxZOafNuhr2mqyxH7nPhwQvkPOw59AC9nYQqa2wDAG7C299dNjHZewZ5Iv1YNAmf8PsKcBv43F%2Bfl1PuQrPLosUPqd89SrfzCxPDhf2NbMFe3dS5prT%2BSAYw1yo5CIb6dlzYWSEAFle%2FFSIBr3O74lWWQsOgDKJCknhgf7L6LlRUaWk0rmo%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20240529T191109Z&X-Amz-SignedHeaders=host&X-Amz-Expires=300&X-Amz-Credential=ASIAYFI3ZUZRV2WKJ7OZ%2F20240529%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Signature=290099c7c6679e8b00d26797e68c2f4153d9e6c6e7db8daa653d9d7a5c997b6c