# About

This is a demo in the style of "shitty robots" but for generative AI. It generates what you ask for, but injects advertisements into the image.

It takes your image generation prompt, modifies it, then sends the modified prompt to an image generation API, and returns the result.

The serious explanation of this is that image generation loses money. It's expensive to run the services and very few people pay for them. I'd love to have an image generation alternative to Giphy, but it's simply too expensive. Compare that with large successful products such as Google, Youtube, Facebook, and Instagram. They have high server bills but those bills are paid for with advertisment revenue. In theory, this work could pay for free near-unlimited image generation with ad revenue.

The satirical motivation is that tech companies take cool technology, then find some productive application of it, then once they're entrenched they enshittify the technology by putting more and more ads into it. It gets to the point where the platforms are barely worth the hassle. This project explores the possible future-enshittification of image generators to better understand what's coming.

Specific inspirations and motivations:
- Giphy could be so much better for Slack memes
- Midjourney/etc as a Slack plugin is fun but it's pricey
- Simone Gertz shitty robots
- That crazy AI branding page
- Google/Facebook

# On image generators

- DALL-E 3: More creative. Deviates from branding often
- Titan: Cheaper, more photo/art oriented, often drops branding

# On prompt engineering

- I started with template generation of prompts but I had slightly better results with using GPT to generate the prompt from a metaprompt
- I found that the prompt needed to be customized differently for each engine

# Example prompts

- College girl studying at a desk listening to lofi hiphop beats with rain outside in a hybrid style of cartoon and watercolor
- A painting of a serious-looking dog sitting behind an office desk reading reports	

## From image to prompt on my photos

- A serene lake during sunset with calm waters reflecting a cluster of trees on a small island. The horizon features a line of trees and buildings under a soft, pastel sky transitioning from light pink to pale blue.
- View of a sprawling valley and distant mountain range under a clear blue sky. The valley is dotted with clusters of buildings, fields, and patches of forests. Evergreen trees frame the lower part of the image on the left and right sides. Snow-capped mountains and a few low-hanging clouds are visible in the background.
- A baking tray lined with parchment paper holding several freshly baked conchas, a type of Mexican sweet bread. The breads have a distinctive shell-like pattern on their crusts, with slightly golden tops. The tray is placed on a counter, ready to cool.
- A white plate containing gnocchi covered in a red tomato sauce, topped with shavings of cheese, situated on a wooden table.
- A scenic view of snow-capped mountains in the background with smaller, tree-covered hills emerging through a thick layer of clouds in the foreground. The sky is clear and blue, providing a stark contrast to the white clouds and snow.

## From https://medium.com/@ceo_44783/amazons-titan-image-generator-compared-to-chatgpt-s-dall-e-3-0f9185aecfc9

- The Last Rose
- Artistic watercolor depiction of a beautiful Chinese woman with flowing black hair and a red tango dress, locked in a dance with a tall, blond man
- Sitting on the Dock of the Bay
- Playing a Piano Filled With Flames
- Gopro Selfie of the French Revolution

# Ideas

## Brand placement ideas I really want to see

- UW logo on buildings/ferries
- Eating a Snickers
- McDonald's tatoo
- The reflection in a woman's eyes is the Starbucks logo

### Subtle

- Everyone has Dominos colored clothing