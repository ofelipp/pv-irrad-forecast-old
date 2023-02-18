# ! ./venv/bin/python3.8

"""
Script containing
"""

from data.io import save_artfact
from logging import debug, info
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression


def calculate_feature_correlation(
    data: pd.DataFrame, feature: str, group: str, group_list: list = []
) -> tuple(pd.DataFrame, dict):

    """ Calculate correlation on the same feature on a group of categories """

    MIN_CORR = 0.8

    _condition = data[group].isin(group_list)
    _cols = ["Datetime", group, feature]

    corr_feat = data[_condition][_cols].pivot_table(
        index="Datetime", columns=group, values=feature
    ).corr()

    corr_feat_melted = corr_feat.melt(col_level=1, value_name=feature)
    _stations = corr_feat_melted[group].drop_duplicates().to_list()
    corr_feat_melted[group + "_Pair"] = _stations * len(_stations)

    # DataFrame with available pairs and correlation values
    _available_pairs = (
        (corr_feat_melted[feature] >= MIN_CORR)
        & (corr_feat_melted[feature] < 1)
    )
    corr_pairs = corr_feat_melted[_available_pairs].copy()

    # Creating dictionary with available pairs
    corr_dict = {}
    for key in corr_pairs[group].unique():
        _cond = corr_pairs[group] == key
        corr_dict[key] = corr_pairs[_cond][group + "_Pair"].to_list()

    return (corr_pairs, corr_dict)


def linear_regression():

    """ Creates a linear regression model """

    return LinearRegression()


def train_linear_regression(
    model: LinearRegression, features: np.ndarray, labels: np.ndarray,
    model_name: str = ""
) -> LinearRegression:

    """ Train Linear Regression model to perform predictions """

    debug(f"Shape of features:\t{features.shape}")
    debug(f"Shape of labels:\t{features.shape}")

    info("Starting training...")

    trained_lr = model.fit(features, labels)

    info("Training complete...")

    debug(f"R_Squared:\t{trained_lr.score(features, labels)}")
    debug(f"Intercept:\t{trained_lr.intercept_}")
    debug(f"Coeficients:\t{trained_lr.coef_}")

    info("Saving Model pickle...")

    save_artfact(trained_lr, f"linear_regression{model_name}.pickle")

    return trained_lr


def predict_linear_regression():

    """ Train Linear Regression Model """

    return ...
