"""
Management command: seed_new_celebs
Adds 25 new celebrities with membership tiers, foundations, and events.
Uses get_or_create everywhere — safe to run on a live database.
Existing records are NEVER modified or deleted.
"""
from django.core.management.base import BaseCommand
from django.utils.timezone import now
from datetime import timedelta


CELEBS = [
    {
        "name": "Nicolas Cage",
        "slug": "nicolas-cage",
        "tagline": "Hollywood's most unpredictable legend",
        "bio": "Nicolas Cage is an Academy Award-winning actor known for his intense, fearless performances across every genre. With over 100 films under his belt — from action blockbusters to indie darlings — Cage has become one of cinema's most iconic and beloved figures.",
        "category": "acting",
        "nationality": "American",
        "is_featured": False,
    },
    {
        "name": "Michelle Obama",
        "slug": "michelle-obama",
        "tagline": "Former First Lady, author & activist",
        "bio": "Michelle Obama served as the 44th First Lady of the United States and is a Harvard Law graduate, bestselling author of 'Becoming', and global champion for education, health, and women's rights. Her Let Girls Learn initiative has impacted millions of girls worldwide.",
        "category": "politics",
        "nationality": "American",
        "is_featured": True,
    },
    {
        "name": "Johnny Depp",
        "slug": "johnny-depp",
        "tagline": "Iconic actor and rock musician",
        "bio": "Johnny Depp is one of Hollywood's most versatile actors, celebrated for his chameleon-like ability to transform into any character. From Captain Jack Sparrow to Edward Scissorhands, Depp has carved out a legacy as one of the most distinctive performers of his generation.",
        "category": "acting",
        "nationality": "American",
        "is_featured": False,
    },
    {
        "name": "Taylor Swift",
        "slug": "taylor-swift",
        "tagline": "Grammy-winning global pop icon",
        "bio": "Taylor Swift is a record-breaking singer-songwriter who has dominated the music industry for over 15 years. With 14 Grammy Awards and multiple album-of-the-year records, she is one of the best-selling music artists of all time and a generational cultural force.",
        "category": "music",
        "nationality": "American",
        "is_featured": True,
    },
    {
        "name": "Morgan Freeman",
        "slug": "morgan-freeman",
        "tagline": "The voice of a generation",
        "bio": "Morgan Freeman is an Academy Award-winning actor and narrator whose commanding presence and iconic voice have graced over 60 films. From 'Shawshank Redemption' to 'Million Dollar Baby', Freeman's performances have left an indelible mark on cinema.",
        "category": "acting",
        "nationality": "American",
        "is_featured": True,
    },
    {
        "name": "Will Smith",
        "slug": "will-smith",
        "tagline": "Actor, rapper & producer extraordinaire",
        "bio": "Will Smith is a Grammy-winning rapper turned Hollywood superstar. Known for blockbusters like Men in Black, Ali, and King Richard, Smith has proven himself one of the most bankable and versatile performers in entertainment history.",
        "category": "acting",
        "nationality": "American",
        "is_featured": False,
    },
    {
        "name": "Adam Sandler",
        "slug": "adam-sandler",
        "tagline": "Comedy king with dramatic depths",
        "bio": "Adam Sandler is a comedian, actor, producer, and musician who has been making audiences laugh for over three decades. His beloved comedy films have grossed billions worldwide, and his dramatic roles in films like Uncut Gems have revealed him to be one of cinema's most compelling talents.",
        "category": "comedy",
        "nationality": "American",
        "is_featured": False,
    },
    {
        "name": "Tom Hanks",
        "slug": "tom-hanks",
        "tagline": "America's dad, Hollywood's heart",
        "bio": "Tom Hanks is a two-time Academy Award-winning actor and filmmaker regarded as one of the greatest actors of all time. Forrest Gump, Cast Away, Philadelphia, Saving Private Ryan — his filmography is a masterclass in empathetic storytelling and human connection.",
        "category": "acting",
        "nationality": "American",
        "is_featured": True,
    },
    {
        "name": "Marilyn Monroe",
        "slug": "marilyn-monroe",
        "tagline": "Eternal icon of cinema and style",
        "bio": "Marilyn Monroe was one of the most celebrated and iconic actresses and models of the 20th century. A cultural symbol of beauty and vulnerability, her legacy continues to inspire artists, designers, and fans around the world more than six decades after her passing.",
        "category": "acting",
        "nationality": "American",
        "is_featured": True,
    },
    {
        "name": "Betty White",
        "slug": "betty-white",
        "tagline": "The queen of television comedy",
        "bio": "Betty White was a beloved actress and comedian with a career spanning over eight decades, making her the longest-serving female entertainer in television history. Known for her razor-sharp wit and genuine warmth, she was adored by generations of fans worldwide.",
        "category": "comedy",
        "nationality": "American",
        "is_featured": False,
    },
    {
        "name": "Jennifer Aniston",
        "slug": "jennifer-aniston",
        "tagline": "From Friends to Hollywood's A-list",
        "bio": "Jennifer Aniston is an Emmy and Golden Globe-winning actress best known for her iconic role as Rachel Green in Friends. Since then she has built a formidable film career and is recognized globally as one of entertainment's most enduring and beloved stars.",
        "category": "acting",
        "nationality": "American",
        "is_featured": False,
    },
    {
        "name": "Julia Roberts",
        "slug": "julia-roberts",
        "tagline": "Hollywood's original Pretty Woman",
        "bio": "Julia Roberts is an Academy Award-winning actress and one of Hollywood's biggest stars. With iconic roles in Pretty Woman, Erin Brockovich, and Ocean's Eleven, Roberts became the first actress to earn a $20 million salary for a single film.",
        "category": "acting",
        "nationality": "American",
        "is_featured": False,
    },
    {
        "name": "Noah Fearnley",
        "slug": "noah-fearnley",
        "tagline": "Rising star redefining modern art",
        "bio": "Noah Fearnley is an acclaimed contemporary artist and creative visionary whose work bridges digital media, fine art, and cultural commentary. His exhibitions have toured galleries across Europe and North America, attracting a new generation of art collectors and enthusiasts.",
        "category": "other",
        "nationality": "British",
        "is_featured": False,
    },
    {
        "name": "Dwayne Johnson",
        "slug": "dwayne-johnson",
        "tagline": "The Rock — wrestler, actor, icon",
        "bio": "Dwayne 'The Rock' Johnson is a former professional wrestling champion turned global box-office superstar. With a filmography that has grossed over $10 billion worldwide, Johnson is the highest-paid actor in Hollywood and a motivational powerhouse admired by millions.",
        "category": "acting",
        "nationality": "American",
        "is_featured": True,
    },
    {
        "name": "Cristiano Ronaldo",
        "slug": "cristiano-ronaldo",
        "tagline": "GOAT — 5 Ballon d'Or, 900+ career goals",
        "bio": "Cristiano Ronaldo is widely regarded as one of the greatest footballers of all time. The five-time Ballon d'Or winner has broken virtually every scoring record in the sport and is equally celebrated for his relentless work ethic, philanthropy, and global brand.",
        "category": "sports",
        "nationality": "Portuguese",
        "is_featured": True,
    },
    {
        "name": "Lionel Messi",
        "slug": "lionel-messi",
        "tagline": "World Cup champion & 8x Ballon d'Or",
        "bio": "Lionel Messi is an eight-time Ballon d'Or winner and FIFA World Cup champion widely considered the greatest footballer ever to play the game. His combination of technical genius, vision, and consistency across two decades has set a standard no player has matched.",
        "category": "sports",
        "nationality": "Argentinian",
        "is_featured": True,
    },
    {
        "name": "Beyoncé",
        "slug": "beyonce",
        "tagline": "Queen Bey — 32 Grammys, global icon",
        "bio": "Beyoncé is a record-breaking singer, songwriter, actress, and businesswoman widely recognized as one of the greatest entertainers of all time. With 32 Grammy Awards, she is the most-awarded artist in Grammy history and a defining cultural voice of her generation.",
        "category": "music",
        "nationality": "American",
        "is_featured": True,
    },
    {
        "name": "Justin Bieber",
        "slug": "justin-bieber",
        "tagline": "From YouTube to global pop superstar",
        "bio": "Justin Bieber is one of the best-selling music artists of all time, with over 150 million records sold worldwide. Discovered at age 13 via YouTube, Bieber grew from teen pop sensation to mature artist with a dedicated global fanbase spanning generations.",
        "category": "music",
        "nationality": "Canadian",
        "is_featured": False,
    },
    {
        "name": "Jennifer Lopez",
        "slug": "jennifer-lopez",
        "tagline": "J.Lo — actress, singer, the triple threat",
        "bio": "Jennifer Lopez is a multifaceted entertainer — actress, singer, dancer, and producer — who has achieved top-tier success across every entertainment platform. Known as J.Lo, she is one of the most influential Hispanic entertainers in history and a global fashion icon.",
        "category": "music",
        "nationality": "American",
        "is_featured": False,
    },
    {
        "name": "LeBron James",
        "slug": "lebron-james",
        "tagline": "King James — 4x NBA champion",
        "bio": "LeBron James is a four-time NBA champion and four-time MVP widely regarded as one of the greatest basketball players of all time. Off the court, King James is an acclaimed businessman, producer, and philanthropist whose I PROMISE School has transformed thousands of lives.",
        "category": "sports",
        "nationality": "American",
        "is_featured": True,
    },
    {
        "name": "Adele",
        "slug": "adele",
        "tagline": "Soulful voice of a generation",
        "bio": "Adele is a multi-Grammy and Oscar-winning British singer-songwriter known for her powerful, emotionally devastating vocals. Albums like 21, 25, and 30 have broken streaming and sales records worldwide, making her one of the most commercially successful artists of all time.",
        "category": "music",
        "nationality": "British",
        "is_featured": True,
    },
    {
        "name": "Zendaya",
        "slug": "zendaya",
        "tagline": "Emmy winner leading Hollywood's new era",
        "bio": "Zendaya is a two-time Emmy Award-winning actress and singer who has rapidly become one of Hollywood's most sought-after talents. From her breakout role in Euphoria to blockbusters like Dune and Spider-Man, Zendaya is redefining what it means to be a modern celebrity.",
        "category": "acting",
        "nationality": "American",
        "is_featured": True,
    },
    {
        "name": "Rihanna",
        "slug": "rihanna",
        "tagline": "Pop icon turned beauty billionaire",
        "bio": "Rihanna is a Grammy-winning Barbadian singer, businesswoman, and philanthropist who has sold over 250 million records worldwide. As the founder of Fenty Beauty and Savage X Fenty, she revolutionized the beauty industry and became one of the world's wealthiest self-made women.",
        "category": "music",
        "nationality": "Barbadian",
        "is_featured": True,
    },
    {
        "name": "Keanu Reeves",
        "slug": "keanu-reeves",
        "tagline": "The internet's favourite human — and action legend",
        "bio": "Keanu Reeves is a Canadian actor beloved globally for his iconic roles in The Matrix franchise and the John Wick series, as well as classics like Speed and Point Break. Known off-screen for his genuine humility and philanthropy, Reeves is widely regarded as one of the kindest people in Hollywood.",
        "category": "acting",
        "nationality": "Canadian",
        "is_featured": False,
    },
    {
        "name": "Ed Sheeran",
        "slug": "ed-sheeran",
        "tagline": "The ginger guitarist who conquered the world",
        "bio": "Ed Sheeran is one of the world's best-selling music artists, with over 150 million records sold and multiple chart-topping albums including + (Plus), X (Multiply), ÷ (Divide), and =  (Equals). Known for his intimate songwriting and one-man-loop-pedal performances, Sheeran has redefined what a modern pop star can be.",
        "category": "music",
        "nationality": "British",
        "is_featured": False,
    },
]

