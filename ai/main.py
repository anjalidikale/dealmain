# ============================================================
# FILE: main.py
# Hospital Triage + AI Discharge Summary
# ============================================================

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Database functions
from database import (
    get_patient,
    get_all_patients,
    get_patient_discharge_data
)


# AI functions
from triage_ai import run_triage, generate_discharge_summary


# ============================================================
# CREATE FASTAPI APP
# ============================================================

app = FastAPI(
    title='Hospital Triage Assistant',
    description='AI-powered patient triage and discharge summary using Groq AI + MySQL',
    version='1.0.0'
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)


# ============================================================
# STATIC FILES
# ============================================================

app.mount('/static', StaticFiles(directory='.'), name='static')


# ============================================================
# ROUTE 1: HOME PAGE
# ============================================================

@app.get('/')
def root():
    return FileResponse('index.html')


# ============================================================
# ROUTE 2: GET ALL PATIENTS
# ============================================================

@app.get('/patients')
def list_patients():

    try:
        patients = get_all_patients()

        return {
            'patients': patients
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f'Database error: {str(e)}'
        )


# ============================================================
# ROUTE 3: AI TRIAGE
#
# POST /triage/{patient_id}
#
# Example:
# POST /triage/10
# ============================================================

@app.post('/triage/{patient_id}')
def triage_patient(patient_id: int):

    # Get patient from database
    patient = get_patient_discharge_data(patient_id)


    # Patient not found
    if not patient:

        raise HTTPException(
            status_code=404,
            detail=f'Patient with ID {patient_id} not found.'
        )

    # Run AI triage
    try:

        result = run_triage(patient)

        return result

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f'AI triage failed: {str(e)}'
        )


# ============================================================
# ROUTE 4: AI DISCHARGE SUMMARY
#
# POST /discharge-summary/{patient_id}
#
# Example:
# POST /discharge-summary/10
# ============================================================

@app.post('/discharge-summary/{patient_id}')
def discharge_summary(patient_id: int):

    # Step 1: Get patient from database
    patient = get_patient(patient_id)

    # Step 2: Patient not found
    if not patient:

        raise HTTPException(
            status_code=404,
            detail=f'Patient with ID {patient_id} not found.'
        )

    # Step 3: Generate discharge summary
    try:

        result = generate_discharge_summary(patient)

        return result

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f'Discharge summary generation failed: {str(e)}'
        )