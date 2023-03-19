# ! ./venv/bin/python3.8

"""
Script containing functions used to separate the ideal input data for linear
regression model to fill missing values that appears on a feature along the
time.
"""

from config import project_paths, log
from data.io import load_artfact
from itertools import combinations
from logging import debug, info, warning
from model.linear_regression import linear_regression, train_linear_regression
import numpy as np
import os
import pandas as pd
from sklearn.model_selection import train_test_split

log()

PATH = project_paths()
STATIC = "".join([PATH["ROOT"], PATH["DATA"]["STATIC"]])
RAW_DATA = "".join([PATH["ROOT"], PATH["DATA"]["RAW"]])
PRC_DATA = "".join([PATH["ROOT"], PATH["DATA"]["PRC"]])
MDL_DATA = "".join([PATH["ROOT"], PATH["MODEL"]])


def calculate_feature_correlation(
    data: pd.DataFrame,
    feature: str,
    group: str,
    allowed_groups: list = None,
    index: str = "Datetime",
) -> tuple([pd.DataFrame, dict]):

    """
    Calculate correlation on the same feature on a group of categories
    This works only in one feature and at time.
        Args:
            data -
                dataframe containing feature values and the group that will
                be calculated
            feature - feature column name containing its values
            group - group column name that will be evaluated
            allowed_groups -
                list with group names to exclude not included values if theres
                a restriction of which groups can be used
            [opt] index - index used to pivot and calculate correlation coef

        Output:
            a **dataframe** containing pairs of groups and their correlation
            coef and a **dict** containing feature, group name and the allowed
            list of pair groups that can be used on linear regression.

    """

    MIN_CORR = 0.8

    if allowed_groups is None:
        allowed_groups = data[group].unique()

    _allowed_groups = data[group].isin(allowed_groups)
    _cols = [index, group, feature]

    corr_feat = (
        data[_allowed_groups][_cols]
        .pivot_table(index=index, columns=group)
        .corr()
    )

    corr_feat_melted = corr_feat.melt()
    corr_feat_melted.columns = ["Feature", group, "Corr_Value"]

    _group = corr_feat_melted[group].drop_duplicates().to_list()
    corr_feat_melted[group + "_Pair"] = _group * len(_group)

    # Removing pairs without min corr coef value and themselves
    _allowed_pairs = (corr_feat_melted["Corr_Value"] >= MIN_CORR) & (
        corr_feat_melted["Corr_Value"] < 1
    )
    corr_pairs = corr_feat_melted[_allowed_pairs].copy()

    # Dictionary {station: [pair_station_allowed]}
    corr_dict = {}
    for key in corr_pairs[group].unique():
        _cond = corr_pairs[group] == key
        _pairs_list = corr_pairs[_cond][group + "_Pair"].to_list()

        _pair_combinations = []
        for pair_comb in combinations(_pairs_list, 2):
            _pair_combinations.append(list(pair_comb))

        corr_dict[key] = _pair_combinations

    return (corr_feat_melted, corr_dict)


def correlation_features_stations(
    data: pd.DataFrame,
    features_list: list,
    group: str = "Station",
    allowed_group: list = [
        "Semasa_Camilopolis",
        "Semasa_Paraiso",
        "Semasa_Tanque_Detencao",
        "Semasa_Vila_Vitoria",
        "UFABC_Solar",
    ],
) -> tuple([pd.DataFrame, dict]):

    """
    Calculate correlation coeficients for a features list by Station.\n
    This functions agreggate results for each feature considered ans returns\n
    a pandas.Dataframe and a Dictionary containing correlations values and
    pairs.
    """

    corr_dict = {}
    corr_df = pd.DataFrame()

    for fn in features_list:
        debug(fn)

        tmp_corr_df, corr_dict[fn] = calculate_feature_correlation(
            data=data, feature=fn, group=group, allowed_groups=allowed_group
        )

        corr_df = pd.concat([corr_df, tmp_corr_df])

    return corr_df, corr_dict


def data_to_train(
    data: pd.DataFrame,
    feature: str,
    filled_group: list,
    to_fill_group: str,
    group: str = "Station",
    index: str = "Datetime",
) -> tuple([np.ndarray, np.ndarray]):

    """
    From a 'feature' data and a 'group' (usualy 'Station') this function
    separate the data to the prediction and feature group data. It returns a
    tuple containing features and label data allowed to the training stage.

    Usage Examples:

        data = dataframe containing all this informations
        feature = "Air_Temperature_C"
        group = "Station"
        to_fill_group = "camilopolis"
        filled_group = dict_corr_feat_station[feature][to_fill_group]

    """

    # Stations on columns
    pivoted_data = data[[index, group, feature]].pivot_table(
        index=index, columns=group, values=feature
    )

    # Drop null rows
    _group_list = [to_fill_group] + filled_group
    pivoted_data = pivoted_data[_group_list].dropna()

    # See if there's data
    if pivoted_data.shape[0] == 0:
        warning("There's no data to train model..")
        return None, None

    # Choose label and features Dataframes
    label = pivoted_data[to_fill_group].to_numpy()
    features = pivoted_data[filled_group].to_numpy()

    return features, label


