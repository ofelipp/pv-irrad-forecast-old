# ! ./venv/bin/python3.8

"""
Script containing linear regression model construction, training and predict
functions.
"""

from logging import debug, warning
import numpy as np
import pandas as pd


def calculate_feature_correlation(
    data: pd.DataFrame, feature: str, group: str, group_list: list = []
) -> tuple([pd.DataFrame, dict]):

    """ Calculate correlation on the same feature on a group of categories """

    MIN_CORR = 0.8

    _condition = data[group].isin(group_list)
    _cols = ["Datetime", group, feature]

    corr_feat = data[_condition][_cols].pivot_table(
        index="Datetime", columns=group
    ).corr()

    corr_feat_melted = corr_feat.melt()
    corr_feat_melted.columns = ["Feature", group, "Corr_Value"]

    _group = corr_feat_melted[group].drop_duplicates().to_list()
    corr_feat_melted[group + "_Pair"] = _group * len(_group)

    # DataFrame with available pairs and correlation values
    _available_pairs = (
        (corr_feat_melted["Corr_Value"] >= MIN_CORR)
        & (corr_feat_melted["Corr_Value"] < 1)
    )
    corr_pairs = corr_feat_melted[_available_pairs].copy()

    # Creating dictionary with available pairs
    corr_dict = {}
    for key in corr_pairs[group].unique():
        _cond = corr_pairs[group] == key
        corr_dict[key] = corr_pairs[_cond][group + "_Pair"].to_list()

    return (corr_feat_melted, corr_dict)


def correlation_features_stations(
    data: pd.DataFrame, features_list: list, group: str = "Station",
    allowed_group: list = [
        'camilopolis', 'paraiso', 'tanquedetencao', 'vila_vitoria'
    ]
) -> tuple([pd.DataFrame, dict]):

    """ Calculate correlation coeficients for a features series by Station """

    corr_dict = {}
    corr_df = pd.DataFrame()

    for fn in features_list:
        debug(fn)

        tmp_corr_df, corr_dict[fn] = calculate_feature_correlation(
            data=data, feature=fn, group=group,
            group_list=allowed_group
        )

        corr_df = pd.concat([corr_df, tmp_corr_df])

    return corr_df, corr_dict


def data_to_train(
    data: pd.DataFrame, feature: str, filled_group: list, to_fill_group: str,
    group: str = "Station", index: str = "Datetime"
) -> tuple([np.ndarray, np.ndarray]):

    """
    From a 'feature' data and a 'group' (usualy 'Station') this function
    separate the data to the prediction and feature group data. It returns a
    tuple containing features and label data allowed to the training stage.

    Usage Examples:

        feature = "Air_Temperature_C"
        group = "Station"
        to_fill_group = "camilopolis"
        filled_group = dict_corr_feat_station[feature][to_fill_group]

    """

    debug('Station to be predicted:\t', to_fill_group)
    debug('Stations used as variables:\t', filled_group)

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


def data_to_fill(
    data: pd.DataFrame, feature: str, filled_group: list, to_fill_group: str,
    group: str = "Station", index: str = "Datetime"
) -> np.ndarray:

    debug('Station to be predicted:\t', to_fill_group)
    debug('Stations used as variables:\t', filled_group)

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
        warning("There's no data to train model..")
        return None, None

    # Choose label and features Dataframes
    index = filled_data.index
    features = filled_data.to_numpy()

    return features, index
