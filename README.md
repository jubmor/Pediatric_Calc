# Paediatric Emergency Calculator

A comprehensive web-based calculator for pediatric emergency drug dosing and equipment sizing based on ETC guidelines.

## Features

- **Weight Calculation**: Automatic weight estimation from age using standard pediatric formulas
- **Airway Management**: ET tube sizing, supraglottic devices, chest tube sizing
- **Analgesia Dosing**: Multiple routes (nasal, IM, IV) for:
  - Fentanyl
  - Diamorphine
  - Ketamine
  - Paracetamol
  - Morphine
- **Circulation**: Fluid resuscitation, blood products, and critical medications
- **Disability**: Osmotherapy and glucose management
- **Emergency Drugs**: Adrenaline, Atropine, Lorazepam dosing
- **Defibrillation**: Energy calculations based on weight

## Installation

### 1. Set up Python Virtual Environment

```bash
cd c:\Users\joana\py_new\Peds
python -m venv venv
venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

## Running the Application

### 1. Activate Virtual Environment

```bash
venv\Scripts\activate
```

### 2. Start the Flask Server

```bash
python app.py
```

The application will be available at: **http://127.0.0.1:5000**

## Usage

1. Enter patient information:
   - **Age (years)** OR **Age (months)** - for automatic weight calculation
   - OR manually enter **Weight (kg)**

2. Click **Calculate** button

3. View all calculated values organized by:
   - **A** - Airway
   - **Analgesia** - Pain management
   - **C** - Circulation
   - **D** - Disability
   - **E** - Emergency drugs & Energy

## Project Structure

```
Peds/
├── app.py                 # Flask application with all calculations
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # Main HTML template
└── static/
    ├── style.css         # CSS styling
    └── script.js         # Frontend JavaScript logic
```

## Reference Formulas

### Weight Calculation
- **1-12 months**: (0.5 × age_months) + 4 kg
- **1-5 years**: (2 × age_years) + 8 kg
- **6-12 years**: (3 × age_years) + 7 kg

### ET Tube Size
- **Uncuffed**: (age/4) + 4 mm
- **Cuffed**: (age/4) + 3.5 mm

### Defibrillation Energy
- **<50 kg**: 4 J/kg
- **≥50 kg**: 150 J

## Important Disclaimer

⚠️ **This is a reference tool only.** Always:
- Verify all calculations with senior clinicians
- Follow your local emergency protocols
- Use this as a supplement to, not a replacement for, clinical judgment
- In emergency situations, prioritize rapid assessment and treatment over calculations

## Clinical References

- ETC (Emergency Trauma Care) Guidelines
- Local emergency medicine protocols

## License

For educational and clinical reference purposes only.

## Contact

For questions or improvements, please contact the development team.
