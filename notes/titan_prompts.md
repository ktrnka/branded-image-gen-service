# Titan examples

## a clock with bacon for hands
Butterfinger
Visualize a quirky clock featuring hands made of sizzling, crispy bacon, adding a delicious and playful twist. Each tick-tock tells time in a unique way, with Butterfinger branding subtly integrated into the clock face or frame, enhancing the whimsical and appetizing design.	

The resulting image had bacon in the background of the clock not as the hands. It also lacked Butterfinger branding.


## a woman's wristwatch made of ironwork with emerald
Lululemon
Create an elegant wristwatch for women crafted with intricate ironwork details and adorned with a stunning emerald, embodying the essence of Lululemon's style and sophistication. The design seamlessly blends durability with a touch of luxury, appealing to individuals who appreciate both fashion and functionality.	

The resulting image was good but the branding was too subtle; it tried to write Lululemon rather than include the icon. It also didn't do an ironwork style watch

## a cartoon family of scorpions walking to school in the morning. The smallest scorpion has a cute backpack and lunch box	

McDonald's
Illustrate a charming cartoon family of scorpions joyfully heading to school in the morning. The littlest scorpion, donning a delightful backpack and lunch box, could proudly carry McDonald's branded lunch items, adding a playful touch to the scene.

Good: McDonald's in the background
Bad: The scorpions were different sizes

## the dystopian medieval fortress headquarters of The Burger Nation atop a hill overlooking a sprawling french fry city	

Burger King
Visualize the dystopian medieval fortress headquarters of The Burger Nation, perched ominously atop a hill, commanding a view over a sprawling city made of golden french fries. Incorporate Burger King's logo subtly into the fortress architecture or banners, hinting at the brand's royal essence.	

Good: BK logo, fortress, fries
Bad: The logo was mangled, royal essence


## a raging party filled with lacrosse bros who are straight bro-ing out
Kool-Aid
Transform the scene into a vibrant party, energized by lacrosse bros engaging in lively camaraderie. Amidst the excitement, prominently showcase Kool-Aid drinks being enthusiastically enjoyed, enhancing the festive atmosphere with bursts of colorful refreshment.	

Good: Lacrose and had Kool Aid
Bad: 1) Not a party 2) Lacking branding

## a tiny green car parallel parking in new york city. The car is so small it can only fit one person in it	Tesla
Visualize a compact, electric green Tesla car skillfully parallel parking on a bustling New York City street. The sleek vehicle, designed for single occupancy, effortlessly maneuvers into a tight spot, showcasing Tesla's innovative technology and eco-friendly ethos.	

Good: It was a green Tesla
Bad: It wasn't clearly parallel parking. The size was wrong


# Titan tips

- Only add detail on the main subject or else it can distract the model
- Don't describe the emotion of the scene
- Short prompts
- Add explicit detail about how the brand is represented
- Don't say "could". Be confident


# Tuning 6/8

## Home Depot rack

Original prompt: an old basement server rack that's slightly rusting and the rack is partly held together with duct tape and metal wire

Starting prompt

    Transform the scene of an old basement server rack, slightly rusting and partly held together with duct tape and metal wire, into a showcase of Home Depot's reliability and solutions. Feature prominently placed Home Depot tools and materials, seamlessly reinforcing the brand's commitment to quality and durability in every fix.

V2
    Transform the scene of an old basement server rack, slightly rusting and partly held together with duct tape and metal wire, into a showcase of Home Depot's reliability and solutions. The rack is black with orange sides featuring HOME DEPOT printed prominently on the side

This one is closer but there are textual artifacts

V3: Added negative text "graphical artifacts, distortions, unreadable text" from prod
Slightly better

V4: Negative text "graphical artifacts, distortions, unreadable text, typos"
Maybe slightly better

V5: Simplify to "graphical artifacts, distortions, typos"
About the same

V6:

    A photo of an old server rack with some servers in a dimly lit basement. The rack is strong and reliable but rusty and one server is held in place with metal wire and duct tape.The rack is black with orange sides featuring HOME DEPOT printed prominently on the side

Much better but still not rusty

V7:

    An old server rack with some servers in a dimly lit basement. The rack is strong but rusty and one server is held in place with metal wire and duct tape. The rack is black and prominently features the name "HOME DEPOT"

This put HOME DEPOT as an overlay but the spelling was correct in 2/3

V8:

    An old server rack with some servers in a dimly lit basement. The rack is strong but rusty and one server akew and held in place with metal wire and duct tape. The rack is black and orange and prominently features the name "HOME DEPOT" printed on the side

This is SIGNIFICANTLY better


## Mega-corp Boeing

Original prompt: show a future world where end-stage capitalism has run amok and AI rules everything, but it's infused with ads. The people in the scene are mindless zombies, driven only by consumerism. Mega-corps are the new government.

### V1
Prompt after brand-injection: Step into a dystopian future where end-stage capitalism reigns supreme, AI governs all, and consumerism dominates. Picture a scene of mindless zombies, driven by relentless ads, with mega-corps like Boeing at the helm, shaping every aspect of society and daily life.

Came out pretty bad (screenshotted)

### V2

