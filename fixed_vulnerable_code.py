import os
import sys
import json
import hashlib
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SecurityAudit:
    def __init__(self, target_path: str):
        self.target_path = Path(target_path)
        self.results: List[Dict[str, Any]] = []
        self.checks = [
            self.check_sensitive_files,
            self.check_hardcoded_secrets,
            self.check_dependency_vulns,
            self.check_file_permissions,
            self.check_sql_injection,
            self.check_xss_vulnerabilities,
            self.check_command_injection,
            self.check_deserialization,
            self.check_log_forging,
            self.check_crypto_misuse
        ]

    def run_scan(self) -> Dict[str, Any]:
        logger.info(f"Starting security audit for: {self.target_path}")
        if not self.target_path.exists():
            raise FileNotFoundError(f"Target path does not exist: {self.target_path}")

        for check in self.checks:
            try:
                check()
            except Exception as e:
                logger.error(f"Check {check.__name__} failed: {e}")

        return {
            "target": str(self.target_path),
            "total_checks": len(self.checks),
            "results": self.results
        }

    def check_sensitive_files(self):
        sensitive_patterns = [".env", "config.json", "id_rsa", "*.pem", "*.key"]
        for pattern in sensitive_patterns:
            for file in self.target_path.rglob(pattern):
                if file.is_file():
                    self.results.append({
                        "type": "sensitive_file",
                        "file": str(file),
                        "severity": "high",
                        "message": f"Sensitive file found: {file}"
                    })

    def check_hardcoded_secrets(self):
        secret_patterns = ["password", "secret", "key", "token", "api_key"]
        for file in self.target_path.rglob("*.py"):
            try:
                content = file.read_text(errors='ignore')
                for pattern in secret_patterns:
                    if pattern in content.lower():
                        self.results.append({
                            "type": "hardcoded_secret",
                            "file": str(file),
                            "severity": "critical",
                            "message": f"Potential hardcoded secret ({pattern}) in {file}"
                        })
            except Exception as e:
                logger.warning(f"Could not read {file}: {e}")

    def check_dependency_vulns(self):
        req_files = ["requirements.txt", "Pipfile", "pyproject.toml"]
        for req_file in req_files:
            file_path = self.target_path / req_file
            if file_path.exists():
                self.results.append({
                    "type": "dependency_check",
                    "file": str(file_path),
                    "severity": "medium",
                    "message": f"Dependency file found: {req_file}. Consider using safety or dependabot."
                })

    def check_file_permissions(self):
        for file in self.target_path.rglob("*"):
            if file.is_file():
                try:
                    mode = file.stat().st_mode
                    if mode & 0o777 == 0o777:
                        self.results.append({
                            "type": "file_permission",
                            "file": str(file),
                            "severity": "high",
                            "message": f"File with overly permissive permissions (777): {file}"
                        })
                except Exception as e:
                    logger.warning(f"Could not check permissions for {file}: {e}")

    def check_sql_injection(self):
        sql_patterns = ["execute(", "executemany(", "cursor.execute("]
        for file in self.target_path.rglob("*.py"):
            try:
                content = file.read_text(errors='ignore')
                for pattern in sql_patterns:
                    if pattern in content:
                        lines = [i+1 for i, line in enumerate(content.split('\n')) if pattern in line]
                        self.results.append({
                            "type": "sql_injection",
                            "file": str(file),
                            "severity": "high",
                            "message": f"Potential SQL injection at lines {lines} in {file}"
                        })
            except Exception as e:
                logger.warning(f"Could not read {file}: {e}")

    def check_xss_vulnerabilities(self):
        xss_patterns = ["innerHTML", "document.write", "eval("]
        for file in self.target_path.rglob("*.js"):
            try:
                content = file.read_text(errors='ignore')
                for pattern in xss_patterns:
                    if pattern in content:
                        lines = [i+1 for i, line in enumerate(content.split('\n')) if pattern in line]
                        self.results.append({
                            "type": "xss",
                            "file": str(file),
                            "severity": "high",
                            "message": f"Potential XSS vulnerability at lines {lines} in {file}"
                        })
            except Exception as e:
                logger.warning(f"Could not read {file}: {e}")

    def check_command_injection(self):
        cmd_patterns = ["subprocess.call", "subprocess.Popen", "os.system", "os.popen"]
        for file in self.target_path.rglob("*.py"):
            try:
                content = file.read_text(errors='ignore')
                for pattern in cmd_patterns:
                    if pattern in content:
                        lines = [i+1 for i, line in enumerate(content.split('\n')) if pattern in line]
                        self.results.append({
                            "type": "command_injection",
                            "file": str(file),
                            "severity": "critical",
                            "message": f"Potential command injection at lines {lines} in {file}"
                        })
            except Exception as e:
                logger.warning(f"Could not read {file}: {e}")

    def check_deserialization(self):
        pickle_patterns = ["pickle.load", "pickle.loads", "yaml.load", "marshal.load"]
        for file in self.target_path.rglob("*.py"):
            try:
                content = file.read_text(errors='ignore')
                for pattern in pickle_patterns:
                    if pattern in content:
                        lines = [i+1 for i, line in enumerate(content.split('\n')) if pattern in line]
                        self.results.append({
                            "type": "deserialization",
                            "file": str(file),
                            "severity": "critical",
                            "message": f"Potential unsafe deserialization at lines {lines} in {file}"
                        })
            except Exception as e:
                logger.warning(f"Could not read {file}: {e}")

    def check_log_forging(self):
        log_patterns = ["logging.info", "logging.warning", "logging.error", "print("]
        for file in self.target_path.rglob("*.py"):
            try:
                content = file.read_text(errors='ignore')
                for pattern in log_patterns:
                    if pattern in content:
                        lines = [i+1 for i, line in enumerate(content.split('\n')) if pattern in line]
                        self.results.append({
                            "type": "log_forging",
                            "file": str(file),
                            "severity": "medium",
                            "message": f"Potential log forging at lines {lines} in {file}"
                        })
            except Exception as e:
                logger.warning(f"Could not read {file}: {e}")

    def check_crypto_misuse(self):
        weak_crypto = ["md5", "sha1", "DES", "RC4", "base64"]
        for file in self.target_path.rglob("*.py"):
            try:
                content = file.read_text(errors='ignore')
                for pattern in weak_crypto:
                    if pattern in content.lower():
                        lines = [i+1 for i, line in enumerate(content.split('\n')) if pattern in line.lower()]
                        self.results.append({
                            "type": "crypto_misuse",
                            "file": str(file),
                            "severity": "high",
                            "message": f"Potential weak crypto ({pattern}) at lines {lines} in {file}"
                        })
            except Exception as e:
                logger.warning(f"Could not read {file}: {e}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python security_audit.py <target_path>")
        sys.exit(1)

    target_path = sys.argv[1]
    auditor = SecurityAudit(target_path)
    try:
        report = auditor.run_scan()
        print(json.dumps(report, indent=2))
    except Exception as e:
        logger.error(f"Audit failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()