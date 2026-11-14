"""
TB burden and risk toolkit - streamlit app
Run:
   pip install streamlit panadas numpy
   streamlit run tb_toolkit.py

Tabs:
1. symptoms + risk factors screening (WHO-style symptom screen)
2. Burden and care cascade (cases, detection gap,CFR,DALYS)
3. Airborne transmissions risk (Wells-Rilley equation)
4. Population attributable fraction (PAF) of TB risk factors
5. About

Educational purposes only, not as a diagnostic tool by  Dr hadeera.
"""

import math

import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(page_title="TB toolkit",layout="wide")
st.title("TB burden and risk toolkit")
st.caption("educational tool.follow national TB program guidelines for real decisions.")

t1, t2, t3, t4, t5 = st.tabs(
    ["Screening", "Burden and cascade", "transmission (Wells-Riley)", "Risk factors (PAF)", "About",]
)

#--------------------------------------------------------------------------------TAB 1
with t1:
    st.subheader("symptoms and risk-factor screen")
    c1, c2=st.columns(2)

with c1: 
    st.markdown("**symptoms**")
    cough = st.checkbox("Cough (any duration; 2+ weeks is classic)")
    hemo = st.checkbox("Coughing up blood")
    fever = st.checkbox("Fever")
    sweats = st.checkbox("Night sweats")
    w1 = st.checkbox("Unintentional weight loss")

with c2:
    st.markdown("**Risk factors**")
    rf = {
          "HIV infection": st.checkbox("HIV infection"),
          "Close contact with a TB patient": st.checkbox("Close contact with a TB patient"),
          "Diabetes": st.checkbox("Diabetes"),
          "Undernutrition (BMI < 18.5)": st.checkbox("Undernutrition (BMI < 18.5)"),
          "Smoking": st.checkbox("Current smoker"),
          "Heavy alcohol use": st.checkbox("Heavy alcohol use"),
          "Immunosuppression": st.checkbox("Steroids, cancer treatment, transplant, or biologics"),
          "Chronic kidney disease / silicosis": st.checkbox("Chronic kidney disease or silicosis"),
          "Congregate setting / health worker": st.checkbox(
           "Prison, shelter, crowded housing, or health-care worker"
            ),
         }

if st.button("access",key="screen"):
    n_sym =sum([cough, hemo, fever, sweats, w1])
    n_rf=sum(rf.values())

    if n_sym > 0:
        st.error(f"presumptive TB:{n_sym} symptoms(s) present.")
        st.write(
           "suggested work-up: sputum rapid molecular test"
           "(e.g., Xpert MTB/RIF),which also detects rifampicin resistance),"
           "chest X-ray,and drug resistance testing if positive."
            "consider infection-control measures while waiting for results."
         )
        if hemo:
            st.write("hemoptysis is a red flag for TB. consider prompt clininical evaluation.")
    elif n_rf > 0:
            st.warning("no symptoms, but risk factors are present.")
            st.write(
                "consider TB infection testing( IGRA or TST) for contacts",
                "people with HIV, and immunosupressed patients. if positive"
                "and active TB is ruled out, TB preventive treatment may apply."
        )
    else:
      st.success("no symptoms or listed risk factors. low screening concern.")

    if n_rf:
       st.write("**risk factors present:**"+",".join(k for k, v in rf.items() if v))
       st.caption("this is a qualitative screen, not a probability.")
  
#--------------------------------------------------------------------------------TAB 2
    with t2:
      st.subheader("population TB burden and care cascade")
    a, b=st.columns(2)

    with a:
        pop=st.number_input("population", min_value=1, value=1_000_000, step=10_000)
        inc=st.number_input("estimated incidence(per 100,000 per year)", min_value=0.0, value=200.0)
        notified=st.number_input("cases notified to the program", min_value=0, value=1500)
        deaths=st.number_input("TB deaths per year", min_value=0, value=100)

    with b:
       cohort=st.number_input("treatment cohort size", min_value=0.0, value=1400)
       success=st.number_input("treatment successes (cured+completed)", min_value=0.0, value=1200)
       yll_per_year=st.number_input("average year of life lost per TB death", min_value=0.0, value=30.0)
       dw=st.number_input("disability weight", min_value=0.0, max_value=1.0, value=0.33)
       dur=st.number_input("average duration of illlness(years)", min_value=0.0, value=0.5)

    est=inc*pop/100_000
    if success > cohort:
        st.warning("Treatment successes cannot exceed the cohort size.")
    if est > 0 and deaths > est:
        st.warning("deaths exceed estimated cases; check your inputs.")
        
    m=st.columns(4)
    m[0].metric("estimated cases",f"{est:,.0f}")
    if est > 0:
     m[1].metric("cases detection ratio",f"{notified/est:.0%}")
     m[2].metric("missing cases",f"{max(est-notified,0):,.0f}")
     m[3].metric("case fatality",f"{deaths/est:.1%}")

    n=st.columns(3)
    n[0].metric("TB mortality per 100,000",f"{deaths/pop*100_000:.1f}")
    if cohort > 0:
        n[1].metric("treatment success",f"{success/cohort:.0%}")

    yll=deaths*yll_per_year
    yld=est*dw*dur
    n[2].metric("DALLYs (YLL+YLD)",f"{yll+yld:,.0f}")
    st.write(
             f"YLL={yll:,.0f}  YLD={yld:,.0f}"
             f"DALYs per 100,000=={(yll+yld)/pop*100_000:,.1f}"
    )
    st.caption(
         "WHO End TB targets:80% fewer cases and 90% fewer deaths by 2030 vs 2015, "
           "and treatment sucesss of 90% or more for drug-susceptible TB is a common benchmark."
    )

 #--------------------------------------------------------------------------------TAB 3
