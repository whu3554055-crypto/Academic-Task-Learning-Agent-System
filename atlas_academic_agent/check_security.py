#!/usr/bin/env python3
"""
Security check script for ATLAS project.
Scans the codebase for potential sensitive information leaks.
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Tuple


class SecurityScanner:
    """Scans project files for potential security issues."""
    
    # Patterns that might indicate sensitive information
    SENSITIVE_PATTERNS = [
        (r'(?i)(api[_-]?key|secret[_-]?key)\s*=\s*["\'][A-Za-z0-9]{20,}["\']', 'Potential API key'),
        (r'(?i)(password|passwd|pwd)\s*=\s*["\'].+["\']', 'Hardcoded password'),
        (r'(?i)(token)\s*=\s*["\'][A-Za-z0-9]{20,}["\']', 'Hardcoded token'),
        (r'(?i)(sk-[A-Za-z0-9]{32,})', 'OpenAI-style API key'),
        (r'(?i)(Bearer [A-Za-z0-9]{20,})', 'Bearer token'),
    ]
    
    # Files/directories to skip
    SKIP_PATTERNS = [
        r'\.git[\\/]',
        r'venv[\\/]',
        r'__pycache__[\\/]',
        r'\.pyc$',
        r'\.env$',  # Skip .env files (they should be gitignored)
        r'node_modules[\\/]',
    ]
    
    def __init__(self, root_path: str):
        self.root_path = Path(root_path)
        self.issues: List[Tuple[str, str, int]] = []
        
    def should_skip(self, file_path: Path) -> bool:
        """Check if file should be skipped."""
        try:
            rel_path = str(file_path.relative_to(self.root_path))
            return any(re.search(pattern, rel_path) for pattern in self.SKIP_PATTERNS)
        except ValueError:
            # If file is not relative to root_path, skip it
            return True
    
    def scan_file(self, file_path: Path) -> None:
        """Scan a single file for sensitive patterns."""
        if not file_path.is_file():
            return
            
        # Check file extension
        if file_path.suffix not in ['.py', '.js', '.json', '.yaml', '.yml', '.md', '.txt', '.sh', '.bat', '.ps1']:
            return
            
        # Skip files in ignored directories
        if self.should_skip(file_path):
            return
            
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
                
            for line_num, line in enumerate(lines, 1):
                # Skip comments and example placeholders
                stripped = line.strip()
                if stripped.startswith('#') or stripped.startswith('//'):
                    continue
                if 'your_api_key_here' in line or 'example' in line.lower():
                    continue
                    
                for pattern, description in self.SENSITIVE_PATTERNS:
                    if re.search(pattern, line):
                        rel_path = file_path.relative_to(self.root_path)
                        self.issues.append((str(rel_path), description, line_num))
                        
        except Exception as e:
            print(f"Warning: Could not read {file_path}: {e}")
    
    def scan_directory(self) -> None:
        """Recursively scan directory for issues."""
        for file_path in self.root_path.rglob('*'):
            if file_path.is_file():
                self.scan_file(file_path)
    
    def check_gitignore(self) -> bool:
        """Verify .gitignore properly excludes sensitive files."""
        # Look for .gitignore in parent directories
        gitignore_path = None
        current = self.root_path
        for _ in range(3):  # Check up to 3 levels up
            candidate = current / '.gitignore'
            if candidate.exists():
                gitignore_path = candidate
                break
            current = current.parent
        
        if not gitignore_path:
            self.issues.append(('.gitignore', 'Missing .gitignore file', 0))
            return False
            
        with open(gitignore_path, 'r') as f:
            content = f.read()
            
        required_patterns = ['.env', '*.env', 'venv/', '__pycache__/']
        missing = [p for p in required_patterns if p not in content]
        
        if missing:
            self.issues.append(('.gitignore', f'Missing patterns: {", ".join(missing)}', 0))
            return False
            
        return True
    
    def run_scan(self) -> bool:
        """Run complete security scan."""
        print("🔍 Running security scan...")
        print(f"📁 Scanning: {self.root_path}\n")
        
        # Check .gitignore
        self.check_gitignore()
        
        # Scan all files
        self.scan_directory()
        
        # Report results
        if self.issues:
            print("❌ Security issues found:\n")
            for file_path, description, line_num in self.issues:
                if line_num > 0:
                    print(f"  • {file_path}:{line_num} - {description}")
                else:
                    print(f"  • {file_path} - {description}")
            print(f"\n⚠️  Total issues: {len(self.issues)}")
            return False
        else:
            print("✅ No security issues detected!")
            print("\nSecurity status:")
            print("  ✓ No hardcoded credentials found")
            print("  ✓ .gitignore properly configured")
            print("  ✓ Sample data appears safe")
            return True


def main():
    """Main entry point."""
    # Default to current directory or specified path
    scan_path = sys.argv[1] if len(sys.argv) > 1 else '.'
    
    scanner = SecurityScanner(scan_path)
    is_secure = scanner.run_scan()
    
    # Exit with appropriate code
    sys.exit(0 if is_secure else 1)


if __name__ == '__main__':
    main()
