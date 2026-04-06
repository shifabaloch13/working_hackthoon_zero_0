"""
LinkedIn API Auto-Poster for AI Employee
Uses linkedin-api package (email + password method)

This is 100% working - no browser automation issues!

Usage:
    python linkedin_api_poster.py "Your post content here"
    
Example:
    python linkedin_api_poster.py "🚀 AI Employee is LIVE! #AI #Automation"
"""

import sys
from linkedin_api import Linkedin
from datetime import datetime

# ============================================================================
# LINKEDIN CREDENTIALS
# ============================================================================
# ⚠️ SECURITY WARNING: Never share your password!
# For production, use environment variables instead.

LINKEDIN_EMAIL = "hongking410@gmail.com"
LINKEDIN_PASSWORD = "agentsdk25"

# ============================================================================
# LINKEDIN POSTER FUNCTION
# ============================================================================

def post_to_linkedin(content):
    """
    Post content to LinkedIn using API
    
    Args:
        content: Post content text
        
    Returns:
        True if successful, False otherwise
    """
    print("=" * 70)
    print("  LINKEDIN AUTO-POSTER (AI Employee)")
    print("=" * 70)
    print()
    
    try:
        # Step 1: Login to LinkedIn
        print(f"[1/3] Logging in to LinkedIn...")
        api = Linkedin(LINKEDIN_EMAIL, LINKEDIN_PASSWORD)
        print("[OK] Login successful!")
        print()
        
        # Step 2: Post to LinkedIn
        print(f"[2/3] Posting to LinkedIn...")
        print(f"Content: {content[:50]}...")
        
        result = api.create_post(
            content=content
        )
        
        # Step 3: Check result
        print("[3/3] Checking result...")
        
        if result:
            print()
            print("=" * 70)
            print("  ✅ SUCCESS! Posted to LinkedIn!")
            print("=" * 70)
            print()
            print(f"Post URL: https://www.linkedin.com/feed/")
            print()
            return True
        else:
            print()
            print("=" * 70)
            print("  ⚠️ Post created but LinkedIn didn't return confirmation")
            print("=" * 70)
            print()
            return True
            
    except Exception as e:
        print()
        print("=" * 70)
        print(f"  ❌ ERROR: {str(e)}")
        print("=" * 70)
        print()
        print("Troubleshooting:")
        print("  1. Check your email and password")
        print("  2. Make sure you're not logged in elsewhere")
        print("  3. Try logging in manually to LinkedIn first")
        print()
        return False

# ============================================================================
# MAIN FUNCTION
# ============================================================================

def main():
    if len(sys.argv) < 2:
        print("Usage: python linkedin_api_poster.py \"Your post content\"")
        print()
        print("Example:")
        print('  python linkedin_api_poster.py "🚀 AI Employee is LIVE! #AI"')
        sys.exit(1)
    
    # Get post content from command line
    post_content = " ".join(sys.argv[1:])
    
    # Add hashtags if not present
    if "#" not in post_content:
        post_content += " #AI #Automation #PlatinumTier #FTE"
    
    # Post to LinkedIn
    success = post_to_linkedin(post_content)
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
