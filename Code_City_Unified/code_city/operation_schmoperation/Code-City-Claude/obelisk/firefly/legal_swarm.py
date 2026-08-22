# obelisk/firefly/legal_swarm.py

# [DNA_TAG]
# ORIGIN: Crostini-Chromebook
# PILLAR: codecity-unified
# DEPS: stdlib
# ROLE: Firefly Legal Swarm - Document Analysis for Defense
# AUTHOR: Buffy (Codebuff AI)
# SESSION: 2026-08-22 Bucket 08 DNA Sweep
# TIER: Module (3)
# [/DNA_TAG]

"""
Firefly Legal Swarm - Document Analysis for Defense
Specialized scouts for Brady violations, evidence errors, misconduct
"""

class LegalScout:
    """Base class for legal document analyzers"""
    
    def __init__(self, specialty):
        self.specialty = specialty  # brady, chain_of_custody, signatures, etc.
        self.findings = []
    
    def scan_document(self, doc):
        """Analyze document for issues"""
        raise NotImplementedError

class BradyScout(LegalScout):
    """Finds Brady violations (exculpatory evidence)"""
    
    def __init__(self):
        super().__init__('brady_material')
        self.indicators = [
            'witness recantation',
            'alternative suspect',
            'alibi evidence',
            'forensic contradiction',
            'police misconduct',
            'withheld evidence',
            'inconsistent statement'
        ]
    
    def scan_document(self, doc):
        """Look for exculpatory evidence"""
        findings = []
        
        text = doc['text'].lower()
        
        # Check for Brady indicators
        for indicator in self.indicators:
            if indicator in text:
                findings.append({
                    'type': 'brady_potential',
                    'indicator': indicator,
                    'document': doc['filename'],
                    'page': self._find_page(doc, indicator),
                    'context': self._extract_context(doc, indicator),
                    'severity': 'high'
                })
        
        # Check for withheld evidence
        if self._check_disclosure_dates(doc):
            findings.append({
                'type': 'brady_violation',
                'issue': 'late_disclosure',
                'document': doc['filename'],
                'severity': 'critical'
            })
        
        return findings
    
    def _check_disclosure_dates(self, doc):
        """Did prosecution delay disclosure?"""
        # Compare disclosure date to trial date
        # If disclosed late = potential Brady violation
        pass

class GiglioScout(LegalScout):
    """Finds Giglio violations (witness credibility issues)"""
    
    def __init__(self):
        super().__init__('giglio_material')
    
    def scan_document(self, doc):
        """Look for impeachment material"""
        findings = []
        
        # Check for:
        # - Witness criminal history
        # - Witness deals with prosecution
        # - Witness bias/motive to lie
        # - Witness inconsistent statements
        
        if 'witness' in doc['type']:
            # Compare this statement to prior statements
            inconsistencies = self._compare_statements(doc)
            
            if inconsistencies:
                findings.append({
                    'type': 'giglio_impeachment',
                    'witness': doc['witness_name'],
                    'inconsistencies': inconsistencies,
                    'severity': 'high'
                })
        
        return findings
    
    def _compare_statements(self, current_doc):
        """Compare to witness's prior statements"""
        # Find all statements from same witness
        # Highlight differences
        pass

class ChainOfCustodyScout(LegalScout):
    """Finds breaks in evidence chain of custody"""
    
    def __init__(self):
        super().__init__('chain_of_custody')
    
    def scan_document(self, doc):
        """Analyze evidence handling"""
        findings = []
        
        if doc['type'] == 'evidence_log':
            chain = self._extract_custody_chain(doc)
            
            # Check for gaps
            gaps = self._find_gaps(chain)
            if gaps:
                findings.append({
                    'type': 'custody_break',
                    'evidence_id': doc['evidence_id'],
                    'gaps': gaps,
                    'severity': 'critical'  # Evidence inadmissible
                })
            
            # Check for improper handling
            violations = self._check_handling_procedures(chain)
            if violations:
                findings.append({
                    'type': 'improper_handling',
                    'evidence_id': doc['evidence_id'],
                    'violations': violations,
                    'severity': 'high'
                })
        
        return findings
    
    def _find_gaps(self, chain):
        """Look for missing custody entries"""
        gaps = []
        
        for i in range(len(chain) - 1):
            current = chain[i]
            next_entry = chain[i + 1]
            
            # Check time gap
            if (next_entry['timestamp'] - current['timestamp']) > timedelta(hours=24):
                gaps.append({
                    'from': current,
                    'to': next_entry,
                    'duration': next_entry['timestamp'] - current['timestamp']
                })
            
            # Check if transfer was documented
            if current['transferred_to'] != next_entry['received_by']:
                gaps.append({
                    'issue': 'transfer_mismatch',
                    'expected': current['transferred_to'],
                    'actual': next_entry['received_by']
                })
        
        return gaps

