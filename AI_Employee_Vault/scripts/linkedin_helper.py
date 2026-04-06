"""
LinkedIn Post Helper

Opens LinkedIn and shows you the post content to copy-paste.

Usage:
    python linkedin_helper.py "D:/path/to/vault" "Your post content"
"""

import sys
import webbrowser
import time
from pathlib import Path


def main():
    if len(sys.argv) < 3:
        print('Usage: python linkedin_helper.py <vault_path> <post_content>')
        print()
        print('Or to post from Approved folder:')
        print('  python linkedin_helper.py <vault_path> --from-approved')
        sys.exit(1)
    
    vault_path = Path(sys.argv[1]).resolve()
    
    if sys.argv[2] == '--from-approved':
        # Get content from Approved folder
        approved_folder = vault_path / 'Approved'
        approved_files = list(approved_folder.glob('SOCIAL_POST_*.md'))
        
        if not approved_files:
            print('[ERROR] No approved posts found')
            sys.exit(1)
        
        # Get the first approved file
        post_file = approved_files[0]
        content = post_file.read_text(encoding='utf-8')
        
        # Extract content from markdown
        lines = content.split('\n')
        in_content = False
        post_lines = []
        
        for line in lines:
            if line.strip() == '## Content':
                in_content = True
                continue
            if in_content:
                if line.startswith('##') or line.startswith('---'):
                    break
                post_lines.append(line)
        
        post_content = '\n'.join(post_lines).strip()
    else:
        post_content = sys.argv[2]
    
    print()
    print('=' * 70)
    print('  LINKEDIN POST HELPER')
    print('=' * 70)
    print()
    print('Opening LinkedIn in your default browser...')
    print()
    
    # Open LinkedIn in default browser
    webbrowser.open('https://www.linkedin.com/feed/')
    
    print('Content to post:')
    print()
    print('-' * 70)
    print(post_content)
    print('-' * 70)
    print()
    print('Steps:')
    print('  1. LinkedIn should have opened in your browser')
    print('  2. Copy the content above (Ctrl+C)')
    print('  3. In LinkedIn, click "Start a post"')
    print('  4. Paste the content (Ctrl+V)')
    print('  5. Click "Post"')
    print()
    print('Waiting 60 seconds...')
    print()
    
    time.sleep(60)
    
    print()
    print('=' * 70)
    print('  DONE!')
    print('=' * 70)
    print()
    print('If you posted successfully, move the file to Done folder:')
    print(f'  move Approved\\*.md Done\\')
    print()


if __name__ == '__main__':
    main()
