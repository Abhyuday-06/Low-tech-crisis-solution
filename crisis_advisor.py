# --- Part B: The Data Pipeline ---
# These functions are for processing raw sensor logs into clean data.

def clean_data_batch(raw_data_lines, col_types, missing_val_char=''):
    """
    Main pipeline function.
    Takes a list of raw string lines (e.g., from a sensor log).
    Processes them column by column based on expected types.

    col_types: A list of tuples, e.g., [('num', 'median'), ('cat', 'mode'), ('num', 'mean')]
    """
    parsed_data = []
    for line in raw_data_lines:
        if not line:
            continue
        parts = line.strip().split(',') # comma separated values
        parsed_data.append(parts)

    if not parsed_data:
        return [], {} 

    num_cols = len(parsed_data[0])
    cleaned_data = [[] for _ in range(num_cols)]
    col_mappings = {} 

    for i in range(num_cols):
        col_type, measure = col_types[i]
        column_data = []
        for row in parsed_data:
            if i < len(row):
                column_data.append(row[i])
            else:
                column_data.append(missing_val_char) 

        if col_type == 'num':
            num_column = []
            for val in column_data:
                if val == missing_val_char:
                    num_column.append(None)
                else:
                    try:
                        num_column.append(float(val))
                    except ValueError:
                        num_column.append(None) 

            filled_column = handle_missing_numerical(num_column, measure)
            cleaned_data[i] = normalize_numerical(filled_column)

        elif col_type == 'cat':
            filled_column = handle_missing_categorical(column_data, measure, missing_val_char)
            encoded_col, mapping = encode_categorical(filled_column)
            cleaned_data[i] = encoded_col
            col_mappings[i] = mapping

    final_rows = []
    num_rows = len(cleaned_data[0])
    for i in range(num_rows):
        row = []
        for j in range(num_cols):
            row.append(cleaned_data[j][i])
        final_rows.append(row)

    return final_rows, col_mappings

def handle_missing_numerical(column, measure='median'):
    """Fills None values in a numerical list."""

    valid_data = [x for x in column if x is not None]
    if not valid_data:
        return [0.0] * len(column) 

    replacement = 0.0
    if measure == 'mean':
        replacement = sum(valid_data) / len(valid_data)
    elif measure == 'median':
        sorted_data = sorted(valid_data)
        mid = len(sorted_data) // 2
        if len(sorted_data) % 2 == 0:
            replacement = (sorted_data[mid - 1] + sorted_data[mid]) / 2.0
        else:
            replacement = sorted_data[mid]

    filled_column = []
    for val in column:
        if val is None:
            filled_column.append(replacement)
        else:
            filled_column.append(val)
    return filled_column

def handle_missing_categorical(column, measure='mode', missing_val_char=''):
    """Fills missing string values in a list."""
    counts = {}
    for val in column:
        if val != missing_val_char:
            counts[val] = counts.get(val, 0) + 1

    if not counts:
        replacement = 'unknown' 
    else:
        replacement = max(counts.items(), key=lambda item: item[1])[0]

    filled_column = []
    for val in column:
        if val == missing_val_char:
            filled_column.append(replacement)
        else:
            filled_column.append(val)
    return filled_column

def encode_categorical(column):
    """Converts a list of strings to a list of integers."""
    mapping = {}
    reverse_mapping = {}
    encoded_column = []
    next_id = 0

    for val in column:
        if val not in mapping:
            mapping[val] = next_id
            reverse_mapping[next_id] = val
            next_id += 1
        encoded_column.append(mapping[val])

    return encoded_column, reverse_mapping

def normalize_numerical(column):
    """Min-Max scaling (0 to 1)."""
    min_val = min(column)
    max_val = max(column)
    val_range = max_val - min_val

    if val_range == 0:
        return [0.0] * len(column)

    return [(x - min_val) / val_range for x in column]

# --- Part A: Crisis Advisor ---
# This is a hard coded decision tree to advice on medical and weather crises.