class SignatureScout(LegalScout):
    """Verifies signatures, notarizations, affidavits"""
    
    def __init__(self):
        super().__init__('signatures')
    
    def scan_document(self, doc):
        """Check signature validity"""
        findings = []
        
        if doc['requires_signature']:
            # Check for wet ink signature
            if not self._has_wet_signature(doc):
                findings.append({
                    'type': 'missing_signature',
                    'document': doc['filename'],
                    'severity': 'critical'  # Doc may be invalid
                })
            
            # Check for notarization (if required)
            if doc['requires_notary']:
                if not self._is_notarized(doc):
                    findings.append({
                        'type': 'missing_notarization',
                        'document': doc['filename'],
                        'severity': 'critical'
                    })
            
            # Check for jurat (sworn statement)
            if doc['requires_jurat']:
                if not self._has_jurat(doc):
                    findings.append({
                        'type': 'missing_jurat',
                        'document': doc['filename'],
                        'severity': 'high'
                    })
        
        return findings
    
    def _has_wet_signature(self, doc):
        """Check if document has actual signature (not digital)"""
        # Image analysis or metadata check
        # Digital signature when wet ink required = invalid
        pass

class EvidenceRulesScout(LegalScout):
    """Checks compliance with Kansas Rules of Evidence"""
    
    def __init__(self):
        super().__init__('evidence_rules')
        self.kansas_rules = self._load_kansas_rules()
    
    def scan_document(self, doc):
        """Check evidence admissibility"""
        findings = []
        
        # Check relevance (K.S.A. 60-401)
        if not self._is_relevant(doc):
            findings.append({
                'type': 'irrelevant_evidence',
                'rule': 'KSA 60-401',
                'document': doc['filename'],
                'severity': 'high'
            })
        
        # Check hearsay (K.S.A. 60-460)
        if self._is_hearsay(doc) and not self._has_exception(doc):
            findings.append({
                'type': 'hearsay',
                'rule': 'KSA 60-460',
                'document': doc['filename'],
                'severity': 'critical'
            })
        
        # Check authentication (K.S.A. 60-464)
        if not self._is_authenticated(doc):
            findings.append({
                'type': 'unauthenticated',
                'rule': 'KSA 60-464',
                'document': doc['filename'],
                'severity': 'high'
            })
        
        return findings

class MisconductScout(LegalScout):
    """Detects prosecutorial misconduct"""
    
    def __init__(self):
        super().__init__('prosecutorial_misconduct')
    
    def scan_document(self, doc):
        """Look for misconduct patterns"""
        findings = []
        
        # Witness tampering
        if self._detect_witness_coaching(doc):
            findings.append({
                'type': 'witness_tampering',
                'evidence': self._extract_evidence(doc),
                'severity': 'critical'
            })
        
        # Evidence fabrication
        if self._detect_fabrication(doc):
            findings.append({
                'type': 'evidence_fabrication',
                'evidence': self._extract_evidence(doc),
                'severity': 'critical'
            })
        
        # Failure to disclose exculpatory evidence
        if self._detect_brady_suppression(doc):
            findings.append({
                'type': 'brady_suppression',
                'evidence': self._extract_evidence(doc),
                'severity': 'critical'
            })
        
        return findings

class MalpracticeScout(LegalScout):
    """Identifies legal malpractice by defense attorney (if applicable)"""
    
    def __init__(self):
        super().__init__('defense_malpractice')
    
    def scan_document(self, doc):
        """Check for ineffective assistance of counsel"""
        findings = []
        
        # Missed deadlines
        if self._check_missed_deadlines(doc):
            findings.append({
                'type': 'missed_deadline',
                'deadline': doc['deadline'],
                'severity': 'high'
            })
        
        # Failed to file motions
        if self._check_missing_motions(doc):
            findings.append({
                'type': 'missing_motion',
                'motion_type': 'suppress/dismiss/etc',
                'severity': 'high'
            })
        
        # Failed to investigate
        if self._check_investigation_gaps(doc):
            findings.append({
                'type': 'failed_investigation',
                'gaps': self._extract_gaps(doc),
                'severity': 'critical'
            })
        
        return findings

class TimelineScout(LegalScout):
    """Builds timeline, finds impossibilities"""
    
    def __init__(self):
        super().__init__('timeline')
        self.events = []
    
    def scan_document(self, doc):
        """Extract timeline events"""
        events = self._extract_events(doc)
        self.events.extend(events)
        
        # Check for physical impossibilities
        impossibilities = self._check_physics(self.events)
        
        findings = []
        if impossibilities:
            findings.append({
                'type': 'impossible_timeline',
                'impossibilities': impossibilities,
                'severity': 'critical'
            })
        
        return findings
    
    def _check_physics(self, events):
        """Can someone be in two places at once?"""
        impossibilities = []
        
        # Sort events by time
        sorted_events = sorted(events, key=lambda e: e['timestamp'])
        
        for i in range(len(sorted_events) - 1):
            event1 = sorted_events[i]
            event2 = sorted_events[i + 1]
            
            # Calculate travel time between locations
            distance = self._calculate_distance(event1['location'], event2['location'])
            time_available = event2['timestamp'] - event1['timestamp']
            time_needed = distance / 60  # mph to minutes
            
            if time_needed > time_available:
                impossibilities.append({
                    'event1': event1,
                    'event2': event2,
                    'distance': distance,
                    'time_available': time_available,
                    'time_needed': time_needed,
                    'conclusion': 'Physically impossible for Wade to be at both locations'
                })
        
        return impossibilities