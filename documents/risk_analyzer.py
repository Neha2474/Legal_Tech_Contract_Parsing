import re

RISK_KEYWORDS = {
    "indemnify": {
        "risk": "High",
        "reason": "Indemnification may create financial obligations for the party."
    },

    "indemnification": {
        "risk": "High",
        "reason": "Indemnification obligations may expose a party to financial claims."
    },

    "unlimited liability": {
        "risk": "High",
        "reason": "Unlimited liability may expose a party to uncapped financial losses."
    },

    "penalty": {
        "risk": "High",
        "reason": "Penalty provisions may create additional financial obligations."
    },

    "non-compete": {
        "risk": "High",
        "reason": "A non-compete clause may restrict future business activities."
    },

    "termination": {
        "risk": "Medium",
        "reason": "Termination conditions may affect the ability to end the agreement."
    },

    "confidentiality": {
        "keywords": [
            "confidentiality",
            "confidential",
            "confidential information"
        ],
        "risk": "Medium",
        "reason": "Confidentiality obligations may restrict the use or disclosure of information."
        },

    "exclusive": {
        "risk": "Medium",
        "reason": "An exclusivity clause may restrict the party from working with others."
    },

    "intellectual property": {
        "risk": "Medium",
        "reason": "Intellectual property provisions may affect ownership or usage rights."
    },

    "arbitration": {
        "risk": "Medium",
        "reason": "Arbitration provisions determine how disputes are resolved outside court."
    },

    "force majeure": {
        "risk": "Low",
        "reason": "Force majeure provisions define responsibilities when extraordinary events occur."
    }
}

def analyze_risks(text):

    risks = []

    if not text:
        return risks

    # Split document into sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)

    seen = set()

    for sentence in sentences:

        sentence = sentence.strip()

        if not sentence:
            continue

        sentence = re.sub(r'\s+', ' ', sentence).strip()

        sentence_lower = sentence.lower()

        for keyword, details in RISK_KEYWORDS.items():

            if re.search(
                r'\b' + re.escape(keyword) + r'\b',
                sentence_lower
            ):

                unique_key = (
                    keyword.lower(),
                    sentence_lower
                )

                if unique_key in seen:
                    continue

                seen.add(unique_key)

                highlighted_clause = re.sub(
                    r'\b' + re.escape(keyword) + r'\b',
                    f'[{keyword.upper()}]',
                    sentence,
                    flags=re.IGNORECASE
                )

                risks.append({
                    "keyword": keyword,
                    "risk": details["risk"],
                    "reason": details["reason"],
                    "clause": sentence,
                    "highlighted_clause": highlighted_clause
                })

    return risks


def summarize_risks(risks):

    summary = {
        "total": len(risks),
        "high": 0,
        "medium": 0,
        "low": 0
    }

    for risk in risks:

        if risk["risk"] == "High":
            summary["high"] += 1

        elif risk["risk"] == "Medium":
            summary["medium"] += 1

        elif risk["risk"] == "Low":
            summary["low"] += 1

    return summary




def calculate_risk_score(risks):

    score = 0

    for risk in risks:

        if risk["risk"] == "High":
            score += 20

        elif risk["risk"] == "Medium":
            score += 10

        elif risk["risk"] == "Low":
            score += 5

    # Maximum score
    if score > 100:
        score = 100

    # Determine overall risk level
    if score >= 70:
        level = "High"

    elif score >= 40:
        level = "Medium"

    else:
        level = "Low"

    return {
        "score": score,
        "level": level
    }