def advise_medical(symptoms):
    """
    Takes a dictionary of symptoms and returns a string advice.
    This is a "Decision Tree" implemented as if/elif/else.

    Expected symptoms keys:
    'fever' (bool), 'dizzy' (bool), 'headache' (str: none/mild/severe),
    'cough' (str: none/dry/wet), 'skin_pinch' (str: fast/slow)
    """
    # Rule 1: Dehydration
    if symptoms.get('dizzy') and symptoms.get('skin_pinch') == 'slow' and not symptoms.get('fever'):
        return "ADVICE : Probable dehydration. Give patient 1 liter of water with 1tsp salt and 6tsp sugar. Monitor."

    # Rule 2: Severe Infection / Sepsis warning
    if symptoms.get('fever') and symptoms.get('headache') == 'severe' and symptoms.get('dizzy'):
        return "CRITICAL: Fever + Severe Headache + Dizziness. Possible severe infection (e.g., meningitis) or other critical issue. Monitor vital signs CONSTANTLY. Attempt to cool patient with damp cloths. Isolate if possible."

    # Rule 3: Respiratory Infection
    if symptoms.get('fever') and symptoms.get('cough') in ('dry', 'wet'):
        if symptoms.get('cough') == 'wet':
            return "ADVICE: Probable respiratory infection (e.g., pneumonia). Keep patient warm, hydrated. Have them cough to clear lungs. Monitor breathing."
        else:
            return "ADVICE: Probable respiratory infection (e.g., flu/cold). Hydration and rest. Isolate from others."

    # Rule 4: Simple exhaustion / low blood sugar
    if symptoms.get('dizzy') and symptoms.get('headache') == 'mild' and not symptoms.get('fever'):
        return "ADVICE : Possible exhaustion or low blood sugar. Give water and a small amount of sugar/food. Rest for 1 hour."

    # Rule 5: Concussion check
    if symptoms.get('headache') == 'severe' and symptoms.get('dizzy') and not symptoms.get('fever'):
        return "WARNING: Check for recent head injury. Possible concussion. Wake patient every 2 hours (if sleeping) to check alertness. Do not give painkillers."

    return "INFO: Symptoms inconclusive. Monitor patient, ensure hydration and rest."

def advise_weather(sensors):
    """
    Takes a dictionary of sensor readings and returns a string advice.

    Expected sensor keys:
    'baro_trend' (str: falling_fast/falling/steady/rising)
    'wind_speed' (int: knots)
    'cloud_type' (str: none/high_wispy/dark_low/layered_grey)
    """
    # Rule 1: Immediate severe storm
    if sensors.get('baro_trend') == 'falling_fast':
        return "CRITICAL : Barometer is crashing. Severe storm or high-wind event imminent (< 3 hours). SECURE ALL SHELTER. GO INDOORS NOW."

    # Rule 2: Approaching storm
    if sensors.get('baro_trend') == 'falling' and sensors.get('cloud_type') == 'dark_low':
        if sensors.get('wind_speed') > 20:
            return "WARNING : Storm approaching (4-8 hours). Winds are already high. Secure camp. Prepare for heavy rain."
        else:
            return "ADVICE: Storm likely (6-12 hours). Barometer falling and clouds lowering. Begin preparations."

    # Rule 3: Bad weather, but stable
    if sensors.get('baro_trend') == 'steady' and sensors.get('cloud_type') == 'layered_grey':
        return "INFO: Weather is poor but stable. Drizzle or light rain likely, but no severe storm indicated. Standard precautions."
    
    # Rule 4: Improving weather
    if sensors.get('baro_trend') == 'rising':
        if sensors.get('cloud_type') == 'none' or sensors.get('cloud_type') == 'high_wispy':
             return "INFO: Weather is clear or improving. Good conditions for travel or outdoor work."
        else:
             return "INFO: Barometer rising, weather should improve. Remaining clouds will likely clear."

    return "INFO: Sensor readings inconclusive. Use visual observation."

# --- Part C: Text Based Interface ---

def get_input(prompt, valid_options=None):
    """Helper function to get validated user input."""
    while True:
        print(prompt)
        if valid_options:
            print(f"   (Options: {', '.join(valid_options)})")
        
        try:
            val = input("> ").strip().lower()
        except EOFError:
            val = 'q' 
            
        if val == 'help':
            print("\nHELP: Type your answer from the options list. Type 'q' to quit to main menu.\n")
            continue
            
        if not valid_options:
            return val 
        
        if val in valid_options:
            return val
        else:
            print(f"Error: Invalid input. Please choose from: {', '.join(valid_options)}")