with t3:
 st.subheader("airborne transmission risk :Wells-Rilley equation")
 st.write("P(infection)=1-exp(-I*q*p*t/Q)")
 x,y=st.columns(2)
 with x:
     n_inf=st.number_input("infectious people in the room (I)",min_value=1,value=1)
     q=st.number_input(
         "Quanta generation rate (per hour,q)",
          min_value=0.01,
          value=1.25,
          help="Highly variable : roughly 1 for a typical TB patient, "
               "much higher for super spreaders or procedures like intubation."
    )
     p=st.number_input(
       "Breathing rate of a susceptible person (m3/hour,p)",
        min_value= 0.1,
        value=0.5
     )
                    
with y:
     t = st.number_input(
                        "Exposure time (hour, t)",
                        min_value=0.1,
                        max_value=24.0,
                        value=1.0,
                    )
vol = st.number_input("Room volume (m3)", min_value=5.0, value=100.0)
ach = st.number_input("Air changes per hour (ACH)", min_value=0.1, value=2.0)

Q=ach*vol # ventilation rate m3/hour
risk=1-math.exp(-n_inf*q*p*t/Q)
st.metric("Infection probability for one exposed person",f"{risk:.1%}")

sweep=np.array([0.5,1,2,4,6,12,20])
curve=pd.DataFrame(
    {"ACH":sweep,"risk": 1-np.exp(-n_inf*q*p*t/(sweep*vol))},
     ).set_index("ACH")
st.line_chart(curve)
st.caption(
           "More ventilation lowers risk. WHO suggests 12 ACH for new"
           "airbrone-isolation rooms.Masks and UV-C add further protection."
           )

#---------------------------------------------------------------------------------TAB 4
with t4:
    st.subheader("Population attributable fraction (PAF)")
    st.write(
           "PAF=p(RR-1)/(1+p(RR-1)), where p=prevalance of the factor"
           "and RR=relative risk of TB. Replace the placeholder values below"
           "with figures from your own data or a published source."
    )
    default=pd.DataFrame(
        {
          "Risk factor":["Factor A", "Factor B","factor C"],
          "Prevalance (0-1)":[0.05, 0.01, 0.02],
             "Relative risk":[10.0, 3.0, 2.0],
        }
    )
tb1=st.data_editor(default, num_rows="dynamic",width="stretch")

if st.button("Calculate PAF"):
     d= tb1.dropna().copy()
     if d.empty:
        st.warning("Enter a least one complete row.")
     elif not d["Prevalance (0-1)"].between(0-1).all() or (d["Relative risk"] <1).any():
         st.error("Prevalance must be between 0 and 1, and relative risk must be at least 1.")
     else:
       pr,rr=d["Prevalance(0.1)"],d["Relative risk"]
       d["PAF"]=pr*(rr-1)/(1+pr*(rr-1))
       combined=1-(1-d["PAF"]).prod()
       st.dataframe(d.assign(PAF=d["PAF"].map("{:.1%}".format)),width="stretch")
       st.metric("Combined PAF(assumes independent factors)",f"{combined:.1%}")
st.caption(
         "Overlapping risk factors mean the true combined PAF is usually"
         "lower than this independent estimate."
    )
#------------------------------------------------------------------------------------TAB 5
with t5:
    st.subheader("About")
    st.write(
        "This toolkit supports TB screening, burden estimation, airbrone"
        "Transmission modeling, and risk factor analysis. It was developed"
        "in Python with Streamlit by Dr hadeera for educational use only."
    )                 
    st.write("It is not a diagnostic tool and has not been clinically valided.")
                


                       




