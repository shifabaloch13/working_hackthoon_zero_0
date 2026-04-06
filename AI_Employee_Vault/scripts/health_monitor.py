"""
Health Monitoring System for Platinum Tier

Monitors cloud and local services, sends alerts on failures.

Usage:
    python health_monitor.py
"""

import os
import sys
import subprocess
import json
import requests
from pathlib import Path
from datetime import datetime
from typing import Dict, List


class HealthMonitor:
    """Monitor health of AI Employee services."""

    def __init__(self, vault_path: str):
        self.vault = Path(vault_path).resolve()
        self.logs_folder = self.vault / 'Logs'
        self.health_log = self.logs_folder / 'health_checks.json'
        
        # Ensure logs folder exists
        self.logs_folder.mkdir(parents=True, exist_ok=True)

    def check_docker_containers(self) -> Dict:
        """Check if Docker containers are running."""
        result = {
            'status': 'unknown',
            'containers': []
        }
        
        try:
            output = subprocess.run(
                ['docker', 'ps', '--format', '{{.Names}}:{{.Status}}'],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            containers = output.stdout.strip().split('\n')
            result['containers'] = []
            
            for container in containers:
                if ':' in container:
                    name, status = container.split(':', 1)
                    is_running = 'running' in status.lower()
                    result['containers'].append({
                        'name': name,
                        'status': status,
                        'running': is_running
                    })
            
            result['status'] = 'healthy' if result['containers'] else 'no_containers'
            
        except Exception as e:
            result['status'] = 'error'
            result['error'] = str(e)
        
        return result

    def check_odoo(self, url: str = 'http://localhost:8069') -> Dict:
        """Check if Odoo is accessible."""
        result = {
            'status': 'unknown',
            'url': url
        }
        
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                result['status'] = 'healthy'
            else:
                result['status'] = 'unhealthy'
                result['status_code'] = response.status_code
        except requests.exceptions.ConnectionError:
            result['status'] = 'unreachable'
        except Exception as e:
            result['status'] = 'error'
            result['error'] = str(e)
        
        return result

    def check_python_processes(self) -> Dict:
        """Check if Python processes (watchers) are running."""
        result = {
            'status': 'unknown',
            'processes': []
        }
        
        try:
            if sys.platform == 'win32':
                # Windows
                output = subprocess.run(
                    ['tasklist', '/FI', 'IMAGENAME eq python*.exe'],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                result['processes'] = output.stdout.strip().split('\n')
            else:
                # Linux/Mac
                output = subprocess.run(
                    ['ps', 'aux'],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                processes = [p for p in output.stdout.split('\n') if 'python' in p.lower()]
                result['processes'] = processes
            
            result['status'] = 'healthy' if result['processes'] else 'no_processes'
            
        except Exception as e:
            result['status'] = 'error'
            result['error'] = str(e)
        
        return result

    def check_disk_space(self) -> Dict:
        """Check available disk space."""
        result = {
            'status': 'unknown',
            'total_gb': 0,
            'used_gb': 0,
            'free_gb': 0,
            'percent_used': 0
        }
        
        try:
            if sys.platform == 'win32':
                import shutil
                total, used, free = shutil.disk_usage(str(self.vault.parent))
            else:
                import os
                stat = os.statvfs(str(self.vault.parent))
                total = stat.f_blocks * stat.f_frsize
                used = (stat.f_blocks - stat.f_bfree) * stat.f_frsize
                free = stat.f_bavail * stat.f_frsize
            
            result['total_gb'] = round(total / (1024**3), 2)
            result['used_gb'] = round(used / (1024**3), 2)
            result['free_gb'] = round(free / (1024**3), 2)
            result['percent_used'] = round((used / total) * 100, 2)
            
            if result['percent_used'] > 90:
                result['status'] = 'critical'
            elif result['percent_used'] > 75:
                result['status'] = 'warning'
            else:
                result['status'] = 'healthy'
            
        except Exception as e:
            result['status'] = 'error'
            result['error'] = str(e)
        
        return result

    def check_git_sync(self) -> Dict:
        """Check if Git sync is working."""
        result = {
            'status': 'unknown',
            'last_commit': None
        }
        
        try:
            # Check last commit time
            output = subprocess.run(
                ['git', 'log', '-1', '--format=%ci'],
                cwd=self.vault.parent,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if output.returncode == 0:
                result['last_commit'] = output.stdout.strip()
                result['status'] = 'healthy'
            else:
                result['status'] = 'error'
                
        except Exception as e:
            result['status'] = 'error'
            result['error'] = str(e)
        
        return result

    def run_full_check(self) -> Dict:
        """Run all health checks."""
        results = {
            'timestamp': datetime.now().isoformat(),
            'checks': {
                'docker': self.check_docker_containers(),
                'odoo': self.check_odoo(),
                'processes': self.check_python_processes(),
                'disk': self.check_disk_space(),
                'git_sync': self.check_git_sync()
            }
        }
        
        # Determine overall status
        statuses = [v['status'] for v in results['checks'].values()]
        
        if 'critical' in statuses or 'error' in statuses:
            results['overall_status'] = 'unhealthy'
        elif 'warning' in statuses:
            results['overall_status'] = 'warning'
        else:
            results['overall_status'] = 'healthy'
        
        return results

    def log_health_check(self, results: Dict):
        """Log health check results."""
        with open(self.health_log, 'a', encoding='utf-8') as f:
            f.write(json.dumps(results) + '\n')

    def send_alert(self, message: str):
        """Send alert (implement based on your notification system)."""
        # For now, just log
        print(f"🚨 ALERT: {message}")
        
        # TODO: Implement email/SMS/Slack alerts
        # Example: Send email via Gmail MCP
        # Example: Send Slack webhook
        # Example: Send SMS via Twilio

    def check_and_alert(self):
        """Run health check and send alerts if needed."""
        results = self.run_full_check()
        self.log_health_check(results)
        
        # Check for issues
        if results['overall_status'] == 'unhealthy':
            self.send_alert(f"AI Employee is unhealthy! Check {self.health_log}")
            
            # Specific alerts
            if results['checks']['docker']['status'] == 'error':
                self.send_alert("Docker check failed!")
            if results['checks']['odoo']['status'] == 'unreachable':
                self.send_alert("Odoo is unreachable!")
            if results['checks']['disk']['status'] == 'critical':
                self.send_alert(f"Disk space critical: {results['checks']['disk']['percent_used']}% used")
        
        return results


def main():
    vault_path = os.getenv('VAULT_PATH', '../AI_Employee_Vault')
    
    if not Path(vault_path).exists():
        print(f'Vault path does not exist: {vault_path}')
        sys.exit(1)
    
    monitor = HealthMonitor(vault_path)
    
    print("=" * 60)
    print("  AI Employee Health Check")
    print("=" * 60)
    print()
    
    results = monitor.check_and_alert()
    
    print(f"Overall Status: {results['overall_status']}")
    print()
    
    for check_name, check_result in results['checks'].items():
        status_icon = "✅" if check_result['status'] == 'healthy' else "⚠️" if check_result['status'] == 'warning' else "❌"
        print(f"{status_icon} {check_name}: {check_result['status']}")
    
    print()
    print(f"Health log: {monitor.health_log}")
    print("=" * 60)


if __name__ == '__main__':
    main()