def run_medical_ui():
    """UI for the medical advisor."""
    print("\n--- Medical Advisor ---")
    print("Answer the following. Type 'help' for help, 'q' to quit.")
    
    symptoms = {}
    
    # Question 1
    val = get_input("Does the patient have a fever?", ['y', 'n', 'q'])
    if val == 'q': return
    symptoms['fever'] = (val == 'y')
    
    # Question 2
    val = get_input("Is the patient dizzy or light-headed?", ['y', 'n', 'q'])
    if val == 'q': return
    symptoms['dizzy'] = (val == 'y')
    
    # Question 3
    val = get_input("Headache severity?", ['none', 'mild', 'severe', 'q'])
    if val == 'q': return
    symptoms['headache'] = val
    
    # Question 4
    val = get_input("Cough type?", ['none', 'dry', 'wet', 'q'])
    if val == 'q': return
    symptoms['cough'] = val
    
    # Question 5
    print("Gently pinch the skin on the back of the patient's hand.")
    val = get_input("Does the skin snap back fast, or return slowly?", ['fast', 'slow', 'q'])
    if val == 'q': return
    symptoms['skin_pinch'] = val
    
    advice = advise_medical(symptoms)
    print("\n" + "-"*100)
    print(advice)
    print("-"*100 + "\n")
    input("Press Enter to continue...")

def run_weather_ui():
    """UI for the weather advisor."""
    print("\n--- Weather Advisor ---")
    print("Enter current sensor readings. Type 'help' for help, 'q' to quit.")

    sensors = {}

    # Question 1
    val = get_input("Barometer trend?", ['falling_fast', 'falling', 'steady', 'rising', 'q'])
    if val == 'q': return
    sensors['baro_trend'] = val
    
    # Question 2
    val = get_input("Cloud type?", ['none', 'high_wispy', 'dark_low', 'layered_grey', 'q'])
    if val == 'q': return
    sensors['cloud_type'] = val

    # Question 3
    while True:
        val_str = get_input("Current wind speed (knots)? (e.g., 5)", None)
        if val_str == 'q': return
        try:
            sensors['wind_speed'] = int(val_str)
            break
        except ValueError:
            print("Error: Please enter a whole number.")
            
    advice = advise_weather(sensors)
    print("\n" + "-"*100)
    print(advice)
    print("-"*100 + "\n")
    input("Press Enter to continue...")

def run_pipeline_demo():
    """Demo for the data pipeline."""
    print("\n--- Data Pipeline ---")
    raw_data = [
        "25.5,cloudy,1010.2",
        "26.1,rain,1009.1",
        ",cloudy,1008.5", # Missing temp
        "24.9,clear,1011.0",
        "25.2,,1011.5", # Missing weather
        "bad_data,rain,1009.0" # Bad temp
    ]
    
    print("Temp, Weather, Pressure\n")
    for line in raw_data:
        print(line)
        
    col_types = [('num', 'median'), ('cat', 'mode'), ('num', 'mean')]
    
    print("\nRunning pipeline...")
    cleaned, mappings = clean_data_batch(raw_data, col_types, missing_val_char='')
    
    print("\nPipeline Complete.")
    print("\nCleaned & Normalized Data:")
    for row in cleaned:
        print([round(val, 2) if isinstance(val, float) else val for val in row])
        
    print("\nCategorical Mappings:")
    print(mappings)
    input("\nPress Enter to continue...")


def main():
    """Main application loop."""
    print("-"*100)
    print("  Powering up Crisis Advisor...")
    print("-"*100)
    
    while True:
        print("\n--- MAIN MENU ---")
        print("What do you need help with?")
        print("  1: Medical Advisor")
        print("  2: Weather Advisor")
        print("  3: Run Data Pipeline")
        print("  q: Quit")
        
        try:
            choice = input("Enter choice: ").strip().lower()
        except EOFError:
            choice = 'q'
        
        if choice == '1':
            run_medical_ui()
        elif choice == '2':
            run_weather_ui()
        elif choice == '3':
            run_pipeline_demo()
        elif choice == 'q':
            print("Powering down advisor...")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, or q.")

if __name__ == "__main__":
    main()
