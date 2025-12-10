Here's an analysis of the provided COBOL programs, formatted in markdown as requested:

## LTCAL032 Analysis

### Files Accessed and Description

This program does not explicitly access any files in the `FILE-CONTROL` section. However, it uses a `COPY` statement to include the `LTDRG031` copybook, which likely contains data used for DRG calculations.

*   **LTDRG031:** Copybook containing DRG-related data (e.g., relative weights, average lengths of stay).

### Data Structures in WORKING-STORAGE SECTION

*   **01 W-STORAGE-REF**:  (PIC X(46))  Contains a string identifying the program and that it's the working storage.
*   **01 CAL-VERSION**: (PIC X(05)) Contains the version of the calculation logic. Value is 'C03.2'.
*   **01 HOLD-PPS-COMPONENTS**: This group of data items stores various components used in the PPS (Prospective Payment System) calculations.
    *   **05 H-LOS**:  (PIC 9(03)) Length of Stay.
    *   **05 H-REG-DAYS**: (PIC 9(03)) Regular Days.
    *   **05 H-TOTAL-DAYS**: (PIC 9(05)) Total Days.
    *   **05 H-SSOT**: (PIC 9(02)) Short Stay Outlier Threshold.
    *   **05 H-BLEND-RTC**: (PIC 9(02)) Blend Return Code.
    *   **05 H-BLEND-FAC**: (PIC 9(01)V9(01)) Blend Facility Percentage.
    *   **05 H-BLEND-PPS**: (PIC 9(01)V9(01)) Blend PPS Percentage.
    *   **05 H-SS-PAY-AMT**: (PIC 9(07)V9(02)) Short Stay Payment Amount.
    *   **05 H-SS-COST**: (PIC 9(07)V9(02)) Short Stay Cost.
    *   **05 H-LABOR-PORTION**: (PIC 9(07)V9(06)) Labor Portion of Payment.
    *   **05 H-NONLABOR-PORTION**: (PIC 9(07)V9(06)) Non-Labor Portion of Payment.
    *   **05 H-FIXED-LOSS-AMT**: (PIC 9(07)V9(02)) Fixed Loss Amount.
    *   **05 H-NEW-FAC-SPEC-RATE**: (PIC 9(05)V9(02)) New Facility Specific Rate.
*   **01 PRICER-OPT-VERS-SW**: This group contains a switch to indicate if all tables are passed or just the provider record.
    *   **05 PRICER-OPTION-SW**: (PIC X(01))  Switch indicator.
        *   **88 ALL-TABLES-PASSED**: (VALUE 'A')  Indicates all tables are passed.
        *   **88 PROV-RECORD-PASSED**: (VALUE 'P') Indicates only the provider record is passed.
    *   **05 PPS-VERSIONS**: Group to hold the version of the PPS related programs.
        *   **10 PPDRV-VERSION**: (PIC X(05)) Version of the PPDRV program.
