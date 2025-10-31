"""Duplicate checking utilities for people/contacts."""

from typing import Dict, List, Any, Optional


class DuplicateChecker:
    """Utility class for checking duplicate contacts based on FUB's deduplication rules."""
    
    @staticmethod
    def normalize_phone(phone: str) -> str:
        """
        Normalize phone number for comparison.
        Removes spaces, dashes, parentheses, and other formatting.
        """
        if not phone:
            return ""
        # Remove common formatting characters
        normalized = "".join(c for c in phone if c.isdigit())
        # Remove leading country code if it's 1 (US/Canada)
        if len(normalized) == 11 and normalized.startswith("1"):
            normalized = normalized[1:]
        return normalized
    
    @staticmethod
    def normalize_email(email: str) -> str:
        """Normalize email for comparison (lowercase, trim)."""
        if not email:
            return ""
        return email.lower().strip()
    
    @staticmethod
    def normalize_name(name: str) -> str:
        """Normalize name for comparison (lowercase, trim, remove extra spaces)."""
        if not name:
            return ""
        return " ".join(name.lower().strip().split())
    
    @staticmethod
    def check_email_match(email: str, contact: Dict[str, Any]) -> bool:
        """
        Check if email matches any email in the contact.
        Rule: If two contacts share the same email address, they are duplicates.
        """
        if not email:
            return False
        
        normalized_email = DuplicateChecker.normalize_email(email)
        contact_emails = contact.get("emails", [])
        
        for contact_email in contact_emails:
            contact_email_value = contact_email.get("value", "")
            if DuplicateChecker.normalize_email(contact_email_value) == normalized_email:
                return True
        
        return False
    
    @staticmethod
    def check_phone_and_name_match(
        phone: str,
        first_name: Optional[str],
        last_name: Optional[str],
        contact: Dict[str, Any]
    ) -> bool:
        """
        Check if phone and name match.
        Rule: If two contacts have the same phone number AND both first and last names match, they are duplicates.
        """
        if not phone:
            return False
        
        normalized_phone = DuplicateChecker.normalize_phone(phone)
        contact_phones = contact.get("phones", [])
        
        # Check if phone matches
        phone_match = False
        for contact_phone in contact_phones:
            contact_phone_value = contact_phone.get("value", "")
            if DuplicateChecker.normalize_phone(contact_phone_value) == normalized_phone:
                phone_match = True
                break
        
        if not phone_match:
            return False
        
        # Phone matches, now check if both first and last names match
        if not first_name or not last_name:
            return False
        
        contact_first = DuplicateChecker.normalize_name(contact.get("firstName", ""))
        contact_last = DuplicateChecker.normalize_name(contact.get("lastName", ""))
        
        normalized_first = DuplicateChecker.normalize_name(first_name)
        normalized_last = DuplicateChecker.normalize_name(last_name)
        
        return (
            contact_first == normalized_first and
            contact_last == normalized_last
        )
    
    @staticmethod
    def find_duplicates(
        contacts: List[Dict[str, Any]],
        email: Optional[str] = None,
        phone: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Find duplicate contacts based on FUB's deduplication rules.
        
        Args:
            contacts: List of contact dictionaries to check against
            email: Email to check
            phone: Phone number to check
            first_name: First name to check
            last_name: Last name to check
        
        Returns:
            List of duplicate contacts with match reasons
        """
        duplicates = []
        
        for contact in contacts:
            match_reasons = []
            
            # Rule 1: Email match
            if email and DuplicateChecker.check_email_match(email, contact):
                match_reasons.append("email_match")
            
            # Rule 2: Phone + Name match
            if phone and first_name and last_name:
                if DuplicateChecker.check_phone_and_name_match(phone, first_name, last_name, contact):
                    match_reasons.append("phone_and_name_match")
            
            if match_reasons:
                duplicates.append({
                    "contact": contact,
                    "matchReasons": match_reasons,
                    "confidence": "high" if len(match_reasons) > 1 or "email_match" in match_reasons else "medium"
                })
        
        return duplicates
    
    @staticmethod
    def format_duplicate_result(duplicates: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Format duplicate check result for API response."""
        return {
            "hasDuplicates": len(duplicates) > 0,
            "duplicateCount": len(duplicates),
            "duplicates": [
                {
                    "id": dup["contact"].get("id"),
                    "name": dup["contact"].get("name"),
                    "firstName": dup["contact"].get("firstName"),
                    "lastName": dup["contact"].get("lastName"),
                    "emails": dup["contact"].get("emails", []),
                    "phones": dup["contact"].get("phones", []),
                    "matchReasons": dup["matchReasons"],
                    "confidence": dup["confidence"],
                    "created": dup["contact"].get("created"),
                    "source": dup["contact"].get("source"),
                }
                for dup in duplicates
            ]
        }

