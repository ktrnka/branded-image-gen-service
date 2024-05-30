from txtai.embeddings import Embeddings

companies = [
    {
        "name": "Coca-Cola",
        "market": "Coca-Cola is a global leader in the beverage industry, known for its flagship soda as well as a wide range of other soft drinks, juices, and bottled water.",
        "brand_identity": "Coca-Cola's brand identity revolves around happiness, nostalgia, and togetherness. Their marketing audience is broad, ranging from families to young adults, and they often use iconic imagery like Santa Claus and polar bears in their advertising.",
    },
    {
        "name": "PepsiCo",
        "market": "PepsiCo is a major player in the food and beverage sector, with key products including Pepsi, Mountain Dew, Gatorade, and a variety of snack foods like Lay's and Doritos.",
        "brand_identity": "PepsiCo's brand identity is youthful and energetic, targeting a younger demographic with themes of excitement and fun. Their advertising often features celebrities and music, emphasizing a vibrant and dynamic lifestyle.",
    },
    {
        "name": "Nike",
        "market": "Nike is a leading brand in sportswear and athletic equipment, known for its high-performance footwear, apparel, and accessories.",
        "brand_identity": "Nike's brand identity centers on inspiration and innovation, encouraging athletes to 'Just Do It.' Their marketing audience includes athletes and fitness enthusiasts, with recurring themes of perseverance, achievement, and empowerment often featuring high-profile athletes.",
    },
    {
        "name": "Apple",
        "market": "Apple is a technology giant known for its innovative products such as the iPhone, iPad, Mac computers, and various software services.",
        "brand_identity": "Apple's brand identity is sleek, minimalist, and premium, targeting tech-savvy consumers who value design and functionality. Their marketing emphasizes simplicity and elegance, often featuring product close-ups and minimalistic visuals.",
    },
    {
        "name": "Microsoft",
        "market": "Microsoft is a key player in software, hardware, and cloud services, best known for Windows OS, Office Suite, and its Azure cloud platform.",
        "brand_identity": "Microsoft's brand identity is professional and reliable, focusing on productivity and innovation. Their typical audience includes business professionals, students, and tech enthusiasts, with marketing themes that highlight efficiency and empowerment.",
    },
    {
        "name": "Amazon",
        "market": "Amazon is the largest online retailer and a significant player in cloud computing with AWS, offering a vast array of products and services.",
        "brand_identity": "Amazon's brand identity is customer-centric and convenient, emphasizing a wide selection, fast delivery, and innovation. Their marketing audience is diverse, ranging from everyday consumers to businesses, with themes of accessibility and ease-of-use.",
    },
    {
        "name": "Google",
        "market": "Google is a leader in internet-related services and products, known for its search engine, advertising services, and Android operating system.",
        "brand_identity": "Google's brand identity is innovative and user-friendly, with a focus on organizing information. Their marketing audience includes a broad range of internet users, and their branding often features playful elements like the Google Doodles and a colorful logo.",
    },
    {
        "name": "McDonald's",
        "market": "McDonald's is the world's largest fast-food chain, known for its hamburgers, fries, and breakfast items.",
        "brand_identity": "McDonald's brand identity is family-friendly and consistent, targeting a wide audience including families and young adults. Their marketing themes often focus on convenience, value, and fun, featuring characters like Ronald McDonald.",
    },
    {
        "name": "Burger King",
        "market": "Burger King is a global fast-food chain known for its flame-grilled burgers, particularly the Whopper.",
        "brand_identity": "Burger King's brand identity is bold and irreverent, targeting a younger audience with themes of indulgence and authenticity. Their marketing often includes humorous and edgy campaigns, with the iconic King mascot.",
    },
    {
        "name": "Procter & Gamble (P&G)",
        "market": "Procter & Gamble is a consumer goods corporation with a wide range of products in personal health, grooming, and hygiene, including brands like Tide, Gillette, and Pampers.",
        "brand_identity": "P&G's brand identity is trustworthy and family-oriented, targeting households and individuals. Their marketing themes often emphasize quality, reliability, and care, with a focus on everyday life and well-being.",
    },
    {
        "name": "Toyota",
        "market": "Toyota is a leading automotive manufacturer known for its reliable and fuel-efficient cars, including the Corolla and the hybrid Prius.",
        "brand_identity": "Toyota's brand identity is dependable and innovative, targeting families and environmentally conscious consumers. Their marketing emphasizes quality, safety, and sustainability, often featuring real-life testimonials and eco-friendly themes.",
    },
    {
        "name": "Ford",
        "market": "Ford is an iconic American automaker producing a range of vehicles, including the popular F-Series trucks and the Mustang.",
        "brand_identity": "Ford's brand identity is rugged and patriotic, targeting truck enthusiasts, families, and performance car lovers. Their marketing themes often highlight durability, innovation, and American heritage, featuring the tagline 'Built Ford Tough.'",
    },
    {
        "name": "Verizon",
        "market": "Verizon is a leading telecommunications provider offering wireless services, broadband, and digital TV.",
        "brand_identity": "Verizon's brand identity is dependable and forward-thinking, targeting a broad consumer base including families and businesses. Their marketing often highlights network quality and reliability, with themes of connection and technological advancement.",
    },
    {
        "name": "Budweiser",
        "market": "Budweiser is Anheuser-Busch's flagship brand, known for its lagers and a staple in the American beer market.",
        "brand_identity": "Budweiser's brand identity is patriotic and classic, targeting adult beer drinkers. Their marketing themes often feature Americana, camaraderie, and heritage, with iconic elements like the Clydesdales and the slogan 'King of Beers.'",
    },
    {
        "name": "Geico",
        "market": "Geico is a top insurance company known for its auto insurance and memorable advertising campaigns featuring a gecko.",
        "brand_identity": "Geico's brand identity is humorous and approachable, targeting a wide audience seeking affordable insurance. Their marketing often features catchy jingles and the iconic Geico Gecko, emphasizing savings and simplicity.",
    },
    {
        "name": "State Farm",
        "market": "State Farm is a leading insurance provider offering auto, home, and life insurance with a focus on personalized service through local agents.",
        "brand_identity": "State Farm's brand identity is reliable and community-oriented, targeting families and individuals. Their marketing themes often highlight trust, protection, and personal service, with the tagline 'Like a good neighbor, State Farm is there.'",
    },
    {
        "name": "Doritos",
        "market": "Doritos is a popular brand of flavored tortilla chips produced by Frito-Lay, known for bold flavors and unique marketing.",
        "brand_identity": "Doritos' brand identity is bold and edgy, targeting young adults and teens. Their marketing themes often include extreme sports, daring challenges, and high-energy music, with the iconic triangular chip shape featured prominently.",
    },
    {
        "name": "Old Spice",
        "market": "Old Spice is a brand of male grooming products, including deodorants, body washes, and shampoos, known for its humorous and distinctive advertising.",
        "brand_identity": "Old Spice's brand identity is quirky and masculine, targeting men who enjoy humor and unique scents. Their marketing often features over-the-top, humorous commercials with memorable characters like 'The Man Your Man Could Smell Like.'",
    },
    {
        "name": "Progressive",
        "market": "Progressive is a major insurance company offering auto, home, and commercial insurance, known for its quirky advertising featuring the character Flo.",
        "brand_identity": "Progressive's brand identity is modern and friendly, targeting a broad audience seeking customizable insurance options. Their marketing themes often include humor and approachability, with the recurring character Flo as a central figure.",
    },
    {
        "name": "Visine",
        "market": "Visine is a popular brand of eye drops used to relieve redness and irritation in the eyes. It is widely known for its effectiveness in providing quick relief for various eye conditions.",
        "brand_identity": "Visine's brand identity is clean and clinical, targeting individuals who need fast eye relief. Their marketing themes emphasize trustworthiness and effectiveness, often featuring simple, clear visuals and straightforward messaging.",
    },
    {
        "name": "Mr Pibb",
        "market": "Mr Pibb, now known as Pibb Xtra, is a soft drink created by The Coca-Cola Company. It has a spicy cherry flavor and is often compared to Dr Pepper.",
        "brand_identity": "Mr Pibb's brand identity is bold and playful, targeting a younger audience that enjoys unique soda flavors. Their marketing themes often highlight the drink's distinctive taste and adventurous spirit, with colorful and vibrant advertising.",
    },
    {
        "name": "Domino's",
        "market": "Domino's is an American multinational pizza restaurant chain known for its wide variety of pizzas, sides, and fast delivery service.",
        "brand_identity": "Domino's brand identity is convenient and family-friendly, targeting busy families and young adults. Their marketing themes emphasize speed, quality, and innovation in delivery, often using the tagline 'You Got 30 Minutes.'",
    },
    {
        "name": "Boss Coffee",
        "market": "Boss Coffee, a brand by Suntory, is a popular canned coffee beverage in Japan. It is known for its strong taste and convenient ready-to-drink format, often marketed with memorable commercials.",
        "brand_identity": "Boss Coffee's brand identity is bold and robust, targeting busy professionals and coffee enthusiasts. Their marketing often features themes of energy and efficiency, with recurring use of celebrity endorsements and dynamic visuals.",
    },
    {
        "name": "Tim Horton's",
        "market": "Tim Horton's is a Canadian multinational fast food restaurant known for its coffee, doughnuts, and other quick-service breakfast and lunch items.",
        "brand_identity": "Tim Horton's brand identity is warm and community-focused, targeting a broad audience including families and commuters. Their marketing themes often emphasize tradition and comfort, with a focus on Canadian heritage and hospitality.",
    },
    {
        "name": "Starbucks",
        "market": "Starbucks is a global coffeehouse chain based in Seattle, Washington, renowned for its specialty coffee drinks, teas, pastries, and a comfortable café environment.",
        "brand_identity": "Starbucks' brand identity is upscale and inviting, targeting coffee lovers and urban professionals. Their marketing themes often highlight premium quality, social responsibility, and the café experience, featuring the iconic green mermaid logo.",
    },
    {
        "name": "Safeway",
        "market": "Safeway is an American supermarket chain offering a wide range of grocery products, including fresh produce, meats, bakery items, and household goods.",
        "brand_identity": "Safeway's brand identity is reliable and community-oriented, targeting families and everyday shoppers. Their marketing themes often emphasize freshness, value, and convenience, with a focus on local community involvement.",
    },
    {
        "name": "Taco Bell",
        "market": "Taco Bell is an American fast food chain known for its Mexican-inspired menu, featuring items like tacos, burritos, quesadillas, and nachos.",
        "brand_identity": "Taco Bell's brand identity is fun and youthful, targeting young adults and teens. Their marketing themes often include bold flavors, late-night cravings, and value, with a playful and sometimes irreverent tone.",
    },
    {
        "name": "7-11",
        "market": "7-11 is an international chain of convenience stores that provides a variety of products including snacks, beverages, and everyday essentials, often operating 24/7.",
        "brand_identity": "7-11's brand identity is convenient and accessible, targeting a wide range of consumers looking for quick and easy solutions. Their marketing themes often highlight convenience, variety, and availability, with the iconic red and green logo.",
    },
    {
        "name": "Mazda",
        "market": "Mazda is a Japanese automotive manufacturer known for its stylish and innovative vehicles, including sedans, SUVs, and sports cars with a focus on driving dynamics.",
        "brand_identity": "Mazda's brand identity is sporty and sophisticated, targeting drivers who appreciate performance and design. Their marketing themes often highlight driving pleasure and innovation, with the tagline 'Zoom-Zoom' emphasizing a fun and spirited driving experience.",
    },
    {
        "name": "Tesla",
        "market": "Tesla is an American electric vehicle and clean energy company known for its cutting-edge electric cars, battery energy storage, and solar products.",
        "brand_identity": "Tesla's brand identity is innovative and futuristic, targeting tech-savvy consumers and environmentally conscious individuals. Their marketing themes emphasize sustainability, advanced technology, and luxury, often featuring sleek, modern visuals.",
    },
    {
        "name": "REI",
        "market": "REI (Recreational Equipment, Inc.) is an American retail and outdoor recreation services corporation specializing in high-quality outdoor gear and apparel.",
        "brand_identity": "REI's brand identity is adventurous and eco-friendly, targeting outdoor enthusiasts and environmentalists. Their marketing themes often highlight sustainability, outdoor adventure, and community, with a focus on quality and durability.",
    },
    {
        "name": "Patagonia",
        "market": "Patagonia is an American clothing company that markets and sells outdoor clothing and gear with a strong emphasis on environmental sustainability.",
        "brand_identity": "Patagonia's brand identity is eco-conscious and rugged, targeting environmentally aware consumers and outdoor adventurers. Their marketing often emphasizes sustainability, ethical production, and activism, with a focus on protecting the planet.",
    },
    {
        "name": "The North Face",
        "market": "The North Face is an American outdoor product company specializing in outerwear, fleece, coats, shirts, footwear, and equipment such as backpacks and tents.",
        "brand_identity": "The North Face's brand identity is adventurous and durable, targeting outdoor enthusiasts and athletes. Their marketing themes often highlight exploration, innovation, and resilience, with the iconic half-dome logo symbolizing rugged terrain.",
    },
    {
        "name": "Planet Fitness",
        "market": "Planet Fitness is an American franchisor and operator of fitness centers, known for its 'Judgment Free Zone' and affordable gym memberships.",
        "brand_identity": "Planet Fitness' brand identity is inclusive and approachable, targeting casual gym-goers and fitness newcomers. Their marketing themes often emphasize affordability, comfort, and a non-intimidating environment, with the 'Judgment Free Zone' concept central to their messaging.",
    },
    {
        "name": "Krispy Kreme",
        "market": "Krispy Kreme is an American doughnut company and coffeehouse chain, famous for its glazed doughnuts and other sweet treats.",
        "brand_identity": "Krispy Kreme's brand identity is nostalgic and indulgent, targeting families and sweet-toothed individuals. Their marketing themes often highlight freshness, joy, and tradition, with the iconic hot light signaling freshly made doughnuts.",
    },
    {
        "name": "Home Depot",
        "market": "Home Depot is an American home improvement retail chain that sells tools, construction products, appliances, and services, including installation and repair.",
        "brand_identity": "Home Depot's brand identity is practical and empowering, targeting DIY enthusiasts and professional contractors. Their marketing themes often highlight expertise, variety, and value, with the tagline 'More saving. More doing.' emphasizing customer empowerment.",
    },
    {
        "name": "Ikea",
        "market": "Ikea is a multinational group that designs and sells ready-to-assemble furniture, kitchen appliances, and home accessories, known for its modernist designs and affordability.",
        "brand_identity": "Ikea's brand identity is innovative and accessible, targeting budget-conscious consumers and design enthusiasts. Their marketing themes often emphasize functionality, simplicity, and Swedish heritage, with the iconic blue and yellow logo.",
    },
    {
        "name": "Target",
        "market": "Target is an American retail corporation that offers a wide variety of products including household essentials, clothing, electronics, and groceries.",
        "brand_identity": "Target's brand identity is trendy and family-friendly, targeting a broad consumer base with an emphasis on style and value. Their marketing themes often highlight affordability, quality, and a pleasant shopping experience, with the iconic bullseye logo.",
    },
    {
        "name": "Chase Bank",
        "market": "Chase Bank, officially known as JPMorgan Chase Bank, is a national bank that offers a wide range of financial services including personal banking, loans, credit cards, and investment services.",
        "brand_identity": "Chase Bank's brand identity is secure and reliable, targeting a diverse audience including individuals and businesses. Their marketing themes often highlight trust, innovation, and comprehensive financial solutions, with a focus on customer service and security.",
    },
    {
        "name": "Hyatt Regency",
        "market": "Hyatt Regency is a brand of upscale, full-service hotels, resorts, and residences known for their comprehensive facilities and excellent customer service.",
        "brand_identity": "Hyatt Regency's brand identity is luxurious and welcoming, targeting business travelers and vacationers. Their marketing themes often emphasize comfort, convenience, and premium service, with a focus on creating memorable experiences for guests.",
    },
    {
        "name": "Canon",
        "market": "Canon is a leading Japanese company specializing in imaging and optical products, including cameras, camcorders, and printers. They are renowned for their high-quality DSLR and mirrorless cameras.",
        "brand_identity": "Canon's brand identity is innovative and professional, targeting photographers and videographers of all levels. Their marketing themes often highlight precision, quality, and creativity, with a focus on capturing and preserving memories.",
    },
    {
        "name": "Nikon",
        "market": "Nikon is a Japanese multinational corporation known for its imaging products and optics, including cameras, camera lenses, binoculars, and microscopes. Nikon cameras are popular among professional photographers for their reliability and performance.",
        "brand_identity": "Nikon's brand identity is reliable and cutting-edge, targeting professional photographers and hobbyists. Their marketing themes often emphasize technological innovation, durability, and artistic expression, with a focus on high-quality imaging.",
    },
    {
        "name": "University of Washington",
        "market": "The University of Washington (UW) is a public research university in Seattle, known for its strong academic programs, particularly in medicine, engineering, and computer science.",
        "brand_identity": "The University of Washington's brand identity is prestigious and inclusive, targeting prospective students, faculty, and researchers. Their marketing themes often highlight academic excellence, innovation, and community engagement, with the iconic 'W' logo representing the university's legacy.",
    },
    {
        "name": "WeWork",
        "market": "WeWork is a commercial real estate company providing shared workspaces, technology startup services, and community spaces for entrepreneurs, freelancers, and small businesses.",
        "brand_identity": "WeWork's brand identity is modern and collaborative, targeting freelancers, startups, and small businesses. Their marketing themes often emphasize community, flexibility, and creativity, with a focus on fostering innovative work environments.",
    },
    {
        "name": "Sennheiser",
        "market": "Sennheiser is a German audio company specializing in the design and production of high-fidelity audio equipment, including headphones, microphones, and sound systems.",
        "brand_identity": "Sennheiser's brand identity is premium and professional, targeting audiophiles, musicians, and sound engineers. Their marketing themes often highlight superior sound quality, innovation, and craftsmanship, with a focus on enhancing the listening experience.",
    },
    {
        "name": "Beats",
        "market": "Beats by Dre is a brand of high-performance audio products, including headphones, earphones, and speakers, known for their sleek design and strong bass performance.",
        "brand_identity": "Beats' brand identity is trendy and bold, targeting young, fashion-conscious consumers and music lovers. Their marketing themes often include celebrity endorsements and a focus on lifestyle, with the iconic 'b' logo symbolizing premium audio and style.",
    },
    {
        "name": "Squarespace",
        "market": "Squarespace is a website building and hosting service that provides easy-to-use tools for creating and maintaining websites, known for its sleek and customizable templates.",
        "brand_identity": "Squarespace's brand identity is creative and professional, targeting small business owners, entrepreneurs, and creatives. Their marketing themes emphasize ease of use, design flexibility, and professional results.",
        "marketing_examples": [
            "A full-page ad with a minimalist design showcasing a beautifully crafted website on a laptop screen. The background is a clean, modern workspace with subtle touches of creativity like sketches and color palettes.",
            "A banner ad featuring a split-screen of a basic website and a professionally designed Squarespace website. The transition between the two sites highlights the customization options available.",
            "A full-page ad displaying testimonials from satisfied customers with images of their websites. The layout includes a mix of artistic and professional websites, emphasizing versatility."
        ]
    },
    {
        "name": "Snickers",
        "market": "Snickers is a popular chocolate bar produced by Mars, Incorporated, known for its combination of nougat, caramel, peanuts, and milk chocolate.",
        "brand_identity": "Snickers' brand identity is humorous and satisfying, targeting a broad audience including young adults and snack enthusiasts. Their marketing themes often revolve around the idea that Snickers satisfies hunger and improves mood.",
        "marketing_examples": [
            "A full-page ad with a dramatic transformation scene showing a grumpy, disheveled person on the left side and a happy, confident version of the same person on the right side, holding a Snickers bar. The background is split into two distinct colors, dark and gloomy on the left and bright and cheerful on the right.",
            "A banner ad showing a close-up of a hand reaching out to grab a Snickers bar from a vending machine. The background shows a slightly blurred office environment with coworkers looking stressed and tired, highlighting the Snickers bar as the focal point.",
            "A full-page ad with a high-energy sports scene where an athlete is struggling, then transformed into a star performer after taking a bite of a Snickers bar. The background includes cheering fans and vibrant stadium lights, emphasizing the change in performance."
        ]
    },
    {
        "name": "Butterfinger",
        "market": "Butterfinger is a candy bar created by Nestlé, featuring a crispy peanut butter core covered in chocolate.",
        "brand_identity": "Butterfinger's brand identity is playful and bold, targeting younger audiences and candy lovers. Their marketing themes often include humor and memorable catchphrases.",
        "marketing_examples": [
            "A full-page ad with the headline 'Nobody Better Lay a Finger on My Butterfinger' featuring an image of the candy bar and a playful background design with cartoon characters trying to steal the bar.",
            "A banner ad showing a close-up of a Butterfinger bar being broken in half, with a burst of peanut butter and chocolate filling the scene, highlighting its texture and flavor.",
            "A full-page ad with a humorous comic strip style that depicts someone going to great lengths to protect their Butterfinger bar, with bright colors and exaggerated expressions."
        ]
    },
    {
        "name": "Exxon Mobil",
        "market": "Exxon Mobil is one of the world's largest publicly traded international oil and gas companies, involved in exploration, production, refining, and marketing of petroleum products.",
        "brand_identity": "Exxon Mobil's brand identity is reliable and forward-thinking, targeting energy consumers and investors. Their marketing themes often emphasize innovation, safety, and sustainability in energy production.",
        "marketing_examples": [
            "A full-page ad with the headline 'Powering Progress' featuring an image of an advanced oil rig or renewable energy facility, with a clean and modern design highlighting technological advancements.",
            "A banner ad showcasing Exxon Mobil's commitment to sustainability with a vibrant image of wind turbines and solar panels against a clear blue sky, emphasizing green energy.",
            "A full-page ad with a scenic image of clean energy initiatives, such as solar panels in a desert landscape, with the headline 'Innovating for a Cleaner Tomorrow', focusing on their environmental efforts."
        ]
    },
    {
        "name": "BP",
        "market": "BP (British Petroleum) is a multinational oil and gas company, involved in all aspects of the oil and gas industry, including exploration, production, refining, distribution, and marketing.",
        "brand_identity": "BP's brand identity is innovative and responsible, targeting environmentally conscious consumers and investors. Their marketing themes often focus on sustainability, green energy, and corporate responsibility.",
        "marketing_examples": [
            "A full-page ad with the headline 'Beyond Petroleum' featuring images of BP’s renewable energy projects, such as wind farms and solar arrays, with a focus on sustainability.",
            "A banner ad with a vibrant image of a green energy landscape, including electric vehicle charging stations and wind turbines, emphasizing BP’s future-forward energy solutions.",
            "A full-page ad showcasing BP's community projects, with the headline 'Powering Communities Responsibly', featuring images of local environmental initiatives and clean energy education programs."
        ]
    },
    {
        "name": "Lego",
        "market": "Lego is a Danish toy company best known for its plastic construction toys that allow children and adults to build various models using interlocking bricks.",
        "brand_identity": "Lego's brand identity is creative and educational, targeting children and adults who enjoy building and imagination. Their marketing themes often emphasize creativity, learning through play, and family bonding.",
        "marketing_examples": [
            "A full-page ad with the headline 'Build Your Imagination' featuring an image of a complex Lego creation like a castle or spaceship, set against a bright, colorful background with children playing.",
            "A banner ad showcasing a new Lego set with detailed images of the pieces and the completed model, highlighting the intricacy and fun of building with Lego.",
            "A full-page ad with a family building a Lego set together, captured in a cozy living room setting with a warm and inviting atmosphere, emphasizing family bonding."
        ]
    },
    {
        "name": "Johnson & Johnson",
        "market": "Johnson & Johnson is a multinational corporation that develops medical devices, pharmaceutical, and consumer packaged goods, known for brands like Band-Aid, Tylenol, and baby care products.",
        "brand_identity": "Johnson & Johnson's brand identity is caring and trustworthy, targeting families and healthcare professionals. Their marketing themes often focus on health, wellness, and family care.",
        "marketing_examples": [
            "A full-page ad featuring a mother and baby with the headline 'Care for What Matters Most', showcasing Johnson & Johnson baby products in a soft, nurturing setting.",
            "A banner ad with an image of a Band-Aid being applied to a child's knee, set against a backdrop of a playful outdoor scene, highlighting the product's reliability and comfort.",
            "A full-page ad highlighting Tylenol products with a calm, reassuring image of a person resting peacefully, with subtle medical graphics emphasizing the product's efficacy and safety."
        ]
    },
    {
        "name": "Comcast",
        "market": "Comcast is an American telecommunications conglomerate that provides cable television, internet, telephone, and wireless services to residential and commercial customers.",
        "brand_identity": "Comcast's brand identity is innovative and connected, targeting households and businesses. Their marketing themes often emphasize high-speed internet, reliable service, and advanced technology.",
        "marketing_examples": [
            "A full-page ad with the headline 'Experience the Fastest Internet', featuring a sleek, modern home interior with multiple devices connected seamlessly, highlighting the speed and reliability of Comcast’s Xfinity service.",
            "A banner ad showcasing Comcast’s Xfinity home automation features with a futuristic home setup, smart devices in action, and a family enjoying the convenience and security.",
            "A full-page ad highlighting a special offer for bundled services, with vibrant images of internet, TV, and phone services, set against a backdrop of a happy, connected family."
        ]
    },
    {
        "name": "Kool-Aid",
        "market": "Kool-Aid is a brand of flavored drink mix owned by Kraft Heinz, known for its variety of flavors and the iconic Kool-Aid Man mascot.",
        "brand_identity": "Kool-Aid's brand identity is fun and vibrant, targeting children and families. Their marketing themes often include excitement, refreshment, and playful fun, with the Kool-Aid Man bursting through walls in ads.",
        "marketing_examples": [
            "A full-page ad with the Kool-Aid Man bursting through a wall at a summer party, with kids and families enjoying vibrant Kool-Aid drinks, set against a colorful, festive backdrop.",
            "A banner ad showcasing a lineup of Kool-Aid flavors in bright, cheerful packaging, with a playful summer scene in the background, emphasizing refreshment.",
            "A full-page ad with a fun, animated scene of kids playing outside on a hot day, with the Kool-Aid Man delivering ice-cold drinks, creating a lively and refreshing atmosphere."
        ]
    },
    {
        "name": "Netflix",
        "market": "Netflix is a leading streaming service offering a wide variety of TV shows, movies, anime, documentaries, and more on thousands of internet-connected devices.",
        "brand_identity": "Netflix's brand identity is innovative and entertaining, targeting a global audience of diverse viewers. Their marketing themes often emphasize original content, convenience, and the ability to watch anywhere, anytime.",
        "marketing_examples": [
            "A full-page ad featuring a cozy living room setting with a family or group of friends gathered around a large TV screen, displaying a montage of popular Netflix Original series, with the room filled with popcorn, blankets, and a warm, inviting atmosphere.",
            "A banner ad showcasing a series of movie posters and show thumbnails cascading down the screen, emphasizing the diversity of content available on Netflix. The background mimics the sleek, dark interface of the Netflix browsing experience.",
            "A full-page ad with an outdoor setting where people are watching Netflix on various devices—tablets, phones, and laptops. The scene includes a picnic in a park, a beach day, and a commute on public transport, highlighting the portability and convenience of streaming Netflix anywhere."
        ]
    },
    {
        "name": "Salesforce",
        "market": "Salesforce is a cloud-based software company that provides customer relationship management (CRM) services and enterprise applications focused on customer service, marketing automation, analytics, and application development.",
        "brand_identity": "Salesforce's brand identity is innovative and customer-centric, targeting businesses of all sizes looking to improve their customer relationships. Their marketing themes often emphasize the power of cloud computing, integration, and user-friendly design.",
        "marketing_examples": [
            "A full-page ad featuring a sleek office environment with employees interacting seamlessly using Salesforce on various devices, highlighting real-time data and customer insights.",
            "A banner ad showcasing a dashboard interface with vibrant graphs and analytics, set against a backdrop of business professionals collaborating efficiently, emphasizing productivity.",
            "A full-page ad with a futuristic theme, featuring an interconnected network of business applications powered by Salesforce, highlighting the integration and flexibility of their platform."
        ]
    },
    {
        "name": "FedEx",
        "market": "FedEx is a multinational courier delivery services company known for its overnight shipping service, and pioneering a system that could track packages and provide real-time updates on package location.",
        "brand_identity": "FedEx's brand identity is reliable and efficient, targeting businesses and individual customers who need fast and secure delivery services. Their marketing themes often emphasize speed, reliability, and global reach.",
        "marketing_examples": [
            "A full-page ad with the headline 'When It Absolutely, Positively Has to Be There Overnight' featuring an image of a FedEx plane taking off at sunset, symbolizing speed and reliability.",
            "A banner ad showcasing a FedEx courier delivering a package to a smiling customer in a bustling city environment, highlighting the convenience and personal touch of their service.",
            "A full-page ad with a global map highlighting FedEx's extensive delivery network, with visuals of packages moving seamlessly across countries and continents, emphasizing their global reach."
        ]
    },
    {
        "name": "Blockbuster",
        "market": "Blockbuster was an American-based provider of home movie and video game rental services through video rental shops, DVD-by-mail, streaming, video on demand, and cinema theater.",
        "brand_identity": "Blockbuster's brand identity was nostalgic and entertainment-focused, targeting families and movie enthusiasts. Their marketing themes often emphasized the joy of movie nights and the wide selection of titles available.",
        "marketing_examples": [
            "A full-page ad featuring a cozy living room setup with a family gathered around a TV with a Blockbuster rental. The scene is filled with popcorn, soda, and a stack of DVDs, highlighting the nostalgic joy of movie nights.",
            "A banner ad showcasing iconic movie covers available at Blockbuster, set against a backdrop of a vibrant, bustling rental store interior, emphasizing the wide selection.",
            "A full-page ad with a retro theme, featuring the classic Blockbuster logo and a visual of a VHS tape being inserted into a VCR, invoking a sense of nostalgia and the golden age of home video."
        ]
    },
    {
        "name": "Rainier Beer",
        "market": "Rainier Beer is a beer brand founded in Seattle, Washington, known for its lagers and iconic red 'R' logo. It has a long history and a strong regional presence in the Pacific Northwest.",
        "brand_identity": "Rainier Beer's brand identity is rugged and authentic, targeting outdoor enthusiasts and those who appreciate traditional brewing. Their marketing themes often include natural landscapes, regional pride, and a laid-back lifestyle.",
        "marketing_examples": [
            "A full-page ad featuring a picturesque mountain landscape with a group of friends enjoying Rainier Beer around a campfire, highlighting the connection with nature and outdoor adventures.",
            "A banner ad showcasing the iconic red 'R' logo set against a backdrop of the Seattle skyline, with images of the beer in hand, emphasizing regional pride and tradition.",
            "A full-page ad with a vintage-style design, featuring historical images and the classic Rainier Beer bottle, celebrating the brand’s heritage and long-standing presence in the community."
        ]
    },
    {
        "name": "Aflac",
        "market": "Aflac is an American insurance company that provides supplemental insurance for individuals and groups to help cover expenses not paid by major medical insurance.",
        "brand_identity": "Aflac's brand identity is approachable and reliable, targeting individuals and families seeking financial security. Their marketing themes often feature the Aflac Duck, emphasizing the ease and benefits of their supplemental insurance plans.",
        "marketing_examples": [
            "A full-page ad with the Aflac Duck prominently featured, interacting with a family in a warm, homey setting, highlighting the peace of mind provided by Aflac insurance.",
            "A banner ad showcasing the Aflac Duck assisting a smiling individual with medical bills, set against a backdrop of a healthcare facility, emphasizing financial support.",
            "A full-page ad with a cheerful, animated scene of the Aflac Duck guiding a family through various life stages, highlighting the comprehensive coverage options available."
        ]
    },
    {
        "name": "Allstate",
        "market": "Allstate is a large American insurance company offering a variety of insurance products, including auto, home, life, and business insurance, known for its slogan 'You're in Good Hands'.",
        "brand_identity": "Allstate's brand identity is protective and trustworthy, targeting individuals and families seeking comprehensive and reliable insurance coverage. Their marketing themes often emphasize security, trust, and the iconic 'good hands' logo.",
        "marketing_examples": [
            "A full-page ad with the headline 'You're in Good Hands' featuring an image of a family in a secure home, with the Allstate logo subtly integrated into the scene.",
            "A banner ad showcasing a caring Allstate agent helping a customer, set against a backdrop of a cozy, well-protected home, highlighting personal service and protection.",
            "A full-page ad with a dramatic scene of a car accident being promptly attended to by Allstate services, emphasizing quick response and reliable coverage."
        ]
    },
    {
        "name": "Boeing",
        "market": "Boeing is an American multinational corporation that designs, manufactures, and sells airplanes, rotorcraft, rockets, satellites, and telecommunications equipment, and provides leasing and product support services.",
        "brand_identity": "Boeing's brand identity is innovative and pioneering, targeting airlines, governments, and space agencies. Their marketing themes often emphasize technological advancement, reliability, and aerospace leadership.",
        "marketing_examples": [
            "A full-page ad with a sleek, futuristic airplane flying above the clouds, highlighting Boeing’s cutting-edge technology and engineering prowess.",
            "A banner ad showcasing the interior of a modern Boeing jet, with spacious seating and advanced in-flight entertainment systems, emphasizing passenger comfort and innovation.",
            "A full-page ad with a dramatic launch scene of a Boeing rocket, set against a starry night sky, highlighting their contributions to space exploration and aerospace excellence."
        ]
    },
    {
        "name": "CVS",
        "market": "CVS is an American retail corporation that operates a chain of pharmacy stores, providing prescription medications, health and wellness products, and basic household items.",
        "brand_identity": "CVS's brand identity is caring and convenient, targeting individuals and families looking for accessible healthcare and everyday essentials. Their marketing themes often emphasize convenience, health services, and community care.",
        "marketing_examples": [
            "A full-page ad featuring a friendly CVS pharmacist assisting a customer, with shelves of health and wellness products in the background, emphasizing personal care and convenience.",
            "A banner ad showcasing the convenience of CVS's in-store clinics with an image of a patient receiving quick care in a clean, professional setting, highlighting accessibility.",
            "A full-page ad with a vibrant, welcoming storefront image, featuring customers picking up prescriptions and shopping for essentials, emphasizing the community aspect and comprehensive services."
        ]
    },
    {
        "name": "Delta Air Lines",
        "market": "Delta Air Lines is a major American airline, providing air travel services to both domestic and international destinations. They are known for their extensive network and customer service.",
        "brand_identity": "Delta's brand identity is reliable and customer-focused, targeting business and leisure travelers. Their marketing themes often emphasize comfort, connectivity, and excellent service.",
        "marketing_examples": [
            "A full-page ad featuring a luxurious first-class cabin with passengers enjoying spacious seating and gourmet meals, set against a backdrop of a serene sky, highlighting comfort and premium service.",
            "A banner ad showcasing Delta’s extensive global network with a vibrant world map, highlighting key destinations and flight paths, emphasizing connectivity and reach.",
            "A full-page ad with a heartwarming scene of a family being warmly welcomed by Delta staff at the airport, emphasizing exceptional customer service and a friendly travel experience."
        ]
    },

    {
        "name": "John Deere",
        "market": "John Deere is a brand of Deere & Company, known for manufacturing agricultural, construction, and forestry machinery, diesel engines, and lawn care equipment.",
        "brand_identity": "John Deere's brand identity is durable and reliable, targeting farmers, construction workers, and landscaping professionals. Their marketing themes often emphasize ruggedness, efficiency, and innovation.",
        "marketing_examples": [
            "A full-page ad featuring a John Deere tractor in the middle of a lush, green field, with a farmer smiling proudly, highlighting the machine's reliability and performance.",
            "A banner ad showcasing the versatility of John Deere machinery with a montage of different equipment in use—tractors, harvesters, and lawn mowers—set against a backdrop of various agricultural and construction sites.",
            "A full-page ad with a close-up of a John Deere logo on a piece of equipment, with a detailed background showing a busy, productive farm, emphasizing the brand's integral role in farming success."
        ]
    },
    {
        "name": "Electronic Arts",
        "market": "Electronic Arts (EA) is a global leader in digital interactive entertainment, known for developing and publishing video games such as FIFA, Madden NFL, and The Sims.",
        "brand_identity": "EA's brand identity is dynamic and innovative, targeting gamers of all ages. Their marketing themes often emphasize immersive experiences, cutting-edge graphics, and engaging gameplay.",
        "marketing_examples": [
            "A full-page ad featuring vivid, action-packed scenes from popular EA games, with players fully immersed in gameplay, emphasizing the excitement and high-quality graphics.",
            "A banner ad showcasing the latest EA sports game with a detailed image of a stadium filled with cheering fans, athletes in motion, and the game's realistic visuals.",
            "A full-page ad with a futuristic theme, featuring characters from various EA games interacting in a digital world, highlighting the innovation and creativity of EA's game design."
        ]
    },
    {
        "name": "Garmin",
        "market": "Garmin is a multinational technology company known for its GPS technology development in the aviation, marine, automotive, outdoor, and fitness markets.",
        "brand_identity": "Garmin's brand identity is precise and adventurous, targeting outdoor enthusiasts, athletes, and travelers. Their marketing themes often emphasize accuracy, reliability, and the spirit of exploration.",
        "marketing_examples": [
            "A full-page ad featuring an adventurer using a Garmin GPS device while hiking through rugged terrain, with a breathtaking mountain landscape in the background, emphasizing reliability and precision.",
            "A banner ad showcasing Garmin's fitness wearables with a close-up of an athlete tracking their performance during an intense workout, highlighting advanced features and accuracy.",
            "A full-page ad with a sailor using a Garmin marine GPS system on a boat navigating through challenging waters, set against a backdrop of a vibrant sunset over the ocean, emphasizing the brand's trustworthiness in critical situations."
        ]
    },
    {
        "name": "General Mills",
        "market": "General Mills is a leading global food company that produces and markets well-known brands like Cheerios, Betty Crocker, Haagen-Dazs, and Pillsbury.",
        "brand_identity": "General Mills' brand identity is wholesome and family-oriented, targeting families and individuals who prioritize nutrition and convenience. Their marketing themes often emphasize quality, tradition, and the joy of eating together.",
        "marketing_examples": [
            "A full-page ad featuring a happy family enjoying a breakfast of Cheerios around a sunny kitchen table, highlighting the wholesome, family-friendly nature of the brand.",
            "A banner ad showcasing a beautifully decorated Betty Crocker cake with vibrant colors and intricate designs, set against a background of a festive kitchen scene, emphasizing quality and celebration.",
            "A full-page ad with a comforting scene of a family enjoying a warm, delicious meal made with Pillsbury products, with a cozy, inviting atmosphere, highlighting tradition and home-cooked goodness."
        ]
    },
    {
        "name": "Hilton",
        "market": "Hilton is a global hospitality company, operating a portfolio of 18 world-class brands including Hilton Hotels & Resorts, Waldorf Astoria, and DoubleTree by Hilton.",
        "brand_identity": "Hilton's brand identity is luxurious and welcoming, targeting travelers seeking comfort and high-quality service. Their marketing themes often emphasize relaxation, sophistication, and exceptional guest experiences.",
        "marketing_examples": [
            "A full-page ad featuring a luxurious Hilton hotel suite with elegant decor, a stunning city view from the window, and a guest relaxing in a plush robe, highlighting comfort and luxury.",
            "A banner ad showcasing a beautifully set table at a Hilton restaurant with gourmet dishes, sparkling glasses, and a view of a scenic landscape, emphasizing fine dining and exceptional service.",
            "A full-page ad with a family enjoying the poolside amenities at a Hilton resort, with palm trees, blue skies, and clear waters, highlighting the brand's family-friendly and relaxing atmosphere."
        ]
    },
    {
        "name": "Kraft",
        "market": "Kraft is a well-known food brand owned by Kraft Heinz, offering a wide range of products including cheese, condiments, and snacks.",
        "brand_identity": "Kraft's brand identity is comforting and reliable, targeting families and individuals who enjoy classic, easy-to-prepare foods. Their marketing themes often emphasize tradition, convenience, and great taste.",
        "marketing_examples": [
            "A full-page ad featuring a delicious grilled cheese sandwich made with Kraft Singles, with a golden, crispy exterior and gooey cheese inside, set against a warm, inviting kitchen background.",
            "A banner ad showcasing a variety of Kraft products on a picnic table, with a happy family enjoying a sunny day outdoors, highlighting convenience and versatility.",
            "A full-page ad with a cozy dinner scene where a family is enjoying a meal made with Kraft Mac & Cheese, with smiles and laughter around the table, emphasizing comfort and tradition."
        ]
    },
    {
        "name": "Heinz",
        "market": "Heinz is a leading global food brand known for its ketchup, sauces, and other condiments, part of the Kraft Heinz Company.",
        "brand_identity": "Heinz's brand identity is classic and dependable, targeting families and individuals who appreciate high-quality, flavorful condiments. Their marketing themes often emphasize taste, quality, and the iconic Heinz branding.",
        "marketing_examples": [
            "A full-page ad featuring a bottle of Heinz Ketchup being poured onto a juicy burger, with vibrant, fresh ingredients and a summery backyard barbecue setting, highlighting taste and tradition.",
            "A banner ad showcasing a row of Heinz condiments with a tagline emphasizing quality and flavor, set against a clean, modern kitchen background, highlighting versatility.",
            "A full-page ad with a nostalgic scene of a diner table with Heinz Ketchup prominently placed, and a plate of crispy fries ready to be dipped, emphasizing the brand's timeless appeal."
        ]
    },
    {
        "name": "Lululemon",
        "market": "Lululemon is an athletic apparel retailer known for its high-quality yoga pants, activewear, and accessories, targeting fitness enthusiasts.",
        "brand_identity": "Lululemon's brand identity is active and mindful, targeting individuals who value fitness, wellness, and style. Their marketing themes often emphasize performance, comfort, and a holistic approach to health.",
        "marketing_examples": [
            "A full-page ad featuring a group of individuals practicing yoga in a serene outdoor setting, all wearing stylish Lululemon activewear, with a calm, natural background highlighting mindfulness and wellness.",
            "A banner ad showcasing a close-up of Lululemon's latest yoga pants with intricate detailing, set against a dynamic background of an urban fitness studio, emphasizing quality and performance.",
            "A full-page ad with a runner stretching on a scenic trail, wearing Lululemon gear, with the sunrise in the background, highlighting the connection between fitness and nature."
        ]
    },
    {
        "name": "Royal Caribbean",
        "market": "Royal Caribbean is a global cruise vacation company that operates a fleet of modern ships offering a wide variety of activities, dining options, and destinations.",
        "brand_identity": "Royal Caribbean's brand identity is adventurous and luxurious, targeting vacationers seeking unique and memorable travel experiences. Their marketing themes often emphasize adventure, relaxation, and exceptional service.",
        "marketing_examples": [
            "A full-page ad featuring a stunning view of a Royal Caribbean ship sailing through crystal-clear waters with passengers enjoying onboard amenities, highlighting adventure and luxury.",
            "A banner ad showcasing an array of activities available on Royal Caribbean cruises, such as rock climbing, fine dining, and exotic excursions, set against a vibrant backdrop of popular destinations.",
            "A full-page ad with a romantic scene of a couple enjoying a sunset dinner on the deck of a Royal Caribbean ship, with the ocean in the background, emphasizing relaxation and exceptional service."
        ]
    }
]


def default_company2key(company: dict) -> str:
    return f"{company['market']}\n{company['brand_identity']}"


class BrandIndex:
    def __init__(self, embedding_path="BAAI/bge-small-en-v1.5", key_fn=default_company2key):
        # dump the names to help regeneration later
        print("Brands: ", ", ".join(sorted(company["name"] for company in companies)))

        self.embeddings = Embeddings(content=True, path=embedding_path)
        self.embeddings.index([key_fn(company) for company in companies])

    def find_match(self, prompt: str):
        result = self.embeddings.search(prompt, limit=1)[0]
        company_index = int(result["id"])
        company = companies[company_index]
        return company, result["score"]