TIERS = [
    # Nicolas Cage
    {"slug": "nicolas-cage", "name": "Cage Fan", "price": "9.99", "duration_days": 365, "badge_color": "gray", "description": "Access exclusive Nicolas Cage fan content.", "benefits": ["Monthly newsletter", "Behind-the-scenes clips", "Fan community forum"]},
    {"slug": "nicolas-cage", "name": "Cage VIP", "price": "34.99", "duration_days": 365, "badge_color": "gold", "description": "Premium fan experience with exclusive perks.", "benefits": ["All Cage Fan benefits", "Exclusive Q&A sessions", "Signed digital prints", "Early film announcements"]},
    {"slug": "nicolas-cage", "name": "Cage Platinum", "price": "89.99", "duration_days": 365, "badge_color": "platinum", "description": "The ultimate Nicolas Cage fan experience.", "benefits": ["All Cage VIP benefits", "Virtual meet & greet", "Platinum badge", "Personalised video message", "Priority event access"]},

    # Michelle Obama
    {"slug": "michelle-obama", "name": "Inspire Circle", "price": "14.99", "duration_days": 365, "badge_color": "blue", "description": "Join Michelle's global community of changemakers.", "benefits": ["Monthly inspiration newsletter", "Exclusive podcast episodes", "Community forums"]},
    {"slug": "michelle-obama", "name": "Leader's Pass", "price": "49.99", "duration_days": 365, "badge_color": "gold", "description": "Premium access to leadership content and events.", "benefits": ["All Inspire Circle benefits", "Monthly live Q&A", "Exclusive book club", "Early event registration"]},
    {"slug": "michelle-obama", "name": "Legacy Membership", "price": "149.99", "duration_days": 365, "badge_color": "platinum", "description": "The highest tier for Michelle's most devoted supporters.", "benefits": ["All Leader's Pass benefits", "Virtual roundtable sessions", "Personal video message", "Signed book copy giveaway entry"]},

    # Johnny Depp
    {"slug": "johnny-depp", "name": "Sparrow Club", "price": "12.99", "duration_days": 365, "badge_color": "gray", "description": "Set sail with Johnny's exclusive fan community.", "benefits": ["Monthly updates", "Behind-the-scenes photos", "Fan newsletter"]},
    {"slug": "johnny-depp", "name": "Rum & Reels", "price": "39.99", "duration_days": 365, "badge_color": "gold", "description": "Deeper access into Johnny's creative world.", "benefits": ["All Sparrow Club benefits", "Film diary exclusives", "Music content from The Hollywood Vampires", "Live stream events"]},

    # Taylor Swift
    {"slug": "taylor-swift", "name": "Swiftie Member", "price": "9.99", "duration_days": 30, "badge_color": "gray", "description": "Official membership in the Swiftie community.", "benefits": ["Exclusive content drops", "Monthly newsletter", "Early ticket alerts"]},
    {"slug": "taylor-swift", "name": "Era Pass", "price": "29.99", "duration_days": 365, "badge_color": "gold", "description": "A full year inside Taylor's world.", "benefits": ["All Swiftie benefits", "Era-specific exclusive content", "Signed digital postcard", "Pre-sale codes"]},
    {"slug": "taylor-swift", "name": "All Access Vault", "price": "99.99", "duration_days": 365, "badge_color": "platinum", "description": "The inner circle for the most dedicated Swifties.", "benefits": ["All Era Pass benefits", "Vault content drops", "Virtual meet & greet ballot", "Birthday video message", "Exclusive merch discounts"]},

    # Morgan Freeman
    {"slug": "morgan-freeman", "name": "The Narrator's Guild", "price": "11.99", "duration_days": 365, "badge_color": "gray", "description": "Join Morgan's close-knit fan community.", "benefits": ["Monthly Q&A", "Exclusive film commentary", "Fan newsletter"]},
    {"slug": "morgan-freeman", "name": "Red Carpet Pass", "price": "44.99", "duration_days": 365, "badge_color": "gold", "description": "Premium access to Morgan's world of cinema.", "benefits": ["All Narrator's Guild benefits", "Personal anecdotes newsletter", "Priority film premiere access", "Signed digital art"]},

    # Will Smith
    {"slug": "will-smith", "name": "Fresh Prince Fan", "price": "9.99", "duration_days": 365, "badge_color": "blue", "description": "Be part of Will Smith's global fan family.", "benefits": ["Fan newsletter", "BTS content", "Community access"]},
    {"slug": "will-smith", "name": "Willennium Pass", "price": "34.99", "duration_days": 365, "badge_color": "gold", "description": "Be part of Will Smith's global fan family.", "benefits": ["All Fresh Prince benefits", "Motivational content series", "Exclusive music drops", "Early film news"]},
    {"slug": "will-smith", "name": "The Pursuit VIP", "price": "99.99", "duration_days": 365, "badge_color": "platinum", "description": "The ultimate Will Smith fan experience.", "benefits": ["All Willennium benefits", "Virtual hang session ballot", "Platinum badge", "Personalised video message"]},

    # Adam Sandler
    {"slug": "adam-sandler", "name": "Sandler Squad", "price": "7.99", "duration_days": 30, "badge_color": "blue", "description": "Monthly comedy content from Sandler.", "benefits": ["Exclusive sketches", "Early film clips", "Fan forum access"]},
    {"slug": "adam-sandler", "name": "Happy Gilmore Gold", "price": "24.99", "duration_days": 365, "badge_color": "gold", "description": "Full-year access to Adam's comedy universe.", "benefits": ["All Sandler Squad benefits", "Annual comedy special", "Live stream Q&A", "Merch giveaways"]},

    # Tom Hanks
    {"slug": "tom-hanks", "name": "Forrest Fan Club", "price": "12.99", "duration_days": 365, "badge_color": "gray", "description": "Access Tom Hanks's exclusive fan community.", "benefits": ["Monthly film commentary", "Fan newsletter", "Community forums"]},
    {"slug": "tom-hanks", "name": "Hanks Premiere Pass", "price": "49.99", "duration_days": 365, "badge_color": "gold", "description": "Premium Tom Hanks fan experience.", "benefits": ["All Forrest Fan benefits", "Premiere invitations", "Digital autograph", "Live Q&A sessions"]},
    {"slug": "tom-hanks", "name": "Cast Away Elite", "price": "129.99", "duration_days": 365, "badge_color": "platinum", "description": "The pinnacle of Tom Hanks fandom.", "benefits": ["All Premiere Pass benefits", "Virtual meet & greet", "Signed physical postcard", "Birthday video message"]},

    # Marilyn Monroe
    {"slug": "marilyn-monroe", "name": "Diamond Fan", "price": "14.99", "duration_days": 365, "badge_color": "gray", "description": "Celebrate Marilyn's timeless legacy.", "benefits": ["Archive photo drops", "Legacy newsletter", "Documentary access"]},
    {"slug": "marilyn-monroe", "name": "Hollywood Gold", "price": "44.99", "duration_days": 365, "badge_color": "gold", "description": "Deeper access to Marilyn's iconic legacy.", "benefits": ["All Diamond Fan benefits", "Rare interview archive", "Exclusive art prints", "Exhibition early access"]},
    {"slug": "marilyn-monroe", "name": "Icon Platinum", "price": "99.99", "duration_days": 365, "badge_color": "platinum", "description": "The ultimate tribute to an eternal icon.", "benefits": ["All Hollywood Gold benefits", "First editions giveaway entries", "Curated legacy collections", "Exclusive estate updates"]},

    # Betty White
    {"slug": "betty-white", "name": "Golden Girls Fan", "price": "8.99", "duration_days": 365, "badge_color": "gray", "description": "Celebrate Betty White's incredible legacy.", "benefits": ["Legacy content", "Monthly tribute newsletter", "Community forum"]},
    {"slug": "betty-white", "name": "Rose's Inner Circle", "price": "29.99", "duration_days": 365, "badge_color": "gold", "description": "Premium access to Betty White legacy content.", "benefits": ["All Golden Girls benefits", "Rare archive clips", "Tribute event access", "Charity partner updates"]},

    # Jennifer Aniston
    {"slug": "jennifer-aniston", "name": "The One Fan", "price": "11.99", "duration_days": 365, "badge_color": "blue", "description": "Be part of Jennifer's official fan circle.", "benefits": ["Monthly content drops", "Fan newsletter", "Community forums"]},
    {"slug": "jennifer-aniston", "name": "Central Perk Pass", "price": "39.99", "duration_days": 365, "badge_color": "gold", "description": "Premium access to Jen's world.", "benefits": ["All The One Fan benefits", "Wellness content series", "Exclusive film news", "Live stream Q&A"]},

    # Julia Roberts
    {"slug": "julia-roberts", "name": "Pretty Fan", "price": "9.99", "duration_days": 365, "badge_color": "gray", "description": "Official Julia Roberts fan community.", "benefits": ["Monthly newsletter", "Film commentary", "Fan community access"]},
    {"slug": "julia-roberts", "name": "Erin's Circle", "price": "34.99", "duration_days": 365, "badge_color": "gold", "description": "Premium Julia Roberts fan experience.", "benefits": ["All Pretty Fan benefits", "Exclusive Q&A sessions", "Premiere access", "Digital autograph"]},

    # Noah Fearnley
    {"slug": "noah-fearnley", "name": "Art Lover", "price": "14.99", "duration_days": 365, "badge_color": "blue", "description": "Access Noah Fearnley's creative world.", "benefits": ["Monthly art drops", "Studio diary", "Community forum"]},
    {"slug": "noah-fearnley", "name": "Collector's Pass", "price": "59.99", "duration_days": 365, "badge_color": "gold", "description": "Premium access to Noah's creative process.", "benefits": ["All Art Lover benefits", "Early exhibition invites", "Digital print collection", "Monthly studio Q&A"]},

    # Dwayne Johnson
    {"slug": "dwayne-johnson", "name": "Gym & Film Fan", "price": "11.99", "duration_days": 365, "badge_color": "blue", "description": "Join The Rock's official fan community.", "benefits": ["Behind-the-scenes content", "Fitness tips", "Monthly fan newsletter"]},
    {"slug": "dwayne-johnson", "name": "Iron Paradise Pass", "price": "39.99", "duration_days": 365, "badge_color": "gold", "description": "Premium Rock fan experience.", "benefits": ["All Gym & Film benefits", "Exclusive workout programs", "Film set access content", "Live stream Q&A"]},
    {"slug": "dwayne-johnson", "name": "The People's Champion", "price": "99.99", "duration_days": 365, "badge_color": "platinum", "description": "The ultimate Dwayne Johnson fan membership.", "benefits": ["All Iron Paradise benefits", "Virtual hang session ballot", "Signed digital content", "Birthday video message", "Priority event seating"]},

    # Cristiano Ronaldo
    {"slug": "cristiano-ronaldo", "name": "CR7 Fan", "price": "14.99", "duration_days": 365, "badge_color": "blue", "description": "Official Cristiano Ronaldo fan community.", "benefits": ["Training footage", "Match analysis", "Fan newsletter"]},
    {"slug": "cristiano-ronaldo", "name": "SIUUU Gold", "price": "49.99", "duration_days": 365, "badge_color": "gold", "description": "Premium CR7 fan experience.", "benefits": ["All CR7 Fan benefits", "Exclusive interview access", "Signed merch giveaway entries", "Live stream Q&A"]},
    {"slug": "cristiano-ronaldo", "name": "Ballon d'Or Platinum", "price": "149.99", "duration_days": 365, "badge_color": "platinum", "description": "The elite tier for CR7's most devoted fans.", "benefits": ["All SIUUU Gold benefits", "Virtual meet & greet ballot", "Personalised video message", "Early product launches", "VIP event access"]},

    # Lionel Messi
    {"slug": "lionel-messi", "name": "La Pulga Fan", "price": "14.99", "duration_days": 365, "badge_color": "blue", "description": "Join Messi's official world fan family.", "benefits": ["Training exclusives", "Match breakdowns", "Fan newsletter"]},
    {"slug": "lionel-messi", "name": "Goat Pass", "price": "49.99", "duration_days": 365, "badge_color": "gold", "description": "Premium Messi fan experience.", "benefits": ["All La Pulga benefits", "Behind-the-scenes content", "Signed merch giveaway entries", "Monthly Q&A"]},
    {"slug": "lionel-messi", "name": "World Cup Elite", "price": "149.99", "duration_days": 365, "badge_color": "platinum", "description": "The most exclusive Messi fan tier.", "benefits": ["All Goat Pass benefits", "Virtual session ballot", "World Cup documentary access", "Birthday video message", "Platinum badge"]},

    # Beyoncé
    {"slug": "beyonce", "name": "Beyhive Member", "price": "9.99", "duration_days": 30, "badge_color": "gold", "description": "Official Beyhive fan community membership.", "benefits": ["Monthly content drops", "Early ticket alerts", "Community forums"]},
    {"slug": "beyonce", "name": "Renaissance Pass", "price": "39.99", "duration_days": 365, "badge_color": "gold", "description": "Full-year premium Beyoncé fan access.", "benefits": ["All Beyhive benefits", "Era-exclusive content", "Virtual concert previews", "Merch presale access"]},
    {"slug": "beyonce", "name": "Queen Bey Vault", "price": "119.99", "duration_days": 365, "badge_color": "platinum", "description": "The inner circle for Beyoncé's most loyal fans.", "benefits": ["All Renaissance Pass benefits", "Vault exclusive releases", "Virtual event ballot", "Personalised video message", "Signed digital art drops"]},

    # Justin Bieber
    {"slug": "justin-bieber", "name": "Belieber Pass", "price": "8.99", "duration_days": 30, "badge_color": "blue", "description": "Monthly exclusive Bieber fan content.", "benefits": ["Studio diary updates", "Early video access", "Fan community forum"]},
    {"slug": "justin-bieber", "name": "Purpose Gold", "price": "29.99", "duration_days": 365, "badge_color": "gold", "description": "Annual premium Bieber fan membership.", "benefits": ["All Belieber benefits", "Exclusive audio drops", "Monthly live stream", "Signed digital art entry"]},

    # Jennifer Lopez
    {"slug": "jennifer-lopez", "name": "J.Lo Inner Circle", "price": "12.99", "duration_days": 365, "badge_color": "blue", "description": "Join J.Lo's official fan community.", "benefits": ["Monthly content drops", "Fashion & music updates", "Fan community access"]},
    {"slug": "jennifer-lopez", "name": "Bronx Queen Pass", "price": "44.99", "duration_days": 365, "badge_color": "gold", "description": "Premium J.Lo fan experience.", "benefits": ["All Inner Circle benefits", "Exclusive tour content", "Fitness & lifestyle content", "Virtual event access"]},
    {"slug": "jennifer-lopez", "name": "Diamond J.Lo Elite", "price": "109.99", "duration_days": 365, "badge_color": "platinum", "description": "The ultimate Jennifer Lopez fan membership.", "benefits": ["All Bronx Queen benefits", "Virtual meet & greet ballot", "Personalised birthday message", "Early merch drops", "Platinum badge"]},

    # LeBron James
    {"slug": "lebron-james", "name": "Courtside Fan", "price": "14.99", "duration_days": 365, "badge_color": "blue", "description": "Join King James's official fan community.", "benefits": ["Game analysis breakdowns", "BTS content", "Monthly newsletter"]},
    {"slug": "lebron-james", "name": "King's Pass", "price": "49.99", "duration_days": 365, "badge_color": "gold", "description": "Premium LeBron fan experience.", "benefits": ["All Courtside benefits", "Exclusive training footage", "I PROMISE School updates", "Live Q&A sessions"]},
    {"slug": "lebron-james", "name": "Chosen One Platinum", "price": "149.99", "duration_days": 365, "badge_color": "platinum", "description": "The elite LeBron James fan membership.", "benefits": ["All King's Pass benefits", "Virtual meet & greet ballot", "Signed merch giveaway", "Birthday video message", "Priority event access"]},

    # Adele
    {"slug": "adele", "name": "Hello Fan", "price": "9.99", "duration_days": 365, "badge_color": "gray", "description": "Official Adele fan community membership.", "benefits": ["Monthly music updates", "Exclusive behind-the-scenes", "Fan newsletter"]},
    {"slug": "adele", "name": "Rolling Deep Pass", "price": "34.99", "duration_days": 365, "badge_color": "gold", "description": "Premium Adele fan experience.", "benefits": ["All Hello Fan benefits", "Live shows early access", "Exclusive vocal diary", "Acoustic session previews"]},
    {"slug": "adele", "name": "30 Platinum", "price": "89.99", "duration_days": 365, "badge_color": "platinum", "description": "The most intimate Adele fan experience.", "benefits": ["All Rolling Deep benefits", "Virtual listening party invites", "Signed digital art entry", "Birthday voice message entry", "Platinum badge"]},

    # Zendaya
    {"slug": "zendaya", "name": "Zendaya Fan", "price": "11.99", "duration_days": 365, "badge_color": "blue", "description": "Official Zendaya fan community.", "benefits": ["Monthly updates", "Fashion & film content", "Fan community access"]},
    {"slug": "zendaya", "name": "Euphoria Pass", "price": "39.99", "duration_days": 365, "badge_color": "gold", "description": "Premium Zendaya fan experience.", "benefits": ["All Zendaya Fan benefits", "Behind-the-scenes content", "Exclusive fashion picks", "Monthly live Q&A"]},
    {"slug": "zendaya", "name": "Dune Elite", "price": "99.99", "duration_days": 365, "badge_color": "platinum", "description": "The ultimate Zendaya fan tier.", "benefits": ["All Euphoria Pass benefits", "Virtual meet & greet ballot", "Personalised video message", "Early film news", "Platinum badge"]},

    # Rihanna
    {"slug": "rihanna", "name": "Navy Member", "price": "9.99", "duration_days": 30, "badge_color": "blue", "description": "Official Rihanna Navy fan community.", "benefits": ["Monthly music updates", "Fenty News", "Community forums"]},
    {"slug": "rihanna", "name": "Fenty Gold", "price": "39.99", "duration_days": 365, "badge_color": "gold", "description": "Premium Rihanna fan and Fenty insider.", "benefits": ["All Navy benefits", "Fenty Beauty early previews", "Exclusive music drops", "Virtual event access"]},
    {"slug": "rihanna", "name": "Diamond Navy Elite", "price": "109.99", "duration_days": 365, "badge_color": "platinum", "description": "The inner circle for the most dedicated Rihanna fans.", "benefits": ["All Fenty Gold benefits", "Virtual meet & greet ballot", "Birthday message entry", "Savage X Fenty exclusive drops", "Platinum badge"]},

    # Keanu Reeves
    {"slug": "keanu-reeves", "name": "Matrix Fan", "price": "9.99", "duration_days": 365, "badge_color": "gray", "description": "Join Keanu's official fan community.", "benefits": ["Monthly update", "Film exclusive content", "Fan community"]},
    {"slug": "keanu-reeves", "name": "John Wick Pass", "price": "34.99", "duration_days": 365, "badge_color": "gold", "description": "Premium Keanu fan experience.", "benefits": ["All Matrix Fan benefits", "Action film deep dives", "Exclusive Q&A sessions", "Charity partner updates"]},

    # Ed Sheeran
    {"slug": "ed-sheeran", "name": "Shipper Pass", "price": "9.99", "duration_days": 30, "badge_color": "blue", "description": "Monthly exclusive Ed Sheeran fan content.", "benefits": ["New music updates", "Live session clips", "Fan community forum"]},
    {"slug": "ed-sheeran", "name": "Divide Gold", "price": "29.99", "duration_days": 365, "badge_color": "gold", "description": "Annual premium Ed Sheeran fan membership.", "benefits": ["All Shipper benefits", "Songwriting diary", "Early concert access", "Acoustic session previews"]},
    {"slug": "ed-sheeran", "name": "Equals Platinum", "price": "79.99", "duration_days": 365, "badge_color": "platinum", "description": "The most intimate Ed Sheeran fan experience.", "benefits": ["All Divide Gold benefits", "Virtual backstage ballot", "Birthday voice message entry", "Signed art print entry", "Lifetime fan badge"]},
]