*   **01 PROV-NEW-HOLD**: This group of data items holds provider record information.
    *   **02 PROV-NEWREC-HOLD1**:
        *   **05 P-NEW-NPI10**:  NPI (National Provider Identifier)
            *   **10 P-NEW-NPI8**: (PIC X(08))  NPI (first 8 characters).
            *   **10 P-NEW-NPI-FILLER**: (PIC X(02)) Filler for NPI.
        *   **05 P-NEW-PROVIDER-NO**: (PIC X(06)) Provider Number.
        *   **05 P-NEW-DATE-DATA**: Date related data.
            *   **10 P-NEW-EFF-DATE**: Effective Date
                *   **15 P-NEW-EFF-DT-CC**: (PIC 9(02)) Century of Effective Date.
                *   **15 P-NEW-EFF-DT-YY**: (PIC 9(02)) Year of Effective Date.
                *   **15 P-NEW-EFF-DT-MM**: (PIC 9(02)) Month of Effective Date.
                *   **15 P-NEW-EFF-DT-DD**: (PIC 9(02)) Day of Effective Date.
            *   **10 P-NEW-FY-BEGIN-DATE**: Fiscal Year Begin Date
                *   **15 P-NEW-FY-BEG-DT-CC**: (PIC 9(02)) Century of FY Begin Date.
                *   **15 P-NEW-FY-BEG-DT-YY**: (PIC 9(02)) Year of FY Begin Date.
                *   **15 P-NEW-FY-BEG-DT-MM**: (PIC 9(02)) Month of FY Begin Date.
                *   **15 P-NEW-FY-BEG-DT-DD**: (PIC 9(02)) Day of FY Begin Date.
            *   **10 P-NEW-REPORT-DATE**: Report Date
                *   **15 P-NEW-REPORT-DT-CC**: (PIC 9(02)) Century of Report Date.
                *   **15 P-NEW-REPORT-DT-YY**: (PIC 9(02)) Year of Report Date.
                *   **15 P-NEW-REPORT-DT-MM**: (PIC 9(02)) Month of Report Date.
                *   **15 P-NEW-REPORT-DT-DD**: (PIC 9(02)) Day of Report Date.
            *   **10 P-NEW-TERMINATION-DATE**: Termination Date
                *   **15 P-NEW-TERM-DT-CC**: (PIC 9(02)) Century of Termination Date.
                *   **15 P-NEW-TERM-DT-YY**: (PIC 9(02)) Year of Termination Date.
                *   **15 P-NEW-TERM-DT-MM**: (PIC 9(02)) Month of Termination Date.
                *   **15 P-NEW-TERM-DT-DD**: (PIC 9(02)) Day of Termination Date.
        *   **05 P-NEW-WAIVER-CODE**: (PIC X(01)) Waiver Code.
            *   **88 P-NEW-WAIVER-STATE**: (VALUE 'Y') Indicates the waiver state.
        *   **05 P-NEW-INTER-NO**: (PIC 9(05)) Internal Number.
        *   **05 P-NEW-PROVIDER-TYPE**: (PIC X(02)) Provider Type.
        *   **05 P-NEW-CURRENT-CENSUS-DIV**: (PIC 9(01)) Current Census Division.
        *   **05 P-NEW-MSA-DATA**: MSA (Metropolitan Statistical Area) Data.
            *   **10 P-NEW-CHG-CODE-INDEX**: (PIC X) Charge Code Index.
            *   **10 P-NEW-GEO-LOC-MSAX**: (PIC X(04)) Geographic Location MSA (Just Right).
            *   **10 P-NEW-WAGE-INDEX-LOC-MSA**: (PIC X(04)) Wage Index Location MSA (Just Right).
            *   **10 P-NEW-STAND-AMT-LOC-MSA**: (PIC X(04)) Standard Amount Location MSA (Just Right).
            *   **10 P-NEW-SOL-COM-DEP-HOSP-YR**: (PIC XX) Solitary, Community, Dependent Hospital Year.
            *   **05 P-NEW-LUGAR**: (PIC X) Lugar.
            *   **05 P-NEW-TEMP-RELIEF-IND**: (PIC X) Temporary Relief Indicator.
            *   **05 P-NEW-FED-PPS-BLEND-IND**: (PIC X) Federal PPS Blend Indicator.
            *   **05 FILLER**: (PIC X(05)) Filler.
    *   **02 PROV-NEWREC-HOLD2**:
        *   **05 P-NEW-VARIABLES**:
            *   **10 P-NEW-FAC-SPEC-RATE**: (PIC 9(05)V9(02)) Facility Specific Rate.
            *   **10 P-NEW-COLA**: (PIC 9(01)V9(03)) COLA (Cost of Living Adjustment).
            *   **10 P-NEW-INTERN-RATIO**: (PIC 9(01)V9(04)) Intern Ratio.
            *   **10 P-NEW-BED-SIZE**: (PIC 9(05)) Bed Size.
            *   **10 P-NEW-OPER-CSTCHG-RATIO**: (PIC 9(01)V9(03)) Operating Cost-to-Charge Ratio.
            *   **10 P-NEW-CMI**: (PIC 9(01)V9(04)) CMI (Case Mix Index).
            *   **10 P-NEW-SSI-RATIO**: (PIC V9(04)) SSI Ratio.
            *   **10 P-NEW-MEDICAID-RATIO**: (PIC V9(04)) Medicaid Ratio.
            *   **10 P-NEW-PPS-BLEND-YR-IND**: (PIC 9(01)) PPS Blend Year Indicator.
            *   **10 P-NEW-PRUF-UPDTE-FACTOR**: (PIC 9(01)V9(05)) PRUF Update Factor.
            *   **10 P-NEW-DSH-PERCENT**: (PIC V9(04)) DSH (Disproportionate Share Hospital) Percent.
            *   **10 P-NEW-FYE-DATE**: (PIC X(08)) Fiscal Year End Date.
        *   **05 FILLER**: (PIC X(23)) Filler.
    *   **02 PROV-NEWREC-HOLD3**:
        *   **05 P-NEW-PASS-AMT-DATA**:
            *   **10 P-NEW-PASS-AMT-CAPITAL**: (PIC 9(04)V99) Passed Amount - Capital.
            *   **10 P-NEW-PASS-AMT-DIR-MED-ED**: (PIC 9(04)V99) Passed Amount - Direct Medical Education.
            *   **10 P-NEW-PASS-AMT-ORGAN-ACQ**: (PIC 9(04)V99) Passed Amount - Organ Acquisition.
            *   **10 P-NEW-PASS-AMT-PLUS-MISC**: (PIC 9(04)V99) Passed Amount - Plus Miscellaneous.
        *   **05 P-NEW-CAPI-DATA**:
            *   **15 P-NEW-CAPI-PPS-PAY-CODE**: (PIC X) CAPI PPS Pay Code.
            *   **15 P-NEW-CAPI-HOSP-SPEC-RATE**: (PIC 9(04)V99) CAPI Hospital Specific Rate.
            *   **15 P-NEW-CAPI-OLD-HARM-RATE**: (PIC 9(04)V99) CAPI Old Harm Rate.
            *   **15 P-NEW-CAPI-NEW-HARM-RATIO**: (PIC 9(01)V9999) CAPI New Harm Ratio.
            *   **15 P-NEW-CAPI-CSTCHG-RATIO**: (PIC 9V999) CAPI Cost-to-Charge Ratio.
            *   **15 P-NEW-CAPI-NEW-HOSP**: (PIC X) CAPI New Hospital.
            *   **15 P-NEW-CAPI-IME**: (PIC 9V9999) CAPI IME.
            *   **15 P-NEW-CAPI-EXCEPTIONS**: (PIC 9(04)V99) CAPI Exceptions.
        *   **05 FILLER**: (PIC X(22)) Filler.
