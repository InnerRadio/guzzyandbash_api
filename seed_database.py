import os
import sys
from datetime import datetime, timedelta
import random
import uuid
import json
from faker import Faker
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from passlib.context import CryptContext

# Add the parent directory to the sys.path to allow imports from 'app'
# This is crucial for imports like 'from models.user import User' to work
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'app')))

# Import your models and enums
from models.user import User, UserRole
from models.content import Content, ContentType, ContentStatus
from models.nft import NFT
from models.activity_log import ActivityLog
from models.affiliate import Affiliate, AffiliateClick, AffiliateCommission # Direct import now that we've confirmed existence


# Password Hashing Context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Database URL from environment or default
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+mysqlconnector://ab2583ta_admin:RaviSQL2025!@localhost/ab2583ta_ab2583tarot_lyrical_tarot_db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
fake = Faker()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

async def seed_data():
    db: Session = next(get_db()) # Get a database session

    print("Checking if database is empty...")
    if db.query(User).count() > 0:
        print("Database already contains data. Clearing existing data...")
        # Clear data in reverse order of dependencies (most dependent tables first)

        # 1. Clear Activity Logs (depends on Users)
        db.query(ActivityLog).delete(synchronize_session='fetch')
        print("- Cleared Activity Logs")

        # 2. Clear Affiliate Clicks (depends on Users for affiliate_id)
        db.query(AffiliateClick).delete(synchronize_session='fetch')
        print("- Cleared Affiliate Clicks")
        
        # 3. Clear Affiliate Commissions (depends on Affiliates)
        db.query(AffiliateCommission).delete(synchronize_session='fetch')
        print("- Cleared Affiliate Commissions")

        # 4. Clear NFTs (depends on Users and Content)
        db.query(NFT).delete(synchronize_session='fetch')
        print("- Cleared NFTs")

        # 5. Clear User User Types (direct culprit in earlier error, depends on Users)
        # Using raw SQL for this association table for robustness
        try:
            db.execute(text("DELETE FROM user_user_types;"))
            print("- Cleared user_user_types table")
        except Exception as e:
            # This might fail if the table doesn't exist or is already empty
            print(f"Error clearing user_user_types: {e}. (Ignored if table doesn't exist/empty)")

        # 6. Clear Content Items (depends on Users)
        db.query(Content).delete(synchronize_session='fetch')
        print("- Cleared Content Items")
        
        # 7. Clear Affiliates (depends on Users) - This was the last problematic table
        db.query(Affiliate).delete(synchronize_session='fetch')
        print("- Cleared Affiliates")

        # 8. Clear Users (parent table)
        db.query(User).delete(synchronize_session='fetch')
        print("- Cleared Users")

        db.commit()
        print("Existing data cleared successfully.")
    else:
        print("Database is empty. Proceeding with seeding.")

    # --- Seed Users ---
    print("\nSeeding Users...")
    seeded_users = []

    # Superuser
    guzzy_superuser_id = str(uuid.uuid4())
    superuser_user = User(
        id=guzzy_superuser_id,
        uuid=str(uuid.uuid4()),
        username="guzzy_superuser",
        email="superuser@guzzybash.com",
        hashed_password=get_password_hash("TestPassword123!"),
        is_active=True,
        created_at=datetime.utcnow() - timedelta(days=365),
        last_updated_at=datetime.utcnow() - timedelta(days=30),
        role=UserRole.SUPER_USER.value,
        permissions_level=100,
        is_verified=True,
        has_api_access=True,
        is_superuser=True,
        first_name="Guzzy",
        last_name="Superuser",
        last_login_at=datetime.utcnow()
    )
    db.add(superuser_user)
    seeded_users.append(superuser_user)
    print(f" - Added Superuser: {superuser_user.username}")

    # Admin user
    admin_user_id = str(uuid.uuid4())
    admin_user = User(
        id=admin_user_id,
        uuid=str(uuid.uuid4()),
        username="guzzy_admin",
        email="admin@guzzybash.com",
        hashed_password=get_password_hash("AdminPass123!"),
        is_active=True,
        created_at=datetime.utcnow() - timedelta(days=300),
        last_updated_at=datetime.utcnow() - timedelta(days=15),
        role=UserRole.ADMIN.value,
        permissions_level=90,
        is_verified=True,
        has_api_access=True,
        is_superuser=False,
        first_name="Guzzy",
        last_name="Admin",
        last_login_at=datetime.utcnow()
    )
    db.add(admin_user)
    seeded_users.append(admin_user)
    print(f" - Added Admin: {admin_user.username}")

    # Sample Creator Users
    creator_users = []
    for _ in range(5):
        first_name = fake.first_name()
        last_name = fake.last_name()
        username = f"{first_name.lower()}{last_name.lower()}{random.randint(10, 99)}"
        user = User(
            id=str(uuid.uuid4()),
            uuid=str(uuid.uuid4()),
            username=username,
            email=fake.unique.email(),
            hashed_password=get_password_hash("password123"),
            is_active=True,
            created_at=fake.date_time_between(start_date="-2y", end_date="now"),
            last_updated_at=datetime.utcnow(),
            full_name=f"{first_name} {last_name}",
            bio=fake.text(max_nb_chars=200),
            role=UserRole.CREATOR.value,
            permissions_level=30,
            is_verified=fake.boolean(chance_of_getting_true=80),
            has_api_access=fake.boolean(chance_of_getting_true=50),
            is_superuser=False,
            first_name=first_name,
            last_name=last_name,
            last_login_at=datetime.utcnow()
        )
        db.add(user)
        seeded_users.append(user)
        creator_users.append(user)
        print(f" - Added Creator: {user.username}")

    # Sample Consumer Users
    consumer_users = []
    for _ in range(10):
        first_name = fake.first_name()
        last_name = fake.last_name()
        username = f"{first_name.lower()}{last_name.lower()}{random.randint(10, 99)}"
        user = User(
            id=str(uuid.uuid4()),
            uuid=str(uuid.uuid4()),
            username=username,
            email=fake.unique.email(),
            hashed_password=get_password_hash("password123"),
            is_active=True,
            created_at=fake.date_time_between(start_date="-2y", end_date="now"),
            last_updated_at=datetime.utcnow(),
            full_name=f"{first_name} {last_name}",
            bio=fake.text(max_nb_chars=100),
            role=UserRole.CONSUMER.value,
            permissions_level=10,
            is_verified=fake.boolean(chance_of_getting_true=60),
            has_api_access=False,
            is_superuser=False,
            first_name=first_name,
            last_name=last_name,
            last_login_at=datetime.utcnow()
        )
        db.add(user)
        seeded_users.append(user)
        consumer_users.append(user)
        print(f" - Added Consumer: {user.username}")
    
    db.commit() # Commit users first to establish IDs

    # --- Seed Affiliates (needs to be after users are committed) ---
    print("\nSeeding Affiliates...")
    seeded_affiliates = []
    # Seed affiliates for some of the new users (e.g., all creators, some consumers)
    affiliate_candidates = creator_users + random.sample(consumer_users, k=min(len(consumer_users), 5))
    for user in affiliate_candidates:
        affiliate = Affiliate(
            id=str(uuid.uuid4()),
            user_id=user.id,
            referral_code=f"{user.username.upper()}{random.randint(100, 999)}",
            commission_rate=round(random.uniform(0.05, 0.20), 2),
            is_active=fake.boolean(chance_of_getting_true=90),
            created_at=fake.date_time_between(start_date=user.created_at, end_date="now")
        )
        db.add(affiliate)
        seeded_affiliates.append(affiliate)
        print(f" - Added Affiliate: '{affiliate.referral_code}' for user {user.username}")
    db.commit() # Commit affiliates

    # --- Seed Content Items ---
    print("\nSeeding Content Items...")
    seeded_content_items = []
    content_types = [ct.value for ct in ContentType]
    content_statuses = [cs.value for cs in ContentStatus]

    for user in creator_users + random.sample(consumer_users, min(5, len(consumer_users))): # Some consumers might create too
        for _ in range(random.randint(2, 7)): # Each creator creates 2-7 content items
            content_item = Content(
                id=str(uuid.uuid4()),
                uuid=str(uuid.uuid4()),
                title=fake.sentence(nb_words=5).replace('.', ''),
                description=fake.text(max_nb_chars=500),
                content_type=random.choice(content_types),
                content_status=random.choice(content_statuses),
                views=random.randint(0, 5000),
                likes=random.randint(0, 500),
                sales=round(random.uniform(0, 1000.00), 2),
                tags=json.dumps(random.sample(fake.words(nb=5), k=random.randint(1,3))),
                created_at=fake.date_time_between(start_date=user.created_at, end_date="now"),
                owner_user_id=user.id
            )
            db.add(content_item)
            seeded_content_items.append(content_item)
            print(f" - Added Content: '{content_item.title}' by {user.username}")
    db.commit() # Commit content items

    # --- Seed NFTs ---
    print("\nSeeding NFTs...")
    seeded_nfts = []
    # Create NFTs for some published content
    for content_item in seeded_content_items:
        if content_item.content_status == ContentStatus.PUBLISHED.value and random.random() < 0.6: # 60% chance to have an NFT
            owner_user = db.query(User).filter(User.id == content_item.owner_user_id).first()
            if owner_user:
                nft = NFT(
                    id=str(uuid.uuid4()),
                    uuid=str(uuid.uuid4()),
                    token_id=fake.unique.random_int(min=10000, max=99999),
                    name=f"NFT: {content_item.title}",
                    description=f"NFT version of '{content_item.title}'. {fake.sentence(nb_words=10)}",
                    image_url=fake.image_url(),
                    metadata_url=fake.url(),
                    owner_id=owner_user.id,
                    content_id=content_item.id,
                    minted_at=fake.date_time_between(start_date=content_item.created_at, end_date="now")
                )
                db.add(nft)
                seeded_nfts.append(nft)
                print(f" - Added NFT: '{nft.name}' for content '{content_item.title}'")
    db.commit() # Commit NFTs

    # --- Seed Affiliate Commissions and Clicks ---
    print("\nSeeding Affiliate Commissions and Clicks...")
    for affiliate in seeded_affiliates:
        # Seed some commissions for this affiliate
        num_commissions = random.randint(1, 10)
        for _ in range(num_commissions):
            sale_value = round(random.uniform(10.00, 500.00), 2)
            commission_amount = round(sale_value * affiliate.commission_rate, 2)
            commission = AffiliateCommission(
                id=str(uuid.uuid4()),
                affiliate_id=affiliate.id,
                referred_sale_id=str(uuid.uuid4()) if random.random() < 0.8 else None, # Not all commissions have a specific sale ID
                referred_sale_value=sale_value,
                commission_amount=commission_amount,
                commission_date=fake.date_time_between(start_date=affiliate.created_at, end_date="now"),
                is_paid=fake.boolean(chance_of_getting_true=70),
                paid_date=fake.date_time_between(start_date=affiliate.created_at, end_date="now") if fake.boolean(chance_of_getting_true=70) else None
            )
            db.add(commission)
            print(f" - Added Commission: {commission.commission_amount} for affiliate {affiliate.referral_code}")

        # Seed some clicks for this affiliate
        num_clicks = random.randint(10, 50)
        for _ in range(num_clicks):
            click = AffiliateClick(
                id=str(uuid.uuid4()),
                affiliate_id=affiliate.id,
                timestamp=fake.date_time_between(start_date=affiliate.created_at, end_date="now"),
                ip_address=fake.ipv4(),
                user_agent=fake.user_agent(),
                referer_url=fake.url() if random.random() < 0.7 else None,
                click_destination_url=fake.url(),
                campaign_id=str(uuid.uuid4()) if random.random() < 0.3 else None,
                ad_id=str(uuid.uuid4()) if random.random() < 0.2 else None
            )
            db.add(click)
            # print(f" - Added Click for affiliate {affiliate.referral_code}") # Too verbose, uncomment if needed
    db.commit() # Commit affiliate commissions and clicks

    # --- Seed Activity Logs ---
    print("\nSeeding Activity Logs...")
    activity_types = ["login", "content_created", "nft_minted", "profile_update", "comment_posted", "content_viewed", "liked_content", "affiliate_link_clicked", "affiliate_commission_earned"]
    for user in seeded_users:
        num_activities = random.randint(5, 20)
        for _ in range(num_activities):
            activity_date = fake.date_time_between(start_date=user.created_at, end_date="now")
            activity_log = ActivityLog(
                id=str(uuid.uuid4()),
                user_id=user.id,
                activity_type=random.choice(activity_types),
                description=fake.sentence(nb_words=15),
                timestamp=activity_date,
                metadata_json=json.dumps({"ip_address": fake.ipv4(), "device": fake.user_agent()})
            )
            db.add(activity_log)
            # print(f" - Added Activity for {user.username}: {activity_log.activity_type}") # Too verbose
    db.commit() # Commit activity logs


    print("\nDatabase seeding complete!")
    db.close()

if __name__ == "__main__":
    import asyncio
    asyncio.run(seed_data())
