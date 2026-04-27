"""AI Code Review Analyzer - Core analysis engine."""
import re
import json
from typing import Dict, List, Any


class CodeReviewAnalyzer:
    """AI-powered code review analyzer."""
    
    def __init__(self):
        self.issues = []
        self.score = 100
        
    def analyze(self, code: str, language: str) -> Dict[str, Any]:
        """Main analysis method that runs all checks."""
        self.issues = []
        self.score = 100
        
        # Run all analysis checks
        self._check_syntax_errors(code, language)
        self._check_security_issues(code, language)
        self._check_code_style(code, language)
        self._check_best_practices(code, language)
        self._check_performance(code, language)
        self._check_potential_bugs(code, language)
        self._calculate_complexity(code, language)
        
        # Generate overall report
        report = {
            'score': max(0, self.score),
            'total_issues': len(self.issues),
            'issues_by_severity': self._group_by_severity(),
            'issues_by_category': self._group_by_category(),
            'issues': self.issues,
            'summary': self._generate_summary(),
            'suggestions': self._generate_suggestions(),
            'complexity': self._calculate_metrics(code),
        }
        
        return report
    
    def _add_issue(self, category: str, severity: str, message: str, line: int = None, suggestion: str = None):
        """Add an issue to the list."""
        issue = {
            'category': category,
            'severity': severity,
            'message': message,
            'line': line,
            'suggestion': suggestion
        }
        self.issues.append(issue)
        
        # Deduct points based on severity
        if severity == 'critical':
            self.score -= 15
        elif severity == 'high':
            self.score -= 10
        elif severity == 'medium':
            self.score -= 5
        elif severity == 'low':
            self.score -= 2
    
    def _check_syntax_errors(self, code: str, language: str):
        """Check for basic syntax errors."""
        if language == 'python':
            # Check for common Python syntax issues
            lines = code.split('\n')
            for i, line in enumerate(lines, 1):
                # Check for tabs vs spaces issue
                if line.startswith('\t'):
                    self._add_issue(
                        'Syntax',
                        'medium',
                        'Use spaces instead of tabs for indentation',
                        i,
                        'Replace tabs with 4 spaces for PEP 8 compliance'
                    )
                
                # Check for missing colons after function/class definitions
                if re.match(r'^\s*(def|class|if|else|elif|for|while|try|except|finally|with)\s*:', line):
                    pass  # This is correct
                elif re.match(r'^\s*(def|class|if|else|elif|for|while|try|except|finally|with)\s+', line):
                    self._add_issue(
                        'Syntax',
                        'high',
                        f'Missing colon at end of statement',
                        i,
                        'Add ":" at the end of the line'
                    )
                
                # Check for undefined variables (basic check)
                if '=' in line and '==' not in line and '!=' not in line:
                    if re.match(r'^\s*[a-zA-Z_][a-zA-Z0-9_]*\s*=\s*$', line):
                        self._add_issue(
                            'Syntax',
                            'medium',
                            'Empty assignment detected',
                            i,
                            'Remove empty assignments'
                        )
    
    def _check_security_issues(self, code: str, language: str):
        """Check for common security issues."""
        # Check for hardcoded credentials
        patterns = [
            (r'password\s*=\s*["\'][^"\']{3,}["\']', 'Hardcoded password detected', 'Use environment variables'),
            (r'api[_-]?key\s*=\s*["\'][^"\']{3,}["\']', 'Hardcoded API key detected', 'Use environment variables'),
            (r'secret\s*=\s*["\'][^"\']{3,}["\']', 'Hardcoded secret detected', 'Use environment variables'),
            (r'token\s*=\s*["\'][^"\']{3,}["\']', 'Hardcoded token detected', 'Use environment variables'),
        ]
        
        lines = code.split('\n')
        for i, line in enumerate(lines, 1):
            for pattern, msg, suggestion in patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    self._add_issue(
                        'Security',
                        'critical',
                        msg,
                        i,
                        suggestion
                    )
        
        # Check for SQL injection vulnerabilities
        if 'execute(' in code or 'cursor.execute' in code:
            if '"%s"' in code or "'%s'" in code or '.format(' in code:
                self._add_issue(
                    'Security',
                    'critical',
                    'Potential SQL injection vulnerability',
                    None,
                    'Use parameterized queries instead of string formatting'
                )
        
        # Check for eval usage (security risk)
        if re.search(r'\beval\s*\(', code):
            self._add_issue(
                'Security',
                'high',
                'Use of eval() is a security risk',
                None,
                'Avoid using eval(). Use ast.literal_eval for safe parsing'
            )
        
        # Check for pickle usage (security risk)
        if re.search(r'\bpickle\.loads?\s*\(', code):
            self._add_issue(
                'Security',
                'high',
                'Unpickling data from untrusted sources is dangerous',
                None,
                'Use JSON for untrusted data or validate input thoroughly'
            )
    
    def _check_code_style(self, code: str, language: str):
        """Check for code style issues."""
        lines = code.split('\n')
        
        # Check line length
        for i, line in enumerate(lines, 1):
            if len(line) > 120:
                self._add_issue(
                    'Style',
                    'low',
                    f'Line too long ({len(line)} characters)',
                    i,
                    'Keep lines under 120 characters for readability'
                )
        
        # Check for trailing whitespace
        for i, line in enumerate(lines, 1):
            if line.rstrip() != line:
                self._add_issue(
                    'Style',
                    'low',
                    'Trailing whitespace',
                    i,
                    'Remove trailing whitespace'
                )
        
        # Check for multiple statements on one line
        for i, line in enumerate(lines, 1):
            if ';' in line and language == 'python':
                self._add_issue(
                    'Style',
                    'medium',
                    'Multiple statements on one line',
                    i,
                    'Use separate lines for each statement'
                )
        
        # Check for very long lines (over 200 chars)
        for i, line in enumerate(lines, 1):
            if len(line) > 200:
                self._add_issue(
                    'Style',
                    'medium',
                    f'Very long line ({len(line)} characters)',
                    i,
                    'Break long lines into multiple lines'
                )
    
    def _check_best_practices(self, code: str, language: str):
        """Check for best practice violations."""
        lines = code.split('\n')
        
        # Check for bare except
        if re.search(r'except\s*:', code):
            self._add_issue(
                'Best Practice',
                'high',
                'Bare except clause catches all exceptions',
                None,
                'Specify exception type: except Exception:'
            )
        
        # Check for print statements in production code
        if re.search(r'\bprint\s*\(', code):
            self._add_issue(
                'Best Practice',
                'low',
                'Print statement found - use logging instead',
                None,
                'Use Python logging module for production code'
            )
        
        # Check for TODO comments
        if 'TODO' in code or 'FIXME' in code or 'XXX' in code:
            self._add_issue(
                'Best Practice',
                'low',
                'TODO/FIXME comment found',
                None,
                'Address TODO items before production'
            )
        
        # Check for magic numbers
        for i, line in enumerate(lines, 1):
            if re.search(r'\b\d{3,}\b', line):  # Numbers with 3+ digits
                if 'http' not in line.lower() and 'url' not in line.lower():
                    self._add_issue(
                        'Best Practice',
                        'medium',
                        'Magic number detected - use named constant',
                        i,
                        'Define as constant with meaningful name'
                    )
        
        # Check for missing docstrings
        if 'def ' in code and '"""' not in code and "'''" not in code:
            self._add_issue(
                'Best Practice',
                'low',
                'Function without docstring',
                None,
                'Add docstring to document function purpose'
            )
    
    def _check_performance(self, code: str, language: str):
        """Check for performance issues."""
        lines = code.split('\n')
        
        # Check for string concatenation in loops
        if 'for ' in code and '+=' in code:
            # Check if string concatenation in loop
            in_loop = False
            for line in lines:
                if 'for ' in line:
                    in_loop = True
                elif line.strip().startswith('def ') or line.strip().startswith('class '):
                    in_loop = False
                elif in_loop and '+=' in line:
                    self._add_issue(
                        'Performance',
                        'medium',
                        'String concatenation in loop - use list or join()',
                        None,
                        'Use "".join() or list append for better performance'
                    )
                    break
        
        # Check for repeated function calls in loops
        if 'for ' in code:
            # Check for len() in loop condition
            for i, line in enumerate(lines, 1):
                if 'for ' in line and 'len(' in line:
                    self._add_issue(
                        'Performance',
                        'medium',
                        'len() called in loop - cache the length',
                        i,
                        'Store len() result before loop'
                    )
                    break
        
        # Check for using + instead of join for strings
        if '+ ' in code and 'join' not in code:
            string_ops = sum(1 for line in lines if '+ ' in line and '=' in line)
            if string_ops > 2:
                self._add_issue(
                    'Performance',
                    'low',
                    'Multiple string concatenations - use join()',
                    None,
                    'Use str.join() for better performance'
                )
    
    def _check_potential_bugs(self, code: str, language: str):
        """Check for potential bugs."""
        lines = code.split('\n')
        
        # Check for comparison using = instead of ==
        for i, line in enumerate(lines, 1):
            if re.search(r'\bif\s+.*[^=]=[^=].*:', line):
                self._add_issue(
                    'Bug',
                    'critical',
                    'Assignment used instead of comparison (did you mean ==?)',
                    i,
                    'Use == for comparison, = for assignment'
                )
        
        # Check for mutable default arguments
        if 'def ' in code:
            for i, line in enumerate(lines, 1):
                if re.search(r'def\s+\w+\s*\([^)]*=\s*\[\s*\]', line):
                    self._add_issue(
                        'Bug',
                        'high',
                        'Mutable default argument detected',
                        i,
                        'Use None as default and assign inside function'
                    )
                elif re.search(r'def\s+\w+\s*\([^)]*=\s*\{', line):
                    self._add_issue(
                        'Bug',
                        'high',
                        'Mutable default argument detected',
                        i,
                        'Use None as default and assign inside function'
                    )
        
        # Check for unused variables
        for i, line in enumerate(lines, 1):
            if re.match(r'^\s*[a-zA-Z_][a-zA-Z0-9_]*\s*=\s*', line):
                var_name = re.match(r'^\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*=', line)
                if var_name:
                    var = var_name.group(1)
                    # Check if variable is used later
                    remaining_code = '\n'.join(lines[i:])
                    if f'{var}' not in remaining_code or remaining_code.count(f'{var}') == 1:
                        if not var.startswith('_'):
                            self._add_issue(
                                'Bug',
                                'low',
                                f'Variable "{var}" may be unused',
                                i,
                                'Remove unused variable or prefix with _'
                            )
        
        # Check for shadowing built-in functions
        builtins = ['list', 'dict', 'set', 'str', 'int', 'float', 'bool', 'type', 'id']
        for i, line in enumerate(lines, 1):
            for builtin in builtins:
                if re.search(rf'\b{builtin}\s*=', line):
                    self._add_issue(
                        'Bug',
                        'medium',
                        f'Shadowing built-in function "{builtin}"',
                        i,
                        'Use different variable name'
                    )
    
    def _calculate_complexity(self, code: str, language: str):
        """Calculate code complexity metrics."""
        lines = code.split('\n')
        
        # Count functions
        functions = len(re.findall(r'def\s+\w+', code))
        
        # Count classes
        classes = len(re.findall(r'class\s+\w+', code))
        
        # Count loops
        loops = len(re.findall(r'\b(for|while)\s+', code))
        
        # Count conditionals
        conditionals = len(re.findall(r'\b(if|elif|else)\s*:', code))
        
        # Calculate cyclomatic complexity (rough estimate)
        complexity = 1 + loops + conditionals
        
        return {
            'functions': functions,
            'classes': classes,
            'loops': loops,
            'conditionals': conditionals,
            'cyclomatic_complexity': complexity,
            'total_lines': len([l for l in lines if l.strip()]),
            'code_lines': len([l for l in lines if l.strip() and not l.strip().startswith('#')]),
        }
    
    def _calculate_metrics(self, code: str) -> Dict[str, Any]:
        """Calculate various code metrics."""
        lines = code.split('\n')
        code_lines = [l for l in lines if l.strip() and not l.strip().startswith('#')]
        comment_lines = [l for l in lines if l.strip().startswith('#')]
        
        return {
            'total_lines': len(lines),
            'code_lines': len(code_lines),
            'comment_lines': len(comment_lines),
            'blank_lines': len([l for l in lines if not l.strip()]),
        }
    
    def _group_by_severity(self) -> Dict[str, int]:
        """Group issues by severity."""
        grouped = {'critical': 0, 'high': 0, 'medium': 0, 'low': 0}
        for issue in self.issues:
            grouped[issue['severity']] = grouped.get(issue['severity'], 0) + 1
        return grouped
    
    def _group_by_category(self) -> Dict[str, int]:
        """Group issues by category."""
        grouped = {}
        for issue in self.issues:
            category = issue['category']
            grouped[category] = grouped.get(category, 0) + 1
        return grouped
    
    def _generate_summary(self) -> str:
        """Generate a summary of the review."""
        if not self.issues:
            return "Great job! No issues found in your code."
        
        critical = sum(1 for i in self.issues if i['severity'] == 'critical')
        high = sum(1 for i in self.issues if i['severity'] == 'high')
        medium = sum(1 for i in self.issues if i['severity'] == 'medium')
        low = sum(1 for i in self.issues if i['severity'] == 'low')
        
        summary = f"Found {len(self.issues)} issues: "
        parts = []
        if critical > 0:
            parts.append(f"{critical} critical")
        if high > 0:
            parts.append(f"{high} high")
        if medium > 0:
            parts.append(f"{medium} medium")
        if low > 0:
            parts.append(f"{low} low")
        
        return summary + ", ".join(parts)
    
    def _generate_suggestions(self) -> List[str]:
        """Generate improvement suggestions."""
        suggestions = []
        
        # Add suggestions based on issues found
        categories = set(i['category'] for i in self.issues)
        
        if 'Security' in categories:
            suggestions.append("Review and fix security issues before deploying to production")
        
        if 'Bug' in categories:
            suggestions.append("Address all bug-related issues to prevent runtime errors")
        
        if 'Performance' in categories:
            suggestions.append("Optimize performance-critical sections of your code")
        
        if 'Best Practice' in categories:
            suggestions.append("Follow Python best practices and coding standards")
        
        if 'Style' in categories:
            suggestions.append("Run a linter to automatically fix style issues")
        
        if self.score >= 90:
            suggestions.append("Excellent code quality! Keep up the good work.")
        elif self.score >= 70:
            suggestions.append("Good code quality. Consider addressing the remaining issues.")
        else:
            suggestions.append("Code needs improvement. Focus on critical and high severity issues first.")
        
        return suggestions


def analyze_code(code: str, language: str = 'python') -> Dict[str, Any]:
    """Main function to analyze code."""
    analyzer = CodeReviewAnalyzer()
    return analyzer.analyze(code, language)