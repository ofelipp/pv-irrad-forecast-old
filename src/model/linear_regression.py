# ! ./venv/bin/python3.8

"""
Script containing linear regression model construction, training and predict
functions.
"""

from data.io import save_artfact
from logging import debug, info
import numpy as np
from sklearn.linear_model import LinearRegression


def linear_regression():

    """Creates a linear regression model"""

    return LinearRegression()


def train_linear_regression(
    model: LinearRegression,
    features: np.ndarray,
    labels: np.ndarray,
    model_name: str,
    save_path: str,
) -> LinearRegression:

    """Train Linear Regression model to perform predictions"""

    info("===== Training Linear Regression ===== ")

    debug(f"Shape of features:\t{features.shape}")
    debug(f"Shape of labels:\t{features.shape}")

    trained_lr = model.fit(features, labels)

    info("Training complete...")

    debug(f"\tR_Squared:\t{trained_lr.score(features, labels)}")
    debug(f"\tIntercept:\t{trained_lr.intercept_}")
    debug(f"\tCoeficients:\t{trained_lr.coef_}")

    info("Saving Model pickle...")

    save_artfact(trained_lr, model_name, save_path)

    return trained_lr
