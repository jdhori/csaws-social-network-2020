"""Single source of truth for the accessible CSaWS Social Network brief.

Every deliverable (Markdown, HTML, PDF) is generated from the data below so the
three formats can never drift apart. Content is a FAITHFUL transcription of the
original infographic:

    "Concerns About Violence Within Social Networks: Results from the 2020
     California Safety and Wellbeing Survey (CSaWS)"
    California Firearm Violence Research Center, UC Davis Health. January 2023.

NON-NEGOTIABLE: do not fabricate, modernize, or "correct" any figure. Pie/donut
percentages are transcribed exactly as printed (they may not sum to 100% due to
rounding and non-responses, per the source's own footnote). The two horizontal
bar charts on page 2 carry NO numeric labels in the source -- only a 0-50% axis
-- so they are represented as ordered categories with a relative-magnitude
description and an explicit "exact percentages not labeled in source" note. No
numbers are invented for them.
"""

# ---------------------------------------------------------------------------
# Document-level metadata
# ---------------------------------------------------------------------------

META = {
    "title": "Concerns About Violence Within Social Networks",
    "subtitle": "Results from the 2020 California Safety and Wellbeing Survey (CSaWS)",
    "date": "January 2023",
    "publisher": "California Firearm Violence Research Center, UC Davis Health",
    "lang": "en",
    "description": (
        "Accessible (WCAG 2.1 AA) digital edition of the UC Davis California "
        "Firearm Violence Research Center research brief summarizing the 2020 "
        "California Safety and Wellbeing Survey findings on anticipatory "
        "concerns about violence within social networks."
    ),
    "keywords": (
        "CSaWS, California Safety and Wellbeing Survey, violence prevention, "
        "firearm violence, self-directed violence, social networks, UC Davis, "
        "public health, accessibility"
    ),
    # Recommended citation for the underlying peer-reviewed study.
    "citation": (
        "Aubel AJ, Wintemute GJ, Kravitz-Wirtz N. Anticipatory concerns about "
        "violence within social networks: prevalence and implications for "
        "prevention. Prev. Med. 2023;167:107421."
    ),
    "doi": "10.1016/j.ypmed.2023.107421",
    "doi_url": "https://doi.org/10.1016/j.ypmed.2023.107421",
    "pmid": "36641127",
    "study_url": "https://www.sciencedirect.com/science/article/pii/S0091743523000014",
    "center_url": "https://health.ucdavis.edu/vprp/ucfc",
    "center_email": "hs-vprp@ucdavis.edu",
}

# Headline question and top-line statistic (page 1).
QUESTION = (
    'We asked California adults, "Are you concerned that anyone you know might '
    'physically hurt [another person/themselves] on purpose?"'
)

HEADLINE = {
    "stat": "1 in 5",
    "detail": (
        "respondents (22%) reported knowing someone at perceived risk of "
        "hurting others or themselves."
    ),
}

# Footnotes printed on page 1.
FOOTNOTES = [
    'Nonbinary includes any gender other than "male" or "female."',
    "Percentages may not sum to 100% due to rounding and non-responses.",
]

# ---------------------------------------------------------------------------
# Pie-chart data (page 1). Values are exact as printed.
# Each entry: (label, percent). "nb_note" marks the nonbinary footnote target.
# ---------------------------------------------------------------------------

# Persons at perceived risk of OTHER-directed violence were described as...
OTHER_RELATIONSHIP = [
    ("Friend", 32),
    ("Neighbor, coworker, or other", 25),
    ("Other close family member", 22),
    ("Spouse or intimate partner", 7),
    ("Parent or stepparent", 6),
    ("Child or stepchild", 6),
]
OTHER_GENDER = [
    ("Male", 74),
    ("Female", 20),
    ("Nonbinary", 2),  # see footnote 1
]
OTHER_AGE = [
    ("0-19 years", 11),
    ("20-29 years", 15),
    ("30-39 years", 22),
    ("40-49 years", 26),
    ("50-59 years", 13),
    ("60+ years", 10),
]
OTHER_CALLOUTS = ["32% friends", "74% male", "26% are 40-49 years old"]

# Persons at perceived risk of SELF-directed violence were described as...
SELF_RELATIONSHIP = [
    ("Friend", 33),
    ("Other close family member", 19),
    ("Neighbor, coworker, or other", 17),
    ("Child or stepchild", 16),
    ("Spouse or intimate partner", 7),
    ("Parent or stepparent", 6),
]
SELF_GENDER = [
    ("Male", 47),
    ("Female", 47),
    ("Nonbinary", 2),  # see footnote 1
]
SELF_AGE = [
    ("0-19 years", 16),
    ("20-29 years", 28),
    ("30-39 years", 19),
    ("40-49 years", 13),
    ("50-59 years", 11),
    ("60+ years", 10),
]
SELF_CALLOUTS = ["33% friends", "47% male", "28% are 20-29 years old"]