*   **01 WAGE-NEW-INDEX-RECORD**: This group contains Wage Index information.
    *   **05 W-MSA**: (PIC X(4)) MSA (Metropolitan Statistical Area) code.
    *   **05 W-EFF-DATE**: (PIC X(8)) Effective Date.
    *   **05 W-WAGE-INDEX1**: (PIC S9(02)V9(04)) Wage Index 1.
    *   **05 W-WAGE-INDEX2**: (PIC S9(02)V9(04)) Wage Index 2.
    *   **05 W-WAGE-INDEX3**: (PIC S9(02)V9(04)) Wage Index 3.

### Data Structures in LINKAGE SECTION

*   **01 BILL-NEW-DATA**: This structure represents the bill data passed *to* the program.
    *   **10 B-NPI10**: NPI (National Provider Identifier)
        *   **15 B-NPI8**: (PIC X(08))  NPI (first 8 characters).
        *   **15 B-NPI-FILLER**: (PIC X(02)) Filler for NPI.
    *   **10 B-PROVIDER-NO**: (PIC X(06)) Provider Number.
    *   **10 B-PATIENT-STATUS**: (PIC X(02)) Patient Status.
    *   **10 B-DRG-CODE**: (PIC X(03)) DRG (Diagnosis Related Group) Code.
    *   **10 B-LOS**: (PIC 9(03)) Length of Stay.
    *   **10 B-COV-DAYS**: (PIC 9(03)) Covered Days.
    *   **10 B-LTR-DAYS**: (PIC 9(02)) Lifetime Reserve Days.
    *   **10 B-DISCHARGE-DATE**: Discharge Date
        *   **15 B-DISCHG-CC**: (PIC 9(02)) Century of Discharge Date.
        *   **15 B-DISCHG-YY**: (PIC 9(02)) Year of Discharge Date.
        *   **15 B-DISCHG-MM**: (PIC 9(02)) Month of Discharge Date.
        *   **15 B-DISCHG-DD**: (PIC 9(02)) Day of Discharge Date.
    *   **10 B-COV-CHARGES**: (PIC 9(07)V9(02)) Covered Charges.
    *   **10 B-SPEC-PAY-IND**: (PIC X(01)) Special Payment Indicator.
    *   **10 FILLER**: (PIC X(13)) Filler.
