# DiagnoScan 

## Description
A cloud-based AI-driven medical imaging solution designed to assist healthcare professionals by automating the detection of abnormalities in MRI and X-ray scans. It enhances accessibility, efficiency, and diagnostic accuracy using AWS HealthImaging and advanced deep learning techniques.

## Problem Statement
Medical imaging analysis is time-consuming and requires expert radiologists, leading to delays in diagnosis and treatment. This project aims to bridge this gap by providing an AI-powered system for automated detection, multilingual accessibility, and patient-centric insights, ensuring faster and more accurate diagnoses.

## Features
- **AI-Powered Auto-Detection**: Uses deep learning models, including Vision Transformers (ViTs), to detect abnormalities in MRI and X-ray images.
- **AWS HealthImaging Integration**: Enables scalable and cost-effective cloud storage with high-speed retrieval of medical images.
- **Multilingual Support**: Provides speech-to-text and text-to-speech capabilities in multiple languages.
- **Patient History Analysis**: Analyzes past medical records, including blood test reports and family history.
- **Emergency Alerts**: Notifies nearby hospitals in case of critical findings.
- **Dietary & Lifestyle Recommendations**: Suggests personalized dietary plans based on medical reports, regional dietary habits, and allergies.
- **Image-Based Diagnosis**: Supports interpretation of radiology images such as MRI, X-ray, and CT scans.
- **Sign Language Support**: Ensures accessibility for hearing-impaired users.
- **Mental Health Assistance**: Provides basic mental health analysis and recommendations.

## Technologies Used
- **AWS HealthImaging**: For secure and scalable image storage.
- **Visual Transformers (ViTs)**: For AI-based auto-detection of anomalies.
- **Speech-to-Text & Text-to-Speech APIs**: For multilingual accessibility.
- **OCR (Optical Character Recognition)**: For processing scanned medical documents.
- **Denoising & Profanity Filter**: For clean and relevant outputs.
- **AWS Lambda & S3**: For scalable backend processing.

## Setup Instructions
```sh
# Clone the repository
git clone https://github.com/your-repo/medical-ai-assistant.git
cd medical-ai-assistant

# Install dependencies
pip install -r requirements.txt

# Configure AWS HealthImaging:
# - Create an AWS HealthImaging instance.
# - Set up an S3 bucket for image storage.
# - Obtain API credentials.

# Run the application
python app.py
```

## Future Enhancements
- **Federated Learning Support**: To improve model accuracy while ensuring data privacy.
- **Integration with Wearable Devices**: For continuous health monitoring.
- **Real-Time Diagnosis Support**: Live consultation with doctors via AI-driven recommendations.

## Contributors
- Your Name (@your-handle)
- Team Members (@team-handle)

## License
This project is licensed under the MIT License. See the LICENSE file for details.

