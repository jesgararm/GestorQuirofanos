# Métodos de codificación
import pandas as pd
import numpy as np


def codificaEstandar(df: pd.DataFrame) -> pd.DataFrame:
    """
    Codifica los datos de entrada en un formato estandarizado
    """
    # Establecemos la columna TIPO como int64
    df['TIPO'] = df['TIPO'].astype('int64')
    # Usamos One Hot Enconding para codificar la columna ESPECIALIDAD
    df['ESPECIALIDAD'] = df['ESPECIALIDAD'].astype('category')
    df = pd.get_dummies(df, columns=['ESPECIALIDAD'])
    return df


def codificaAmpliado(df: pd.DataFrame) -> pd.DataFrame:
    """
    Codifica los datos de entrada en un formato ampliado
    :param df:
    :return:
    """
    # Eliminamos la columna ESPECIALIDAD
    df = df.drop(['ESPECIALIDAD'], axis=1)
    # Codificamos el sexo de forma binaria
    df['Usuario (Sexo)'] = df['Usuario (Sexo)'].replace(['Hombre', 'Mujer'], [0, 1])
    df['Usuario (Sexo)'] = df['Usuario (Sexo)'].astype('int64')
    # Codificamos los valores de garantía y ASA de forma ordinal
    df['Garantía del procedimiento (Con garantía| Sin garantía)'] = df[
        'Garantía del procedimiento (Con garantía| Sin garantía)'].replace(
        ['Sin garantía', 'Garantía según diagnóstico', 'Con garantía'], [0, 1, 2])
    df['Garantía del procedimiento (Con garantía| Sin garantía)'] = df[
        'Garantía del procedimiento (Con garantía| Sin garantía)'].astype('int64')
    df['Asa'] = df['Asa'].replace(['ASA I', 'ASA II', 'ASA III', 'ASA IV', 'ASA V'], [1, 2, 3, 4, 5])
    df['Asa'] = df['Asa'].astype('int64')

    return df
