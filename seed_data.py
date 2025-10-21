from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://admin:Dasun%402013@cluster01.dusr25j.mongodb.net/?retryWrites=true&w=majority&appName=Cluster01")
client = MongoClient(MONGO_URI)
db = client["citizen_portal"]

services_col = db["services"]
categories_col = db["categories"]
officers_col = db["officers"]
ads_col = db["ads"]

# Clear existing data
services_col.delete_many({})
categories_col.delete_many({})
officers_col.delete_many({})
ads_col.delete_many({})

# Create categories
categories = [
    {
        "id": "cat_it",
        "name": {"en": "IT & Digital Affairs", "si": "තොරතුරු තාක්ෂණ", "ta": "தகவல் தொழில்நுட்ப"},
        "ministry_ids": ["ministry_it"]
    },
    {
        "id": "cat_education",
        "name": {"en": "Education", "si": "අධ්යාපනය", "ta": "கல்வி"},
        "ministry_ids": ["ministry_education"]
    },
    {
        "id": "cat_health",
        "name": {"en": "Health & Wellness", "si": "සෞඛ්යය", "ta": "சுகாதாரம்"},
        "ministry_ids": ["ministry_health"]
    },
    {
        "id": "cat_transport",
        "name": {"en": "Transport", "si": "ප්‍රවහනය", "ta": "போக்குவரத்து"},
        "ministry_ids": ["ministry_transport"]
    },
    {
        "id": "cat_finance",
        "name": {"en": "Finance & Tax", "si": "මූල්‍යය", "ta": "நிதி"},
        "ministry_ids": ["ministry_finance"]
    },
    {
        "id": "cat_housing",
        "name": {"en": "Housing & Land", "si": "නිවාස", "ta": "வீடுகள்"},
        "ministry_ids": ["ministry_housing"]
    },
]

categories_col.insert_many(categories)

# Create sample officers
officers = [
    {
        "id": "off_it_01",
        "name": "Ms. Nayana Perera",
        "role": "Director - Digital Services",
        "ministry_id": "ministry_it",
        "contact": {"email": "nayana@it.gov.lk", "phone": "011-2345678"}
    },
    {
        "id": "off_education_01",
        "name": "Mr. Ruwan Silva",
        "role": "Assistant Secretary - Education",
        "ministry_id": "ministry_education",
        "contact": {"email": "ruwan@edu.gov.lk", "phone": "011-9876543"}
    },
    {
        "id": "off_health_01",
        "name": "Dr. Lakshmi Jayasinghe",
        "role": "Director - Public Health",
        "ministry_id": "ministry_health",
        "contact": {"email": "lakshmi@health.gov.lk", "phone": "011-5555555"}
    },
]

officers_col.insert_many(officers)

# Create sample ads
ads = [
    {
        "id": "ad_digital_skills",
        "title": "Free Digital Skills Course",
        "body": "Enroll now in government-approved digital skills training. Limited seats available.",
        "link": "https://example.com/digital-skills",
        "image": "/static/img/course-card.png"
    },
    {
        "id": "ad_passport",
        "title": "Fast-Track Passport Service",
        "body": "Apply online and get your passport in 3 days.",
        "link": "https://example.com/passport",
        "image": "/static/img/passport.png"
    },
    {
        "id": "ad_education",
        "title": "Exam Results Available",
        "body": "Check your exam results on the official education portal.",
        "link": "https://example.com/results",
        "image": "/static/img/exam-results.png"
    },
    {
        "id": "ad_health",
        "title": "Free Health Checkup Camp",
        "body": "Free medical checkup every Saturday at your nearest health center.",
        "link": "https://example.com/health-camp",
        "image": "/static/img/health.png"
    },
]

ads_col.insert_many(ads)

