import os
from pathlib import Path
from supabase import create_client, Client
from dotenv import load_dotenv

# Load .env from the backend directory
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# Supabase Configuration
SUPABASE_URL = "https://uhnslmutvdtctgkkdonu.supabase.co"
SUPABASE_KEY = "sb_publishable_OEz2B-qiUplqgrHdCk2PNg_Lp1TN9W1"

# Initialize Supabase Client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Storage Bucket Name
STORAGE_BUCKET = "complaints-images"

