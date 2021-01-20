"""
Utility math functions

Lukas Adamowicz
Pfizer DMTI 2021
"""
from numpy import moveaxis

from skimu.utility import _extensions


__all__ = ["rolling_mean", "rolling_sd", "rolling_skewness", "rolling_kurtosis"]


def rolling_mean(a, w_len, skip, axis=-1):
    r"""
    Compute the rolling mean.

    Parameters
    ----------
    a : array-like
        Signal to compute rolling mean for.
    w_len : int
        Window length in number of samples.
    skip : int
        Window start location skip in number of samples.
    axis : int, optional
        Axis to compute the rolling mean along. Default is -1.

    Returns
    -------
    rmean : numpy.ndarray
        Rolling mean. Note that if the rolling axis is not the last axis, then the result
        will *not* be c-contiguous.

    Notes
    -----
    On the rolling axis, the output length can be computed as follows:

    .. math:: \frac{n - w_{len}}{skip} + 1

    where `n` is the length of the rolling axis.

    Examples
    --------
    Compute the with non-overlapping windows:

    >>> import numpy as np
    >>> x = np.arange(10)
    >>> rolling_mean(x, 3, 3)
    array([1., 4., 7.])

    Compute with overlapping windows:

    >>> rolling_mean(x, 3, 1)
    array([1., 2., 3., 4., 5., 6., 7., 8.])

    Compute on a nd-array to see output shape. On the rolling axis, the output should be equal to
    :math:`(n - w_{len}) / skip + 1`.

    >>> n = 500
    >>> window_length = 100
    >>> window_skip = 50
    >>> shape = (3, n, 5, 10)
    >>> y = np.random.random(shape)
    >>> res = rolling_mean(y, window_length, window_skip, axis=1)
    >>> print(res.shape)
    (3, 9, 5, 10)

    Check flags for different axis output

    >>> z = np.random.random((10, 10, 10))
    >>> rolling_mean(z, 3, 3, axis=0).flags['C_CONTIGUOUS']
    False

    >>> rolling_mean(z, 3, 3, axis=1).flags['C_CONTIGUOUS']
    False

    >>> rolling_mean(z, 3, 3, axis=2).flags['C_CONTIGUOUS']
    True
    """
    if w_len <= 0 or skip <= 0:
        raise ValueError("`wlen` and `skip` cannot be less than or equal to 0.")

    # move computation axis to end
    x = moveaxis(a, axis, -1)

    # check that there are enough samples
    if w_len > x.shape[-1]:
        raise ValueError("Cannot have a window length larger than the computation axis.")

    rmean = _extensions.rolling_mean(x, w_len, skip)

    # move computation axis back to original place and return
    return moveaxis(rmean, -1, axis)


def rolling_sd(a, w_len, skip, axis=-1, return_previous=True):
    r"""
    Compute the rolling sample standard deviation.

    Parameters
    ----------
    a : array-like
        Signal to compute rolling sample standard deviation for.
    w_len : int
        Window length in number of samples.
    skip : int
        Window start location skip in number of samples.
    axis : int, optional
        Axis to compute the rolling mean along. Default is -1.
    return_previous : bool, optional
        Return previous moments. These are computed either way, and are therefore optional returns.
        Default is True.

    Returns
    -------
    rsd : numpy.ndarray
        Rolling sample standard deviation. Note that if the rolling axis is not the last axis,
        then the result will *not* be c-contiguous.
    rmean : numpy.ndarray, optional.
        Rolling mean. Note that if the rolling axis is not the last axis, then the result
        will *not* be c-contiguous. Only returned if `return_previous=True`.

    Notes
    -----
    On the rolling axis, the output length can be computed as follows:

    .. math:: \frac{n - w_{len}}{skip} + 1

    where `n` is the length of the rolling axis.

    Examples
    --------
    Compute the with non-overlapping windows:

    >>> import numpy as np
    >>> x = np.arange(10)**2
    >>> rolling_sd(x, 3, 3, return_previous=True)
    (array([ 2.081666  ,  8.02080628, 14.0118997 ]),
     array([ 1.66666667, 16.66666667, 49.66666667]))

    Compute with overlapping windows:

    >>> rolling_mean(x, 3, 1, return_previous=False)
    array([ 2.081666  ,  4.04145188,  6.02771377,  8.02080628, 10.0166528 ,
           12.01388086, 14.0118997 , 16.01041328])

    Compute on a nd-array to see output shape. On the rolling axis, the output should be equal to
    :math:`(n - w_{len}) / skip + 1`.

    >>> n = 500
    >>> window_length = 100
    >>> window_skip = 50
    >>> shape = (3, n, 5, 10)
    >>> y = np.random.random(shape)
    >>> res = rolling_sd(y, window_length, window_skip, axis=1, return_previous=False)
    >>> print(res.shape)
    (3, 9, 5, 10)

    Check flags for different axis output

    >>> z = np.random.random((10, 10, 10))
    >>> rolling_sd(z, 3, 3, axis=0, return_previous=False).flags['C_CONTIGUOUS']
    False

    >>> rolling_sd(z, 3, 3, axis=1, return_previous=False).flags['C_CONTIGUOUS']
    False

    >>> rolling_sd(z, 3, 3, axis=2, return_previous=False).flags['C_CONTIGUOUS']
    True
    """
    if w_len <= 0 or skip <= 0:
        raise ValueError("`wlen` and `skip` cannot be less than or equal to 0.")

    # move computation axis to end
    x = moveaxis(a, axis, -1)

    # check that there are enough samples
    if w_len > x.shape[-1]:
        raise ValueError("Cannot have a window length larger than the computation axis.")

    res = _extensions.rolling_sd(x, w_len, skip, return_previous)

    # move computation axis back to original place and return
    if return_previous:
        return moveaxis(res[0], -1, axis), moveaxis(res[1], -1, axis)
    else:
        return moveaxis(res, -1, axis)


