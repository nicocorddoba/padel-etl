from sqlalchemy import Engine
import psycopg2
import pandas as pd

def table_creator(table_name:str, df:pd.DataFrame, engine: Engine, index: bool= True):
    print(table_name)
    try:
        df.to_sql(name=table_name, con=engine, if_exists= 'fail', index=index)
    except ValueError:
        data = pd.read_sql_query(f'select * from "{table_name}"',con=engine)
        list_col = data.columns.to_list()
        df_in_data = df.merge(data, on=list_col, how='left', indicator=True)
        df_new_only = df_in_data[df_in_data['_merge'] == 'left_only'].drop(columns='_merge')
        # print(df_new_only)
        if len(df_new_only) > 0:
            df_new_only.to_sql(name=table_name, con=engine, if_exists='append',index=index)
        else: print(f'Los datos de {table_name} ya se encuentran insertados')
    except Exception as e:
        print(e)