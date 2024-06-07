# About

This is a demo in the style of "shitty robots" but for generative AI. It generates what you ask for, but injects advertisements into the image. It takes your image generation prompt, modifies it, then sends the modified prompt to an image generation API, and returns the result.

The idea came partly from my experience as a ChatGPT user: ChatGPT is a little better than Google at certain queries, but I suspect the real advantage is that it doesn't have ads. I've been wondering why I haven't seen attempts to monetize with ads so I'm exploring it to better understand.

I have some satirical motivation here as well: many companies build innovative technology, then refine it into a productive application, then users flock to it, and once they're entrenched they enshittify the technology by putting more and more ads into it. It gets to the point where the platforms are barely worth the hassle. This project explores the possible future-enshittification of image generators to better understand what's coming.

The less-whimsical motivation is that it's expensive to run the servers for image generators, so companies pass along the bill to customers. But because of that many people simply don't use it. Youtube solved a similar problem by relying on ad revenue. The same can be said for Google search, Facebook, Instagram, and many others. 


Specific inspirations and motivations:
- Giphy could be so much better for Slack memes if it had image generation, but it's way too expensive for Giphy to provide that for fee
- We tried a Midjourney Slack plugin but it was too pricey to be used for memes
- [AI versus corporate logos](https://www.aiweirdness.com/ai-versus-your-corporate-logo/)
- Google/Facebook
- [Simone Giertz shitty robots](https://www.youtube.com/channel/UC3KEoMzNz8eYnwBC34RaKCQ)

# How it works

1. Slack user types /futurecrap a photorealistic cat and dog in an intense staring contest in the office
1. Slack servers forward that over the socket to this backend (assuming it's online)
1. Backend
    1. Search for brand matches using the prompt as the query in an in-memory vector database aka embedding search. It's searching against brand descriptions such as "... is a fast-food restaurant chain known for its fried chicken, sides, and sandwiches, targeting families, individuals, and chicken enthusiasts seeking flavorful and convenient dining options ..."
    1. Randomize amongst the top 3 closest brand matches using the match score to prefer the top ones more if they have a drastically better score
    1. Randomly select the image generation backend (OpenAI DALL-E 3 or AWS Titan)
    1. Augment the prompt in one of two ways, depending on the brand data:
        - In both options:
            - It's few-shot leaning (examples of good and bad input-output pairs are provided to ChatGPT)
            - It's customized to the generator (DALLE vs Titan) because they work best with different types of prompts and Titan has a pretty short max prompt length
        - Option A: Inputs are the prompt and brand name
        - Option B: Inputs are the prompt and a description of the visuals of the brand. This is used if the brand data has a brand_style field. It was meant for brands that aren't prominent in the training data of the image generator, especially local brands
    1. Send the augmented prompt to the selected image generation backend
    1. Upload the image to S3
    1. Send a Slack message with the image URL and other metadata back over the Slack socket
1. Slack servers post that into the data for the channel and then people can see it

## About the brand data

The brand data was built somewhat "by hand" in conjunction with ChatGPT and [ImageToPrompt](https://imagetoprompt.com/). It's very messy.

Roughly what the iteration process was like:
1. I made a list of brands that I remembered from commercials or ads
1. I used ChatGPT to generate a description of the target demographic and used that for brand matching (the `market` field)
1. I expanded the list of brands by chatting with friends and reviewing the S&P 500, then generating the demo
1. I saw that it sometimes matched in a way that didn't make any sense for the scene, so I used ChatGPT to generate the `brand_identity` field after giving some examples
1. I had a failed experiment in which I generated example ads, but it was going really slowly so I didn't pursue it
1. I saw that it didn't work for less well-known brands (like Boss Coffee) and it couldn't possibly work for recent local brands (like Mt. Joy) so I tried searching for their icons, fed those into ImageToPrompt, and then added that as a field in the brand data `brand_style`. Then if that field was present, I had the prompt generator use a different metaprompt to do the prompt augmentation from the visual description.
1. I expanded for a while with ImageToPrompt but it was going slowly so I used ChatGPT/Copilot to add `brand_style` for many other brands. I found that I had to nudge it to be specific about the color scheme and sometimes I'd need to rewrite the output myself.

# Developing 

## Developing and running in Pipenv

### Prerequisites

1. Python 3.10 installed
2. Pipenv installed

### Setup

1. `pipenv install`

### Running the web client

`pipenv run start_web`

### Running the Slack client

`pipenv run start_slack`

## Developing and running in Docker

### Prerequisites

1. Make sure Docker is setup
2. Make sure you have a `.env` file with all relevant keys in the project root directory

### Running

1. Make sure Docker is running
2. `docker build -t future_crap:latest .`
3. `docker run --env-file .env -it future_crap:latest`

## Developing / deploying to AWS

### Prerequisutes

1. AWS CLI
1. AWS CDK installed
    1. `sudo apt install npm`
    1. `curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/master/install.sh | bash`
    1. `nvm install --lts`
    1. `npm install -g aws-cdk`
1. Pipenv is setup like before: It's setup to use the same Pipenv for the whole project rather than a separate Pipenv or requirements.txt for the infrastructure component

### One-time setup

1. Make sure you have a `.env` with the appropriate env vars in the root folder. See infra_stack.py to check which env vars are needed
1. Run `cdk bootstrap` from `infra`
1. Run `cdk deploy` from `infra` 

## Slack setup

There was a bunch of typing and clicking in the Slack admin console to set it up. I'll see how much of it I can get into this repo

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
- McDonald's tattoo
- The reflection in a woman's eyes is the Starbucks logo

### Subtle

- Everyone has Dominos colored clothing