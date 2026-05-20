class SkinAdvisoryEngine:
    def __init__(self):
        # Disease knowledge base mapped to HAM10000 classes
        self.knowledge_base = {
            'Actinic keratoses': {
                'en': {
                    'name': 'Actinic Keratoses',
                    'severity_base': 'Moderate',
                    'description': 'A rough, scaly patch on the skin caused by years of sun exposure. Can sometimes progress to skin cancer.',
                    'precautions': [
                        'Avoid unnecessary sun exposure, especially midday.',
                        'Use broad-spectrum sunscreen daily.',
                        'Wear protective clothing and hats.',
                        'Monitor the size and color of the patch.'
                    ]
                },
                'hi': {
                    'name': 'धूप से झुलसी त्वचा (Actinic Keratoses)',
                    'severity_base': 'Moderate',
                    'description': 'यह त्वचा पर एक खुरदरा और पपड़ीदार हिस्सा है जो सालों तक धूप में रहने के कारण होता है। अगर ध्यान न दिया जाए तो यह आगे चलकर स्किन कैंसर का रूप ले सकता है।',
                    'precautions': [
                        'धूप में ज्यादा देर तक बाहर न रहें, खासकर दोपहर की तेज धूप में।',
                        'रोजाना अच्छी क्वालिटी का सनस्क्रीन (Sunscreen) जरूर लगाएं।',
                        'बाहर जाते समय पूरी बाजू के कपड़े पहनें और टोपी / छाते का इस्तेमाल करें।',
                        'इस दाग के आकार, रंग या मोटापे में किसी भी बदलाव पर ध्यान देते रहें।'
                    ]
                }
            },
            'Basal cell carcinoma': {
                'en': {
                    'name': 'Basal Cell Carcinoma',
                    'severity_base': 'High',
                    'description': 'A type of skin cancer that begins in the basal cells. It usually appears as a slightly transparent bump on the skin.',
                    'precautions': [
                        'URGENT: Schedule a biopsy/consultation with a dermatologist.',
                        'Protect the area from further UV exposure.',
                        'Avoid scratching or irritating the area.'
                    ]
                },
                'hi': {
                    'name': 'त्वचा का कैंसर - बेसल सेल (Basal Cell Carcinoma)',
                    'severity_base': 'High',
                    'description': 'यह एक प्रकार का त्वचा कैंसर (Skin Cancer) है। यह अक्सर त्वचा पर हल्के पारदर्शी (मोतियों जैसे) दाने या घाव के रूप में दिखाई देता है जो जल्दी ठीक नहीं होता।',
                    'precautions': [
                        'URGENT (अत्यंत जरूरी): बिना देरी किए तुरंत किसी अच्छे त्वचा विशेषज्ञ (Dermatologist) से मिलें।',
                        'प्रभावित हिस्से को धूप और धूल से पूरी तरह बचाकर रखें।',
                        'इसे बिल्कुल न खुजलाएं और न ही फोड़ने की कोशिश करें।'
                    ]
                }
            },
            'Benign keratosis-like lesions': {
                'en': {
                    'name': 'Benign Keratosis',
                    'severity_base': 'Low',
                    'description': 'A non-cancerous skin growth that can appear scaly, waxy, or slightly elevated. Common with age.',
                    'precautions': [
                        'Generally harmless, but monitor for changes.',
                        'Keep the skin moisturized.',
                        'Avoid picking or peeling the scale.'
                    ]
                },
                'hi': {
                    'name': 'उम्र के साथ होने वाले त्वचा के दाग (Benign Keratosis)',
                    'severity_base': 'Low',
                    'description': 'ये त्वचा पर होने वाले सामान्य दाग या निशान हैं जो कैंसर नहीं होते। ये उम्र बढ़ने के साथ अक्सर दिखाई देते हैं और पपड़ीदार या उभरे हुए हो सकते हैं।',
                    'precautions': [
                        'ये आमतौर पर चिंता की बात नहीं हैं, लेकिन फिर भी इन पर निगरानी रखें।',
                        'स्किन को अच्छी तरह से मॉइस्चराइज़ रखें, सूखी न पड़ने दें।',
                        'इन पपड़ियों को नोचने या छीलने की कोशिश बिलकुल न करें।'
                    ]
                }
            },
            'Dermatofibroma': {
                'en': {
                    'name': 'Dermatofibroma',
                    'severity_base': 'Low',
                    'description': 'A common benign skin growth, often occurring on the lower legs. They can feel firm like a hard lump.',
                    'precautions': [
                        'Usually requires no treatment.',
                        'Avoid shaving closely over the bump to prevent bleeding.',
                        'If it becomes painful, consult a doctor.'
                    ]
                },
                'hi': {
                    'name': 'त्वचा की छोटी गांठ (Dermatofibroma)',
                    'severity_base': 'Low',
                    'description': 'यह त्वचा के नीचे एक सामान्य और हानिरहित गांठ होती है, जो ज्यादातर पैरों या हाथों पर देखी जाती है। छूने पर यह थोड़ी सख्त महसूस होती है।',
                    'precautions': [
                        'इसे आमतौर पर किसी इलाज की जरूरत नहीं होती है और यह सामान्य बात है।',
                        'इसके ऊपर रेजर या ब्लेड चलाने से बचें ताकि खून न निकले और इंफेक्शन न हो।',
                        'अगर इसमें दर्द होने लगे या यह तेजी से बढ़ने लगे, तब ही डॉक्टर को दिखाएं।'
                    ]
                }
            },
            'Melanoma': {
                'en': {
                    'name': 'Melanoma',
                    'severity_base': 'High',
                    'description': 'The most serious type of skin cancer, developing in the melanocytes. High risk of spreading if untreated.',
                    'precautions': [
                        'URGENT: Immediate consultation with an oncologist or dermatologist required.',
                        'Do not delay medical evaluation.',
                        'Track any changes in ABCD (Asymmetry, Border, Color, Diameter).'
                    ]
                },
                'hi': {
                    'name': 'गंभीर त्वचा कैंसर - मेलेनोमा (Melanoma)',
                    'severity_base': 'High',
                    'description': 'यह सबसे खतरनाक किस्म का स्किन कैंसर है। अगर इसका सही समय पर इलाज न किया जाए तो यह शरीर के दूसरे हिस्सों में बहुत तेजी से फैल सकता है।',
                    'precautions': [
                        'URGENT (अत्यंत जरूरी): तुरंत कैंसर विशेषज्ञ (Oncologist) या डर्मेटोलॉजिस्ट से मिलें, इसमें एक दिन की भी देरी भारी पड़ सकती है।',
                        'डॉक्टर के पास जाने में बिलकुल भी देरी न करें।',
                        'ABCD नियम का ध्यान रखें: A (आकार का बिगड़ना), B (किनारों का खुरदरा होना), C (रंग बदलना), D (आकार का बढ़ना)।'
                    ]
                }
            },
            'Melanocytic nevi': {
                'en': {
                    'name': 'Normal Mole / Nevi',
                    'severity_base': 'Low',
                    'description': 'A common mole. Usually harmless, but should be monitored for malignant transformation.',
                    'precautions': [
                        'Regularly check for changes in size, shape, or color.',
                        'Use sunscreen when exposed to the sun.',
                        'Perform monthly self-examinations.'
                    ]
                },
                'hi': {
                    'name': 'सामान्य तिल (Normal Mole / Nevi)',
                    'severity_base': 'Low',
                    'description': 'यह त्वचा पर होने वाला एक सामान्य काला या भूरा तिल है। यह आमतौर पर बिल्कुल सुरक्षित होता है, लेकिन कभी-कभी (बहुत कम मामलों में) यह खतरनाक रूप ले सकता है।',
                    'precautions': [
                        'अगर तिल के आकार, रंग या मोटाई में कोई अचानक बदलाव दिखे तो डॉक्टर से मिलें।',
                        'धूप में निकलने से पहले इस पर और बाकी त्वचा पर सनस्क्रीन का इस्तेमाल करें।',
                        'समय-समय पर अपने शरीर के तिलों को खुद चेक करते रहें।'
                    ]
                }
            },
            'Vascular lesions': {
                'en': {
                    'name': 'Vascular Lesions',
                    'severity_base': 'Low',
                    'description': 'A relatively common skin finding representing a range of conditions from cherry angiomas to birthmarks.',
                    'precautions': [
                        'Avoid forcefully scratching to prevent bleeding.',
                        'Most are harmless, but seek medical advice if they bleed frequently or grow rapidly.'
                    ]
                },
                'hi': {
                    'name': 'खून की नसों के लाल निशान (Vascular Lesions)',
                    'severity_base': 'Low',
                    'description': 'ये त्वचा पर लाल रंग के निशान होते हैं, जो खून की नसों (Blood vessels) के एक जगह इकट्ठा होने से बनते हैं। इसमें लाल दाने या जन्म के निशान शामिल हो सकते हैं।',
                    'precautions': [
                        'इन्हें जोर से न रगड़ें और न ही खुजलाएं, क्योंकि इनमें से बहुत जल्दी खून निकल सकता है।',
                        'ज़्यादातर ये बिलकुल सुरक्षित होते हैं, लेकिन अगर इनसे बार-बार खून आए या ये तेजी से बड़े हों तो डॉक्टर से मिलें।'
                    ]
                }
            },
            'Unknown': {
                'en': {
                    'name': 'Unknown / Unrecognized',
                    'severity_base': 'Unknown',
                    'description': 'The model could not confidently identify the condition.',
                    'precautions': [
                        'Consult a dermatologist for a professional diagnosis.'
                    ]
                },
                'hi': {
                    'name': 'अज्ञात / पहचान नहीं हो पाई (Unknown)',
                    'severity_base': 'Unknown',
                    'description': 'माफ़ करें, एआई मॉडल इस बीमारी की सही से पहचान नहीं कर पा रहा है।',
                    'precautions': [
                        'सही जानकारी और उचित इलाज के लिए कृपया किसी त्वचा विशेषज्ञ (Dermatologist) से संपर्क करें।'
                    ]
                }
            }
        }

    def analyze(self, class_name, confidence, lang='en'):
        """
        Returns a dictionary containing severity, description, and precautions
        in the specified language ('en' or 'hi').
        """
        if class_name not in self.knowledge_base:
            class_name = 'Unknown'
            
        info = self.knowledge_base[class_name][lang]
        base_severity = info['severity_base']
        
        # Risk Engine Logic & Formatting translated dynamically
        if base_severity == 'High':
            risk_level = 'Urgent Consultation Recommended' if lang == 'en' else 'तत्काल डॉक्टर से मिलें (Urgent Consultation Recommended)'
            final_severity = 'High'
        elif base_severity == 'Moderate':
            if confidence > 80:
                final_severity = 'Moderate'
                risk_level = 'Medium Risk - Medical evaluation advised' if lang == 'en' else 'मध्यम जोखिम - डॉक्टर को दिखाना ठीक रहेगा (Medium Risk - Medical evaluation advised)'
            else:
                final_severity = 'Moderate-Low'
                risk_level = 'Low to Medium Risk - Monitor the area' if lang == 'en' else 'कम जोखिम - इस पर निगरानी रखें (Low Risk - Monitor the area)'
        elif base_severity == 'Unknown':
             final_severity = 'Unknown'
             risk_level = 'Unknown Risk - Consult Doctor' if lang == 'en' else 'अज्ञात - डॉक्टर से परामर्श लें (Unknown Risk - Consult Doctor)'
        else:
            final_severity = 'Low'
            risk_level = 'Low Risk - Routine monitoring recommended' if lang == 'en' else 'कम जोखिम - घबराने की बात नहीं, बस ध्यान रखें (Low Risk - Routine monitoring)'

        return {
            'disease_key': class_name,
            'name': info['name'],
            'description': info['description'],
            'severity': final_severity,
            'risk_level': risk_level,
            'precautions': info['precautions']
        }