def rolling_skewness(a, w_len, skip, axis=-1, return_previous=True):
    r"""
    Compute the rolling sample skewness.

    Parameters
    ----------
    a : array-like
        Signal to compute rolling skewness for.
    w_len : int
        Window length in number of samples.
    skip : int
        Window start location skip in number of samples.
    axis : int, optional
        Axis to compute the rolling mean along. Default is -1.
    return_previous : bool, optional
        Return previous moments. These are computed either way, and are therefore optional returns.
        Default is True.

    Returns
    -------
    rskew : numpy.ndarray
        Rolling skewness. Note that if the rolling axis is not the last axis,
        then the result will *not* be c-contiguous.
    rsd : numpy.ndarray, optional
        Rolling sample standard deviation. Note that if the rolling axis is not the last axis,
        then the result will *not* be c-contiguous. Only returned if `return_previous=True`.
    rmean : numpy.ndarray, optional.
        Rolling mean. Note that if the rolling axis is not the last axis, then the result
        will *not* be c-contiguous. Only returned if `return_previous=True`.

    Notes
    -----
    On the rolling axis, the output length can be computed as follows:

    .. math:: \frac{n - w_{len}}{skip} + 1

    where `n` is the length of the rolling axis.

    Examples
    --------
    Compute the with non-overlapping windows:

    >>> import numpy as np
    >>> x = np.arange(10)**2
    >>> rolling_skewness(x, 3, 3, return_previous=True)
    (array([0.52800497, 0.15164108, 0.08720961]),
     array([ 2.081666  ,  8.02080628, 14.0118997 ]),
     array([ 1.66666667, 16.66666667, 49.66666667]))

    Compute with overlapping windows:

    >>> rolling_skewness(x, 3, 1, return_previous=False)
    array([0.52800497, 0.29479961, 0.20070018, 0.15164108, 0.12172925,
           0.10163023, 0.08720961, 0.07636413])

    Compute on a nd-array to see output shape. On the rolling axis, the output should be equal to
    :math:`(n - w_{len}) / skip + 1`.

    >>> n = 500
    >>> window_length = 100
    >>> window_skip = 50
    >>> shape = (3, n, 5, 10)
    >>> y = np.random.random(shape)
    >>> res = rolling_skewness(y, window_length, window_skip, axis=1, return_previous=False)
    >>> print(res.shape)
    (3, 9, 5, 10)

    Check flags for different axis output

    >>> z = np.random.random((10, 10, 10))
    >>> rolling_skewness(z, 3, 3, axis=0, return_previous=False).flags['C_CONTIGUOUS']
    False

    >>> rolling_skewness(z, 3, 3, axis=1, return_previous=False).flags['C_CONTIGUOUS']
    False

    >>> rolling_skewness(z, 3, 3, axis=2, return_previous=False).flags['C_CONTIGUOUS']
    True
    """
    if w_len <= 0 or skip <= 0:
        raise ValueError("`wlen` and `skip` cannot be less than or equal to 0.")

    # move computation axis to end
    x = moveaxis(a, axis, -1)

    # check that there are enough samples
    if w_len > x.shape[-1]:
        raise ValueError("Cannot have a window length larger than the computation axis.")

    res = _extensions.rolling_skewness(x, w_len, skip, return_previous)

    # move computation axis back to original place and return
    if return_previous:
        return tuple(moveaxis(i, -1, axis) for i in res)
    else:
        return moveaxis(res, -1, axis)


