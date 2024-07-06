from dataloader import create_cursor
import pandas as pd
import pandas as pd
import numpy as np
import pickle

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import GridSearchCV
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error

CONNN, CURSOR = create_cursor()


def get_data_transform() -> pd.DataFrame:

    CURSOR.execute("""
        SELECT 
            Country,
            EdLevel,
            YearsCodePro,
            Employment,
            Salary
        FROM 
        survey
    """)
    df = pd.DataFrame(CURSOR.fetchall(), columns=[
        'Country',
        'EdLevel',
        'YearsCodePro',
        'Employment',
        'Salary'
        ]
    )

    df = df[df['Employment'] == 'Employed, full-time']
    df = df.drop('Employment', axis=1)

    return df


def _shorten_categories(categories, cutoff):
    cat_map = {}
    for c in range(len(categories)):
        if categories.values[c] >= cutoff:
            cat_map[categories.index[c]] = categories.index[c]
        else:
            cat_map[categories.index[c]] = 'Other'
    return cat_map


def remove_red(df):
    country_map = _shorten_categories(df.Country.value_counts(), 400)
    df['Country'] = df['Country'].map(country_map)
    df = df[df['Salary'] <= 250_000]
    df = df[df['Salary'] >= 10_000]
    df = df[df['Salary'] != 'Other']

    return df


def clean_expr(x):
    if x == 'More than 50 years':
        return 50
    elif x == 'Less than 1 year':
        return 0.5
    return float(x)


def clean_edu(x):
    if 'Bachelor’s degree' in x:
        return "Bachelor's degree"
    elif  'Master’s degree' in x:
        return "Master's degree"
    elif 'Professional degree' in x or 'Other doctoral' in x:
        return 'Post grad'
    return 'Less than a Bachelors'


def data_label(df):
    le_education = LabelEncoder()
    df['EdLevel'] = le_education.fit_transform(df['EdLevel'])
    df['EdLevel'].unique()
    le_country = LabelEncoder()
    df['Country'] = le_country.fit_transform(df['Country'])
    x = df.drop('Salary', axis=1)
    y = df['Salary']

    return ((x, y), (le_education, le_country))


if __name__ == '__main__':
    df = get_data_transform()
    df = remove_red(df)
    df['YearsCodePro'] = df['YearsCodePro'].apply(clean_expr)
    df['EdLevel'] = df['EdLevel'].apply(clean_edu)

    x,y = data_label(df)[0]
    le_education, le_country = data_label(df)[1]

    max_depth = [None, 2, 4, 6, 8, 10, 12]
    parameters = {'max_depth': max_depth}
    regressor = DecisionTreeRegressor(random_state=0)
    gs = GridSearchCV(regressor, parameters, scoring='neg_mean_squared_error')
    gs.fit(x, y.values)
    regressor = gs.best_estimator_

    regressor.fit(x, y.values)
    y_pred = regressor.predict(x)
    error = np.sqrt(mean_absolute_error(y, y_pred))
    print(f'MEAN ABSOLUTE ERROR: {error}')
    
    #x = np.array([['United States of America', "Master's degree", 15]])
    #print(x)
    #x[:, 0] = le_country.transform(x[:, 0])
    #x[:, 1] = le_education.transform(x[:, 1])
    #x = x.astype(float)
    #y_pred = regressor.predict(x)
    
    data = {
        'model': regressor,
        'le_country': le_country,
        'le_education': le_education
    }
    
    with open('./data/steps.pkl', 'wb') as file:
        pickle.dump(data, file)
    print('DATA LOADED')