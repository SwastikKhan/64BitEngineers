import pytesseract
from pdf2image import convert_from_path
from typing import Dict, List, Tuple
import json
import requests
import spacy

# ===================== Configuration Section =====================
BHASHINI_API_KEY = "your_bhashini_api_key_here"
BHASHINI_USER_ID = "your_bhashini_user_id_here"
GOOGLE_MAPS_API_KEY = "your_google_maps_api_key_here"
# ==================================================================

class MedicalReportAnalyzer:
    def __init__(self, bhashini_api_key: str, bhashini_user_id: str, google_maps_api_key: str):
        self.bhashini_api_key = bhashini_api_key
        self.bhashini_user_id = bhashini_user_id
        self.google_maps_api_key = google_maps_api_key
        self.reference_ranges = {
            'TSH': {'min': 0.5, 'max': 5.0, 'unit': 'mIU/L'},
            'Hemoglobin': {'min': 13.5, 'max': 17.5, 'unit': 'g/dL'},
            'Glucose': {'min': 70, 'max': 100, 'unit': 'mg/dL'},
        }
        self.nlp = spacy.load("xx_ent_wiki_sm")

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        images = convert_from_path(pdf_path)
        text = "".join([pytesseract.image_to_string(image) for image in images])
        return text

    def call_bhashini_pipeline(self, pipeline_name: str, input_data: dict) -> dict:
        url = f"https://api.bhashini.gov.in/v1/pipeline/compute/{pipeline_name}"
        headers = {
            "Authorization": f"Bearer {self.bhashini_api_key}",
            "Content-Type": "application/json",
            "User-ID": self.bhashini_user_id
        }
        response = requests.post(url, headers=headers, json=input_data)
        response.raise_for_status()
        return response.json()

    def extract_location_and_state(self, text: str) -> Tuple[str, str]:
        doc = self.nlp(text)
        locations = [ent.text for ent in doc.ents if ent.label_ in ["GPE", "LOC"]]
        if not locations:
            return "No location found", "State not found"

        location = locations[0]
        url = f"https://maps.googleapis.com/maps/api/geocode/json?address={location}, India&key={self.google_maps_api_key}"
        response = requests.get(url).json()

        for component in response.get("results", [{}])[0].get("address_components", []):
            if "administrative_area_level_1" in component["types"]:
                return location, component["long_name"]

        return location, "State not found"

    def parse_medical_data(self, text: str) -> Dict[str, float]:
        input_data = {
            "text": text,
            "tasks": ["extract_medical_data"],
            "reference_tests": list(self.reference_ranges.keys())
        }
        result = self.call_bhashini_pipeline("medical-parser", input_data)
        return {k: float(str(v).replace(',', '.')) for k, v in result.get("test_results", {}).items() if k in self.reference_ranges}

    def analyze_results(self, test_results: Dict[str, float]) -> List[Dict]:
        analysis = []
        for test, value in test_results.items():
            ref = self.reference_ranges[test]
            status = 'LOW' if value < ref['min'] else 'HIGH' if value > ref['max'] else 'NORMAL'
            analysis.append({
                'test': test, 'value': value, 'unit': ref['unit'], 'status': status,
                'reference': f"{ref['min']}-{ref['max']} {ref['unit']}"
            })
        return analysis

    def generate_recommendations(self, analysis: List[Dict], state: str) -> Dict:
        input_data = {
            "analysis": analysis,
            "tasks": ["generate_medical_recommendations"],
            "preferences": {"cuisine": state}
        }
        return self.call_bhashini_pipeline("medical-advice", input_data)

    def check_emergency(self, analysis: List[Dict]) -> Tuple[bool, str]:
        emergency_ranges = {'Glucose': {'min': 50, 'max': 400}, 'Hemoglobin': {'min': 7, 'max': 20}}
        for test in analysis:
            if test['test'] in emergency_ranges:
                ref = emergency_ranges[test['test']]
                if test['value'] < ref['min'] or test['value'] > ref['max']:
                    return True, f"Critical {test['test']} level ({test['value']} {test['unit']}) - Seek immediate care!"
        return False, "No critical levels detected"


def main():
    print("=== Medical Report Analyzer ===\n")
    pdf_path = input("Enter PDF file path: ").strip()
    analyzer = MedicalReportAnalyzer(BHASHINI_API_KEY, BHASHINI_USER_ID, GOOGLE_MAPS_API_KEY)

    try:
        print("\nProcessing report...")
        text = analyzer.extract_text_from_pdf(pdf_path)
        location, state = analyzer.extract_location_and_state(text)
        test_results = analyzer.parse_medical_data(text)

        if not test_results:
            print("No valid test results found")
            return

        analysis = analyzer.analyze_results(test_results)
        recommendations = analyzer.generate_recommendations(analysis, state)
        is_emergency, emergency_msg = analyzer.check_emergency(analysis)

        print("\n=== Analysis Results ===")
        for test in analysis:
            status_icon = "🟢" if test['status'] == 'NORMAL' else "🔴"
            print(f"{status_icon} {test['test']}: {test['value']} {test['unit']}")
            print(f"   (Reference: {test['reference']}, Status: {test['status']})")

        if is_emergency:
            print("\n🚨 EMERGENCY ALERT 🚨")
            print(emergency_msg)
            print("Seek immediate medical attention!")

        print("\n📍 Extracted Location: ", location)
        print("🌍 Identified State: ", state)

        print("\n🍽️ Dietary Recommendations:")
        for item in recommendations.get('diet', []):
            print(f"- {item}")

        print("\n🏃 Lifestyle Recommendations:")
        for item in recommendations.get('lifestyle', []):
            print(f"- {item}")

        if recommendations.get('warnings'):
            print("\n⚠️ Health Warnings:")
            for warning in recommendations.get('warnings', []):
                print(f"- {warning}")

    except Exception as e:
        print(f"\nError: {str(e)}")

if __name__ == "__main__":
    main()
