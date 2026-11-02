import re


def extract_contract_info(text):

    result = {
        "governing_law": None,
        "jurisdiction": None,
        "duration": None
    }

    if not text:
        return result

    # Normalize spaces
    clean_text = re.sub(r'\s+', ' ', text).strip()

    # =========================================
    # GOVERNING LAW
    # =========================================

    governing_law_patterns = [
        r'governed by the laws of ([A-Za-z ]+?)(?:\.|,|;)',
        r'governed by laws of ([A-Za-z ]+?)(?:\.|,|;)',
        r'laws of the State of ([A-Za-z ]+?)(?:\.|,|;)',
        r'law of ([A-Za-z ]+?)(?:\.|,|;)',
    ]

    for pattern in governing_law_patterns:

        match = re.search(
            pattern,
            clean_text,
            re.IGNORECASE
        )

        if match:
            result["governing_law"] = match.group(1).strip()
            break

    # =========================================
    # JURISDICTION
    # =========================================

    jurisdiction_patterns = [
        r'courts of ([A-Za-z ]+?) shall have exclusive jurisdiction',
        r'courts of ([A-Za-z ]+?) shall have jurisdiction',
        r'courts in ([A-Za-z ]+?) shall have exclusive jurisdiction',
        r'courts in ([A-Za-z ]+?) shall have jurisdiction',
        r'jurisdiction of the courts of ([A-Za-z ]+?)(?:\.|,|;)',
        r'subject to the jurisdiction of ([A-Za-z ]+?)(?:\.|,|;)',
    ]

    for pattern in jurisdiction_patterns:

        match = re.search(
            pattern,
            clean_text,
            re.IGNORECASE
        )

        if match:
            result["jurisdiction"] = match.group(1).strip()
            break

    # =========================================
    # CONTRACT DURATION
    # =========================================

    duration_patterns = [
        r'term of this agreement shall be (\d+\s+(?:year|years|month|months|day|days))',
        r'term of the agreement shall be (\d+\s+(?:year|years|month|months|day|days))',
        r'this agreement shall remain in effect for (\d+\s+(?:year|years|month|months|day|days))',
        r'agreement shall remain in force for (\d+\s+(?:year|years|month|months|day|days))',
        r'term shall be (\d+\s+(?:year|years|month|months|day|days))',
        r'for a period of (\d+\s+(?:year|years|month|months|day|days))',
        r'for (\d+\s+(?:year|years|month|months|day|days))',
    ]

    for pattern in duration_patterns:

        match = re.search(
            pattern,
            clean_text,
            re.IGNORECASE
        )

        if match:
            result["duration"] = match.group(1).strip()
            break

    return result