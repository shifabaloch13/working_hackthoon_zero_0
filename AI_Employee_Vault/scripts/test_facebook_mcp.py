"""
Test Script for Facebook/Instagram MCP - Gold Tier

Tests all Facebook/Instagram MCP functionality:
- Facebook post creation
- Instagram post creation
- Approval workflow
- Post publishing

Usage:
    python test_facebook_mcp.py "../AI_Employee_Vault"
"""

import sys
import json
from pathlib import Path
from datetime import datetime


def test_facebook_mcp(vault_path: str):
    """Test all Facebook MCP functions."""
    
    print('=' * 70)
    print('  FACEBOOK/INSTAGRAM MCP - TEST SUITE')
    print('=' * 70)
    print()
    
    # Import the MCP class
    sys.path.insert(0, str(Path(__file__).parent.parent / 'AI_Employee_Vault' / 'scripts'))
    try:
        from facebook_poster import FacebookMCP
        print('[OK] FacebookMCP module imported')
    except ImportError as e:
        print(f'[ERROR] Failed to import FacebookMCP: {e}')
        print('[INFO] Make sure facebook_poster.py exists in AI_Employee_Vault/scripts/')
        return False
    
    # Initialize MCP
    print()
    print('Initializing Facebook MCP...')
    facebook = FacebookMCP(vault_path)
    print(f'[OK] Facebook MCP initialized')
    print(f'     Vault: {facebook.vault}')
    print(f'     Config: {facebook.config_path}')
    print()
    
    # Test results
    results = {
        'test_facebook_post_draft': False,
        'test_instagram_post_draft': False,
        'test_post_with_link': False,
        'test_process_approved': False
    }
    
    # Test 1: Create Facebook Post Draft
    print('-' * 70)
    print('TEST 1: Create Facebook Post Draft')
    print('-' * 70)
    try:
        draft_file = facebook.create_post_draft(
            message='Excited to announce our Q1 results! Revenue up 45% 🚀 #growth #business #success',
            platform='facebook',
            link=None,
            photo_path=None
        )
        
        if draft_file.exists():
            print(f'[PASS] Facebook post draft created: {draft_file.name}')
            results['test_facebook_post_draft'] = True
            
            # Show draft content
            print()
            print('Draft Content Preview:')
            content = draft_file.read_text()
            for line in content.split('\n')[:20]:
                print(f'  {line}')
        else:
            print(f'[FAIL] Facebook post draft file not created')
    except Exception as e:
        print(f'[FAIL] Error creating Facebook post draft: {e}')
    
    print()
    
    # Test 2: Create Instagram Post Draft
    print('-' * 70)
    print('TEST 2: Create Instagram Post Draft')
    print('-' * 70)
    try:
        draft_file = facebook.create_post_draft(
            message='New product launch! Innovation meets design. #innovation #newproduct #launch',
            platform='instagram',
            link=None,
            photo_path='path/to/image.jpg'  # This is optional in simulation
        )
        
        if draft_file.exists():
            print(f'[PASS] Instagram post draft created: {draft_file.name}')
            results['test_instagram_post_draft'] = True
            
            # Show draft content
            print()
            print('Draft Content Preview:')
            content = draft_file.read_text()
            for line in content.split('\n')[:15]:
                print(f'  {line}')
        else:
            print(f'[FAIL] Instagram post draft file not created')
    except Exception as e:
        print(f'[FAIL] Error creating Instagram post draft: {e}')
    
    print()
    
    # Test 3: Create Post with Link
    print('-' * 70)
    print('TEST 3: Create Facebook Post with Link')
    print('-' * 70)
    try:
        draft_file = facebook.create_post_draft(
            message='Check out our latest offer! Limited time only.',
            platform='facebook',
            link='https://example.com/special-offer',
            photo_path=None
        )
        
        if draft_file.exists():
            print(f'[PASS] Facebook post with link created: {draft_file.name}')
            results['test_post_with_link'] = True
        else:
            print(f'[FAIL] Facebook post with link not created')
    except Exception as e:
        print(f'[FAIL] Error creating post with link: {e}')
    
    print()
    
    # Test 4: Process Approved Posts
    print('-' * 70)
    print('TEST 4: Process Approved Posts')
    print('-' * 70)
    try:
        # First create a test approved post
        draft_file = facebook.create_post_draft(
            message='Test post for approval workflow testing #test',
            platform='facebook'
        )
        
        # Move to approved
        approved_file = facebook.approved / draft_file.name
        draft_file.rename(approved_file)
        print(f'[INFO] Created test approved post: {approved_file.name}')
        
        # Process approved
        posted = facebook.process_approved_posts()
        
        print(f'[PASS] Processed {posted} approved post(s)')
        results['test_process_approved'] = True
    except Exception as e:
        print(f'[FAIL] Error processing approved posts: {e}')
    
    print()
    
    # Summary
    print('=' * 70)
    print('  TEST SUMMARY')
    print('=' * 70)
    print()
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, result in results.items():
        status = '[PASS]' if result else '[FAIL]'
        print(f'  {status} - {test_name}')
    
    print()
    print(f'Total: {passed}/{total} tests passed ({passed/total*100:.1f}%)')
    print()
    
    if passed == total:
        print('[SUCCESS] ALL TESTS PASSED! Facebook/Instagram MCP is working correctly.')
        return True
    else:
        print('[WARNING] Some tests failed. Check the output above for details.')
        return False


def main():
    if len(sys.argv) < 2:
        print('Usage: python test_facebook_mcp.py <vault_path>')
        print()
        print('Examples:')
        print('  python test_facebook_mcp.py "../AI_Employee_Vault"')
        sys.exit(1)
    
    vault_path = sys.argv[1]
    
    if not Path(vault_path).exists():
        print(f'[ERROR] Vault path does not exist: {vault_path}')
        sys.exit(1)
    
    success = test_facebook_mcp(vault_path)
    
    print()
    print('=' * 70)
    print('  NEXT STEPS')
    print('=' * 70)
    print()
    print('1. Configure Facebook/Instagram:')
    print('   - Create facebook_config.json with access tokens')
    print('   - Get Page Access Token from Facebook Developer')
    print('   - Connect Instagram Business account')
    print()
    print('2. Test Real Posting:')
    print('   python facebook_poster.py "../AI_Employee_Vault" --post "Hello World!"')
    print()
    print('3. Approval Workflow:')
    print('   - Review draft in Pending_Approval/')
    print('   - Move to Approved/ to publish')
    print('   - Run: python facebook_poster.py "../AI_Employee_Vault" --post-approved')
    print()
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
