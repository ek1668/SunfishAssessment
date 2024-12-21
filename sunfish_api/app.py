from flask import Flask, request, jsonify
import csv, os

app = Flask(__name__)

mappings = {
    "endometriosis": ("formula_endometriosis_true_value", "formula_endometriosis_false_value"),
    "male_factor": ("formula_male_factor_infertility_true_value", "formula_male_factor_infertility_false_value"),
    "tubal_factor": ("formula_tubal_factor_true_value", "formula_tubal_factor_false_value"),
    "ovulatory_disorder": ("formula_ovulatory_disorder_true_value", "formula_ovulatory_disorder_false_value"),
    "diminished_ovarian_reserve": ("formula_diminished_ovarian_reserve_true_value", "formula_diminished_ovarian_reserve_false_value"),
    "uterine_factor": ("formula_uterine_factor_true_value", "formula_uterine_factor_false_value"),
    "other_infertilty_reason": ("formula_other_reason_true_value", "formula_other_reason_false_value"),
    "unexplained_infertility": ("formula_unexplained_infertility_true_value", "formula_unexplained_infertility_false_value")
}

pregnancy_mapping = {
    0: 'formula_prior_pregnancies_0_value',
    1: 'formula_prior_pregnancies_1_value',
    2: 'formula_prior_pregnancies_2+_value'
}

live_birth_mapping = {
    0: 'formula_prior_live_births_0_value',
    1: 'formula_prior_live_births_1_value',
    2: 'formula_prior_live_births_2+_value'
}

def get_pregnancy_field(value):
    if value >= 3:
        return pregnancy_mapping[2]
    return pregnancy_mapping[value]

def get_live_birth_field(value):
    if value >= 3:
        return live_birth_mapping[2]
    return live_birth_mapping[value]

def calculate_bmi(user_weight_in_lbs, user_height_in_feet, user_height_in_inches):
  bmi = user_weight_in_lbs/(user_height_in_feet * 12 + user_height_in_inches)**2 * 703
  return round(bmi, 1)

def get_cdc_formula_from_csv(own_eggs, attempted_ivf, reason_known):

    with open("sunfish_api/ivf_success_formulas.csv", mode='r') as csv_file:
        
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            # Check if the conditions match
         
            if (row['param_using_own_eggs'] == own_eggs and
                row['param_attempted_ivf_previously'] == attempted_ivf and
                row['param_is_reason_for_infertility_known'] == reason_known):
          
                return row
                # Return the entire matching row as a dictionary
        return None

def calculate_possibility(formula_values, user_age, user_bmi, input_json):
    
    prior_pregnancies = int(input_json['prior_pregnancies'])  
    prior_live_births = int(input_json['prior_live_births'])
    if prior_live_births > prior_pregnancies:
        return None

    pregnancy_field = get_pregnancy_field(prior_pregnancies)
    live_birth_field = get_live_birth_field(prior_live_births)

    pregnancy_value = float(formula_values[pregnancy_field])
    live_birth_value = float(formula_values[live_birth_field])
    
    total = sum(
    [
        float(formula_values['formula_intercept']),
        (float(formula_values['formula_age_linear_coefficient']) * int(user_age) + float(formula_values['formula_age_power_coefficient']) * (int(user_age)**float(formula_values['formula_age_power_factor']))),
        (float(formula_values['formula_bmi_linear_coefficient']) * float(user_bmi) + float(formula_values['formula_bmi_power_coefficient']) * (user_bmi**float(formula_values['formula_bmi_power_factor']))),
    ]+
    [   
        float(formula_values[mappings[key][0]] if value == "TRUE" else formula_values[mappings[key][1]]) for key, value in input_json.items() if key in mappings 
    ]+
    [
        pregnancy_value,
        live_birth_value
    ]
    )
  
    total = round(total, 6)
    total = 100 * (2.718**total/(1 + 2.718**total))
    return round(total, 2)

@app.route('/calculate_ivf/', methods=['POST'])
def calc_ivf():
  json_data = request.json
  user_bmi = calculate_bmi(json_data['user_weight_in_lbs'], json_data['user_height_in_feet'], json_data['user_height_in_inches'])
  
  formula_use = get_cdc_formula_from_csv(
      json_data['using_own_eggs'], 
      json_data['previously_attempted_ivf'], 
      json_data['reason_for_infertility_known']
      )
  
  if formula_use is None:
      return jsonify({"error":"cdc formula doesn't exist for your combination of 'using_own_eggs', 'previously_attempted_ivf', 'reason_for_infertility_known'"})

  calc_possibility = calculate_possibility(formula_use, json_data['user_age'], user_bmi, json_data)
  if calc_possibility is None:
      return jsonify({"error":"'prior_live_births' cannot exceed 'prior_pregnancies'"})
  
  return jsonify({"success_probability":f"{calc_possibility}%"})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)