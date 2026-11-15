markdown
# TB BURDEN AND RISK TOOLKIT
an educational streamlit app for TB screening, burden estimation,airbrone transmission modeling and risk-factor analysis
> ** not a diagnostic tool and clinically validated. **follow national TB program guidelines for real decisions.
## run locally
 """
  pip install streamlit pandas numpy
  streamlit run tb_toolkit.py
  """

  ## features
- **Screening:** qualitative symptom and risk-factor screen (no probability given)
- **Burden and cascade:** estimated cases, case detection ratio, case fatality, treatment success, DALYs
- **Transmission:** Wells-Riley equation, P = 1 - exp(-I·q·p·t / Q), with a ventilation (ACH) sensitivity curve
- **Risk factors:** population attributable fraction (Levin's formula), PAF = p(RR-1) / (1 + p(RR-1))
## default values
all defaults( population,icidence,diasability weight,quanta rate, breathing rate, PAF table)  are **illustrative placeholders**. Replace them with your own data or published sources before any research use.
## References

- Riley EC, Murphy G, Riley RL. Am J Epidemiol. 1978;107(5):421-432.
- Levin ML. Acta Unio Int Contra Cancrum. 1953;9:531-541.

## Citation and license

See `CITATION.cff` for how to cite this software. Released under the MIT license (see `LICENSE`).

Author: Hadeera Ali
