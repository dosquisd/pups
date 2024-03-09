import os
import pandas as pd
from dotenv import load_dotenv
load_dotenv()


def search_account(username: str, password: str) -> tuple[bool, str]:
    df_accounts: pd.DataFrame = pd.read_csv('files/student.csv', delimiter=';')
    df_accounts = df_accounts.astype(str)

    sub_df: pd.DataFrame = df_accounts.loc[(df_accounts['username'] == username)
                                           & (df_accounts['password'] == password)]

    return len(sub_df) > 0, str(sub_df['id'])


def login_validating(username: str, password: str) -> tuple[str, str]:
    # Validate if it's an admin
    if os.getenv('ADMIN_USER') == username and os.getenv('ADMIN_PASSWORD') == password:
        return 'admin', ''

    if (out := search_account(username, password))[0]:
        return 'student', out[1]

    return '', ''
