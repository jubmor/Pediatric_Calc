from flask import Flask, render_template, request, jsonify
import math

app = Flask(__name__)

# ==================== CALCULATION FUNCTIONS ====================

class PedsCalculator:
    """Pediatric emergency calculation reference from ETC"""
    
    @staticmethod
    def calculate_weight(age_years=None, age_months=None):
        """Calculate weight (kg) from age using current pediatric formulas."""
        if age_months is not None and age_months <= 12:
            # 1-12 months: Updated APLS infant formula = (age in months ÷ 2) + 4
            return (0.5 * age_months) + 4
        elif age_years is not None:
            if age_years <= 5:
                # 1-5 years: Best Guess formula = (2 × age in years) + 8
                return (2 * age_years) + 8
            elif age_years <= 12:
                # 6-12 years: Luscombe formula = (3 × age in years) + 7
                return (3 * age_years) + 7
            else:
                # >12 years: fixed estimate = 50 kg
                return 50
        return None
    
    @staticmethod
    def et_tube_size(age_years):
        """ET tube size in mm"""
        return (age_years / 4) + 4
    
    @staticmethod
    def et_tube_cuff_size(age_years):
        """Cuffed ET tube size (0.5mm smaller)"""
        return (age_years / 4) + 4 - 0.5
    
    @staticmethod
    def et_tube_length_oral(age_years):
        """ET tube length for oral insertion"""
        return (age_years / 2) + 12
    
    @staticmethod
    def chest_tube_size(age_years):
        """Chest tube size (Fr gauge)"""
        et_size = (age_years / 4) + 4
        return et_size * 4
    
    @staticmethod
    def supraglottic_device_size(weight_kg):
        """Supraglottic airway device size based on weight"""
        if weight_kg < 5:
            return 1
        elif weight_kg <= 10:
            return 1.5
        elif weight_kg <= 25:
            return 2
        elif weight_kg <= 35:
            return 2.5
        elif weight_kg <= 60:
            return 3
        else:
            return 4
    
    @staticmethod
    def ventilated_tidal_volume(weight_kg):
        """Ventilated tidal volume: 6 ml/kg"""
        return 6 * weight_kg

    @staticmethod
    def laryngoscope_blade(weight_kg):
        """Select laryngoscope blade based on weight."""
        if weight_kg < 1:
            return 'Miller 0'
        elif weight_kg < 3:
            return 'Miller 0/1'
        elif weight_kg < 10:
            return 'Miller 1'
        elif weight_kg < 12:
            return 'Miller 1/Mac 1'
        elif weight_kg < 14:
            return 'Mac 2'
        elif weight_kg < 22:
            return 'Mac 1/2'
        elif weight_kg < 40:
            return 'Mac 2'
        elif weight_kg < 60:
            return 'Mac 3'
        else:
            return 'Mac 4'
    
    # ==================== RSI ====================
    
    @staticmethod
    def ketamine_rsi_iv_min(weight_kg):
        """Ketamine RSI IV: 1 mg/kg"""
        return 1 * weight_kg
    
    @staticmethod
    def ketamine_rsi_iv_max(weight_kg):
        """Ketamine RSI IV: 2 mg/kg"""
        return 2 * weight_kg
    
    @staticmethod
    def ketamine_rsi_im_min(weight_kg):
        """Ketamine RSI IM: 4 mg/kg"""
        return 4 * weight_kg
    
    @staticmethod
    def ketamine_rsi_im_max(weight_kg):
        """Ketamine RSI IM: 5 mg/kg"""
        return 5 * weight_kg
    
    @staticmethod
    def etomidate_rsi_iv_min(weight_kg):
        """Etomidate RSI IV: 0.2 mg/kg"""
        return 0.2 * weight_kg
    
    @staticmethod
    def etomidate_rsi_iv_max(weight_kg):
        """Etomidate RSI IV: 0.3 mg/kg (max 20 mg)"""
        dose = 0.3 * weight_kg
        return min(dose, 20)
    
    @staticmethod
    def propofol_rsi_iv_min(weight_kg):
        """Propofol RSI IV: 2 mg/kg"""
        return 2 * weight_kg
    
    @staticmethod
    def propofol_rsi_iv_max(weight_kg):
        """Propofol RSI IV: 3 mg/kg"""
        return 3 * weight_kg
    
    @staticmethod
    def rocuronium_rsi(weight_kg):
        """Rocuronium RSI: 1.2 mg/kg"""
        return 1.2 * weight_kg
    
    @staticmethod
    def sugammadex_rsi(weight_kg):
        """Sugammadex RSI: 16 mg/kg"""
        return 16 * weight_kg
    
    # ==================== ANALGESIA ====================
    
    @staticmethod
    def fentanyl_nasal(weight_kg):
        """Fentanyl nasal: 2 micrograms/kg"""
        return 2 * weight_kg
    
    @staticmethod
    def diamorphine_nasal(weight_kg):
        """Diamorphine nasal: 0.1 mg/kg"""
        return 0.1 * weight_kg
    
    @staticmethod
    def ketamine_nasal(weight_kg):
        """Ketamine nasal: 3 mg/kg"""
        return 3 * weight_kg
    
    @staticmethod
    def ketamine_im(weight_kg):
        """Ketamine IM: 2 mg/kg"""
        return 2 * weight_kg
    
    @staticmethod
    def paracetamol_iv(weight_kg):
        """Paracetamol IV: 15 mg/kg (Max 1g)"""
        dose = 15 * weight_kg
        return min(dose, 1000)
    
    @staticmethod
    def morphine_iv_min(weight_kg):
        """Morphine IV: 0.03-0.1 mg/kg"""
        return 0.03 * weight_kg
    
    @staticmethod
    def morphine_iv_max(weight_kg):
        """Morphine IV: 0.03-0.1 mg/kg"""
        return 0.1 * weight_kg
    
    @staticmethod
    def fentanyl_iv_min(weight_kg):
        """Fentanyl IV: 0.5-1 microgram/kg"""
        return 0.5 * weight_kg
    
    @staticmethod
    def fentanyl_iv_max(weight_kg):
        """Fentanyl IV: 0.5-1 microgram/kg"""
        return 1 * weight_kg
    
    @staticmethod
    def ketamine_iv_min(weight_kg):
        """Ketamine IV: 0.2-0.5 mg/kg"""
        return 0.2 * weight_kg
    
    @staticmethod
    def ketamine_iv_max(weight_kg):
        """Ketamine IV: 0.2-0.5 mg/kg"""
        return 0.5 * weight_kg
    
    # ==================== FLUIDS & TRANSFUSION ====================
    
    @staticmethod
    def crystalloid_bolus(weight_kg):
        """Crystalloid: 10ml/kg bolus (Max 500mls)"""
        dose = 10 * weight_kg
        return f"{min(dose, 500)} ml"
    
    @staticmethod
    def burn_fluid_rate(weight_kg, burn_percent):
        """Burns: 0.9% Saline 3-4 ml x % burn x weight (kg)"""
        min_rate = 3 * burn_percent * weight_kg
        max_rate = 4 * burn_percent * weight_kg
        return f"{min_rate:.0f} - {max_rate:.0f} ml total (half in first 8hrs, half in next 16hrs)"
    
    @staticmethod
    def blood_transfusion(weight_kg):
        """Blood: 5-10 ml/kg"""
        min_vol = 5 * weight_kg
        max_vol = 10 * weight_kg
        return f"{min_vol:.0f} - {max_vol:.0f} ml"
    
    @staticmethod
    def ffp_transfusion(weight_kg):
        """FFP: 5-10 ml/kg"""
        min_vol = 5 * weight_kg
        max_vol = 10 * weight_kg
        return f"{min_vol:.0f} - {max_vol:.0f} ml"
    
    @staticmethod
    def platelets_transfusion(weight_kg):
        """Platelets: 5-10 ml/kg (apheresis platelets)"""
        min_vol = 5 * weight_kg
        max_vol = 10 * weight_kg
        return f"{min_vol:.0f} - {max_vol:.0f} ml"
    
    # ==================== MEDICATIONS ====================
    
    @staticmethod
    def tranexamic_acid_bolus(weight_kg):
        """TXA bolus: 15mg/kg (Max 1g)"""
        dose = 15 * weight_kg
        return min(dose, 1000)
    
    @staticmethod
    def tranexamic_acid_infusion(weight_kg):
        """TXA infusion: 2mg/kg/hr for 8 hours (Max 25mg/kg over 8 hours = Max 125mg/hr)"""
        rate_per_hour = 2 * weight_kg
        max_rate_per_hour = 125
        return f"{min(rate_per_hour, max_rate_per_hour):.0f} mg/hr"
    
    @staticmethod
    def calcium_chloride(weight_kg):
        """10% Calcium Chloride: 0.2ml/kg over 10 mins (Max 10ml over 10mins)"""
        dose_ml = 0.2 * weight_kg
        return f"{min(dose_ml, 10):.1f} ml over 10 minutes"
    
    @staticmethod
    def adrenaline(weight_kg):
        """Adrenaline: 10 micrograms/kg (Max 1mg)"""
        dose = 10 * weight_kg
        return min(dose, 1000)
    
    @staticmethod
    def atropine(weight_kg):
        """Atropine: 20 microgram/kg (Max 600mcg)"""
        dose = 20 * weight_kg
        return min(dose, 600)
    
    @staticmethod
    def lorazepam(weight_kg):
        """Lorazepam: 0.1 mg/kg (Max 4mg)"""
        dose = 0.1 * weight_kg
        return min(dose, 4)
    
    # ==================== DISABILITY ====================
    
    @staticmethod
    def hypertonic_saline(weight_kg):
        """Hypertonic 3% Saline: 3-5 ml/kg over 10-20 mins (if >50kg then 250ml bolus)"""
        if weight_kg > 50:
            return "250 ml over 10-20 minutes"
        else:
            min_vol = 3 * weight_kg
            max_vol = 5 * weight_kg
            return f"{min_vol:.0f} - {max_vol:.0f} ml over 10-20 minutes"
    
    @staticmethod
    def mannitol_20percent(weight_kg):
        """20% Mannitol: 250mg - 500mg/kg (Equiv to 1.25 - 2.5 ml/kg)"""
        min_ml = 1.25 * weight_kg
        max_ml = 2.5 * weight_kg
        min_mg = 250 * weight_kg
        max_mg = 500 * weight_kg
        return f"{min_mg:.0f} - {max_mg:.0f} mg ({min_ml:.1f} - {max_ml:.1f} ml)"
    
    @staticmethod
    def dextrose_10percent(weight_kg):
        """10% Dextrose: 2ml/kg"""
        return 2 * weight_kg
    
    # ==================== ENERGY ====================
    
    @staticmethod
    def defibrillation_energy(weight_kg):
        """Defibrillation: 4 Joules/kg (if >50kg then 150 Joules)"""
        if weight_kg >= 50:
            return 150
        else:
            return 4 * weight_kg


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/calculate', methods=['POST'])
def calculate():
    """API endpoint for calculations"""
    try:
        data = request.json
        age_years = data.get('age_years')
        age_months = data.get('age_months')
        weight_kg = data.get('weight_kg')
        
        # Calculate weight if not provided
        if not weight_kg:
            if age_months:
                weight_kg = PedsCalculator.calculate_weight(age_months=age_months)
            elif age_years:
                weight_kg = PedsCalculator.calculate_weight(age_years=age_years)
        
        if not weight_kg:
            return jsonify({'error': 'Invalid input: please provide age or weight'}), 400
        
        # Prepare results
        results = {
            'weight_kg': round(weight_kg, 2),
            'airway': {
                'laryngoscope_blade': PedsCalculator.laryngoscope_blade(weight_kg),
                'et_tube_size': round(PedsCalculator.et_tube_size(age_years or 0), 1),
                'et_tube_cuff': round(PedsCalculator.et_tube_cuff_size(age_years or 0), 1),
                'et_tube_length': round(PedsCalculator.et_tube_length_oral(age_years or 0), 1),
                'chest_tube_size': round(PedsCalculator.chest_tube_size(age_years or 0), 1),
                'supraglottic_device': PedsCalculator.supraglottic_device_size(weight_kg),
                'ventilated_tidal_volume': round(PedsCalculator.ventilated_tidal_volume(weight_kg), 1),
                'rsi': {
                    'ketamine_iv_min': round(PedsCalculator.ketamine_rsi_iv_min(weight_kg), 2),
                    'ketamine_iv_max': round(PedsCalculator.ketamine_rsi_iv_max(weight_kg), 2),
                    'ketamine_im_min': round(PedsCalculator.ketamine_rsi_im_min(weight_kg), 2),
                    'ketamine_im_max': round(PedsCalculator.ketamine_rsi_im_max(weight_kg), 2),
                    'etomidate_iv_min': round(PedsCalculator.etomidate_rsi_iv_min(weight_kg), 2),
                    'etomidate_iv_max': round(PedsCalculator.etomidate_rsi_iv_max(weight_kg), 2),
                    'propofol_iv_min': round(PedsCalculator.propofol_rsi_iv_min(weight_kg), 2),
                    'propofol_iv_max': round(PedsCalculator.propofol_rsi_iv_max(weight_kg), 2),
                    'rocuronium': round(PedsCalculator.rocuronium_rsi(weight_kg), 2),
                    'sugammadex': round(PedsCalculator.sugammadex_rsi(weight_kg), 2),
                },
            },
            'analgesia': {
                'fentanyl_nasal': round(PedsCalculator.fentanyl_nasal(weight_kg), 2),
                'diamorphine_nasal': round(PedsCalculator.diamorphine_nasal(weight_kg), 2),
                'ketamine_nasal': round(PedsCalculator.ketamine_nasal(weight_kg), 2),
                'ketamine_im': round(PedsCalculator.ketamine_im(weight_kg), 2),
                'paracetamol_iv': round(PedsCalculator.paracetamol_iv(weight_kg), 0),
                'morphine_iv': f"{round(PedsCalculator.morphine_iv_min(weight_kg), 2)} - {round(PedsCalculator.morphine_iv_max(weight_kg), 2)}",
                'fentanyl_iv': f"{round(PedsCalculator.fentanyl_iv_min(weight_kg), 2)} - {round(PedsCalculator.fentanyl_iv_max(weight_kg), 2)}",
                'ketamine_iv': f"{round(PedsCalculator.ketamine_iv_min(weight_kg), 2)} - {round(PedsCalculator.ketamine_iv_max(weight_kg), 2)}",
            },
            'circulation': {
                'crystalloid_bolus': PedsCalculator.crystalloid_bolus(weight_kg),
                'blood_transfusion': PedsCalculator.blood_transfusion(weight_kg),
                'ffp_transfusion': PedsCalculator.ffp_transfusion(weight_kg),
                'platelets_transfusion': PedsCalculator.platelets_transfusion(weight_kg),
                'tranexamic_acid_bolus': round(PedsCalculator.tranexamic_acid_bolus(weight_kg), 0),
                'tranexamic_acid_infusion': PedsCalculator.tranexamic_acid_infusion(weight_kg),
                'calcium_chloride': PedsCalculator.calcium_chloride(weight_kg),
            },
            'emergency_drugs': {
                'adrenaline': round(PedsCalculator.adrenaline(weight_kg), 0),
                'atropine': round(PedsCalculator.atropine(weight_kg), 0),
                'lorazepam': round(PedsCalculator.lorazepam(weight_kg), 2),
            },
            'disability': {
                'hypertonic_saline': PedsCalculator.hypertonic_saline(weight_kg),
                'mannitol_20percent': PedsCalculator.mannitol_20percent(weight_kg),
                'dextrose_10percent': round(PedsCalculator.dextrose_10percent(weight_kg), 1),
            },
            'energy': {
                'defibrillation': round(PedsCalculator.defibrillation_energy(weight_kg), 1),
            }
        }
        
        return jsonify(results)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