def data_to_predict(
    data: pd.DataFrame,
    feature: str,
    filled_group: list,
    to_fill_group: str,
    group: str = "Station",
    index: str = "Datetime",
) -> np.ndarray:

    """
    From a 'feature' data and a 'group' (usualy 'Station') this function
    separate the data to the prediction and feature group data. It returns a
    tuple containing array with data used to predict missing values.

    Usage Examples:

        data = dataframe containing all this informations
        feature = "Air_Temperature_C"
        group = "Station"
        to_fill_group = "camilopolis"
        filled_group = dict_corr_feat_station[feature][to_fill_group]
    """

    # Stations on columns
    pivoted_data = data[[index, group, feature]].pivot_table(
        index=index, columns=group, values=feature
    )

    # Select null rows on 'to_fill_group'
    _cond_empty_rows = pivoted_data[to_fill_group].isnull()
    pivoted_data = pivoted_data[_cond_empty_rows].copy()

    # Remove rows without data on filled groups
    filled_data = pivoted_data[filled_group].dropna()

    # See if there's data
    if filled_data.shape[0] == 0:
        warning("There's no data to predict model..")
        return None, None

    # Choose label and features Dataframes
    index = filled_data.index
    features = filled_data.to_numpy()

    return features, index


def fill_missing_values_feature(
    data: pd.DataFrame,
    feature: str,
    to_fill_group: str,
    filled_group: list,
    index: str = "Datetime",
    group: str = "Station",
    flg_use_trained_model: bool = True,
) -> pd.DataFrame:

    """
    Unit function to fill the missing specific feature values.

    A liner multiple regression model is trained from a 'data'
    dataframe for a specific 'feature' and 'to_fill_group'. From
    this, the training data are composed by data from 'filled_group'
    that can be retrieved by 'corr_dict'.

    The ouptput is the 'data' dataframe with previous missing values
    filled.

    **Args**
        data - dataframe containing index, group and feature infos
        feature - feature name (column from 'data' dataframe)
        to_fill_group - group name that will be filled
        filled_group - list of group names that will be used to
            fill another
        group - group name (column from 'data' dataframe)
        flg_use_trained_model - use trained model if exists

    **Ouptut**
        The 'data' dataframe with previous missing values filled



    """

    _model_name = "".join(
        [f"lr_{feature}_{to_fill_group}_", "_".join(filled_group)]
    )
    _model_path = f"{MDL_DATA}/fill_missing/"

    # Training =========
    if (
        os.path.isfile(f"{_model_path}{_model_name}.pickle")
        & flg_use_trained_model
    ):
        lr = load_artfact(f"{_model_path}{_model_name}.pickle")

    else:

        # Data
        train_features, train_labels = data_to_train(
            data=data,
            feature=feature,
            filled_group=filled_group,
            to_fill_group=to_fill_group,
        )

        if train_features is None:
            return data

        # Spliting into train, cv, test
        train_features, cv_features, train_labels, cv_labels = train_test_split(
            train_features, train_labels, test_size=0.3, random_state=22
        )

        cv_features, test_features, cv_labels, test_labels = train_test_split(
            cv_features, cv_labels, test_size=0.33, random_state=22
        )

        # Model
        lr = linear_regression()
        lr = train_linear_regression(
            lr, train_features, train_labels, _model_name, _model_path
        )

    # Evaluate =========
    # TODO: create a form to evaluate automatticaly.

    # Predict =========

    # Input
    predict_features, predict_idx = data_to_predict(
        data=data,
        feature=feature,
        filled_group=filled_group,
        to_fill_group=to_fill_group,
    )

    if predict_features is None:
        return data

    # Output
    fill_missing_result = pd.DataFrame(
        {
            index: predict_idx,
            group: to_fill_group,
            feature: lr.predict(predict_features),
        }
    )

    # Filling Missing Values =======

    data = pd.merge(
        data,
        fill_missing_result,
        on=["Datetime", "Station"],
        suffixes=["", "_fill"],
        how="left",
    )

    nulls_before = data[feature].isnull()
    debug(f"\t\tExisting { nulls_before.sum()} nulls")

    to_fill = data[feature + "_fill"].notnull()
    info(f"\t\tFilling {to_fill.sum()} rows")

    data.loc[to_fill, feature] = data.loc[to_fill, feature + "_fill"].values

    nulls_after = data[feature].isnull()
    debug(f"\t\tFinal shape with {nulls_after.sum()} nulls")

    assert (
        nulls_before.sum() - to_fill.sum() == nulls_after.sum()
    ), "Loc fill doesnt work correctly.. "

    return data.drop(columns=feature + "_fill")


def fill_missing_values(data: pd.DataFrame, corr_dict: dict) -> pd.DataFrame:

    """
    Main function from 'fill_missings.py' script.
    With a dictionary containing correlation coeficients 'corr_dict'
    for each feature and the list of allowed groups, this function
    is capable of predict the missing values on a 'data' dataframe.

    **Args**
        data - dataframe containing index, group and feature infos
        corr_dict -  dictionary containing correlation coeficients
            from each feature that can be predicted
    """

    for feature in corr_dict.keys():
        info(f"feature: ===== ===== {feature} ===== =====")

        for to_fill_group in corr_dict[feature]:
            info(f"\tto_fill_group: {to_fill_group}")
            filled_group_combinations = corr_dict[feature][to_fill_group]

            for filled_group in filled_group_combinations:
                info(f"\tfilled_group: {filled_group}")
                data = fill_missing_values_feature(
                    data=data,
                    feature=feature,
                    to_fill_group=to_fill_group,
                    filled_group=filled_group,
                )

    return data