# Likelihood of harm in the next year (page 1, bottom).
LIKELIHOOD = [
    {
        "percent": "27%",
        "text": (
            "of respondents said it was likely or very likely the person will "
            "hurt another person in the next year."
        ),
    },
    {
        "percent": "22%",
        "text": (
            "of respondents said it was likely or very likely the person will "
            "hurt themselves in the next year."
        ),
    },
]

# ---------------------------------------------------------------------------
# Page 2 data
# ---------------------------------------------------------------------------

# Reasons for concern -- bar chart WITHOUT numeric labels in the source.
# Ordered top-to-bottom exactly as printed. The "relative" string describes the
# visible bar lengths qualitatively; NO exact percentages are claimed.
REASONS_CONCERN = {
    "title": "Respondents were concerned about violence because the person has...",
    "axis_note": "Source bars run on a 0%-50% axis with no numeric labels.",
    "rows": [
        # (category, other-directed relative, self-directed relative)
        ("Trouble with alcohol or drugs", "highest", "moderate"),
        ("Hurt someone else before", "high", "low"),
        ("Hurt themselves before", "low", "highest"),
        ("Talked about violence or made threats", "moderate", "moderate"),
        ("Suffered a major loss", "low-moderate", "high"),
    ],
}

# Donut statistics: took 1+ action.
ACTION_TAKEN = [
    {
        "percent": "67%",
        "text": (
            "of respondents who knew someone at perceived risk of "
            "other-directed violence took one or more actions to reduce their "
            "own risk of being hurt by the person."
        ),
    },
    {
        "percent": "85%",
        "text": (
            "of respondents who knew someone at perceived risk of self-directed "
            "violence took one or more actions to reduce the risk of the person "
            "hurting themselves."
        ),
    },
]

# Reasons for inaction -- bar chart WITHOUT numeric labels in the source.
REASONS_INACTION = {
    "title": "Some respondents didn't take action because...",
    "axis_note": "Source bars run on a 0%-50% axis with no numeric labels.",
    "rows": [
        ("Dangerous situation didn't seem likely", "high", "highest"),
        ("Seemed like a personal matter", "moderate", "high"),
        ("Didn't think their actions would help", "low", "moderate"),
        ("Thought it might make the situation worse", "low", "moderate"),
    ],
}

# Firearm-access callout.
FIREARMS = (
    "1 in 5 persons at perceived risk to others and 1 in 10 persons at "
    "perceived risk to themselves have access to firearms."
)

# "What we learned" takeaways.
TAKEAWAYS = [
    (
        "An estimated 6.5 million Californians -- 1 in 5 adults -- are concerned "
        "someone they know, usually a friend or family member, is at risk of "
        "violence to others or themselves."
    ),
    (
        "The ability to identify when someone is behaving dangerously or "
        "exhibiting warning signs is an important component of violence "
        "prevention efforts."
    ),
    (
        "Access to firearms is common among persons at perceived risk of "
        "violence, though taking action to reduce this access was rare."
    ),
    (
        "Continued efforts to empower the public, especially those close to "
        "people at elevated risk, to act on their knowledge about risk factors "
        "for violence are needed."
    ),
]

# Survey methodology box.
METHODOLOGY = (
    "The California Safety and Wellbeing Survey (CSaWS) is an ongoing, "
    "statewide, probability-based Internet survey developed by the California "
    "Firearm Violence Research Center and administered by the research firm "
    "Ipsos. CSaWS asks questions on a wide range of topics related to firearm "
    "ownership and exposure to violence and its consequences. More than 2,500 "
    "California adults participate in CSaWS at each wave, and their answers are "
    "weighted to be statistically representative of the adult population of the "
    "state. The 2020 wave of CSaWS was administered from July 14-27, 2020, with "
    "funding from the State of California."
)

DISCLAIMER = (
    "The California Firearm Violence Research Center is housed at the UC Davis "
    "Violence Prevention Research Program. For more information, visit "
    "health.ucdavis.edu/vprp/ucfc or send an email to hs-vprp@ucdavis.edu. This "
    "content is solely the responsibility of the study's authors and does not "
    "necessarily represent the views of the California Firearm Violence "
    "Research Center."
)

# Clearly-labeled editorial addition (NOT part of the original infographic).
# Responsible inclusion for a public, self-harm-related resource.
EDITOR_NOTE = {
    "heading": "About this accessible edition",
    "body": (
        "This is a faithful, accessible (WCAG 2.1 AA) digital re-creation of a "
        "two-page infographic published by the California Firearm Violence "
        "Research Center at UC Davis Health. All survey figures are transcribed "
        "exactly as printed in the original. The two reasons-related bar charts "
        "in the original carry no numeric labels, so they are presented here as "
        "ordered categories with a relative-magnitude description rather than "
        "invented percentages. This edition is not affiliated with or endorsed "
        "by UC Davis."
    ),
    "crisis": (
        "If you or someone you know is in crisis, call or text 988 (the U.S. "
        "Suicide and Crisis Lifeline), available 24/7. In an emergency, call "
        "911. This crisis resource is added by this accessible edition and was "
        "not part of the original infographic."
    ),
}
