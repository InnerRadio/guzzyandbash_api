# scripts/seed_db.py

import os
import sys
import uuid
import random
from datetime import datetime, timedelta
import json
from faker import Faker
from sqlalchemy.orm import Session
from sqlalchemy.orm import configure_mappers
from sqlalchemy import text
from passlib.context import CryptContext


# Add the project root to the sys.path to allow imports from app.*
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import database and models
from app.database import SessionLocal, engine, Base
from app.models.user import User, UserTypeOption, user_user_types
from app.models.content import Content, ContentType, ContentStatus
from app.models.nft import MintedMemorialEntry
from app.models.affiliate import Affiliate, AffiliateClick, AffiliateCommission
from app.models.referral import Referral
from app.schemas.user_schemas import UserRole

# Call configure_mappers immediately after all model imports.
configure_mappers()


# Initialize Faker
fake = Faker()

# Initialize CryptContext for password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- Helper Functions ---

def get_password_hash(password: str) -> str:
    """Hashes a password using bcrypt via CryptContext."""
    return pwd_context.hash(password)

def create_initial_data(db: Session):
    """
    Creates and adds initial dummy data to the database.
    This function assumes a clean database and configured mappers.
    """
    print("Creating initial data...")

    # --- 1. UserTypeOptions ---
    user_types = {}
    default_user_type_names = ["Registered User", "Consumer", "Creator", "Affiliate", "Admin", "Super User"]
    for name in default_user_type_names:
        user_type_obj = UserTypeOption(
            id=str(uuid.uuid4()),
            name=name,
            description=f"Standard {name} role.",
            is_active=True
        )
        db.add(user_type_obj)
        user_types[name] = user_type_obj
    db.flush()

    print(f"Created {len(user_types)} user types.")

    # --- 2. Users ---
    users_data = []
    num_users = 50

    # Create the ACTUAL super user with provided credentials
    super_user = User(
        id=str(uuid.uuid4()),
        username="guzzy_superuser", # Your desired username
        email="admin@guzzyandbash.com", # Your desired email
        hashed_password=get_password_hash("GuzzyBash#@!9"), # Your desired password, correctly hashed
        is_active=True,
        full_name="Guz The Grand Master",
        role=UserRole.SUPER_USER,
        permissions_level="full_system_access"
    )
    db.add(super_user)
    users_data.append(super_user)
    db.flush()
    # Link super user to its user type
    super_user.user_types.append(user_types["Super User"])


    # Create an admin user (still seeded)
    admin_user = User(
        id=str(uuid.uuid4()),
        username="admin_bash",
        email="admin@example.com",
        hashed_password=get_password_hash("AdminSecure123"),
        is_active=True,
        full_name="Bash The Admin",
        role=UserRole.ADMIN,
        permissions_level="elevated"
    )
    db.add(admin_user)
    users_data.append(admin_user)
    db.flush()
    admin_user.user_types.append(user_types["Admin"])

    # Create other users
    for i in range(num_users - 2): # -2 for the actual superuser and the seeded admin user
        user_id = str(uuid.uuid4())
        username = fake.user_name() + str(i)
        email = fake.email()
        password = fake.password(length=10)
        role = random.choice(list(UserRole))
        
        user = User(
            id=user_id,
            username=username,
            email=email,
            hashed_password=get_password_hash(password),
            is_active=fake.boolean(chance_of_getting_true=95),
            full_name=fake.name(),
            bio=fake.paragraph(nb_sentences=2),
            profile_picture_url=fake.image_url() if fake.boolean(chance_of_getting_true=70) else None,
            social_links=fake.url() if fake.boolean(chance_of_getting_true=50) else None,
            role=role,
            permissions_level="standard",
            affiliate_id=str(uuid.uuid4()) if role == UserRole.AFFILIATE or fake.boolean(chance_of_getting_true=20) else None,
            referral_code=fake.bothify(text='????##') if role == UserRole.AFFILIATE or fake.boolean(chance_of_getting_true=20) else None,
        )
        db.add(user)
        users_data.append(user)
        
        if role == UserRole.REGISTERED_USER:
            user.user_types.append(user_types["Registered User"])
        elif role == UserRole.CONSUMER:
            user.user_types.append(user_types["Consumer"])
        elif role == UserRole.CREATOR:
            user.user_types.append(user_types["Creator"])
        elif role == UserRole.AFFILIATE:
            user.user_types.append(user_types["Affiliate"])
        elif role == UserRole.ADMIN:
            user.user_types.append(user_types["Admin"])
        elif role == UserRole.SUPER_USER:
            user.user_types.append(user_types["Super User"])

    db.flush()

    affiliates_with_ids = [u for u in users_data if u.affiliate_id]
    for user in users_data:
        if user != super_user and user != admin_user and fake.boolean(chance_of_getting_true=30) and affiliates_with_ids:
            user.referring_affiliate_id = random.choice(affiliates_with_ids).affiliate_id
    db.flush()

    print(f"Created {len(users_data)} users.")

    # --- 3. Affiliates (for users who have affiliate_id) ---
    affiliates_created = []
    for user in users_data:
        if user.affiliate_id: 
            existing_affiliate = next((a for a in affiliates_created if a.user_id == user.id), None)
            if not existing_affiliate:
                affiliate = Affiliate(
                    id=str(uuid.uuid4()),
                    user_id=user.id,
                    referral_code=user.referral_code if user.referral_code else fake.lexify(text='??????????'),
                    commission_rate=random.uniform(0.05, 0.20),
                    is_active=fake.boolean(chance_of_getting_true=90)
                )
                db.add(affiliate)
                affiliates_created.append(affiliate)
    db.flush()
    print(f"Created {len(affiliates_created)} affiliate profiles.")


    # --- 4. Content Items ---
    content_items = []
    creators = [u for u in users_data if u.role == UserRole.CREATOR or fake.boolean(chance_of_getting_true=50)]
    
    if not creators:
        creators.append(random.choice(users_data))

    for _ in range(100):
        creator = random.choice(creators)
        content_item = Content(
            uuid=str(uuid.uuid4()),
            title=fake.catch_phrase(),
            description=fake.paragraph(nb_sentences=5),
            content_type=random.choice(list(ContentType)),
            content_status=random.choice(list(ContentStatus)),
            creator_id=creator.id,
            views=random.randint(10, 10000),
            sales=round(random.uniform(0.0, 500.0), 2),
            created_at=fake.date_time_between(start_date="-2y", end_date="now")
        )
        db.add(content_item)
        content_items.append(content_item)
    db.flush()
    print(f"Created {len(content_items)} content items.")


    # --- 5. Minted Memorial Entries (NFTs) ---
    minted_nfts = []
    minters = [u for u in users_data if u.role == UserRole.CREATOR or u.role == UserRole.ADMIN or u.role == UserRole.SUPER_USER or fake.boolean(chance_of_getting_true=10)]
    
    if not minters:
        minters.append(random.choice(users_data))

    for _ in range(30):
        minter = random.choice(minters)
        nft_entry = MintedMemorialEntry(
            id=str(uuid.uuid4()),
            memorial_entry_id=str(uuid.uuid4()),
            nft_token_id=fake.sha256()[:64],
            transaction_hash=fake.sha256()[:64],
            minter_user_id=minter.id,
            minted_at=fake.date_time_between(start_date="-1y", end_date="now"),
            metadata_uri=fake.uri() if fake.boolean(chance_of_getting_true=80) else None,
            name=fake.word().capitalize() + " Memorial NFT",
            description=fake.sentence(),
            image_uri=fake.image_url() if fake.boolean(chance_of_getting_true=70) else None,
            xrpl_response=json.dumps({"result": "success", "ledger_index": fake.random_int(min=100000, max=999999)})
        )
        db.add(nft_entry)
        minted_nfts.append(nft_entry)
    db.flush()
    print(f"Created {len(minted_nfts)} minted memorial entries.")


    # --- 6. Affiliate Clicks ---
    affiliate_clicks = []
    eligible_affiliates_for_clicks = [a for a in affiliates_created if a.is_active]
    
    if not eligible_affiliates_for_clicks:
        print("No active affiliates to generate clicks for. Skipping affiliate clicks.")
    else:
        for _ in range(200):
            affiliate = random.choice(eligible_affiliates_for_clicks)
            click_time = fake.date_time_between(start_date="-1y", end_date="now")
            click = AffiliateClick(
                id=str(uuid.uuid4()),
                affiliate_id=affiliate.user_id,
                timestamp=click_time,
                ip_address=fake.ipv4() if fake.boolean(chance_of_getting_true=80) else None,
                user_agent=fake.user_agent(),
                referer_url=fake.uri() if fake.boolean(chance_of_getting_true=60) else None,
                click_destination_url=fake.url(),
                campaign_id=str(uuid.uuid4()) if fake.boolean(chance_of_getting_true=30) else None,
                ad_id=str(uuid.uuid4()) if fake.boolean(chance_of_getting_true=20) else None,
                created_at=click_time,
                updated_at=click_time
            )
            db.add(click)
            affiliate_clicks.append(click)
        db.flush()
        print(f"Created {len(affiliate_clicks)} affiliate clicks.")


    # --- 7. Affiliate Commissions ---
    affiliate_commissions = []
    
    if not affiliates_created:
        print("No affiliates to generate commissions for. Skipping affiliate commissions.")
    else:
        for _ in range(50):
            affiliate = random.choice(affiliates_created)
            sale_value = round(random.uniform(10.0, 1000.0), 2)
            commission_rate = affiliate.commission_rate
            commission_amount = round(sale_value * commission_rate, 2)
            commission_date = fake.date_time_between(start_date="-1y", end_date="now")
            
            commission = AffiliateCommission(
                id=str(uuid.uuid4()),
                affiliate_id=affiliate.id,
                referred_sale_id=str(uuid.uuid4()) if fake.boolean(chance_of_getting_true=70) else None,
                referred_sale_value=sale_value,
                commission_amount=commission_amount,
                commission_date=commission_date,
                is_paid=fake.boolean(chance_of_getting_true=70),
                paid_date=fake.date_time_between(start_date=commission_date, end_date="now") if fake.boolean(chance_of_getting_true=70) else None
            )
            db.add(commission)
            affiliate_commissions.append(commission)
        db.flush()
        print(f"Created {len(affiliate_commissions)} affiliate commissions.")


    # --- 8. Referrals ---
    referrals = []
    users_to_be_referred = random.sample(users_data, min(40, len(users_data) - 1))

    for referred_user in users_to_be_referred:
        potential_referrers = [u for u in users_data if u.id != referred_user.id and u.affiliate_id]
        
        referrer_user = random.choice(potential_referrers) if potential_referrers else None

        if fake.boolean(chance_of_getting_true=60) and referrer_user:
            referral_code = referrer_user.referral_code if referrer_user.referral_code else fake.bothify(text='????##')
        else:
            referral_code = fake.bothify(text='????##')
            referrer_user = None

        referral_entry = Referral(
            id=str(uuid.uuid4()),
            referred_user_id=referred_user.id,
            referrer_user_id=referrer_user.id if referrer_user else None,
            referral_code_used=referral_code,
            referred_at=fake.date_time_between(start_date="-1y", end_date="now"),
            referral_metadata=json.dumps({"source": fake.word(), "campaign": fake.word()}) if fake.boolean(chance_of_getting_true=30) else None
        )
        db.add(referral_entry)
        referrals.append(referral_entry)
    db.flush()
    print(f"Created {len(referrals)} referral entries.")


    db.commit()
    print("Database seeding complete!")


def create_tables_and_seed():
    """
    Ensures tables are dropped and created in the correct order, then seeds the database.
    """
    db = SessionLocal()
    try:
        print("Dropping all existing database tables in dependency order...")
        for table in reversed(Base.metadata.sorted_tables):
            db.execute(text(f"DROP TABLE IF EXISTS `{table.name}` CASCADE"))
            print(f"Dropped table: {table.name}")
        db.commit()
        print("All tables dropped.")

        print("Creating all database tables...")
        Base.metadata.create_all(bind=engine)
        print("Tables created.")

        create_initial_data(db)
    except Exception as e:
        db.rollback()
        print(f"An error occurred during seeding: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_tables_and_seed()