*   **01 PPS-DATA-ALL**:  This structure is used to pass the calculated PPS data back *to* the calling program.
    *   **05 PPS-RTC**: (PIC 9(02)) Return Code.  Indicates the result of the calculation.
    *   **05 PPS-CHRG-THRESHOLD**: (PIC 9(07)V9(02)) Charge Threshold.
    *   **05 PPS-DATA**:
        *   **10 PPS-MSA**: (PIC X(04)) MSA (Metropolitan Statistical Area) code.
        *   **10 PPS-WAGE-INDEX**: (PIC 9(02)V9(04)) Wage Index.
        *   **10 PPS-AVG-LOS**: (PIC 9(02)V9(01)) Average Length of Stay.
        *   **10 PPS-RELATIVE-WGT**: (PIC 9(01)V9(04)) Relative Weight.
        *   **10 PPS-OUTLIER-PAY-AMT**: (PIC 9(07)V9(02)) Outlier Payment Amount.
        *   **10 PPS-LOS**: (PIC 9(03)) Length of Stay.
        *   **10 PPS-DRG-ADJ-PAY-AMT**: (PIC 9(07)V9(02)) DRG Adjusted Payment Amount.
        *   **10 PPS-FED-PAY-AMT**: (PIC 9(07)V9(02)) Federal Payment Amount.
        *   **10 PPS-FINAL-PAY-AMT**: (PIC 9(07)V9(02)) Final Payment Amount.
        *   **10 PPS-FAC-COSTS**: (PIC 9(07)V9(02)) Facility Costs.
        *   **10 PPS-NEW-FAC-SPEC-RATE**: (PIC 9(07)V9(02)) New Facility Specific Rate.
        *   **10 PPS-OUTLIER-THRESHOLD**: (PIC 9(07)V9(02)) Outlier Threshold.
        *   **10 PPS-SUBM-DRG-CODE**: (PIC X(03)) Submitted DRG Code.
        *   **10 PPS-CALC-VERS-CD**: (PIC X(05)) Calculation Version Code.
        *   **10 PPS-REG-DAYS-USED**: (PIC 9(03)) Regular Days Used.
        *   **10 PPS-LTR-DAYS-USED**: (PIC 9(03)) Lifetime Reserve Days Used.
        *   **10 PPS-BLEND-YEAR**: (PIC 9(01)) Blend Year.
        *   **10 PPS-COLA**: (PIC 9(01)V9(03)) COLA (Cost of Living Adjustment).
        *   **10 FILLER**: (PIC X(04)) Filler.
    *   **05 PPS-OTHER-DATA**:
        *   **10 PPS-NAT-LABOR-PCT**: (PIC 9(01)V9(05)) National Labor Percentage.
        *   **10 PPS-NAT-NONLABOR-PCT**: (PIC 9(01)V9(05)) National Non-Labor Percentage.
        *   **10 PPS-STD-FED-RATE**: (PIC 9(05)V9(02)) Standard Federal Rate.
        *   **10 PPS-BDGT-NEUT-RATE**: (PIC 9(01)V9(03)) Budget Neutrality Rate.
        *   **10 FILLER**: (PIC X(20)) Filler.
    *   **05 PPS-PC-DATA**:
        *   **10 PPS-COT-IND**: (PIC X(01)) Cost Outlier Indicator.
        *   **10 FILLER**: (PIC X(20)) Filler.
*   **01 PRICER-OPT-VERS-SW**: This group contains a switch to indicate if all tables are passed or just the provider record.
    *   **05 PRICER-OPTION-SW**: (PIC X(01))  Switch indicator.
        *   **88 ALL-TABLES-PASSED**: (VALUE 'A')  Indicates all tables are passed.
        *   **88 PROV-RECORD-PASSED**: (VALUE 'P') Indicates only the provider record is passed.
    *   **05 PPS-VERSIONS**: Group to hold the version of the PPS related programs.
        *   **10 PPDRV-VERSION**: (PIC X(05)) Version of the PPDRV program.