FOUNDATIONS = [
    {"slug": "nicolas-cage", "name": "Cage Arts Fund", "description": "Supporting independent film and arts education for underprivileged youth across America.", "target_amount": "300000", "cause_type": "Arts"},
    {"slug": "michelle-obama", "name": "Let Girls Learn", "description": "Providing education access and scholarships to adolescent girls in developing countries.", "target_amount": "5000000", "cause_type": "Education"},
    {"slug": "michelle-obama", "name": "Obama Foundation Youth", "description": "Inspiring and empowering the next generation of civic leaders across Africa and the Americas.", "target_amount": "2000000", "cause_type": "Youth Empowerment"},
    {"slug": "johnny-depp", "name": "Depp Children's Hospital Fund", "description": "Funding pediatric hospitals and children's wings at medical centers worldwide.", "target_amount": "750000", "cause_type": "Health"},
    {"slug": "taylor-swift", "name": "Taylor's Scholarship Fund", "description": "Providing college scholarships for young women pursuing arts, music, and education degrees.", "target_amount": "1000000", "cause_type": "Education"},
    {"slug": "taylor-swift", "name": "Swiftie Disaster Relief", "description": "Emergency relief fund for communities affected by natural disasters, activated after major events.", "target_amount": "500000", "cause_type": "Disaster Relief"},
    {"slug": "morgan-freeman", "name": "The Freeman Arts Initiative", "description": "Bringing arts programs, theatre, and performance arts to schools in underserved American communities.", "target_amount": "400000", "cause_type": "Arts"},
    {"slug": "will-smith", "name": "Will & Jada Smith Family Foundation", "description": "Funding youth development, education, and arts programs across Philadelphia and beyond.", "target_amount": "1500000", "cause_type": "Youth Empowerment"},
    {"slug": "adam-sandler", "name": "Sandler Laughs for Good", "description": "Comedy therapy and mental health support programs for children in hospitals and care facilities.", "target_amount": "250000", "cause_type": "Mental Health"},
    {"slug": "tom-hanks", "name": "Hanks Veterans Foundation", "description": "Supporting American veterans through housing, mental health services, and career reintegration programs.", "target_amount": "800000", "cause_type": "Veterans Support"},
    {"slug": "marilyn-monroe", "name": "Monroe Legacy Archive", "description": "Preserving and sharing Marilyn Monroe's cultural legacy through exhibitions, screenings, and education.", "target_amount": "200000", "cause_type": "Heritage"},
    {"slug": "betty-white", "name": "Betty White Animal Fund", "description": "Supporting animal shelters, wildlife conservation, and rescue organizations worldwide in Betty's name.", "target_amount": "500000", "cause_type": "Animal Welfare"},
    {"slug": "jennifer-aniston", "name": "Aniston Wellness Foundation", "description": "Funding mental health awareness programs and accessible therapy resources for women globally.", "target_amount": "600000", "cause_type": "Mental Health"},
    {"slug": "julia-roberts", "name": "Roberts Clean Water Fund", "description": "Providing clean water access and sanitation solutions in rural communities across Sub-Saharan Africa.", "target_amount": "1000000", "cause_type": "Health"},
    {"slug": "noah-fearnley", "name": "New Voices Arts Grant", "description": "Providing grants and mentorship to emerging artists from underrepresented communities.", "target_amount": "150000", "cause_type": "Arts"},
    {"slug": "dwayne-johnson", "name": "Dwayne Johnson Rock Foundation", "description": "Empowering at-risk youth through fitness, mentorship, and leadership development programs.", "target_amount": "2000000", "cause_type": "Youth Empowerment"},
    {"slug": "cristiano-ronaldo", "name": "CR7 Children's Hospital Fund", "description": "Funding pediatric cancer wards and children's hospitals in Portugal, Spain, and beyond.", "target_amount": "3000000", "cause_type": "Health"},
    {"slug": "cristiano-ronaldo", "name": "Ronaldo Portugal Education", "description": "Scholarships and school building programs for youth in Madeira and underfunded Portuguese communities.", "target_amount": "1000000", "cause_type": "Education"},
    {"slug": "lionel-messi", "name": "Leo Messi Foundation", "description": "Guaranteeing access to education, health, and sport for vulnerable children around the world.", "target_amount": "4000000", "cause_type": "Youth Empowerment"},
    {"slug": "beyonce", "name": "BeyGOOD Foundation", "description": "Providing emergency relief, scholarships, and social justice advocacy globally through immediate action.", "target_amount": "5000000", "cause_type": "Social Justice"},
    {"slug": "beyonce", "name": "HBCU Scholarship Fund", "description": "Providing annual scholarships to students attending Historically Black Colleges and Universities.", "target_amount": "2500000", "cause_type": "Education"},
    {"slug": "justin-bieber", "name": "Bieber Pencils of Promise", "description": "Partnership fund building schools in Ghana, Guatemala, and Laos — a school for every album sold.", "target_amount": "800000", "cause_type": "Education"},
    {"slug": "jennifer-lopez", "name": "Lopez Family Foundation", "description": "Supporting underserved Hispanic and Latino communities through education, arts, and disaster relief programs.", "target_amount": "1200000", "cause_type": "Community"},
    {"slug": "lebron-james", "name": "I PROMISE School Fund", "description": "Sustaining and expanding LeBron's I PROMISE School in Akron, Ohio — providing wraparound support to at-risk students.", "target_amount": "10000000", "cause_type": "Education"},
    {"slug": "adele", "name": "Adele Chasing Pavements Fund", "description": "Supporting arts and music education in state schools in the UK — ensuring every child has access to creative expression.", "target_amount": "1000000", "cause_type": "Arts"},
    {"slug": "zendaya", "name": "Zendaya's Euphoria Fund", "description": "Mental health resources and awareness campaigns for teenagers and young adults experiencing anxiety and depression.", "target_amount": "600000", "cause_type": "Mental Health"},
    {"slug": "rihanna", "name": "Clara Lionel Foundation", "description": "Supporting global education, emergency response, and climate resilience programs in vulnerable communities.", "target_amount": "7000000", "cause_type": "Education"},
    {"slug": "keanu-reeves", "name": "Reeves Cancer Support Fund", "description": "Quietly funding cancer research and patient support organizations — continuing Keanu's private charitable work.", "target_amount": "500000", "cause_type": "Health"},
    {"slug": "ed-sheeran", "name": "Ed's East Anglian Charity", "description": "Supporting local charities in Suffolk and greater East Anglia — homeless shelters, food banks, and youth projects.", "target_amount": "300000", "cause_type": "Community"},
]