def rolling_kurtosis(a, w_len, skip, axis=-1, return_previous=True):
    r"""
    Compute the rolling sample kurtosis.

    Parameters
    ----------
    a : array-like
        Signal to compute rolling kurtosis for.
    w_len : int
        Window length in number of samples.
    skip : int
        Window start location skip in number of samples.
    axis : int, optional
        Axis to compute the rolling mean along. Default is -1.
    return_previous : bool, optional
        Return previous moments. These are computed either way, and are therefore optional returns.
        Default is True.

    Returns
    -------
    rkurt : numpy.ndarray
        Rolling kurtosis. Note that if the rolling axis is not the last axis,
        then the result will *not* be c-contiguous.
    rskew : numpy.ndarray, optional
        Rolling skewness. Note that if the rolling axis is not the last axis,
        then the result will *not* be c-contiguous. Only returned if `return_previous=True`.
    rsd : numpy.ndarray, optional
        Rolling sample standard deviation. Note that if the rolling axis is not the last axis,
        then the result will *not* be c-contiguous. Only returned if `return_previous=True`.
    rmean : numpy.ndarray, optional.
        Rolling mean. Note that if the rolling axis is not the last axis, then the result
        will *not* be c-contiguous. Only returned if `return_previous=True`.

    Notes
    -----
    On the rolling axis, the output length can be computed as follows:

    .. math:: \frac{n - w_{len}}{skip} + 1

    where `n` is the length of the rolling axis.

    Examples
    --------
    Compute the with non-overlapping windows:

    >>> import numpy as np
    >>> x = np.arange(10)**2
    >>> rolling_kurtosis(x, 3, 3, return_previous=True)
    (array([-1.5, -1.5, -1.5]),  # kurtosis
     array([0.52800497, 0.15164108, 0.08720961]),  # skewness
     array([ 2.081666  ,  8.02080628, 14.0118997 ]),  # standard deviation
     array([ 1.66666667, 16.66666667, 49.66666667]))  # mean

    Compute with overlapping windows:

    >>> rolling_kurtosis(np.random.random(100), 50, 20, return_previous=False)
    array([-1.10155074, -1.20785479, -1.24363625])  # random

    Compute on a nd-array to see output shape. On the rolling axis, the output should be equal to
    :math:`(n - w_{len}) / skip + 1`.

    >>> n = 500
    >>> window_length = 100
    >>> window_skip = 50
    >>> shape = (3, n, 5, 10)
    >>> y = np.random.random(shape)
    >>> res = rolling_skewness(y, window_length, window_skip, axis=1, return_previous=False)
    >>> print(res.shape)
    (3, 9, 5, 10)

    Check flags for different axis output

    >>> z = np.random.random((10, 10, 10))
    >>> rolling_kurtosis(z, 3, 3, axis=0, return_previous=False).flags['C_CONTIGUOUS']
    False

    >>> rolling_kurtosis(z, 3, 3, axis=1, return_previous=False).flags['C_CONTIGUOUS']
    False

    >>> rolling_kurtosis(z, 3, 3, axis=2, return_previous=False).flags['C_CONTIGUOUS']
    True
    """
    if w_len <= 0 or skip <= 0:
        raise ValueError("`wlen` and `skip` cannot be less than or equal to 0.")

    # move computation axis to end
    x = moveaxis(a, axis, -1)

    # check that there are enough samples
    if w_len > x.shape[-1]:
        raise ValueError("Cannot have a window length larger than the computation axis.")

    res = _extensions.rolling_kurtosis(x, w_len, skip, return_previous)

    # move computation axis back to original place and return
    if return_previous:
        return tuple(moveaxis(i, -1, axis) for i in res)
    else:
        return moveaxis(res, -1, axis)