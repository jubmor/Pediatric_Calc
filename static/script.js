// DOM Elements
const ageYearsInput = document.getElementById('age_years');
const ageMonthsInput = document.getElementById('age_months');
const weightKgInput = document.getElementById('weight_kg');
const calculateBtn = document.getElementById('calculate-btn');
const resetBtn = document.getElementById('reset-btn');
const inputSection = document.querySelector('.input-section');
const resultsSection = document.getElementById('results-section');

// Event Listeners
calculateBtn.addEventListener('click', performCalculation);
resetBtn.addEventListener('click', resetCalculator);

// Allow Enter key to calculate
document.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && document.activeElement !== resetBtn) {
        performCalculation();
    }
});

async function performCalculation() {
    try {
        // Validate inputs
        const ageYears = ageYearsInput.value ? parseFloat(ageYearsInput.value) : null;
        const ageMonths = ageMonthsInput.value ? parseFloat(ageMonthsInput.value) : null;
        const weightKg = weightKgInput.value ? parseFloat(weightKgInput.value) : null;

        if (!ageYears && !ageMonths && !weightKg) {
            showError('Please enter age (years or months) or weight');
            return;
        }

        // Show loading state
        calculateBtn.disabled = true;
        calculateBtn.textContent = 'Calculating...';

        // Call the API
        const response = await fetch('/api/calculate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                age_years: ageYears,
                age_months: ageMonths,
                weight_kg: weightKg
            })
        });

        if (!response.ok) {
            const error = await response.json();
            showError(error.error || 'Calculation failed');
            return;
        }

        const results = await response.json();
        displayResults(results, ageYears, ageMonths);

        // Scroll to results
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });

    } catch (error) {
        showError('Error: ' + error.message);
    } finally {
        calculateBtn.disabled = false;
        calculateBtn.textContent = 'Calculate';
    }
}

function displayResults(data, ageYears, ageMonths) {
    // Display weight
    document.getElementById('result_weight').textContent = data.weight_kg + ' kg';

    // Airway Section
    document.getElementById('result_et_tube_size').textContent = data.airway.et_tube_size + ' mm';
    document.getElementById('result_et_tube_cuff').textContent = data.airway.et_tube_cuff + ' mm';
    document.getElementById('result_et_tube_length').textContent = data.airway.et_tube_length + ' cm';
    document.getElementById('result_chest_tube').textContent = data.airway.chest_tube_size + ' Fr';
    document.getElementById('result_supraglottic').textContent = 'Size ' + data.airway.supraglottic_device;
    document.getElementById('result_tidal_volume').textContent = data.airway.ventilated_tidal_volume + ' ml';

    // RSI
    document.getElementById('result_ketamine_rsi_iv').textContent = data.airway.rsi.ketamine_iv_min + '-' + data.airway.rsi.ketamine_iv_max + ' mg';
    document.getElementById('result_ketamine_rsi_im').textContent = data.airway.rsi.ketamine_im_min + '-' + data.airway.rsi.ketamine_im_max + ' mg';
    document.getElementById('result_etomidate_rsi_iv').textContent = data.airway.rsi.etomidate_iv_min + '-' + data.airway.rsi.etomidate_iv_max + ' mg';
    document.getElementById('result_propofol_rsi_iv').textContent = data.airway.rsi.propofol_iv_min + '-' + data.airway.rsi.propofol_iv_max + ' mg';

    // Analgesia Section
    document.getElementById('result_fentanyl_nasal').textContent = data.analgesia.fentanyl_nasal + ' mcg';
    document.getElementById('result_diamorphine_nasal').textContent = data.analgesia.diamorphine_nasal + ' mg';
    document.getElementById('result_ketamine_nasal').textContent = data.analgesia.ketamine_nasal + ' mg';
    document.getElementById('result_ketamine_im').textContent = data.analgesia.ketamine_im + ' mg';
    document.getElementById('result_paracetamol_iv').textContent = data.analgesia.paracetamol_iv + ' mg';
    document.getElementById('result_morphine_iv').textContent = data.analgesia.morphine_iv + ' mg';
    document.getElementById('result_fentanyl_iv').textContent = data.analgesia.fentanyl_iv + ' mcg';
    document.getElementById('result_ketamine_iv').textContent = data.analgesia.ketamine_iv + ' mg';

    // Circulation Section
    document.getElementById('result_crystalloid').textContent = data.circulation.crystalloid_bolus;
    document.getElementById('result_blood').textContent = data.circulation.blood_transfusion;
    document.getElementById('result_ffp').textContent = data.circulation.ffp_transfusion;
    document.getElementById('result_platelets').textContent = data.circulation.platelets_transfusion;
    document.getElementById('result_txa_bolus').textContent = data.circulation.tranexamic_acid_bolus + ' mg';
    document.getElementById('result_txa_infusion').textContent = data.circulation.tranexamic_acid_infusion;
    document.getElementById('result_calcium').textContent = data.circulation.calcium_chloride;

    // Disability Section
    document.getElementById('result_hypertonic_saline').textContent = data.disability.hypertonic_saline;
    document.getElementById('result_mannitol').textContent = data.disability.mannitol_20percent;
    document.getElementById('result_dextrose').textContent = data.disability.dextrose_10percent + ' ml';

    // Emergency Drugs & Energy Section
    document.getElementById('result_adrenaline').textContent = data.emergency_drugs.adrenaline + ' mcg';
    document.getElementById('result_atropine').textContent = data.emergency_drugs.atropine + ' mcg';
    document.getElementById('result_lorazepam').textContent = data.emergency_drugs.lorazepam + ' mg';
    document.getElementById('result_defib').textContent = data.energy.defibrillation + ' J';

    // Show vital signs row based on age
    updateVitalSigns(ageYears, ageMonths);

    // Show results section
    resultsSection.style.display = 'block';

    // Remove any error messages
    removeError();
}

function updateVitalSigns(ageYears, ageMonths) {
    const vitalRows = document.querySelectorAll('#vitals-section [data-age-group]');
    const vitalSection = document.getElementById('vitals-section');
    let ageGroup = null;

    let totalYears = ageYears || 0;
    if (ageMonths) {
        totalYears += ageMonths / 12;
    }

    if (totalYears < 1) {
        ageGroup = '1month-1year';
    } else if (totalYears < 2) {
        ageGroup = '1-2';
    } else if (totalYears < 5) {
        ageGroup = '2-5';
    } else if (totalYears < 10) {
        ageGroup = '5-10';
    } else {
        ageGroup = '10+';
    }

    if (ageGroup) {
        vitalSection.style.display = 'block';
        vitalRows.forEach(row => {
            row.style.display = row.dataset.ageGroup === ageGroup ? '' : 'none';
        });
    } else {
        vitalSection.style.display = 'none';
        vitalRows.forEach(row => {
            row.style.display = 'none';
        });
    }
}

function resetCalculator() {
    ageYearsInput.value = '';
    ageMonthsInput.value = '';
    weightKgInput.value = '';
    resultsSection.style.display = 'none';
    removeError();
    ageYearsInput.focus();
}

function showError(message) {
    removeError();
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error';
    errorDiv.textContent = message;
    inputSection.insertBefore(errorDiv, inputSection.firstChild);
}

function removeError() {
    const errorDiv = inputSection.querySelector('.error');
    if (errorDiv) {
        errorDiv.remove();
    }
}

// Focus on input when page loads
window.addEventListener('load', () => {
    ageYearsInput.focus();
});