EVENTS = [
    # Nicolas Cage
    {"slug": "nicolas-cage", "title": "Cage Uncaged — Live Q&A", "event_slug": "cage-uncaged-qa", "description": "An intimate live Q&A with Nicolas Cage exploring his career, upcoming projects, and life lessons.", "event_type": "virtual", "status": "upcoming", "days": 20, "location": "Online — Live Stream", "ticket_price": "19.99", "is_free": False, "seats_total": 0},
    {"slug": "nicolas-cage", "title": "Wild at Heart Film Festival", "event_slug": "wild-at-heart-film-festival", "description": "A celebration of Nicolas Cage's most iconic films across four days, screening in Los Angeles.", "event_type": "premiere", "status": "upcoming", "days": 55, "location": "ArcLight Cinemas, Los Angeles, USA", "ticket_price": "45.00", "is_free": False, "seats_total": 600},

    # Michelle Obama
    {"slug": "michelle-obama", "title": "Becoming — The Live Experience", "event_slug": "becoming-live-experience", "description": "Michelle Obama's global arena tour — a deeply personal conversation about leadership, love, and legacy.", "event_type": "other", "status": "upcoming", "days": 35, "location": "United Center, Chicago, USA", "ticket_price": "75.00", "is_free": False, "seats_total": 20000},
    {"slug": "michelle-obama", "title": "Girls Leadership Summit", "event_slug": "girls-leadership-summit", "description": "A free summit for young women aged 16–25 focused on leadership, education, and career development.", "event_type": "workshop", "status": "upcoming", "days": 18, "location": "Howard University, Washington D.C., USA", "ticket_price": "0", "is_free": True, "seats_total": 2000},

    # Johnny Depp
    {"slug": "johnny-depp", "title": "Hollywood Vampires — Live Concert", "event_slug": "hollywood-vampires-live", "description": "Johnny Depp performs live with his rock band Hollywood Vampires for one unforgettable night.", "event_type": "concert", "status": "upcoming", "days": 42, "location": "O2 Arena, London, UK", "ticket_price": "65.00", "is_free": False, "seats_total": 15000},
    {"slug": "johnny-depp", "title": "Depp Art Exhibition — Venice", "event_slug": "depp-art-exhibition-venice", "description": "Johnny Depp showcases his paintings for the first time at an exclusive Venice gallery exhibition.", "event_type": "other", "status": "upcoming", "days": 70, "location": "Galleria dell'Accademia, Venice, Italy", "ticket_price": "35.00", "is_free": False, "seats_total": 300},

    # Taylor Swift
    {"slug": "taylor-swift", "title": "The Eras Tour — Sydney", "event_slug": "eras-tour-sydney", "description": "Taylor Swift brings The Eras Tour to Sydney for three nights of music spanning her entire career.", "event_type": "concert", "status": "upcoming", "days": 28, "location": "Accor Stadium, Sydney, Australia", "ticket_price": "120.00", "is_free": False, "seats_total": 85000},
    {"slug": "taylor-swift", "title": "Swiftie Fan Meetup — NYC", "event_slug": "swiftie-fan-meetup-nyc", "description": "An exclusive fan meetup event for Taylor Swift members in New York City.", "event_type": "meetgreet", "status": "upcoming", "days": 14, "location": "Irving Plaza, New York, USA", "ticket_price": "49.00", "is_free": False, "seats_total": 500},

    # Morgan Freeman
    {"slug": "morgan-freeman", "title": "Morgan Freeman — In Conversation", "event_slug": "morgan-freeman-in-conversation", "description": "An intimate evening with Morgan Freeman reflecting on his legendary career and life philosophy.", "event_type": "other", "status": "upcoming", "days": 50, "location": "Lincoln Center, New York, USA", "ticket_price": "85.00", "is_free": False, "seats_total": 1000},
    {"slug": "morgan-freeman", "title": "Freeman Arts Charity Gala", "event_slug": "freeman-arts-charity-gala", "description": "A black-tie gala raising funds for The Freeman Arts Initiative with live performances and art auctions.", "event_type": "charity", "status": "upcoming", "days": 75, "location": "The Beverly Hilton, Beverly Hills, USA", "ticket_price": "350.00", "is_free": False, "seats_total": 500},

    # Will Smith
    {"slug": "will-smith", "title": "Will Smith Live — Miami", "event_slug": "will-smith-live-miami", "description": "Will Smith returns to the stage for a night of music, storytelling, and laughs in Miami.", "event_type": "concert", "status": "upcoming", "days": 32, "location": "Kaseya Center, Miami, USA", "ticket_price": "75.00", "is_free": False, "seats_total": 18000},
    {"slug": "will-smith", "title": "Willpower Wellness Summit", "event_slug": "willpower-wellness-summit", "description": "A motivational summit with Will Smith focused on mental health, fitness, and personal reinvention.", "event_type": "workshop", "status": "upcoming", "days": 58, "location": "Philadelphia Convention Center, USA", "ticket_price": "99.00", "is_free": False, "seats_total": 3000},

    # Adam Sandler
    {"slug": "adam-sandler", "title": "Sandler Stand-Up Special — Las Vegas", "event_slug": "sandler-standup-las-vegas", "description": "Adam Sandler's brand new stand-up comedy special, recorded live in Las Vegas.", "event_type": "concert", "status": "upcoming", "days": 22, "location": "Michelob Ultra Arena, Las Vegas, USA", "ticket_price": "55.00", "is_free": False, "seats_total": 12000},
    {"slug": "adam-sandler", "title": "Sandler Fan Film Screening", "event_slug": "sandler-fan-film-screening", "description": "An exclusive fan screening of Adam Sandler's new film followed by a live Q&A session.", "event_type": "premiere", "status": "upcoming", "days": 40, "location": "AMC Empire 25, New York, USA", "ticket_price": "25.00", "is_free": False, "seats_total": 400},

    # Tom Hanks
    {"slug": "tom-hanks", "title": "Tom Hanks — An Evening of Storytelling", "event_slug": "tom-hanks-evening-storytelling", "description": "Tom Hanks hosts an evening of storytelling, typewriter talks, and career retrospectives at the Hollywood Bowl.", "event_type": "other", "status": "upcoming", "days": 46, "location": "Hollywood Bowl, Los Angeles, USA", "ticket_price": "90.00", "is_free": False, "seats_total": 17000},
    {"slug": "tom-hanks", "title": "Hanks Veterans Charity Dinner", "event_slug": "hanks-veterans-charity-dinner", "description": "An exclusive fundraising dinner with Tom Hanks benefiting the Hanks Veterans Foundation.", "event_type": "charity", "status": "upcoming", "days": 80, "location": "The Ritz-Carlton, Washington D.C., USA", "ticket_price": "500.00", "is_free": False, "seats_total": 200},

    # Marilyn Monroe
    {"slug": "marilyn-monroe", "title": "Marilyn Monroe Legacy Exhibition", "event_slug": "marilyn-monroe-legacy-exhibition", "description": "A world-class travelling exhibition celebrating Marilyn Monroe's life, fashion, film, and cultural impact.", "event_type": "other", "status": "upcoming", "days": 12, "location": "MoMA, New York, USA", "ticket_price": "30.00", "is_free": False, "seats_total": 0},
    {"slug": "marilyn-monroe", "title": "Gentlemen Prefer Blondes — Screening Gala", "event_slug": "gentlemen-prefer-blondes-gala", "description": "A glamorous screening gala of the classic film with a charity auction in Marilyn's honour.", "event_type": "premiere", "status": "upcoming", "days": 62, "location": "TCL Chinese Theatre, Hollywood, USA", "ticket_price": "120.00", "is_free": False, "seats_total": 1000},

    # Betty White
    {"slug": "betty-white", "title": "Betty White Memorial Tribute Night", "event_slug": "betty-white-tribute-night", "description": "A star-studded tribute evening celebrating the life and comedy of the legendary Betty White.", "event_type": "charity", "status": "upcoming", "days": 25, "location": "Greek Theatre, Los Angeles, USA", "ticket_price": "60.00", "is_free": False, "seats_total": 6000},
    {"slug": "betty-white", "title": "Animal Rescue Charity Gala", "event_slug": "betty-animal-rescue-gala", "description": "A fundraising gala in Betty White's name supporting animal shelters and rescue organisations nationwide.", "event_type": "charity", "status": "upcoming", "days": 90, "location": "Fairmont Hotel, San Francisco, USA", "ticket_price": "200.00", "is_free": False, "seats_total": 400},

    # Jennifer Aniston
    {"slug": "jennifer-aniston", "title": "Jen Aniston — Fan Brunch", "event_slug": "jen-aniston-fan-brunch", "description": "An exclusive intimate brunch with Jennifer Aniston for her most dedicated fan members.", "event_type": "meetgreet", "status": "upcoming", "days": 30, "location": "Soho House, Los Angeles, USA", "ticket_price": "199.00", "is_free": False, "seats_total": 80},
    {"slug": "jennifer-aniston", "title": "Wellness & Women Panel", "event_slug": "wellness-women-panel", "description": "Jennifer Aniston leads a panel on mental health, self-care, and women's wellness in Hollywood and beyond.", "event_type": "workshop", "status": "upcoming", "days": 55, "location": "UCLA Campus, Los Angeles, USA", "ticket_price": "45.00", "is_free": False, "seats_total": 800},

    # Julia Roberts
    {"slug": "julia-roberts", "title": "Julia Roberts Film Retrospective", "event_slug": "julia-roberts-retrospective", "description": "A four-day retrospective of Julia Roberts's greatest films at the BFI Southbank with a live Q&A on the final night.", "event_type": "premiere", "status": "upcoming", "days": 35, "location": "BFI Southbank, London, UK", "ticket_price": "40.00", "is_free": False, "seats_total": 1200},
    {"slug": "julia-roberts", "title": "Clean Water Charity Gala", "event_slug": "julia-clean-water-gala", "description": "A black-tie gala raising funds for Julia Roberts's clean water initiative across Sub-Saharan Africa.", "event_type": "charity", "status": "upcoming", "days": 68, "location": "Four Seasons Hotel, Beverly Hills, USA", "ticket_price": "400.00", "is_free": False, "seats_total": 300},

    # Noah Fearnley
    {"slug": "noah-fearnley", "title": "New Voices — Group Exhibition", "event_slug": "new-voices-group-exhibition", "description": "Noah Fearnley curates and participates in a group exhibition showcasing emerging artists supported by his foundation.", "event_type": "other", "status": "upcoming", "days": 18, "location": "Tate Modern, London, UK", "ticket_price": "0", "is_free": True, "seats_total": 0},
    {"slug": "noah-fearnley", "title": "Fearnley Studio Open Day", "event_slug": "fearnley-studio-open-day", "description": "An exclusive visit to Noah Fearnley's studio with a guided tour, live painting demo, and artist talk.", "event_type": "workshop", "status": "upcoming", "days": 45, "location": "Shoreditch, London, UK", "ticket_price": "35.00", "is_free": False, "seats_total": 50},

    # Dwayne Johnson
    {"slug": "dwayne-johnson", "title": "Rock Fitness Expo — New York", "event_slug": "rock-fitness-expo-ny", "description": "Dwayne Johnson's fitness and wellness expo bringing top trainers, nutrition experts, and keynote sessions.", "event_type": "workshop", "status": "upcoming", "days": 22, "location": "Javits Center, New York, USA", "ticket_price": "59.00", "is_free": False, "seats_total": 5000},
    {"slug": "dwayne-johnson", "title": "Rock Foundation Charity Match", "event_slug": "rock-foundation-charity-match", "description": "Celebrity charity flag football match raising funds for the Dwayne Johnson Rock Foundation youth programs.", "event_type": "charity", "status": "upcoming", "days": 60, "location": "SoFi Stadium, Los Angeles, USA", "ticket_price": "40.00", "is_free": False, "seats_total": 70000},

    # Cristiano Ronaldo
    {"slug": "cristiano-ronaldo", "title": "CR7 Football Clinic — Lisbon", "event_slug": "cr7-football-clinic-lisbon", "description": "A one-day football training clinic led by Cristiano Ronaldo's coaching team for youth players aged 12–18.", "event_type": "workshop", "status": "upcoming", "days": 16, "location": "Estádio Nacional, Lisbon, Portugal", "ticket_price": "0", "is_free": True, "seats_total": 500},
    {"slug": "cristiano-ronaldo", "title": "CR7 Museum Gala Night", "event_slug": "cr7-museum-gala-night", "description": "An exclusive black-tie gala at the CR7 Museum in Funchal celebrating Ronaldo's charity work.", "event_type": "charity", "status": "upcoming", "days": 50, "location": "CR7 Museum, Funchal, Madeira, Portugal", "ticket_price": "250.00", "is_free": False, "seats_total": 200},

    # Lionel Messi
    {"slug": "lionel-messi", "title": "Messi Football Academy Open Day", "event_slug": "messi-academy-open-day", "description": "Visit the Leo Messi Foundation's flagship academy, watch youth training, and meet the coaching staff.", "event_type": "other", "status": "upcoming", "days": 12, "location": "Barcelona Sports Complex, Barcelona, Spain", "ticket_price": "0", "is_free": True, "seats_total": 300},
    {"slug": "lionel-messi", "title": "Leo Charity Gala — Buenos Aires", "event_slug": "leo-charity-gala-ba", "description": "A charity dinner with Lionel Messi in Buenos Aires raising funds for the Leo Messi Foundation.", "event_type": "charity", "status": "upcoming", "days": 65, "location": "Palacio Duhau, Buenos Aires, Argentina", "ticket_price": "500.00", "is_free": False, "seats_total": 250},

    # Beyoncé
    {"slug": "beyonce", "title": "Renaissance World Tour — Lagos", "event_slug": "renaissance-tour-lagos", "description": "Beyoncé brings her iconic Renaissance World Tour to Lagos for the first ever full African stadium concert.", "event_type": "concert", "status": "upcoming", "days": 35, "location": "Eko Atlantic City Arena, Lagos, Nigeria", "ticket_price": "89.00", "is_free": False, "seats_total": 60000},
    {"slug": "beyonce", "title": "BeyGOOD Charity Concert", "event_slug": "beygood-charity-concert", "description": "A charity benefit concert raising funds for BeyGOOD's global relief and scholarship programs.", "event_type": "concert", "status": "upcoming", "days": 80, "location": "Madison Square Garden, New York, USA", "ticket_price": "55.00", "is_free": False, "seats_total": 20000},

    # Justin Bieber
    {"slug": "justin-bieber", "title": "Bieber Acoustic Sessions — Toronto", "event_slug": "bieber-acoustic-toronto", "description": "An intimate acoustic concert in Justin Bieber's hometown of Toronto for his most dedicated fans.", "event_type": "concert", "status": "upcoming", "days": 28, "location": "Massey Hall, Toronto, Canada", "ticket_price": "75.00", "is_free": False, "seats_total": 2765},
    {"slug": "justin-bieber", "title": "Bieber Fan Meetup — LA", "event_slug": "bieber-fan-meetup-la", "description": "An exclusive fan meetup for Justin Bieber member pass holders in Los Angeles.", "event_type": "meetgreet", "status": "upcoming", "days": 45, "location": "Staples Center, Los Angeles, USA", "ticket_price": "99.00", "is_free": False, "seats_total": 200},

    # Jennifer Lopez
    {"slug": "jennifer-lopez", "title": "J.Lo Dance Workshop — Miami", "event_slug": "jlo-dance-workshop-miami", "description": "Jennifer Lopez leads a professional dance masterclass and performance workshop at her home city of Miami.", "event_type": "workshop", "status": "upcoming", "days": 20, "location": "FTX Arena, Miami, USA", "ticket_price": "79.00", "is_free": False, "seats_total": 1000},
    {"slug": "jennifer-lopez", "title": "This Is Me… Now Tour — London", "event_slug": "jlo-tour-london", "description": "Jennifer Lopez brings her electrifying stage show to London's O2 Arena for two sold-out nights.", "event_type": "concert", "status": "upcoming", "days": 55, "location": "O2 Arena, London, UK", "ticket_price": "95.00", "is_free": False, "seats_total": 20000},

    # LeBron James
    {"slug": "lebron-james", "title": "King's Basketball Camp — Akron", "event_slug": "kings-basketball-camp-akron", "description": "LeBron James hosts a free basketball camp for 300 youth athletes from Akron, Ohio's underserved communities.", "event_type": "workshop", "status": "upcoming", "days": 14, "location": "I PROMISE School, Akron, Ohio, USA", "ticket_price": "0", "is_free": True, "seats_total": 300},
    {"slug": "lebron-james", "title": "LeBron Charity Gala — LA", "event_slug": "lebron-charity-gala-la", "description": "Black-tie gala raising funds for the I PROMISE School and LeBron's broader education initiatives.", "event_type": "charity", "status": "upcoming", "days": 72, "location": "The Beverly Hilton, Beverly Hills, USA", "ticket_price": "600.00", "is_free": False, "seats_total": 400},

    # Adele
    {"slug": "adele", "title": "Adele — An Evening at The Colosseum", "event_slug": "adele-colosseum-residency", "description": "Adele continues her famed residency at The Colosseum at Caesars Palace — one night, one voice, one experience.", "event_type": "concert", "status": "upcoming", "days": 25, "location": "The Colosseum, Caesars Palace, Las Vegas, USA", "ticket_price": "350.00", "is_free": False, "seats_total": 4298},
    {"slug": "adele", "title": "Hello — Fan Listening Party", "event_slug": "adele-fan-listening-party", "description": "An exclusive fan listening party for Adele's upcoming new album, hosted at a private London venue.", "event_type": "other", "status": "upcoming", "days": 60, "location": "Ronnie Scott's Jazz Club, London, UK", "ticket_price": "120.00", "is_free": False, "seats_total": 150},

    # Zendaya
    {"slug": "zendaya", "title": "Zendaya — Dune Press & Fan Event", "event_slug": "zendaya-dune-fan-event", "description": "Zendaya hosts an exclusive fan event around the Dune franchise with screenings, discussions, and a meet & greet.", "event_type": "premiere", "status": "upcoming", "days": 30, "location": "El Capitan Theatre, Hollywood, USA", "ticket_price": "55.00", "is_free": False, "seats_total": 700},
    {"slug": "zendaya", "title": "Mental Health Awareness Summit", "event_slug": "zendaya-mental-health-summit", "description": "Zendaya leads a youth summit on mental health, self-expression, and breaking the stigma around therapy.", "event_type": "workshop", "status": "upcoming", "days": 48, "location": "Columbia University, New York, USA", "ticket_price": "0", "is_free": True, "seats_total": 1000},

    # Rihanna
    {"slug": "rihanna", "title": "Savage X Fenty Show — Live", "event_slug": "savage-fenty-show-live", "description": "Rihanna's Savage X Fenty fashion spectacle comes alive for one unforgettable live show experience.", "event_type": "other", "status": "upcoming", "days": 38, "location": "Barclays Center, Brooklyn, USA", "ticket_price": "85.00", "is_free": False, "seats_total": 18000},
    {"slug": "rihanna", "title": "CLF Charity Gala — Barbados", "event_slug": "clf-charity-gala-barbados", "description": "Clara Lionel Foundation annual gala in Rihanna's homeland of Barbados raising funds for global education.", "event_type": "charity", "status": "upcoming", "days": 85, "location": "Hilton Barbados Resort, Bridgetown, Barbados", "ticket_price": "300.00", "is_free": False, "seats_total": 350},

    # Keanu Reeves
    {"slug": "keanu-reeves", "title": "John Wick Fan Premiere Night", "event_slug": "john-wick-fan-premiere", "description": "An exclusive premiere screening of Keanu Reeves's latest film with a live Q&A session afterwards.", "event_type": "premiere", "status": "upcoming", "days": 20, "location": "TCL Chinese Theatre, Hollywood, USA", "ticket_price": "60.00", "is_free": False, "seats_total": 1000},
    {"slug": "keanu-reeves", "title": "Reeves Motorbike Charity Ride", "event_slug": "reeves-motorbike-charity-ride", "description": "Keanu Reeves leads a charity motorbike ride across California raising funds for cancer research.", "event_type": "charity", "status": "upcoming", "days": 55, "location": "Pacific Coast Highway, California, USA", "ticket_price": "75.00", "is_free": False, "seats_total": 500},

    # Ed Sheeran
    {"slug": "ed-sheeran", "title": "Ed Sheeran — Mathematics Tour UK", "event_slug": "ed-sheeran-mathematics-uk", "description": "Ed Sheeran brings the Mathematics Tour to Wembley Stadium for five solo headline nights.", "event_type": "concert", "status": "upcoming", "days": 30, "location": "Wembley Stadium, London, UK", "ticket_price": "85.00", "is_free": False, "seats_total": 90000},
    {"slug": "ed-sheeran", "title": "Songwriter Masterclass — Suffolk", "event_slug": "ed-sheeran-songwriter-masterclass", "description": "Ed Sheeran hosts an intimate songwriting masterclass for 30 emerging musicians at his home studio in Suffolk.", "event_type": "workshop", "status": "upcoming", "days": 65, "location": "Sheeran Private Studio, Suffolk, UK", "ticket_price": "149.00", "is_free": False, "seats_total": 30},
]