# Create sample services with categories
docs = [
    {
        "id": "ministry_it",
        "category": "cat_it",
        "name": {"en": "Ministry of IT & Digital Affairs", "si": "තොරතුරු තාක්ෂණ අමාත්‍යංශය", "ta": "தகவல் தொழில்நுட்ப அமைச்சு"},
        "subservices": [
            {
                "id": "it_cert",
                "name": {"en": "IT Certificates", "si": "අයිටී සහතික", "ta": "ஐடி சான்றிதழ்"},
                "questions": [
                    {
                        "q": {"en": "How to apply for an IT certificate?", "si": "IT සහතිකය සඳහා ඉල්ලීම් කරන ආකාරය?", "ta": "ஐடி சான்றிதழுக்கு விண்ணப்பிப்பது எப்படி?"},
                        "answer": {"en": "Fill the online form and upload your NIC. Processing takes 5-7 business days.", "si": "ඔන්ලයින් ෆෝරම පිරවා NIC උඩුග කරන්න.", "ta": "ஆன்லைன் படிவத்தை நிரப்பி NIC ஐ பதிவேற்றவும்."},
                        "downloads": ["/static/forms/it_cert_form.pdf"],
                        "location": "https://maps.google.com/?q=Ministry+of+IT+Colombo",
                        "instructions": "Visit the digital portal at https://example.com, register and submit your application."
                    },
                    {
                        "q": {"en": "What documents are required?", "si": "මොන ලේඛන අවශ්‍යද?", "ta": "என்ன ஆவணங்கள் தேவை?"},
                        "answer": {"en": "NIC, educational certificates, and proof of residence.", "si": "NIC, අධ්යාපන සහතිකෙ, සහ නිවාස තහවුරු කිරීම.", "ta": "NIC, கல்வி சான்றிதழ்கள், வாழ்விட நிரூபணம்."},
                        "downloads": [],
                        "location": "",
                        "instructions": "All documents must be in PDF format."
                    }
                ]
            },
            {
                "id": "digital_services",
                "name": {"en": "Digital Services", "si": "ඩිජිටල් සේවා", "ta": "டிஜிட்டல் சேவைகள்"},
                "questions": [
                    {
                        "q": {"en": "How to access government e-services?", "si": "රජයේ ඉ-සේවා ප්‍රවේශ කරන ආකාරය?", "ta": "அரசு இ-சேவைகளை எப்படி அணுகுவது?"},
                        "answer": {"en": "Visit the portal at https://services.gov.lk and login with your digital ID.", "si": "https://services.gov.lk ට යන්න ඔබේ ඩිජිටල් හැඳුනුම්පතින් ලිපිනි ගිණුම ඉවත් කරන්න.", "ta": "https://services.gov.lk ஐ பார்வையிடவும் மற்றும் உங்கள் டிஜிட்டல் ID ஆல் உள்நுழையவும்."},
                        "downloads": ["/static/guides/e-services-guide.pdf"],
                        "location": "https://maps.google.com/?q=IT+Ministry+Services+Center",
                        "instructions": "First-time users need to register with their NIC."
                    }
                ]
            }
        ]
    },
    {
        "id": "ministry_education",
        "category": "cat_education",
        "name": {"en": "Ministry of Education", "si": "අධ්‍යාපන අමාත්‍යංශය", "ta": "கல்வி அமைச்சு"},
        "subservices": [
            {
                "id": "schools",
                "name": {"en": "Schools", "si": "පාසල්ල", "ta": "பள்ளிகள்"},
                "questions": [
                    {
                        "q": {"en": "How to register a school?", "si": "පාසලක් ලියා දාංචි කරන ආකාරය?", "ta": "பள்ளியை பதிவு செய்வது எப்படி?"},
                        "answer": {"en": "Complete registration form and submit documents to the Ministry.", "si": "ලියා දාංචි ෆෝරමය පුරවා අමාත්‍යංශයට ලේඛන ඉදිරිපත් කරන්න.", "ta": "பதிவு படிவத்தை பூர්த்தி செய்து அமைச்சுக்கு ஆவணங்களை சமர්ப்பிக்கவும்."},
                        "downloads": ["/static/forms/school_reg.pdf"],
                        "location": "https://maps.google.com/?q=Ministry+of+Education+Colombo",
                        "instructions": "Processing time is 30 days."
                    }
                ]
            },
            {
                "id": "exams",
                "name": {"en": "Exams & Results", "si": "විභාග & ප්‍රතිඵල", "ta": "பரீட்சைகள் மற்றும் முடிவுகள்"},
                "questions": [
                    {
                        "q": {"en": "How to check exam results?", "si": "විභාගයේ ප්‍රතිඵල පිරික්සා කරන ආකාරය?", "ta": "பரीட்சை முடிவுகளை எப்படி சரிபார்க்கலாம்?"},
                        "answer": {"en": "Visit results.moe.gov.lk and enter your registration number.", "si": "results.moe.gov.lk ට යන්න ඔබේ ලියා දාංචි අංකය ඇතුළත් කරන්න.", "ta": "results.moe.gov.lk ஐ பார்வையிடவும் மற்றும் உங்கள் பதிவு எண்ணை உள்ளிடவும்."},
                        "downloads": [],
                        "location": "",
                        "instructions": "Results are released 6 weeks after the exam."
                    }
                ]
            }
        ]
    },
    {
        "id": "ministry_health",
        "category": "cat_health",
        "name": {"en": "Ministry of Health", "si": "සෞඛ්‍ය අමාත්‍යංශය", "ta": "சுகாதார அமைச்சு"},
        "subservices": [
            {
                "id": "health_services",
                "name": {"en": "Health Services", "si": "සෞඛ්‍ය සේවා", "ta": "சுகாதார சேவைகள்"},
                "questions": [
                    {
                        "q": {"en": "How to register at a health center?", "si": "සෞඛ්‍ය කේන්දරයට ලියා දාංචි කරන ආකාරය?", "ta": "சுகாதார நிலையத்தில் பதிவு செய்வது எப்படி?"},
                        "answer": {"en": "Visit your nearest health center with NIC and proof of address.", "si": "ඔබේ ළඟම සෞඛ්‍ය කේන්දරයට NIC සහ ලිපිනි තහවුරු සමග යන්න.", "ta": "உங்கள் அருகிலுள்ள சுகாதார நிலையத்ைஐ NIC மற்றும் முகவரி ஆதாரத்துடன் பார்வையிடவும்."},
                        "downloads": ["/static/forms/health_reg.pdf"],
                        "location": "https://maps.google.com/?q=Health+Centers+Near+Me",
                        "instructions": "Registration is free and can be completed in 15 minutes."
                    }
                ]
            }
        ]
    },
]

services_col.insert_many(docs)

print("✅ Seed complete!")
print(f"   Categories: {categories_col.count_documents({})}")
print(f"   Officers: {officers_col.count_documents({})}")
print(f"   Ads: {ads_col.count_documents({})}")
print(f"   Services: {services_col.count_documents({})}")