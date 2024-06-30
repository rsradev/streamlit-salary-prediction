import pandas as pd
import psycopg2


def create_cursor():

    conn = psycopg2.connect(
        dbname='stackoverflow_survey',
        user='survey_user',
        password='password',
        host='localhost'
    )
    cursor = conn.cursor()

    return (conn, cursor)


def clean_data(
    file_name: str = './data/survey_results_public.csv'
) -> pd.DataFrame:

    df = pd.read_csv(file_name)

    df = df[
        ['Country',
         'EdLevel',
         'YearsCodePro',
         'Employment',
         'ConvertedCompYearly']
    ]

    df = df.rename({'ConvertedCompYearly': 'Salary'}, axis=1)
    df = df[df['Salary'].notnull()]
    df = df[df['YearsCodePro'].apply(lambda x: str(x).isdigit())]
    df = df[df['Salary'].notnull()]
    df = df.dropna()

    return df


def populate(df: pd.DataFrame) -> None:

    conn, cursor = create_cursor()

    cursor.execute(
        """
        TRUNCATE TABEL survey
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS survey (
            Respondent SERIAL PRIMARY KEY,
            Country TEXT,
            EdLevel TEXT,
            YearsCodePro SMALLINT,
            Employment TEXT,
            Salary FLOAT
        )
        """
    )
    for row in df.itertuples(index=False):
        cursor.execute(
            """
            INSERT INTO survey (
                Country,
                EdLevel,
                YearsCodePro,
                Employment,
                Salary
            ) VALUES (%s, %s, %s, %s, %s)
            """, (
                row.Country,
                row.EdLevel,
                row.YearsCodePro,
                row.Employment,
                row.Salary
            )
        )

    conn.commit()
    cursor.close()
    conn.close()


if __name__ == '__main__':
    df = clean_data()
    
    populate(df)