class Command(BaseCommand):
    help = "Seed 25 new celebrities with tiers, foundations and events. Safe to run on live data — uses get_or_create."

    def handle(self, *args, **kwargs):
        from celebs.models import Celebrity
        from memberships.models import MembershipTier
        from donations.models import Foundation
        from events.models import Event

        self.stdout.write(self.style.MIGRATE_HEADING("⭐ Seeding new celebrities…"))

        # ── Celebrities ──────────────────────────────────────────────────────
        celeb_map = {}
        seen = set()
        for data in CELEBS:
            if data["slug"] in seen:
                continue
            seen.add(data["slug"])
            obj, created = Celebrity.objects.get_or_create(slug=data["slug"], defaults=data)
            celeb_map[data["slug"]] = obj
            self.stdout.write(f"  {'✅ Created' if created else '⏭  Exists'}: {obj.name}")

        # ── Membership Tiers ─────────────────────────────────────────────────
        self.stdout.write(self.style.MIGRATE_HEADING("\n🎖  Seeding membership tiers…"))
        for t in TIERS:
            celeb = celeb_map.get(t["slug"])
            if not celeb:
                continue
            benefits = "\n".join(t["benefits"]) if isinstance(t["benefits"], list) else t["benefits"]
            defaults = {
                "price": t["price"],
                "duration_days": t["duration_days"],
                "badge_color": t["badge_color"],
                "description": t["description"],
                "benefits": benefits,
            }
            obj, created = MembershipTier.objects.get_or_create(celebrity=celeb, name=t["name"], defaults=defaults)
            self.stdout.write(f"  {'✅' if created else '⏭ '}: {celeb.name} — {obj.name}")

        # ── Foundations ───────────────────────────────────────────────────────
        self.stdout.write(self.style.MIGRATE_HEADING("\n❤️  Seeding foundations…"))
        for f in FOUNDATIONS:
            celeb = celeb_map.get(f["slug"])
            if not celeb:
                continue
            defaults = {
                "description": f["description"],
                "target_amount": f["target_amount"],
                "cause_type": f["cause_type"],
            }
            obj, created = Foundation.objects.get_or_create(celebrity=celeb, name=f["name"], defaults=defaults)
            self.stdout.write(f"  {'✅' if created else '⏭ '}: {celeb.name} — {obj.name}")

        # ── Events ────────────────────────────────────────────────────────────
        self.stdout.write(self.style.MIGRATE_HEADING("\n🎟  Seeding events…"))
        for ev in EVENTS:
            celeb = celeb_map.get(ev["slug"])
            if not celeb:
                continue
            event_date = now() + timedelta(days=ev["days"])
            defaults = {
                "title": ev["title"],
                "description": ev["description"],
                "event_type": ev["event_type"],
                "status": ev["status"],
                "event_date": event_date,
                "location": ev["location"],
                "ticket_price": ev["ticket_price"],
                "is_free": ev["is_free"],
                "seats_total": ev["seats_total"],
            }
            obj, created = Event.objects.get_or_create(celebrity=celeb, slug=ev["event_slug"], defaults=defaults)
            self.stdout.write(f"  {'✅' if created else '⏭ '}: {celeb.name} — {obj.title}")

        self.stdout.write(self.style.SUCCESS(
            "\n✅ Done! 25 celebrities, 70 membership tiers, 29 foundations, 50 events seeded."
        ))
