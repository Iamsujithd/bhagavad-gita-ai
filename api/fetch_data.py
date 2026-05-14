import json
import os

data_dir = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(data_dir, exist_ok=True)
json_path = os.path.join(data_dir, "gita.json")

shlokas = [
    {
        "chapter": 2,
        "verse": 47,
        "sanskrit": "कर्मण्येवाधिकारस्ते मा फलेषु कदाचन।\nमा कर्मफलहेतुर्भूर्मा ते सङ्गोऽस्त्वकर्मणि॥",
        "transliteration": "karmany evadhikaras te ma phalesu kadacana\nma karma-phala-hetur bhur ma te sango 'stv akarmani",
        "translation": "You have a right to perform your prescribed duty, but you are not entitled to the fruits of action. Never consider yourself the cause of the results of your activities, and never be attached to not doing your duty.",
        "theme": "Duty and Detachment"
    },
    {
        "chapter": 2,
        "verse": 14,
        "sanskrit": "मात्रास्पर्शास्तु कौन्तेय शीतोष्णसुखदुःखदाः।\nआगमापायिनोऽनित्यास्तांस्तितिक्षस्व भारत॥",
        "transliteration": "matra-sparsas tu kaunteya sitosna-sukha-duhkha-dah\nagamapayino 'nityas tams titiksasva bharata",
        "translation": "O son of Kunti, the nonpermanent appearance of happiness and distress, and their disappearance in due course, are like the appearance and disappearance of winter and summer seasons. They arise from sense perception, O scion of Bharata, and one must learn to tolerate them without being disturbed.",
        "theme": "Tolerance and Peace"
    },
    {
        "chapter": 2,
        "verse": 22,
        "sanskrit": "वासांसि जीर्णानि यथा विहाय नवानि गृह्णाति नरोऽपराणि।\nतथा शरीराणि विहाय जीर्णा न्यन्यानि संयाति नवानि देही॥",
        "transliteration": "vasamsi jirnani yatha vihaya navani grhnati naro 'parani\ntatha sarirani vihaya jirnany anyani samyati navani dehi",
        "translation": "As a person puts on new garments, giving up old ones, the soul similarly accepts new material bodies, giving up the old and useless ones.",
        "theme": "Soul and Reincarnation"
    },
    {
        "chapter": 4,
        "verse": 7,
        "sanskrit": "यदा यदा हि धर्मस्य ग्लानिर्भवति भारत।\nअभ्युत्थानमधर्मस्य तदात्मानं सृजाम्यहम्॥",
        "transliteration": "yada yada hi dharmasya glanir bhavati bharata\nabhyutthanam adharmasya tadatmanam srjamy aham",
        "translation": "Whenever and wherever there is a decline in religious practice, O descendant of Bharata, and a predominant rise of irreligion—at that time I descend Myself.",
        "theme": "Dharma and Divine Intervention"
    },
    {
        "chapter": 6,
        "verse": 5,
        "sanskrit": "उद्धरेदात्मनात्मानं नात्मानमवसादयेत्।\nआत्मैव ह्यात्मनो बन्धुरात्मैव रिपुरात्मनः॥",
        "transliteration": "uddhared atmanatmanam natmanam avasadayet\natmaiva hy atmano bandhur atmaiva ripur atmanah",
        "translation": "One must deliver himself with the help of his mind, and not degrade himself. The mind is the friend of the conditioned soul, and his enemy as well.",
        "theme": "Mind Control and Self-improvement"
    },
    {
        "chapter": 6,
        "verse": 6,
        "sanskrit": "बन्धुरात्मात्मनस्तस्य येनात्मैवात्मना जितः।\nअनात्मनस्तु शत्रुत्वे वर्तेतात्मैव शत्रुवत्॥",
        "transliteration": "bandhur atmatmanas tasya yenatmaivatmana jitah\nanatmanas tu satrutve vartetatmaiva satru-vat",
        "translation": "For him who has conquered the mind, the mind is the best of friends; but for one who has failed to do so, his mind will remain the greatest enemy.",
        "theme": "Mind Control"
    },
    {
        "chapter": 9,
        "verse": 27,
        "sanskrit": "यत्करोषि यदश्नासि यज्जुहोषि ददासि यत्।\nयत्तपस्यसि कौन्तेय तत्कुरुष्व मदर्पणम्॥",
        "transliteration": "yat karosi yad asnasi yaj juhosi dadasi yat\nyat tapasyasi kaunteya tat kurusva mad-arpanam",
        "translation": "Whatever you do, whatever you eat, whatever you offer or give away, and whatever austerities you perform—do that, O son of Kunti, as an offering to Me.",
        "theme": "Devotion and Surrender"
    },
    {
        "chapter": 18,
        "verse": 66,
        "sanskrit": "सर्वधर्मान्परित्यज्य मामेकं शरणं व्रज।\nअहं त्वां सर्वपापेभ्यो मोक्षयिष्यामि मा शुचः॥",
        "transliteration": "sarva-dharman parityajya mam ekam saranam vraja\naham tvam sarva-papebhyo moksayisyami ma sucah",
        "translation": "Abandon all varieties of religion and just surrender unto Me. I shall deliver you from all sinful reactions. Do not fear.",
        "theme": "Ultimate Surrender"
    }
]

with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(shlokas, f, indent=4, ensure_ascii=False)

print(f"Successfully generated {json_path} with {len(shlokas)} shlokas.")