*   **01 PROV-NEW-HOLD**: This group of data items holds provider record information.
    *   **02 PROV-NEWREC-HOLD1**:
        *   **05 P-NEW-NPI10**:  NPI (National Provider Identifier)
            *   **10 P-NEW-NPI8**: (PIC X(08))  NPI (first 8 characters).
            *   **10 P-NEW-NPI-FILLER**: (PIC X(02)) Filler for NPI.
        *   **05 P-NEW-PROVIDER-NO**: (PIC X(06)) Provider Number.
        *   **05 P-NEW-DATE-DATA**: Date related data.
            *   **10 P-NEW-EFF-DATE**: Effective Date
                *   **15 P-NEW-EFF-DT-CC**: (PIC 9(02)) Century of Effective Date.
                *   **15 P-NEW-EFF-DT-YY**: (PIC 9(02)) Year of Effective Date.
                *   **15 P-NEW-EFF-DT-MM**: (PIC 9(02)) Month of Effective Date.
                *   **15 P-NEW-EFF-DT-DD**: (PIC 9(02)) Day of Effective Date.
            *   **10 P-NEW-FY-BEGIN-DATE**: Fiscal Year Begin Date
                *   **15 P-NEW-FY-BEG-DT-CC**: (PIC 9(02)) Century of FY Begin Date.
                *   **15 P-NEW-FY-BEG-DT-YY**: (PIC 9(02)) Year of FY Begin Date.
                *   **15 P-NEW-FY-BEG-DT-MM**: (PIC 9(02)) Month of FY Begin Date.
                *   **15 P-NEW-FY-BEG-DT-DD**: (PIC 9(02)) Day of FY Begin Date.
            *   **10 P-NEW-REPORT-DATE**: Report Date
                *   **15 P-NEW-REPORT-DT-CC**: (PIC 9(02)) Century of Report Date.
                *   **15 P-NEW-REPORT-DT-YY**: (PIC 9(02)) Year of Report Date.
                *   **15 P-NEW-REPORT-DT-MM**: (PIC 9(02)) Month of Report Date.
                *   **15 P-NEW-REPORT-DT-DD**: (PIC 9(02)) Day of Report Date.
            *   **10 P-NEW-TERMINATION-DATE**: Termination Date
                *   **15 P-NEW-TERM-DT-CC**: (PIC 9(02)) Century of Termination Date.
                *   **15 P-NEW-TERM-DT-YY**: (PIC 9(02)) Year of Termination Date.
                *   **15 P-NEW-TERM-DT-MM**: (PIC 9(02)) Month of Termination Date.
                *   **15 P-NEW-TERM-DT-DD**: (PIC 9(02)) Day of Termination Date.
        *   **05 P-NEW-WAIVER-CODE**: (PIC X(01)) Waiver Code.
            *   **88 P-NEW-WAIVER-STATE**: (VALUE 'Y') Indicates the waiver state.
        *   **05 P-NEW-INTER-NO**: (PIC 9(05)) Internal Number.
        *   **05 P-NEW-PROVIDER-TYPE**: (PIC X(02)) Provider Type.
        *   **05 P-NEW-CURRENT-CENSUS-DIV**: (PIC 9(01)) Current Census Division.
        *   **05 P-NEW-MSA-DATA**: MSA (Metropolitan Statistical Area) Data.
            *   **10 P-NEW-CHG-CODE-INDEX**: (PIC X) Charge Code Index.
            *   **10 P-NEW-GEO-LOC-MSAX**: (PIC X(04)) Geographic Location MSA (Just Right).
            *   **10 P-NEW-WAGE-INDEX-LOC-MSA**: (PIC X(04)) Wage Index Location MSA (Just Right).
            *   **10 P-NEW-STAND-AMT-LOC-MSA**: (PIC X(04)) Standard Amount Location MSA (Just Right).
            *   **10 P-NEW-SOL-COM-DEP-HOSP-YR**: (PIC XX) Solitary, Community, Dependent Hospital Year.
            *   **05 P-NEW-LUGAR**: (PIC X) Lugar.
            *   **05 P-NEW-TEMP-RELIEF-IND**: (PIC X) Temporary Relief Indicator.
            *   **05 P-NEW-FED-PPS-BLEND-IND**: (PIC X) Federal PPS Blend Indicator.
            *   **05 FILLER**: (PIC X(05)) Filler.
    *   **02 PROV-NEWREC-HOLD2**:
        *   **05 P-NEW-VARIABLES**:
            *   **10 P-NEW-FAC-SPEC-RATE**: (PIC 9(05)V9(02)) Facility Specific Rate.
            *   **10 P-NEW-COLA**: (PIC 9(01)V9(03)) COLA (Cost of Living Adjustment).
            *   **10 P-NEW-INTERN-RATIO**: (PIC 9(01)V9(04)) Intern Ratio.
            *   **10 P-NEW-BED-SIZE**: (PIC 9(05)) Bed Size.
            *   **10 P-NEW-OPER-CSTCHG-RATIO**: (PIC 9(01)V9(03)) Operating Cost-to-Charge Ratio.
            *   **10 P-NEW-CMI**: (PIC 9(01)V9(04)) CMI (Case Mix Index).
            *   **10 P-NEW-SSI-RATIO**: (PIC V9(04)) SSI Ratio.
            *   **10 P-NEW-MEDICAID-RATIO**: (PIC V9(04)) Medicaid Ratio.
            *   **10 P-NEW-PPS-BLEND-YR-IND**: (PIC 9(01)) PPS Blend Year Indicator.
            *   **10 P-NEW-PRUF-UPDTE-FACTOR**: (PIC 9(01)V9(05)) PRUF Update Factor.
            *   **10 P-NEW-DSH-PERCENT**: (PIC V9(04)) DSH (Disproportionate Share Hospital) Percent.
            *   **10 P-NEW-FYE-DATE**: (PIC X(08)) Fiscal Year End Date.
        *   **05 FILLER**: (PIC X(23)) Filler.
    *   **02 PROV-NEWREC-HOLD3**:
        *   **05 P-NEW-PASS-AMT-DATA**:
            *   **10 P-NEW-PASS-AMT-CAPITAL**: (PIC 9(04)V99) Passed Amount - Capital.
            *   **10 P-NEW-PASS-AMT-DIR-MED-ED**: (PIC 9(04)V99) Passed Amount - Direct Medical Education.
            *   **10 P-NEW-PASS-AMT-ORGAN-ACQ**: (PIC 9(04)V99) Passed Amount - Organ Acquisition.
            *   **10 P-NEW-PASS-AMT-PLUS-MISC**: (PIC 9(04)V99) Passed Amount - Plus Miscellaneous.
        *   **05 P-NEW-CAPI-DATA**:
            *   **15 P-NEW-CAPI-PPS-PAY-CODE**: (PIC X) CAPI PPS Pay Code.
            *   **15 P-NEW-CAPI-HOSP-SPEC-RATE**: (PIC 9(04)V99) CAPI Hospital Specific Rate.
            *   **15 P-NEW-CAPI-OLD-HARM-RATE**: (PIC 9(04)V99) CAPI Old Harm Rate.
            *   **15 P-NEW-CAPI-NEW-HARM-RATIO**: (PIC 9(01)V9999) CAPI New Harm Ratio.
            *   **15 P-NEW-CAPI-CSTCHG-RATIO**: (PIC 9V999) CAPI Cost-to-Charge Ratio.
            *   **15 P-NEW-CAPI-NEW-HOSP**: (PIC X) CAPI New Hospital.
            *   **15 P-NEW-CAPI-IME**: (PIC 9V9999) CAPI IME.
            *   **15 P-NEW-CAPI-EXCEPTIONS**: (PIC 9(04)V99) CAPI Exceptions.
        *   **05 FILLER**: (PIC X(22)) Filler.