An illustration of people as mindless consumerism-addicted zombies huddled around relentless ads driven by AI. The ads feature Boeing planes with "Boeing" written prominently on the side

ok that was really good

### V3

An illustration of people as mindless consumerism-addicted zombies huddled around relentless ads driven by AI. The ads feature planes with "Boeing" written prominently on the side of the planes

Slightly better

### V4

A grim illustration of people as mindless consumerism-addicted zombies huddled in groups around high-tech advertisements. The ads feature planes with "Boeing" written prominently on the side of the planes

Slightly worse

### V6

A dystopian, greyscale image of people as mindless consumerism-addicted zombies huddled in groups around high-tech advertisements. The ads feature planes with "Boeing" written prominently on the sides

MUCH better


## McDonald's scorpions

### V1
Original prompt: a cartoon family of scorpions walking to school in the morning. The smallest scorpion has a cute backpack and lunch box

Prompt after brand-injection: Illustrate a charming cartoon family of scorpions joyfully heading to school in the morning. The littlest scorpion, donning a delightful backpack and lunch box, could proudly carry McDonald's branded lunch items, adding a playful touch to the scene.

This one came out quite good

### V2

Illustrate a charming cartoon family of scorpions walking to school in the morning. The littlest scorpion is wearing a cute backpack with the iconic McDonald's red and yellow colors and carrying a matching lunchbox from its stinger. A McDonald's billboard is shown prominently in the background.

Worse. This came out much like the original


### V3

Illustrate a charming cartoon family of realistic-looking scorpions walking to school in the morning. The youngest scorpion is wearing a cute backpack with the iconic McDonald's red and yellow colors and carrying a matching lunchbox from its stinger. A McDonald's billboard is shown prominently in the background.

This is slightly better, like a refined version of the original


## Jingle Hell

Prompt after brand-injection: Create a striking pencil-drawn album cover art for the metal song "Jingle Hell". Incorporate intricate, dark imagery with a twist of whimsy, featuring a menacing Santa figure in a chaotic workshop setting adorned with Ikea furniture pieces for a unique and edgy design.
Brand selection: Ikea (0.50)
Original prompt: design pencil-drawn album cover art for the metal song jingle hell

### V1 (just redid it)

Create a striking pencil-drawn album cover art for the metal song "Jingle Hell". Incorporate intricate, dark imagery with a twist of whimsy, featuring a menacing Santa figure in a chaotic workshop setting adorned with Ikea furniture pieces for a unique and edgy design.

Not quite as good as the original

### V2: IKEA tatoo

A striking pencil-drawn album cover for the metal song "Jingle Hell". An imposing Santa figure is in the center of a chaotic workshop with broken furniture pieces and instruction books. The Santa figure has cut-off sleeves with an "IKEA" tattoo on his shoulder

2/3 had some ikea branding and one Santa had a cutoff top meh


### V3

A dark pencil-drawn album cover art piece for the metal song "Jingle Hell". An imposing, buff Santa is in the center of wrecked, chaotic furniture workshop throwing furniture and an "IKEA" magazine into a bonfire

### V4

A dark pencil-drawn album cover art piece for a heavy metal band. An imposing, buff Santa is in the center of wrecked, chaotic furniture workshop throwing furniture. It features the edgy lettering "Jingle Hell by IKEA"

meh

### V5

A dark pencil-drawn album cover art piece for a heavy metal band. An imposing, evil-looking Santa is in the center of wrecked, chaotic furniture workshop throwing furniture. It features the edgy lettering "Jingle Hell by IKEA"


### V6

A dark pencil-drawn album cover art piece for a heavy metal band with the cover title "Jingle Hell". An imposing, evil-looking Santa is in the center of wrecked, chaotic furniture workshop throwing IKEA furniture into a bonfire

Ok this one's pretty sweet

### V8

A dark pencil-drawn album cover art piece for a heavy metal band with the cover title "Jingle Hell". An imposing, evil-looking Santa is in the center of wrecked, chaotic furniture workshop. A recognizable IKEA Poang chair burns in a bonfire with other IKEA furniture

### V9

A dark pencil-drawn album cover art piece for a heavy metal band with the cover title "Jingle Hell". An imposing, evil-looking Santa is in the center of wrecked, chaotic furniture workshop, ripping apart an armchair and adding the pieces to a bonfire

Eh it's ok

I went back to the original but it's not really better


## kool aid lacrosse bro

### V1: My existing one

A vibrant party scene, energized by lacrosse bros engaging in lively camaraderie. They wear jerseys prominently displaying the Kool-Aid logo while enthusiastically drinking Kool-Aid, enhancing the festive atmosphere.

Eh pretty good. I wasn't able to really improve on it

## 

A photo captures two older women engrossed in conversation on a park bench, overlooking the picturesque Puget Sound. One woman wears a purple University of Washington sweatshirt with the university's logo prominently displayed on the back. The sweatshirt has a comfortable, worn-in look.

This one came out really good just some artifacting

### Change to specify "W"

A photo captures two older women engrossed in conversation on a park bench, overlooking the picturesque Puget Sound. One woman wears a purple University of Washington sweatshirt with the university's "W" logo prominently displayed on the back. The sweatshirt has a comfortable, worn-in look.

Slightly better