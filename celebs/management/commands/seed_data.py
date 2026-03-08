from django.core.management.base import BaseCommand
from django.utils.timezone import now, timedelta


class Command(BaseCommand):
    help = "Seed the database with 6 sample celebrities, membership tiers, foundations, and events"

    def handle(self, *args, **kwargs):
        from celebs.models import Celebrity
        from memberships.models import MembershipTier
        from donations.models import Foundation
        from events.models import Event

        self.stdout.write(self.style.MIGRATE_HEADING("🌟 Seeding celebrities…"))

        celebs_data = [
            {
                "name": "Aria Valentina",
                "slug": "aria-valentina",
                "tagline": "Grammy-winning pop sensation",
                "bio": "Aria Valentina is a multi-platinum award-winning pop artist known for her powerful vocals and electrifying performances. Born in Rio de Janeiro, she rose to fame at just 19 and has since sold over 50 million records worldwide.",
                "category": "music",
                "nationality": "Brazilian",
                "instagram": "https://instagram.com/",
                "twitter": "https://twitter.com/",
                "is_featured": True,
            },
            {
                "name": "Marcus Thunder",
                "slug": "marcus-thunder",
                "tagline": "NBA All-Star & Philanthropist",
                "bio": "Marcus Thunder is a two-time NBA champion and four-time All-Star. Off the court, he runs multiple youth basketball academies and is a vocal advocate for education in underserved communities.",
                "category": "sports",
                "nationality": "American",
                "twitter": "https://twitter.com/",
                "is_featured": True,
            },
            {
                "name": "Elena Voss",
                "slug": "elena-voss",
                "tagline": "Oscar-nominated actress",
                "bio": "Elena Voss is an acclaimed actress best known for her roles in award-winning dramas and blockbuster thrillers. With over 30 films to her name, she has received numerous accolades including three Golden Globe nominations.",
                "category": "acting",
                "nationality": "German",
                "instagram": "https://instagram.com/",
                "youtube": "https://youtube.com/",
                "is_featured": False,
            },
            {
                "name": "Ray Kola",
                "slug": "ray-kola",
                "tagline": "Africa's biggest comedy star",
                "bio": "Ray Kola is a comedian, TV host, and social media influencer with over 20 million followers. His stand-up specials have sold out venues on four continents, and he's regularly ranked among the world's top 10 comedians.",
                "category": "comedy",
                "nationality": "Nigerian",
                "youtube": "https://youtube.com/",
                "instagram": "https://instagram.com/",
                "is_featured": True,
            },
            {
                "name": "Sophia Chen",
                "slug": "sophia-chen",
                "tagline": "Tech visionary & entrepreneur",
                "bio": "Sophia Chen is a self-made billionaire who founded three unicorn tech companies before the age of 35. She is a prominent speaker on AI ethics, women in technology, and sustainable entrepreneurship.",
                "category": "business",
                "nationality": "Taiwanese",
                "twitter": "https://twitter.com/",
                "is_featured": False,
            },
            {
                "name": "Diego Alvarez",
                "slug": "diego-alvarez",
                "tagline": "World Cup hero",
                "bio": "Diego Alvarez is a legendary footballer who captained his national team to World Cup victory. Now retired from professional play, he runs football academies across Latin America and is an ambassador for multiple global charities.",
                "category": "sports",
                "nationality": "Argentinian",
                "instagram": "https://instagram.com/",
                "twitter": "https://twitter.com/",
                "is_featured": True,
            },
        ]

        celeb_objs = {}
        for data in celebs_data:
            obj, created = Celebrity.objects.get_or_create(slug=data["slug"], defaults=data)
            celeb_objs[data["slug"]] = obj
            status = "Created" if created else "Exists"
            self.stdout.write(f"  {status}: {obj.name}")

        self.stdout.write(self.style.MIGRATE_HEADING("\n🎖 Seeding membership tiers…"))

        tiers_data = [
            # Aria Valentina
            {"celebrity_slug": "aria-valentina", "name": "Fan Club", "price": "9.99", "duration_days": 365, "badge_color": "gray", "description": "Basic access to exclusive fan content.", "benefits": ["Monthly newsletter", "Digital wallpapers", "Early ticket access"]},
            {"celebrity_slug": "aria-valentina", "name": "VIP Member", "price": "29.99", "duration_days": 365, "badge_color": "gold", "description": "Premium fan experience with exclusive perks.", "benefits": ["All Fan Club benefits", "VIP Discord access", "Signed digital content", "Exclusive live streams"]},
            {"celebrity_slug": "aria-valentina", "name": "Platinum Elite", "price": "99.99", "duration_days": 365, "badge_color": "platinum", "description": "Ultimate fan experience — the inner circle.", "benefits": ["All VIP benefits", "Virtual meet & greet", "Platinum badge", "Priority event seating", "Birthday video message"]},
            # Marcus Thunder
            {"celebrity_slug": "marcus-thunder", "name": "Courtside Fan", "price": "14.99", "duration_days": 365, "badge_color": "blue", "description": "Join Marcus Thunder's fan community.", "benefits": ["Exclusive behind-the-scenes content", "Monthly Q&A", "Fan newsletter"]},
            {"celebrity_slug": "marcus-thunder", "name": "All-Star Pass", "price": "49.99", "duration_days": 365, "badge_color": "gold", "description": "Premium membership for true basketball fans.", "benefits": ["All Courtside benefits", "Match day chat rooms", "Signed jersey giveaways", "Training camp previews"]},
            # Elena Voss
            {"celebrity_slug": "elena-voss", "name": "Film Club", "price": "12.99", "duration_days": 365, "badge_color": "gray", "description": "Access behind-the-scenes film content.", "benefits": ["Monthly film commentary", "Script excerpts", "Fan newsletter"]},
            {"celebrity_slug": "elena-voss", "name": "Premiere Circle", "price": "39.99", "duration_days": 365, "badge_color": "gold", "description": "Exclusive premiere and press content.", "benefits": ["All Film Club benefits", "Premiere invitations", "Red carpet updates", "Digital autograph"]},
            # Ray Kola
            {"celebrity_slug": "ray-kola", "name": "Laugh Pass", "price": "7.99", "duration_days": 30, "badge_color": "blue", "description": "Monthly comedy content subscription.", "benefits": ["Exclusive sketches", "Early video access", "Monthly blooper reel"]},
            {"celebrity_slug": "ray-kola", "name": "VIP Comedian", "price": "24.99", "duration_days": 365, "badge_color": "gold", "description": "Full-year comedy fan package.", "benefits": ["All Laugh Pass benefits", "Live show discounts", "Annual comedy special", "Meet & greet raffle entry"]},
            # Sophia Chen
            {"celebrity_slug": "sophia-chen", "name": "Innovator", "price": "19.99", "duration_days": 365, "badge_color": "blue", "description": "Access Sophia's tech insights and talks.", "benefits": ["Monthly newsletter", "Webinar access", "Resource library"]},
            {"celebrity_slug": "sophia-chen", "name": "Visionary", "price": "79.99", "duration_days": 365, "badge_color": "platinum", "description": "Full access to Sophia's knowledge ecosystem.", "benefits": ["All Innovator benefits", "Monthly 1-on-1 Q&A slots", "Startup mentorship program", "Exclusive masterclasses"]},
            # Diego Alvarez
            {"celebrity_slug": "diego-alvarez", "name": "La Hinchada", "price": "9.99", "duration_days": 365, "badge_color": "gray", "description": "Be part of Diego's global fan community.", "benefits": ["Fan newsletter", "Match analysis videos", "Community forum access"]},
            {"celebrity_slug": "diego-alvarez", "name": "El Capitán", "price": "34.99", "duration_days": 365, "badge_color": "gold", "description": "Premium football fan experience.", "benefits": ["All La Hinchada benefits", "Training camp exclusive content", "Signed merch giveaway entries", "Video message for birthdays"]},
        ]

        for t in tiers_data:
            celeb = celeb_objs.get(t.pop("celebrity_slug"))
            if celeb:
                # Convert benefits list to newline-separated string for TextField storage
                if isinstance(t.get("benefits"), list):
                    t["benefits"] = "\n".join(t["benefits"])
                obj, created = MembershipTier.objects.get_or_create(celebrity=celeb, name=t["name"], defaults={**t, "celebrity": celeb})
                self.stdout.write(f"  {'Created' if created else 'Exists'}: {celeb.name} — {obj.name}")

        self.stdout.write(self.style.MIGRATE_HEADING("\n❤️ Seeding foundations…"))

        foundations_data = [
            {"celebrity_slug": "aria-valentina", "name": "Aria Music Education Fund", "description": "Supporting access to music education for underprivileged youth around the world.", "target_amount": "500000", "cause_type": "Education"},
            {"celebrity_slug": "aria-valentina", "name": "Rio Clean Water Initiative", "description": "Providing clean drinking water to rural communities in Brazil.", "target_amount": "250000", "cause_type": "Health"},
            {"celebrity_slug": "marcus-thunder", "name": "Thunder Youth Basketball", "description": "Building basketball courts and coaching programs in low-income neighborhoods.", "target_amount": "1000000", "cause_type": "Youth Sports"},
            {"celebrity_slug": "marcus-thunder", "name": "Books & Balls Scholarship", "description": "Full academic scholarships for student athletes who demonstrate academic excellence.", "target_amount": "300000", "cause_type": "Education"},
            {"celebrity_slug": "elena-voss", "name": "Voss Arts Foundation", "description": "Funding independent cinema and arts programs for emerging filmmakers globally.", "target_amount": "400000", "cause_type": "Arts"},
            {"celebrity_slug": "ray-kola", "name": "Comedy Relief Fund", "description": "Mental health support and comedy therapy programs for veterans and trauma survivors.", "target_amount": "200000", "cause_type": "Mental Health"},
            {"celebrity_slug": "ray-kola", "name": "African Youth Empowerment", "description": "Vocational training and startup grants for youth in Sub-Saharan Africa.", "target_amount": "750000", "cause_type": "Entrepreneurship"},
            {"celebrity_slug": "sophia-chen", "name": "CodeHer Initiative", "description": "Providing coding bootcamps and scholarships exclusively for women and girls in emerging markets.", "target_amount": "2000000", "cause_type": "Technology"},
            {"celebrity_slug": "diego-alvarez", "name": "Goles para la Vida", "description": "Disaster relief and reconstruction support for communities devastated by natural disasters in Latin America.", "target_amount": "600000", "cause_type": "Disaster Relief"},
            {"celebrity_slug": "diego-alvarez", "name": "Academy of Dreams", "description": "Free professional football academies for talented youth who cannot afford training.", "target_amount": "800000", "cause_type": "Youth Sports"},
        ]

        for f in foundations_data:
            celeb = celeb_objs.get(f.pop("celebrity_slug"))
            if celeb:
                obj, created = Foundation.objects.get_or_create(celebrity=celeb, name=f["name"], defaults={**f, "celebrity": celeb})
                self.stdout.write(f"  {'Created' if created else 'Exists'}: {celeb.name} — {obj.name}")

        self.stdout.write(self.style.MIGRATE_HEADING("\n🎟 Seeding events…"))

        events_data = [
            {"celebrity_slug": "aria-valentina", "title": "Valentina World Tour — London", "slug": "valentina-world-tour-london", "description": "Experience the magic of Aria Valentina live at the O2 Arena London. A night of chart-topping hits and spectacular production.", "event_type": "concert", "status": "upcoming", "event_date": now() + timedelta(days=30), "location": "O2 Arena, London, UK", "venue": "O2 Arena", "city": "London", "country": "UK", "ticket_price": "85.00", "is_free": False, "seats_total": 20000},
            {"celebrity_slug": "aria-valentina", "title": "VIP Meet & Greet — Paris", "slug": "vip-meet-greet-paris", "description": "An exclusive intimate meet and greet session with Aria Valentina for her most dedicated fans.", "event_type": "meetgreet", "status": "upcoming", "event_date": now() + timedelta(days=32), "location": "Hotel Ritz, Paris, France", "venue": "Hotel Ritz", "city": "Paris", "country": "France", "ticket_price": "299.00", "is_free": False, "seats_total": 50},
            {"celebrity_slug": "marcus-thunder", "title": "Thunder Basketball Clinic", "slug": "thunder-basketball-clinic", "description": "A full-day basketball training clinic led by Marcus Thunder himself. Open to youth aged 10–18.", "event_type": "workshop", "status": "upcoming", "event_date": now() + timedelta(days=15), "location": "LA Sports Complex, Los Angeles, USA", "venue": "LA Sports Complex", "city": "Los Angeles", "country": "USA", "ticket_price": "0", "is_free": True, "seats_total": 200},
            {"celebrity_slug": "marcus-thunder", "title": "Charity Gala for Books & Balls", "slug": "charity-gala-books-balls", "description": "An exclusive black-tie charity dinner raising funds for the Books & Balls Scholarship fund.", "event_type": "charity", "status": "upcoming", "event_date": now() + timedelta(days=60), "location": "The Beverly Hilton, Beverly Hills, USA", "venue": "The Beverly Hilton", "city": "Beverly Hills", "country": "USA", "ticket_price": "500.00", "is_free": False, "seats_total": 300},
            {"celebrity_slug": "elena-voss", "title": "Voss Film Premiere — Berlin", "slug": "voss-film-premiere-berlin", "description": "The world premiere of Elena Voss's latest film. Join her on the red carpet and attend the exclusive after-party.", "event_type": "premiere", "status": "upcoming", "event_date": now() + timedelta(days=45), "location": "Berlinale Palast, Berlin, Germany", "venue": "Berlinale Palast", "city": "Berlin", "country": "Germany", "ticket_price": "150.00", "is_free": False, "seats_total": 800},
            {"celebrity_slug": "ray-kola", "title": "Ray Kola Live — Lagos", "slug": "ray-kola-live-lagos", "description": "Ray Kola brings his hilarious World comedy tour back home to Lagos. Two hours of non-stop laughter guaranteed!", "event_type": "concert", "status": "upcoming", "event_date": now() + timedelta(days=20), "location": "Eko Convention Centre, Lagos, Nigeria", "venue": "Eko Convention Centre", "city": "Lagos", "country": "Nigeria", "ticket_price": "25.00", "is_free": False, "seats_total": 5000},
            {"celebrity_slug": "ray-kola", "title": "Virtual Comedy Night", "slug": "virtual-comedy-night", "description": "An exclusive live-streamed comedy special for Ray Kola fan members. Tune in from anywhere in the world.", "event_type": "virtual", "status": "upcoming", "event_date": now() + timedelta(days=10), "location": "Online — Zoom/Stream", "ticket_price": "10.00", "is_free": False, "seats_total": 0},
            {"celebrity_slug": "sophia-chen", "title": "Future of AI Summit", "slug": "future-of-ai-summit", "description": "Sophia Chen hosts a one-day summit bringing together tech leaders, investors, and innovators to discuss the future of artificial intelligence.", "event_type": "workshop", "status": "upcoming", "event_date": now() + timedelta(days=50), "location": "Taipei International Convention Center, Taipei, Taiwan", "venue": "TICC", "city": "Taipei", "country": "Taiwan", "ticket_price": "199.00", "is_free": False, "seats_total": 1000},
            {"celebrity_slug": "diego-alvarez", "title": "Football Legends Charity Match", "slug": "football-legends-charity-match", "description": "A charitable exhibition match between football legends, with all proceeds going to the Academy of Dreams foundation.", "event_type": "charity", "status": "upcoming", "event_date": now() + timedelta(days=40), "location": "Estadio Monumental, Buenos Aires, Argentina", "venue": "Estadio Monumental", "city": "Buenos Aires", "country": "Argentina", "ticket_price": "30.00", "is_free": False, "seats_total": 85000},
            {"celebrity_slug": "diego-alvarez", "title": "Diego's Academy Open Day", "slug": "diego-academy-open-day", "description": "Visit Diego Alvarez's flagship football academy, watch youth training sessions, and meet the coaching staff.", "event_type": "other", "status": "upcoming", "event_date": now() + timedelta(days=8), "location": "Arena Ciudad, Mexico City, Mexico", "venue": "Arena Ciudad", "city": "Mexico City", "country": "Mexico", "ticket_price": "0", "is_free": True, "seats_total": 500},
        ]

        for ev in events_data:
            celeb = celeb_objs.get(ev.pop("celebrity_slug"))
            if celeb:
                obj, created = Event.objects.get_or_create(celebrity=celeb, slug=ev["slug"], defaults={**ev, "celebrity": celeb})
                self.stdout.write(f"  {'Created' if created else 'Exists'}: {celeb.name} — {obj.title}")

        self.stdout.write(self.style.SUCCESS("\n✅ Seed complete! 6 celebrities, 13 membership tiers, 10 foundations, 10 events created."))
