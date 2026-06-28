import os
from pathlib import Path
from supabase import create_client, Client
from dotenv import load_dotenv

# Load .env from the backend directory
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# Supabase Configuration
SUPABASE_URL = "https://uhnslmutvdtctgkkdonu.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVobnNsbXV0dmR0Y3Rna2tkb251Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODIzODUwNDUsImV4cCI6MjA5Nzk2MTA0NX0.HZ0uUxv7Gq5K7EcoBh9xH0W_QD6HsowQi6jxaXVJtuw"

# Initialize Supabase Client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Storage Bucket Name
STORAGE_BUCKET = "complaints-images"