*   **01 WAGE-NEW-INDEX-RECORD**: This structure is used to pass the Wage Index data back *to* the calling program.
    *   **05 W-MSA**: (PIC X(4)) MSA (Metropolitan Statistical Area) code.
    *   **05 W-EFF-DATE**: (PIC X(8)) Effective Date.
    *   **05 W-WAGE-INDEX1**: (PIC S9(02)V9(04)) Wage Index 1.
    *   **05 W-WAGE-INDEX2**: (PIC S9(02)V9(04)) Wage Index 2.
    *   **05 W-WAGE-INDEX3**: (PIC S9(02)V9(04)) Wage Index 3.

## LTCAL042 Analysis

### Files Accessed and Description

This program does not explicitly access any files in the `FILE-CONTROL` section. However, it uses a `COPY` statement to include the `LTDRG031` copybook, which likely contains data used for DRG calculations.

*   **LTDRG031:** Copybook containing DRG-related data (e.g., relative weights, average lengths of stay).

### Data Structures in WORKING-STORAGE SECTION

*   **01 W-STORAGE-REF**:  (PIC X(46))  Contains a string identifying the program and that it's the working storage.
*   **01 CAL-VERSION**: (PIC X(05)) Contains the version of the calculation logic. Value is 'C04.2'.
*   **01 HOLD-PPS-COMPONENTS**: This group of data items stores various components used in the PPS (Prospective Payment System) calculations.
    *   **05 H-LOS**:  (PIC 9(03)) Length of Stay.
    *   **05 H-REG-DAYS**: (PIC 9(03)) Regular Days.
    *   **05 H-TOTAL-DAYS**: (PIC 9(05)) Total Days.
    *   **05 H-SSOT**: (PIC 9(02)) Short Stay Outlier Threshold.
    *   **05 H-BLEND-RTC**: (PIC 9(02)) Blend Return Code.
    *   **05 H-BLEND-FAC**: (PIC 9(01)V9(01)) Blend Facility Percentage.
    *   **05 H-BLEND-PPS**: (PIC 9(01)V9(01)) Blend PPS Percentage.
    *   **05 H-SS-PAY-AMT**: (PIC 9(07)V9(02)) Short Stay Payment Amount.
    *   **05 H-SS-COST**: (PIC 9(07)V9(02)) Short Stay Cost.
    *   **05 H-LABOR-PORTION**: (PIC 9(07)V9(06)) Labor Portion of Payment.
    *   **05 H-NONLABOR-PORTION**: (PIC 9(07)V9(06)) Non-Labor Portion of Payment.
    *   **05 H-FIXED-LOSS-AMT**: (PIC 9(07)V9(02)) Fixed Loss Amount.
    *   **05 H-NEW-FAC-SPEC-RATE**: (PIC 9(05)V9(02)) New Facility Specific Rate.
    *   **05 H-LOS-RATIO**: (PIC 9(01)V9(05)) Length of Stay Ratio.
