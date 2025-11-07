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
        "name": {"en": "Education", "si": "අධ්‍යාපනය", "ta": "கல்வி"},
        "ministry_ids": ["ministry_education"]
    },
    {
        "id": "cat_health",
        "name": {"en": "Health & Wellness", "si": "සෞඛ්‍යය", "ta": "சுகாதாரம்"},
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
    {
        "id": "off_transport_01",
        "name": "Mr. Chamara Fernando",
        "role": "Director - Transport Services",
        "ministry_id": "ministry_transport",
        "contact": {"email": "chamara@transport.gov.lk", "phone": "011-2223333"}
    },
    {
        "id": "off_finance_01",
        "name": "Ms. Anusha Jayawardena",
        "role": "Deputy Secretary - Finance",
        "ministry_id": "ministry_finance",
        "contact": {"email": "anusha@finance.gov.lk", "phone": "011-4446666"}
    },
    {
        "id": "off_housing_01",
        "name": "Mr. Sunil Rathnayake",
        "role": "Director - Housing & Land",
        "ministry_id": "ministry_housing",
        "contact": {"email": "sunil@housing.gov.lk", "phone": "011-7778888"}
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

# Create sample services with 6 ministries and 4 subservices each (detailed - 2-3 Q&A per subservice)
services = [
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
                        "answer": {"en": "Fill the online form and upload your NIC. Processing takes 5-7 business days.", "si": "ඔන්ලයින් ෆෝරම පිරවා NIC උඩුග කරන්න. සකස් කිරීම දින 5-7ක් ගැනේ.", "ta": "ஆன்லைன் படிவத்தை நிரப்பி NIC ஐ பதிவேற்றவும். செயலாக்கம் 5-7 வணிக நாட்கள் எடுக்கும்."},
                        "downloads": ["/static/forms/it_cert_form.pdf"],
                        "location": "https://maps.google.com/?q=Ministry+of+IT+Colombo",
                        "instructions": "Visit the digital portal at https://example.com, register and submit your application."
                    },
                    {
                        "q": {"en": "What documents are required?", "si": "මොන ලේඛන අවශ්‍යද?", "ta": "என்ன ஆவணங்கள் தேவை?"},
                        "answer": {"en": "NIC, educational certificates, and proof of residence.", "si": "NIC, අධ්යාපන සහතික, සහ නිවාස තහවුරු කිරීම.", "ta": "NIC, கல்வி சான்றிதழ்கள் மற்றும் வாழ்விட ஆதாரம்."},
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
                        "answer": {"en": "Visit the portal at https://services.gov.lk and login with your digital ID.", "si": "https://services.gov.lk ට යන්න ඔබේ ඩිජිටල් හැඳුනුම්පතෙන් පිවිසෙන්න.", "ta": "https://services.gov.lk ஐ பார்வையிடவும் மற்றும் உங்கள் டிஜிட்டல் ID ஆல் உள்நுழையவும்."},
                        "downloads": ["/static/guides/e-services-guide.pdf"],
                        "location": "https://maps.google.com/?q=IT+Ministry+Services+Center",
                        "instructions": "First-time users need to register with their NIC."
                    },
                    {
                        "q": {"en": "How to report a portal issue?", "si": "පෝටලයේ ගැටලුවක් כיצד වාර්තා කරන්න?", "ta": "போர்டல் பிரச்சனையை எப்படி رپورٹ செய்வது?"},
                        "answer": {"en": "Use the 'Report Issue' link on the portal or email support@services.gov.lk.", "si": "පෝටලයේ 'ගැටලුව වාර්තා කරන්න' සබැඳිය භාවිතා කරන්න හෝ support@services.gov.lk වෙත ඊමේල් කරන්න.", "ta": "போர்டலில் 'பிரச்சனை அறிக்கை' இணைப்பை பயன்படுத்தவும் அல்லது support@services.gov.lk க்கு மின்னஞ்சல் அனுப்பவும்."},
                        "downloads": [],
                        "location": "",
                        "instructions": "Attach screenshots and steps to reproduce the issue."
                    }
                ]
            },
            {
                "id": "open_data",
                "name": {"en": "Open Data & APIs", "si": "විවෘත දත්ත සහ API", "ta": "திறந்த தரவுகள் மற்றும் API"},
                "questions": [
                    {
                        "q": {"en": "How to request API access?", "si": "API ප්‍රවේශය සඳහා ඉල්ලීම් කරන ආකාරය?", "ta": "API அணுகலைどうように கோருவது?"},
                        "answer": {"en": "Complete the API access form and provide a project description; approvals take up to 10 working days.", "si": "API ප්‍රවේශ ෆෝරමය පුරවා ව්‍යාපෘති විස්තරයක් සපයන්න; අනුමැතිය දින 10 ක් ගත විය හැක.", "ta": "API அணுகல் படிவத்தை நிரப்பி திட்ட விவரத்தை வழங்கவும்; அனுமதி 10 வேலை நாட்கள் வரை ஆகும்."},
                        "downloads": ["/static/forms/api_access_form.pdf"],
                        "location": "https://maps.google.com/?q=Data+Center+Colombo",
                        "instructions": "Provide an example use-case and contact email."
                    },
                    {
                        "q": {"en": "Are datasets free to use?", "si": "දත්ත සමුදා නොමිලේ භාවිතා කළ හැකිද?", "ta": "தரவுத்தொகுப்புகள் இலவசமாகப் பயன்படுத்த முடியுமா?"},
                        "answer": {"en": "Most datasets are open under the national open data policy; check the license on each dataset.", "si": "අधिक භාග දත්ත විවෘත ප්‍රතිපත්තිය යටතේ ඇත; සෑම දත්ත සමුදායකුම හිමිකම පරීක්ෂා කරන්න.", "ta": "அதிகமான தரவுத்தொகுப்புகள் தேசிய திறந்த தரவு கொள்கையின் கீழ் திறந்தவையாக உள்ளன; ஒவ்வொரு தொகுப்பும் உரிமம் பார்க்கவும்."},
                        "downloads": [],
                        "location": "",
                        "instructions": "Cite the dataset ID when reusing."
                    }
                ]
            },
            {
                "id": "cyber_security",
                "name": {"en": "Cyber Security", "si": "සයිබර් ආරක්ෂාව", "ta": "சைபர் பாதுகாப்பு"},
                "questions": [
                    {
                        "q": {"en": "How to report a cyber incident?", "si": "සයිබර් සිදුවීමක් වාර්තා කරන ආකාරය?", "ta": "சைபர் நிகழ்வை எப்படி அறிக்கை செய்யலாம்?"},
                        "answer": {"en": "Contact the national CERT via cert@it.gov.lk and provide logs and incident time.", "si": "ජාතික CERT වෙත cert@it.gov.lk ට අමතන්න සහ ලොග් සහ සිදුවීමේ වේලාව ලබා දෙන්න.", "ta": "தேசிய CERT ஐ cert@it.gov.lk மூலம் தொடர்பு கொண்டு பதிவு மற்றும் நிகழ்வு நேரம் வழங்கவும்."},
                        "downloads": ["/static/guides/cyber_incident_checklist.pdf"],
                        "location": "",
                        "instructions": "Preserve logs and avoid powering off affected devices."
                    },
                    {
                        "q": {"en": "Where to get cybersecurity training?", "si": "සයිබර් ආරක්ෂක පුහුණුවක් ලබා ගැනීමට කොහෙන්ද?", "ta": "சைபர் பாதுகாப்பு பயிற்சியை எங்கு பெறலாம்?"},
                        "answer": {"en": "See the trainings page on the ministry portal; scholarships are available for small businesses.", "si": "අමාත්‍යාංශයේ පුහුණු පිටුව බලන්න; කුඩා ව්‍යාපාර සඳහා ශිෂ්‍යත්ව ලබා ගත හැක.", "ta": "அமைச்சரகத்தின் பயிற்சி பக்கத்தைப் பார்க்கவும்; சிறிய நிறுவனங்களுக்கு உதவித் தொகைகள் கிட்டும்."},
                        "downloads": [],
                        "location": "",
                        "instructions": "Apply through the training portal."
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
                "name": {"en": "Schools", "si": "පාසල", "ta": "பள்ளிகள்"},
                "questions": [
                    {
                        "q": {"en": "How to register a school?", "si": "පාසලක් ලියා දාංචි කරන ආකාරය?", "ta": "பள்ளியை பதிவு செய்வது எப்படி?"},
                        "answer": {"en": "Complete registration form and submit documents to the Ministry. Processing time is 30 days.", "si": "ලියා දාංචි ෆෝරමය පුරවා අමාත්‍යංශයට ලේඛන ඉදිරිපත් කරන්න. සැකසීම 30 දිනක් ගතවේ.", "ta": "பதிவு படிவத்தை பூர்த்தி செய்து அமைச்சிற்கு ஆவணங்களை சமர்ப்பிக்கவும். செயலாக்கம் 30 நாட்கள் எடுக்கும்."},
                        "downloads": ["/static/forms/school_reg.pdf"],
                        "location": "https://maps.google.com/?q=Ministry+of+Education+Colombo",
                        "instructions": "Attach school layout, principal NIC copy and approval letters."
                    },
                    {
                        "q": {"en": "How to apply for teacher certification?", "si": "ගුරුවරයාගේ සහතික සඳහා කිසිසේද?", "ta": "பள்ளி ஆசிரியர் சான்றிதழுக்கு எப்படி விண்ணப்பிப்பது?"},
                        "answer": {"en": "Submit teaching qualifications, experience letters and complete the online application.", "si": "ගුරුවරුන්ගේ සුදුසුකම්, පළපුරුදු ලිපි සහ ඔන්ලයින් යටතේ ඉල්ලීම් පුරවන්න.", "ta": "கற்பித்தல் தகுதிகள், அனுபவக் கடிதங்கள் மற்றும் ஆன்லைன் விண்ணப்பத்தைப் பூர்த்திசெய்யவும்."},
                        "downloads": ["/static/forms/teacher_cert.pdf"],
                        "location": "",
                        "instructions": "Original certificates may be requested for verification."
                    }
                ]
            },
            {
                "id": "exams",
                "name": {"en": "Exams & Results", "si": "විභාග & ප්‍රතිඵල", "ta": "பரீட்சைகள் மற்றும் முடிவுகள்"},
                "questions": [
                    {
                        "q": {"en": "How to check exam results?", "si": "විභාගයේ ප්‍රතිඵල පිරික්සා කරන ආකාරය?", "ta": "பரீட்சை முடிவுகளை எப்படி சரிபார்க்கலாம்?"},
                        "answer": {"en": "Visit results.moe.gov.lk and enter your registration number. Results are released 6 weeks after the exam.", "si": "results.moe.gov.lk ට යන්න ඔබේ ලියා දාංචි අංකය ඇතුළත් කරන්න. ප්‍රතිඵල 6 සතියක් පසු නිකුතු වේ.", "ta": "results.moe.gov.lk ஐ பார்வையிடவும் மற்றும் உங்கள் பதிவு எண்ணை உள்ளிடவும். முடிவுகள் தேர்வுக்கு 6 வாரங்களுக்கு பிறகு வெளியிடப்படுகின்றன."},
                        "downloads": [],
                        "location": "",
                        "instructions": "Keep your registration number safe for checking."
                    },
                    {
                        "q": {"en": "How to appeal a result?", "si": "ප්‍රතිඵලයට ආරෝපණයක් ද?</", "ta": "முடிவுக்கு இடைத்தேர்வு செய்ய எப்படி?"},
                        "answer": {"en": "Submit an appeal form within 14 days with required documents and payment of fee.", "si": "අභියාචනා ෆෝරමය 14 දින ඇතුළත ඉදිරිපත් කරන්න.", "ta": "14 நாளுக்குள் தரப்போராட்ட படிவத்தை சமர்ப்பிக்கவும் மற்றும் கட்டணம் செலுத்தவும்."},
                        "downloads": ["/static/forms/result_appeal.pdf"],
                        "location": "",
                        "instructions": "Provide a copy of the original question paper if requested."
                    }
                ]
            },
            {
                "id": "scholarships",
                "name": {"en": "Scholarships & Grants", "si": "ශිෂ්යත්ව සහ ප්‍රතිලාභ", "ta": "பாலிடிகள் மற்றும் உதவித்தொகைகள்"},
                "questions": [
                    {
                        "q": {"en": "Who is eligible for scholarships?", "si": "ශිෂ්යත්ව සඳහා කවුද සුදුසු?", "ta": "பலிடிகளுக்கு யார் தகுதியானவர்கள்?"},
                        "answer": {"en": "Eligibility varies by program; most require academic merit and income proof.", "si": "සාමාන්‍යයෙන් අධ්යාපනිකසුදුසුකම සහ ආදායම් සාධක අවශ්‍ය වේ.", "ta": "பின்னணிக்கேற்ப தகுதியும் வருமான சான்றும் தேவையாக இருக்கும்."},
                        "downloads": ["/static/forms/scholarship_app.pdf"],
                        "location": "",
                        "instructions": "Submit documents before the scholarship closing date."
                    },
                    {
                        "q": {"en": "How to apply for grants for schools?", "si": "පාසල් සඳහා ප්‍රතිලාභ සඳහා ව්‍යාපෘති ඉදිරිපත් කිරීමට?", "ta": "பள்ளிகளுக்கான உதவித்தொகைகளுக்கு எப்படி விண்ணப்பிப்பது?"},
                        "answer": {"en": "Fill the grant proposal form and attach the school budget and project plan.", "si": "ප්‍රතිලාභ යෝජනා ෆෝරමය පුරවා පාසලේ වියදම් සැලැස්ම සහ ව්‍යාපෘති සැලැස්ම එක් කරන්න.", "ta": "அனுமதிப்பத்திரம் படிவத்தை நிரப்பி பள்ளியின் பட்ஜெட் மற்றும் திட்ட திட்டத்தை இணைக்கவும்."},
                        "downloads": [],
                        "location": "",
                        "instructions": "Proposals are evaluated quarterly."
                    }
                ]
            },
            {
                "id": "adult_education",
                "name": {"en": "Adult Education", "si": "වයස්ගත අධ්‍යාපන", "ta": "வருடம்தான் கல்வி"},
                "questions": [
                    {
                        "q": {"en": "How to enrol in adult learning classes?", "si": "වයසික අධ්‍යාපන පන්ති වලට ලියාපදිංචි වන්නේ කෙසේද?", "ta": "வயதில் கல்வி வகுப்புகளில் எப்படி சேரலாம்?"},
                        "answer": {"en": "Check local community centers or apply online for evening classes.", "si": "ස්ථානීය සමාජ මධ්‍යස්ථාන හරහා හෝ රාත්‍රී පන්ති සඳහා ඔන්ලයින් අයදුම් කරන්න.", "ta": "உள்ளூர் சமூக மையங்களில் அல்லது இரவுப் பயிற்சிகளுக்கு ஆன்லைனில் ஐய்டு செய்யவும்."},
                        "downloads": [],
                        "location": "",
                        "instructions": "Many programs are free or low-cost."
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
                        "answer": {"en": "Visit your nearest health center with NIC and proof of address. Registration is free and can be completed in 15 minutes.", "si": "ඔබේ ළඟම සෞඛ්‍ය කේන්දරයට NIC සහ ලිපිනි තහවුරු සමඟ යන්න. ලියාපදිංචිය නොමිලේ වී මිනිත්තු 15කින් අවසන් වේ.", "ta": "உங்கள் அருகிலுள்ள சுகாதார நிலையத்தை NIC மற்றும் முகவரி ஆதாரத்துடன் பார்வையிடவும். பதிவு இலவசமாக 15 நிமிடங்களில் முடியும்."},
                        "downloads": ["/static/forms/health_reg.pdf"],
                        "location": "https://maps.google.com/?q=Health+Centers+Near+Me",
                        "instructions": "Bring original NIC and a medical referral if you have one."
                    },
                    {
                        "q": {"en": "How to get immunizations for children?", "si": "ළමුන් සදහා එන්නත් ලබා ගන්නේ කෙසේද?", "ta": "குழந்தைகளுக்கு தடுப்பூசிகள் எப்படி பெறுவது?"},
                        "answer": {"en": "Child immunizations are available at any government clinic; bring child health book and NIC of parent.", "si": "ළමයින්ගේ එන්නත් රජයේ කදිම සෞඛ්‍ය කේන්ද්‍රවලදී ලබා ගත හැක; ළමා සෞඛ්‍ය පොත සහ දෙමව්පියගේ NIC ගෙන එන්න.", "ta": "குழந்தைகள் தடுப்பூசி எந்த அரசுத் கிளினிக்கிலும் கிடைக்கும்; குழந்தை சுகாதார புத்தகமும் பெற்றோரின் NIC ஐ கொண்டு வாருங்கள்."},
                        "downloads": [],
                        "location": "",
                        "instructions": "Follow the national immunization schedule."
                    }
                ]
            },
            {
                "id": "mental_health",
                "name": {"en": "Mental Health Services", "si": "මානසික සෞඛ්‍ය සේවා", "ta": "மனநல சேவைகள்"},
                "questions": [
                    {
                        "q": {"en": "How to access counselling services?", "si": "ආයුර්වේද උපදෙස් ලබා ගැනීමට කොහේද?", "ta": "ஆலோசனை சேவைகளை எப்படி அணுகுவது?"},
                        "answer": {"en": "Contact your nearest hospital psychiatric unit or call the mental health helpline.", "si": "ඔබේ ළඟම රෝහල් මානසික ඒකකය හෝ මානසික සෞඛ්‍ය හෙල්ප්ලයින් අමතන්න.", "ta": "உங்கள் அருகிலுள்ள மருத்துவமனை மனவியல் பிரிவை தொடர்பு கொள்ளவோ மனநலம் ஹெல்ப்லைனைக் கால் செய்யவோ செய்யவும்."},
                        "downloads": [],
                        "location": "",
                        "instructions": "If emergency, go to the nearest ER immediately."
                    },
                    {
                        "q": {"en": "Are counselling services free?", "si": "ආයුර්වේද උපදේශන නොමිලේ ද?", "ta": "ஆலோசனை சேவைகள் இலவசமானவைகளா?"},
                        "answer": {"en": "Basic counselling is free at government facilities; specialized therapy may have fees.", "si": "මූලික උපදේශනය රජයේ ආයතනවල නොමිලේ ඇත; විශේෂිත ප්‍රතිකාර සඳහා ගාස්තු තිබිය හැක.", "ta": "அடிப்படை ஆலோசனை அரசு வசதிகளில் இலவசமாக உள்ளது; சிறப்பு சிகிச்சைக்கு கட்டணங்கள் இருக்கலாம்."},
                        "downloads": [],
                        "location": "",
                        "instructions": "Check service details at the local health center."
                    }
                ]
            },
            {
                "id": "public_health_campaigns",
                "name": {"en": "Public Health Campaigns", "si": "ජනාධිපති සෞඛ්‍ය ව්‍යාපෘති", "ta": "பொது சுகாதார பிரச்சாரங்கள்"},
                "questions": [
                    {
                        "q": {"en": "How to find vaccination camps near me?", "si": "මට ළඟම එන්නත් කඳවුරු කොහෙද?", "ta": "என் அருகில் தடுப்பூசி முகாம்களை எங்கு காணலாம்?"},
                        "answer": {"en": "Check the campaigns page on the ministry website or local health office notices.", "si": "අමාත්‍යංශ වෙබ් අඩවියේ ව්‍යාපෘති පිටුව හෝ ප්‍රදේශීය සෞඛ්‍ය කාර්යාල දැන්වීම් පරීක්ෂා කරන්න.", "ta": "அமைச்சரகத்தின் தளம் அல்லது உள்ளூர் சுகாதார அலுவலக அறிவிப்புகளைப் பார்க்கவும்."},
                        "downloads": [],
                        "location": "",
                        "instructions": "Bring ID and follow instructions for mass vaccination days."
                    },
                    {
                        "q": {"en": "How are campaigns scheduled?", "si": "ව්‍යාපෘති қалай සැලසුම් කරනවා?", "ta": "அணுக்கள் எப்படி திட்டமிடப்படுகின்றன?"},
                        "answer": {"en": "Campaigns are scheduled regionally and published on the ministry calendar.", "si": "ව්‍යාපෘති ප්‍රදේශයන් අනුව සැලසුම් කර අතර අමාත්‍යාංශයේ දින දර්ශනයේ ප්‍රකාශ වේ.", "ta": "பிரச்சாரங்கள் பிராந்திய வாரியாக திட்டமிடப்படும் மற்றும் அமைச்சின் காலண்டரில் வெளியிடப்படும்."},
                        "downloads": [],
                        "location": "",
                        "instructions": "Subscribe to SMS alerts for your district."
                    }
                ]
            },
            {
                "id": "medical_records",
                "name": {"en": "Medical Records & Certificates", "si": "වෛද්‍ය වාර්තා සහ සහතික", "ta": "மருத்துவ பதிவுகள் மற்றும் சான்றிதழ்கள்"},
                "questions": [
                    {
                        "q": {"en": "How to get a medical certificate?", "si": "වෛද්‍ය සහතිකයක් ලබා ගැනීමට කෙසේද?", "ta": "மருத்துவ சான்றிதழ் எவ்வாறு பெறுவது?"},
                        "answer": {"en": "Request a medical certificate from the treating hospital; fees may apply for formal letters.", "si": "සංචාරක රෝහලෙන් වෛද්‍ය සහතිකයක් ඉල්ලා ගන්න; නිල ලිපි සඳහා ගාස්තු තිබිය හැක.", "ta": "சிகிச்சை பெற்ற மருத்துவமனையில் இருந்து மருத்துவ சான்றிதழ் கோரவும்; அதிகாரப்பூர்வக் கடிதங்களுக்கு கட்டணம் இருக்கலாம்."},
                        "downloads": ["/static/forms/medical_cert_request.pdf"],
                        "location": "",
                        "instructions": "Provide patient ID and date of visit."
                    }
                ]
            }
        ]
    },
    {
        "id": "ministry_transport",
        "category": "cat_transport",
        "name": {"en": "Ministry of Transport", "si": "ප්‍රවාහන අමාත්‍යංශය", "ta": "போக்குவரத்து அமைச்சு"},
        "subservices": [
            {
                "id": "vehicle_registration",
                "name": {"en": "Vehicle Registration", "si": "වාහන ලියාපදිංචිය", "ta": "வாகன பதிவு"},
                "questions": [
                    {
                        "q": {"en": "How to register a vehicle?", "si": "වාහන ලියාපදිංචි කරන ආකාරය?", "ta": "வாகனத்தை பதிவு செய்வது எப்படி?"},
                        "answer": {"en": "Submit proof of ownership, ID and road-worthiness certificate at the transport office.", "si": "අයිතිය පිළිබඳ සාධක, ID සහ මාර්ගෝපයෝග්‍යතා සහතිකය ප්‍රවාහන කාර්යාලයට ඉදිරිපත් කරන්න.", "ta": "உரிமை சான்று, ID மற்றும் சாலை பயன்பாட்டு சான்றிதழை போக்குவரத்து அலுவகத்திற்கு சமர்ப்பிக்கவும்."},
                        "downloads": ["/static/forms/vehicle_reg.pdf"],
                        "location": "https://maps.google.com/?q=Transport+Office+Colombo",
                        "instructions": "Ensure the vehicle passes the inspection before submission."
                    },
                    {
                        "q": {"en": "How to transfer ownership?", "si": "අයිතිය මාරු කරන ආකාරය?", "ta": "உரிமையை மாற்றம் செய்வது எப்படி?"},
                        "answer": {"en": "Both parties must sign the transfer form and settle any outstanding fines before transfer.", "si": "ඔබත් දෙපාර්ශවයම මාරු ෆෝරමය සමඟ අත්සන් කළයුතු අතර ඉතිරි පලස්ථාන පැහැදිලි කළ යුතුය.", "ta": "இரு தரப்பினரும் மாற்ற படிவத்தில் கையொப்பமிட வேண்டும் மற்றும் நிலுவையில் இருக்கும் அபராதங்கள் தீர்க்கப்பட வேண்டும்."},
                        "downloads": [],
                        "location": "",
                        "instructions": "Bring original registration book and ID copies."
                    }
                ]
            },
            {
                "id": "driver_licence",
                "name": {"en": "Driver Licence", "si": "රියදුරු බලපත්‍රය", "ta": "ஓட்டுநர் உரிமம்"},
                "questions": [
                    {
                        "q": {"en": "How to apply for a driving licence?", "si": "රියදුරු බලපත්‍රයක් සඳහා අයදුම් කරන ආකාරය?", "ta": "ஓட்டுநர் உரிமம் பெற எப்படி விண்ணப்பிக்கலாம்?"},
                        "answer": {"en": "Pass the learner test, complete driving lessons and submit medical and ID documents.", "si": "ලණු ලබන්නාගේ පරීක්ෂාව පිණිස, රියදුරු පාඩම් සම්පුර්ණ කිරීම සහ වෛද්‍ය සහ ID ලේඛන ඉදිරිපත් කරන්න.", "ta": "கற்றலாளர் பரீட்சையில் வெற்றி பெற்று, ஓட்டுநர் பாடங்களை முடித்து மருத்துவம் மற்றும் ID ஆவணங்களை சமர்ப்பிக்கவும்."},
                        "downloads": ["/static/forms/driver_app.pdf"],
                        "location": "",
                        "instructions": "Learner permit valid for 6 months."
                    },
                    {
                        "q": {"en": "How to renew a licence?", "si": "බලපත්‍රය නැවත ලබා ගැනීම?", "ta": "உரிமத்தை புதுப்பிப்பது எப்படி?"},
                        "answer": {"en": "Apply online or at the licensing office before expiry and pay the renewal fee.", "si": "කල් ඉකුත්වීමට පෙර ඔන්ලයින් හෝ බලපත්‍ර කාර්යාලයේදී අයදුම් කර නැව්තැන්ගත ගාස්තුවක් ගෙවන්න.", "ta": "காலாவதியாக்விடுமுன் ஆன்லைன்அல்லது அலுவலகத்தில் விண்ணப்பித்து புதுப்பிப்பு கட்டணத்தை செலுத்தவும்."},
                        "downloads": [],
                        "location": "",
                        "instructions": "Bring current licence and ID."
                    }
                ]
            },
            {
                "id": "public_transport",
                "name": {"en": "Public Transport Services", "si": "ප්‍රජා ප්‍රවාහන සේවා", "ta": "பொது போக்குவரத்து சேவைகள்"},
                "questions": [
                    {
                        "q": {"en": "How to report a bus route issue?", "si": "බස් මාර්ග ගැටලුවක් වාර්තා කරන ආකාරය?", "ta": "பஸ் வழித்தட பிரச்சனையை எப்படி அறிக்கையிடுவது?"},
                        "answer": {"en": "Use the transport complaints portal or call the public transport hotline.", "si": "ප්‍රවාහන පැමිණිලි පෝටලය භාවිතා කරන්න හෝ ජනප්‍රවාහන හෙල්ප්ලයින් අමතන්න.", "ta": "போக்குவரத்து புகார் போர்டலை பயன்படுத்தவும் அல்லது பொது போக்குவரத்து ஹெல்ப்லைனை அழைக்கவும்."},
                        "downloads": [],
                        "location": "",
                        "instructions": "Provide route number, time and vehicle details."
                    },
                    {
                        "q": {"en": "How to get concessions?", "si": "රහිත ගාස්තු ලබා ගැනීමට කොහේද?", "ta": "தள்ளுபடி வசதிகளை எங்கு பெறலாம்?"},
                        "answer": {"en": "Senior citizens and students can apply at the transport office with ID and proof of status.", "si": "වයස්ගත ජනතාව සහ ශිෂ්‍යවරුන් ID සහ තත්ත්ව සාධක සමඟ ප්‍රවාහන කාර්යාලයේ අයදුම් කල හැක.", "ta": "வயோமுறை மக்கள் மற்றும் மாணவர்கள் ID மற்றும் நிலையை நிரூபிக்கும் ஆவணத்துடன் போக்குவரத்து அலுவலத்தில் விண்ணப்பிக்கலாம்."},
                        "downloads": ["/static/forms/concession_app.pdf"],
                        "location": "",
                        "instructions": "Concession cards issued after verification."
                    }
                ]
            },
            {
                "id": "road_safety",
                "name": {"en": "Road Safety & Regulations", "si": "මාර්ග ආරක්ෂාව සහ නීති", "ta": "சாலை பாதுகாப்பு மற்றும் விதிகள்"},
                "questions": [
                    {
                        "q": {"en": "How to report road hazards?", "si": "මාර්ග අවදානම් වාර්තා කරන ආකාරය?", "ta": "சாலைக் அபாயங்களை எப்படி அறிவிக்கலாம்?"},
                        "answer": {"en": "Call the road safety hotline or use the mobile reporting app with photos and location.", "si": "මාර්ග ආරක්ෂක හෙල්ප්ලයින් අමතන්න හෝ දුරකථන වාර්තාකරණ යෙදුම භාවිතා කරන්න.", "ta": "சாலை பாதுகாப்பு ஹெல்ப்லைனை அழைக்கவும் அல்லது இடத்தையும் புகைப்படத்தையும் கொண்ட மொபைல் செயலியைப் பயன்படுத்தவும்."},
                        "downloads": [],
                        "location": "",
                        "instructions": "Do not try to clear hazards yourself — report to authorities."
                    }
                ]
            }
        ]
    },
    {
        "id": "ministry_finance",
        "category": "cat_finance",
        "name": {"en": "Ministry of Finance & Tax", "si": "මූල්‍ය හා බද්ද අමාත්‍යංශය", "ta": "நிதி மற்றும் வரி அமைச்சு"},
        "subservices": [
            {
                "id": "tax_registration",
                "name": {"en": "Tax Registration", "si": "බදු ලියාපදිංචිය", "ta": "வரி பதிவு"},
                "questions": [
                    {
                        "q": {"en": "How to register for tax?", "si": "බදු සඳහා කොපමන විදිහට ලියාපදිංචි වන්නද?", "ta": "வரி பதிவு எப்படி செய்வது?"},
                        "answer": {"en": "Register online via the revenue portal with identity documents and business details.", "si": "ආදායම් පෝටලය හරහා ඔන්ලයින්ව ලියාපදිංචි වන්න, හැඳුනුම් ලේඛන සහ ව්‍යාපාර විස්තර එක් කරන්න.", "ta": "வருமானப் போர்டல் மூலம் ஆன்லைனில் பதிவு செய்து அடையாள ஆவணங்கள் மற்றும் வணிக விவரங்களை வழங்கவும்."},
                        "downloads": ["/static/forms/tax_reg.pdf"],
                        "location": "https://maps.google.com/?q=Revenue+Department+Colombo",
                        "instructions": "Keep your TIN for future filings."
                    },
                    {
                        "q": {"en": "Who must register?", "si": "කවුද ලියාපදිංචි විය යුතුය?", "ta": "யார் பதிவு செய்ய வேண்டும்?"},
                        "answer": {"en": "Individuals with income above the threshold and all businesses must register.", "si": "ආදායම් සීමාව ඉක්මවන පුද්ගලයින් සහ සියළු ව්‍යාපාර ලියාපදිංචි විය යුතුය.", "ta": "வரம்பு மீறியவரும் அனைத்து வணிகங்களும் பதிவு செய்ய வேண்டும்."},
                        "downloads": [],
                        "location": "",
                        "instructions": "Check threshold updates on the revenue website."
                    }
                ]
            },
            {
                "id": "tax_filing",
                "name": {"en": "Tax Filing & Payments", "si": "බදු ලිපිගොනු සහ ගෙවීම්", "ta": "வரி தாக்கல் மற்றும் பரிசுராம்கள்"},
                "questions": [
                    {
                        "q": {"en": "How to file taxes online?", "si": "ඔන්ලයින්ව බදු කොපමන වාරිකව лиකරද?", "ta": "ஆன்லைனில் வரியை எப்படி தாக்கல் செய்வது?"},
                        "answer": {"en": "Use the revenue online portal, upload required documents and submit payment through available methods.", "si": "ආදායම් ඔන්ලයින් පෝටලය භාවිතා කරන්න, අවශ්‍ය ලේඛන උඩුගත කර ගෙවීම් ක්‍රම භාවිතයෙන් ගෙවන්න.", "ta": "வருமான ஆன்லைன் போர்ட்டலைப் பயன்படுத்தி தேவையான ஆவணங்களை பதிவேற்றம் செய்து கொடுப்பனவு முறைகளில் செலுத்தவும்."},
                        "downloads": ["/static/guides/tax_filing_guide.pdf"],
                        "location": "",
                        "instructions": "Retain receipts and acknowledgement numbers."
                    },
                    {
                        "q": {"en": "What are payment options?", "si": "ගෙවීම් විකල්ප කුමක්ද?", "ta": "கொடுத்தல் விருப்பங்கள் என்ன?"},
                        "answer": {"en": "Credit/debit card, bank transfer and designated payment agents are accepted.", "si": "ක්‍රෙඩිට්/ඩෙබිට් කාඩ්, බැංකු ගනුදෙනු සහ අනුමෝදිත ගෙවීම් නියෝජිතයන් පිළිගනු ලබයි.", "ta": "கிரெடிட்/டெபிட் கார்டு, வங்கி மாற்றம் மற்றும் ஒதுக்கப்பட்ட கட்டண முகவர்களுக்கு அனுமதி உள்ளது."},
                        "downloads": [],
                        "location": "",
                        "instructions": "Payments must be made before due date to avoid penalties."
                    }
                ]
            },
            {
                "id": "grants_subsidies",
                "name": {"en": "Grants & Subsidies", "si": "ප්‍රතිලාභ සහ දීමනා", "ta": "அனுதானங்கள் மற்றும் தள்ளுபட்டுகள்"},
                "questions": [
                    {
                        "q": {"en": "How to apply for a business grant?", "si": "ව්‍යාපාර ප්‍රතිලාභ සඳහා කොහෙන් අයදුම් කරන්නද?", "ta": "வணிக உதவிக்கு எப்படி விண்ணப்பிக்கலாம்?"},
                        "answer": {"en": "Submit a proposal with financials; evaluation committee meets monthly.", "si": "මුදල් යෝජනාව එක් කර ඉදිරිපත් කරන්න; ඇගයීම් කමිටුව මාසිකව රැස්වෙයි.", "ta": "நிதி விவரங்களுடன் ஒரு முன்மொழிவை சமர்ப்பிக்கவும்; மதிப்பீட்டு குழு மாதந்தோறும் கூட்டம் செல்கிறது."},
                        "downloads": ["/static/forms/grant_app.pdf"],
                        "location": "",
                        "instructions": "Include recent audited accounts if available."
                    },
                    {
                        "q": {"en": "Are subsidies means-tested?", "si": "ප්‍රතිලාභ මගින් පරීක්ෂිතද?", "ta": "தள்ளுபடிகள் வருமான தகுதிக்கு உட்பட்டதா?"},
                        "answer": {"en": "Some subsidies are means-tested; check specific program requirements.", "si": "කිසිදා සමහර ප්‍රතිලාභ මගින් පරීක්ෂා කෙරේ; විශේෂ වැඩසටහනේ අවශ්‍යතා පරීක්ෂා කරන්න.", "ta": "சில தள்ளுபடிகள் வருமானத்தைக் கணக்கிட்டு தரப்படுகின்றன; ஒவ்வொரு திட்டத்தைப் பார்க்கவும்."},
                        "downloads": [],
                        "location": "",
                        "instructions": "Provide income proof if requested."
                    }
                ]
            },
            {
                "id": "public_spending",
                "name": {"en": "Public Spending & Budgets", "si": "ප්‍රජා වියදම් සහ වියදම් සැලසුම්", "ta": "பொது செலவுகள் மற்றும் பட்ஜெட்டுகள்"},
                "questions": [
                    {
                        "q": {"en": "Where to find the national budget?", "si": "ජාතික වියදම් සැලසුම කොතැනින් ලබාගන්නද?", "ta": "தேசிய பட்ஜெட்டை எங்கே காணலாம்?"},
                        "answer": {"en": "The national budget and spending reports are published on the finance ministry website.", "si": "ජාතික වියදම් සහ වාර්තා අමාත්‍යංශ වෙබ් අඩවියේ ප්‍රකාශ වේ.", "ta": "தேசிய பட்ஜெட் மற்றும் செலவுக் அறிக்கைகள் நிதி அமைச்சின் இணையதளத்தில் வெளியிடப்படுகின்றன."},
                        "downloads": ["/static/reports/national_budget.pdf"],
                        "location": "",
                        "instructions": "Use published CSVs for data analysis where provided."
                    }
                ]
            }
        ]
    },
    {
        "id": "ministry_housing",
        "category": "cat_housing",
        "name": {"en": "Ministry of Housing & Land", "si": "නිවාස සහ භූමි අමාත්‍යංශය", "ta": "வீடுகள் மற்றும் நிலம் அமைச்சு"},
        "subservices": [
            {
                "id": "land_registration",
                "name": {"en": "Land Registration", "si": "භූමි ලියාපදිංචිය", "ta": "நிலப் பதிவு"},
                "questions": [
                    {
                        "q": {"en": "How to register land?", "si": "භූමිය ලියාපදිංචි කරන ආකාරය?", "ta": "நிலத்தை பதிவு செய்வது எப்படி?"},
                        "answer": {"en": "Submit title deeds, surveys and ID to the land registry; registration time varies by district.", "si": "හිතුරු ලේඛන, නිරීක්ෂණ සහ ID භූමි ලේඛන කාර්යාලයට ඉදිරිපත් කරන්න; ලියාපදිංචි කාලය දිස්ත්‍රික්කය අනුව වෙනස් වේ.", "ta": "தலைப்புத்தகங்கள், பரிசோதனைகள் மற்றும் ID-ஐ நில பதிவில் சமர்ப்பிக்கவும்; பதிவு காலம் மாவட்டப்பகுதியில் மாறக்கூடும்."},
                        "downloads": ["/static/forms/land_reg.pdf"],
                        "location": "https://maps.google.com/?q=Land+Registry+Colombo",
                        "instructions": "Ensure survey plans are certified by a licensed surveyor."
                    },
                    {
                        "q": {"en": "How to check title disputes?", "si": "ශීර්ෂ අයිතිවාසිකම් ගැටලු පරීක්ෂා කරන්නේ කෙසේද?", "ta": "தலைப்பு கூட்டணி சிக்கல்களை எப்படி சரிபார்க்கலாம்?"},
                        "answer": {"en": "Visit the land registry or use the online title search service to see encumbrances.", "si": "භූමි ලේඛන කාර්යාලයට යන්න හෝ ඔන්ලයින් ශීර්ෂ සෙවීමේ සේවාව භාවිතා කරන්න.", "ta": "நில பதிவகம் சென்று அல்லது ஆன்லைன் தலைப்பு தேடல் சேவையைப் பயன்படுத்தி கட்டுப்பாடுகளை காணலாம்."},
                        "downloads": [],
                        "location": "",
                        "instructions": "Keep transaction receipts and surveyor certificates."
                    }
                ]
            },
            {
                "id": "housing_allocations",
                "name": {"en": "Housing Allocations", "si": "නිවාස පැවරුම්", "ta": "வீட்டு ஒதுக்கீடுகள்"},
                "questions": [
                    {
                        "q": {"en": "How to apply for subsidized housing?", "si": "අඩුගාස්තු නිවාස සඳහා කොහෙන් අයදුම් කරන්නද?", "ta": "தள்ளுபடு வீடுகளுக்கு எப்படி விண்ணப்பிக்கலாம்?"},
                        "answer": {"en": "Submit an application with income proof; shortlisting is done based on criteria and availability.", "si": "ආදායම් සාධක සහිත අයදුම්පත ඉදිරිපත් කරන්න; තේරීම් හා ලබාගැනීම අනුපාතව සිදු වේ.", "ta": "வருமான சான்றுடன் விண்ணப்பத்தை சமர்ப்பிக்கவும்; தேர்வு மற்றும் கிடைக்குதல் நிபந்தனைகளின்படி நடைபெறும்."},
                        "downloads": ["/static/forms/housing_app.pdf"],
                        "location": "",
                        "instructions": "Include family size and current address proof."
                    },
                    {
                        "q": {"en": "Can I transfer allocated housing?", "si": "පැවරුම් ලබා දී ඇති නිවාස මාරු කළ හැකිද?", "ta": "ஒதுக்கப்பட்ட வீடுகளை மாற்ற முடியுமா?"},
                        "answer": {"en": "Transfers are restricted; apply to the housing authority with valid reasons and documents.", "si": "මාරු සීමා කර ඇත; නිවැරදි හේතු සහ ලේඛන සමඟ නිවාස අධිකාරියට අයදුම් කරන්න.", "ta": "மாற்றங்கள் கட்டுப்படுத்தப்படுகின்றன; காரணங்கள் மற்றும் ஆவணங்களுடன் வீடு அதிகாரிக்கு விண்ணப்பிக்கவும்."},
                        "downloads": [],
                        "location": "",
                        "instructions": "Provide supporting legal documents for transfers."
                    }
                ]
            },
            {
                "id": "building_permits",
                "name": {"en": "Building Permits", "si": "ගොඩනැගිලි අවසර", "ta": "கட்டிட அனுமதிகள்"},
                "questions": [
                    {
                        "q": {"en": "How to apply for a building permit?", "si": "ගොඩනැගිලි අවසර සඳහා කොහෙන් අයදුම් කරන්නද?", "ta": "கட்டிட அனுமதிக்கு எப்படி விண்ணப்பிக்கலாம்?"},
                        "answer": {"en": "Submit plans certified by an architect, land documents and pay the assessment fee.", "si": "වාස්තු විදුහල්ඥයා විසින් සහතික කළ සැලසුම්, භූමික ලේඛන සහ ඇගයීමේ ගාස්තුව ගෙවන්න.", "ta": "வாஸ்து நிபுணர் ஆவணமிட்ட திட்டப் படிவங்கள், நில ஆவணங்கள் மற்றும் மதிப்பீட்டு கட்டணத்தை செலுத்தவும்."},
                        "downloads": ["/static/forms/building_permit.pdf"],
                        "location": "",
                        "instructions": "Allow time for environmental and safety clearances."
                    }
                ]
            },
            {
                "id": "land_tax",
                "name": {"en": "Land Tax & Rates", "si": "ඉඩම් බදු සහ අනුපාත", "ta": "நில வரி மற்றும் விகிதங்கள்"},
                "questions": [
                    {
                        "q": {"en": "How to pay land tax?", "si": "ඉඩම් බදු ගෙවන්නේ කෙසේද?", "ta": "நில வரியை எப்படி செலுத்துவது?"},
                        "answer": {"en": "Pay via the local council portal or at designated revenue centers; keep the receipt.", "si": "දේශීය සභා පෝටලය හෝ අනුමත ආදායම් මධ්‍යස්ථාන වෙත ගෙවීම් කරන්න; පිටපත රඳවන්න.", "ta": "உங்கள் உள்ளூராட்சி போர்டலிலோ அல்லது நியமிக்கப்பட்ட வருமான மையங்களில் செலுத்தவும்; ரசீதினை காப்பாற்றவும்."},
                        "downloads": [],
                        "location": "",
                        "instructions": "Check deadlines to avoid interest/penalties."
                    }
                ]
            }
        ]
    }
]

services_col.insert_many(services)

print("✅ Seed complete!")
print(f"   Categories: {categories_col.count_documents({})}")
print(f"   Officers: {officers_col.count_documents({})}")
print(f"   Ads: {ads_col.count_documents({})}")
print(f"   Services: {services_col.count_documents({})}")
