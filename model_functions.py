def predict_state_places(df, weather=None, crowd=None, famous_for=None, budget=None):
    """
    Predicts matching places for all states based on input features.
    Returns a dictionary {State: [matching places]}.
    """
    # Criteria dictionary
    criteria = {
        'Weather': weather,
        'Crowd_Level': crowd,
        'Famous_For': famous_for,
        'Budget_Level': budget
    }
    
    # Remove None values
    criteria = {k:v for k,v in criteria.items() if v is not None}
    
    # Start filtering with all criteria
    df_filtered = df.copy()
    for col, val in criteria.items():
        df_filtered = df_filtered[df_filtered[col] == val]
    
    # Relax criteria one by one if nothing found
    relax_order = list(criteria.keys())
    while df_filtered.empty and relax_order:
        relax_col = relax_order.pop()
        df_filtered = df.copy()
        for col, val in criteria.items():
            if col != relax_col:
                df_filtered = df_filtered[df_filtered[col] == val]
    
    # Group by State
    result = df_filtered.groupby('State')['Place_Name'].apply(list).to_dict()
    
    # Print in required format
    for state, places in result.items():
        print(f"State: {state}")
        for place in places:
            print(f"  - {place}")
        print("\n")
    
    return result