*   **01 PRICER-OPT-VERS-SW**: This group contains a switch to indicate if all tables are passed or just the provider record.
    *   **05 PRICER-OPTION-SW**: (PIC X(01))  Switch indicator.
        *   **88 ALL-TABLES-PASSED**: (VALUE 'A')  Indicates all tables are passed.
        *   **88 PROV-RECORD-PASSED**: (VALUE 'P') Indicates only the provider record is passed.
    *   **05 PPS-VERSIONS**: Group to hold the version of the PPS related programs.
        *   **10 PPDRV-VERSION**: (PIC X(05)) Version of the PPDRV program.
*   **01 PROV-NEW-HOLD**: This group of data items holds provider record information.
    *   **02 PROV-NEWREC-HOLD1**:
        *   **05 P-NEW-NPI10**:  NPI (National Provider Identifier)
            *   **10 P-NEW-NPI8**: (PIC X(08))  NPI (first 8 characters).
            *   **10 P-NEW-NPI-FILLER**: (PIC X(02)) Filler for NPI.
        *   **05 P-NEW-PROVIDER-NO**: (PIC X(06)) Provider Number.
        *   **05 P-NEW-DATE-DATA**: Date related data.
            *   **10 P-NEW-EFF-DATE**: Effective Date
                *   **15 P-NEW-EFF-DT-CC**: (PIC 9(02)) Century of Effective Date.
                *   **15 P-NEW-EFF-DT-YY**: (PIC 9(02)) Year of Effective Date.
                *   **15 P-NEW-EFF-DT-MM**: (PIC 9(02)) Month of Effective Date.
                *   **15 P-NEW-EFF-DT-DD**: (PIC 9(02)) Day of Effective Date.
            *   **10 P-NEW-FY-BEGIN-DATE**: Fiscal Year Begin Date
                *   **15 P-NEW-FY-BEG-DT-CC**: (PIC 9(02)) Century of FY Begin Date.
                *   **15 P-NEW-FY-BEG-DT-YY**: (PIC 9(02)) Year of FY Begin Date.
                *   **15 P-NEW-FY-BEG-DT-MM**: (PIC 9(02)) Month of FY Begin Date.
                *   **15 P-NEW-FY-BEG-DT-DD**: (PIC 9(02)) Day of FY Begin Date.
            *   **10 P-NEW-REPORT-DATE**: Report Date
                *   **15 P-NEW-REPORT-DT-CC**: (PIC 9(02)) Century of Report Date.
                *   **15 P-NEW-REPORT-DT