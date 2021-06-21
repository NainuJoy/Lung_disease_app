import random

R_P1 = "Viruses, bacteria, and fungi can all cause pneumonia. In the United States, common causes of viral pneumonia are influenza, respiratory syncytial virus (RSV), and SARS-CoV-2 (the virus that causes COVID-19). A common cause of bacterial pneumonia is Streptococcus pneumonia ."

R_ADVICE = "If I were you, I would go to the internet and type exactly what you wrote there!"
R_P2 = """The first symptoms of pneumonia usually resemble those of a cold or flu. The person then develops a high fever, chills, and cough with sputum.
\n\nCommon symptoms include:\n\n* cough\n* rusty or green phlegm, or sputum, coughed up from lungs\n* fever\n* fast breathing and shortness of breath\n* shaking chills
chest pain that usually worsens when taking a deep breath, known as pleuritic pain\n* fast heartbeat\n* fatigue and weakness\n* nausea and vomiting\n* diarrhea\n* sweating
\n* headache\n* muscle pain\n* confusion or delirium, especially in older adults\n* dusky or purplish skin color, or cyanosis, from poorly oxygenated blood
\n\nSymptoms can vary depending on other underlying conditions and the type of pneumonia"""
R_P3 = """Depending on the cause of pneumonia, a doctor will prescribe medication to treat the infection.\n\nDuring recovery, they will also recommend:
\n\n* getting plenty of rest\n* eating nutritious foods\n* drinking lots of fluids\n* saltwater gargle\n* drinking ginger or turmeric tea"""

R_E1 = """Emphysema is a lung condition that causes shortness of breath. In people with emphysema, the air sacs in the lungs (alveoli) are damaged. Over time, the inner walls of the air sacs weaken and rupture — creating larger air spaces instead of many small ones."""
R_E2 = """ The main cause of emphysema is long-term exposure to airborne irritants, including:\n\n* Tobacco smoke\n* Marijuana smoke\n* Air pollution\n* Chemical fumes and dust
\n\nRarely, emphysema is caused by an inherited deficiency of a protein that protects the elastic structures in the lungs. It's called alpha-1-antitrypsin deficiency emphysema."""
R_F1 = """Fibrosis, also known as fibrotic scarring, is a pathological wound healing in which connective tissue replaces normal parenchymal tissue to the extent that it goes unchecked, leading to considerable tissue remodelling and the formation of permanent scar tissue."""
R_F2 = """The main symptoms of pulmonary fibrosis are: breathlessness. a cough that doesn't go away. feeling tired all the time.\n\n * Shortness of breath, particularly during exercise.\n* Dry, hacking cough.\n* Fast, shallow breathing.\n* Gradual unintended weight loss.\n* Tiredness.
\n* Aching joints and muscles.\n* Clubbing (widening and rounding) of the tips of the fingers or toes."""
R_F3 = """Pulmonary fibrosis can occur at any age but usually happens between the ages 50 and 70."""
def unknown():
    response = ["...... ",
                "...",
                "------------",
                "-------"][
        random.randrange(4)]
    return response