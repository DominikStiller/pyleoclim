"""Tests for pyleoclim.core.ui.EnsembleSeries

Naming rules:
1. class: Test{filename}{Class}{method} with appropriate camel case
2. function: test_{method}_t{test_id}

Notes on how to test:
0. Make sure [pytest](https://docs.pytest.org) has been installed: `pip install pytest`
1. execute `pytest {directory_path}` in terminal to perform all tests in all testing files inside the specified directory
2. execute `pytest {file_path}` in terminal to perform all tests in the specified file
3. execute `pytest {file_path}::{TestClass}::{test_method}` in terminal to perform a specific test class/method inside the specified file
4. after `pip install pytest-xdist`, one may execute "pytest -n 4" to test in parallel with number of workers specified by `-n`
5. for more details, see https://docs.pytest.org/en/stable/usage.html
"""

import numpy as np
import pytest

import pyleoclim as pyleo


# Tests below
class TestUIEnsembleSeriesCorrelation:
    def test_correlation_t0(self, gen_ts, nt=100):
        """Test for EnsembleSeries.correlation() when the target is a Series"""

        ts0 = gen_ts(model="colored_noise", nt=nt).standardize()
        noise = gen_ts(model="colored_noise", alpha=0, nt=nt).standardize().value

        t0 = ts0.time
        v0 = ts0.value

        ts0 = pyleo.Series(time=t0, value=v0, verbose=False, auto_time_params=True)
        ts1 = pyleo.Series(
            time=t0, value=v0 + noise, verbose=False, auto_time_params=True
        )
        ts2 = pyleo.Series(
            time=t0, value=v0 + 2 * noise, verbose=False, auto_time_params=True
        )

        ts_list = [ts1, ts2]

        ts_ens = pyleo.EnsembleSeries(ts_list)

        corr_res = ts_ens.correlation(ts0)
        signif_list = corr_res.signif
        for signif in signif_list:
            assert signif == True

    def test_correlation_t1(self, gen_ts):
        """Test for EnsembleSeries.correlation() when the target is an EnsembleSeries with same number of Series"""
        nt = 100
        ts0 = gen_ts(model="colored_noise", nt=nt).standardize()
        noise = gen_ts(model="colored_noise", alpha=0, nt=nt).standardize().value

        t0 = ts0.time
        v0 = ts0.value

        ts0 = pyleo.Series(time=t0, value=v0, verbose=False, auto_time_params=True)
        ts1 = pyleo.Series(
            time=t0, value=v0 + noise, verbose=False, auto_time_params=True
        )
        ts2 = pyleo.Series(
            time=t0, value=v0 + 2 * noise, verbose=False, auto_time_params=True
        )
        ts3 = pyleo.Series(
            time=t0, value=v0 + 1 / 2 * noise, verbose=False, auto_time_params=True
        )

        ts_list1 = [ts0, ts1]
        ts_list2 = [ts2, ts3]

        ts_ens = pyleo.EnsembleSeries(ts_list1)
        ts_target = pyleo.EnsembleSeries(ts_list2)

        corr_res = ts_ens.correlation(ts_target)
        signif_list = corr_res.signif
        for signif in signif_list:
            assert signif == True

        assert np.size(corr_res.p) == np.size(ts_list1)

    def test_correlation_t2(self, gen_ts):
        """Test for EnsembleSeries.correlation() when the target is an EnsembleSeries with fewer Series"""
        nt = 100
        ts0 = gen_ts(model="colored_noise", nt=nt).standardize()
        noise = gen_ts(model="colored_noise", alpha=0, nt=nt).standardize().value

        t0 = ts0.time
        v0 = ts0.value

        ts0 = pyleo.Series(time=t0, value=v0, verbose=False, auto_time_params=True)
        ts1 = pyleo.Series(
            time=t0, value=v0 + noise, verbose=False, auto_time_params=True
        )
        ts2 = pyleo.Series(
            time=t0, value=v0 + 2 * noise, verbose=False, auto_time_params=True
        )
        ts3 = pyleo.Series(
            time=t0, value=v0 + 1 / 2 * noise, verbose=False, auto_time_params=True
        )
        ts4 = pyleo.Series(
            time=t0, value=v0 + 3 / 2 * noise, verbose=False, auto_time_params=True
        )

        ts_list1 = [ts0, ts1, ts4]
        ts_list2 = [ts2, ts3]

        ts_ens = pyleo.EnsembleSeries(ts_list1)
        ts_target = pyleo.EnsembleSeries(ts_list2)

        corr_res = ts_ens.correlation(ts_target)
        signif_list = corr_res.signif
        for signif in signif_list:
            assert signif == True

        assert np.size(corr_res.p) == np.size(ts_list1)

    def test_correlation_t3(self, gen_ts):
        """Test for EnsembleSeries.correlation() when the target is an EnsembleSeries with more Series"""
        nt = 100
        ts0 = gen_ts(model="colored_noise", nt=nt).standardize()
        noise = gen_ts(model="colored_noise", alpha=0, nt=nt).standardize().value

        t0 = ts0.time
        v0 = ts0.value
        ts1 = pyleo.Series(
            time=t0, value=v0 + noise, verbose=False, auto_time_params=True
        )
        ts2 = pyleo.Series(
            time=t0, value=v0 + 2 * noise, verbose=False, auto_time_params=True
        )
        ts3 = pyleo.Series(
            time=t0, value=v0 + 1 / 2 * noise, verbose=False, auto_time_params=True
        )
        ts4 = pyleo.Series(
            time=t0, value=v0 + 3 / 2 * noise, verbose=False, auto_time_params=True
        )

        ts_list1 = [ts0, ts1]
        ts_list2 = [ts2, ts3, ts4]

        ts_ens = pyleo.EnsembleSeries(ts_list1)
        ts_target = pyleo.EnsembleSeries(ts_list2)

        corr_res = ts_ens.correlation(ts_target)
        signif_list = corr_res.signif
        for signif in signif_list:
            assert signif == True

        assert np.size(corr_res.p) == np.size(ts_list1)

    @pytest.mark.parametrize("corr_method", ["ttest", "built-in", "ar1sim", "phaseran"])
    def test_correlation_t4(self, corr_method, gen_ts):
        """Test for EnsembleSeries.correlation() when the target is a Series
        Test that all allowable methods are passed.
        """
        nt = 100
        ts0 = gen_ts(model="colored_noise", nt=nt).standardize()
        noise = gen_ts(model="colored_noise", alpha=0, nt=nt).standardize().value

        t0 = ts0.time
        v0 = ts0.value
        ts1 = pyleo.Series(
            time=t0, value=v0 + noise, verbose=False, auto_time_params=True
        )
        ts2 = pyleo.Series(
            time=t0, value=v0 + 2 * noise, verbose=False, auto_time_params=True
        )

        ts_list = [ts1, ts2]

        ts_ens = pyleo.EnsembleSeries(ts_list)

        corr_res = ts_ens.correlation(ts0, method=corr_method)
        signif_list = corr_res.signif
        for signif in signif_list:
            assert signif == True

    @pytest.mark.parametrize(
        "stat", ["pearsonr", "spearmanr", "pointbiserialr", "kendalltau", "weightedtau"]
    )
    def test_correlation_t5(self, stat, gen_ts):
        """Test that various statistics can be used
        https://docs.scipy.org/doc/scipy/reference/stats.html#association-correlation-tests
        """
        nt = 200
        rho = 0.8
        ts0 = gen_ts(model="colored_noise", nt=nt, alpha=1.0).standardize()

        ts_list = []
        for k in range(2):
            v = rho * ts0.value + np.sqrt(1 - rho**2) * np.random.normal(
                loc=0, scale=1, size=nt
            )
            ts = pyleo.Series(
                time=ts0.time, value=v, verbose=False, auto_time_params=True
            )
            ts_list.append(ts)

        ts_ens = pyleo.EnsembleSeries(ts_list)

        corr_res = ts_ens.correlation(ts0, statistic=stat, method="phaseran")
        signif_list = corr_res.signif
        for signif in signif_list:
            assert signif == True


class TestUIEnsembleSeriesPlots:
    def test_histplot_t0(self, gen_ts):
        """Test for EnsembleSeries.histplot()"""
        nn = 30  # number of noise realizations
        nt = 500
        series_list = []

        signal = gen_ts(model="colored_noise", nt=nt, alpha=1.0).standardize()
        noise = np.random.randn(nt, nn)

        for idx in range(nn):  # noise
            ts = pyleo.Series(time=signal.time, value=signal.value + noise[:, idx])
            series_list.append(ts)

        ts_ens = pyleo.EnsembleSeries(series_list)

        ts_ens.histplot()
        pyleo.closefig()

    def test_plot_envelope_t0(self, gen_ts):
        """Test EnsembleSeries.plot_envelope() on a list of colored noise"""
        nn = 30  # number of noise realizations
        nt = 500
        series_list = []

        signal = gen_ts(model="colored_noise", nt=nt, alpha=1.0).standardize()

        noise = np.random.randn(nt, nn)

        for idx in range(nn):  # noise
            ts = pyleo.Series(time=signal.time, value=signal.value + noise[:, idx])
            series_list.append(ts)

        ts_ens = pyleo.EnsembleSeries(series_list)

        fig, ax = ts_ens.plot_envelope(curve_lw=1.5)
        pyleo.closefig(fig)

    @pytest.mark.parametrize("label", ["ensemble", None])
    def test_plot_traces_t0(self, label, gen_ts):
        """Test EnsembleSeries.plot_traces() on a list of colored noise"""
        nn = 30  # number of noise realizations
        nt = 500
        series_list = []

        signal = gen_ts(model="colored_noise", nt=nt, alpha=1.0).standardize()
        noise = np.random.randn(nt, nn)

        for idx in range(nn):  # noise
            ts = pyleo.Series(time=signal.time, value=signal.value + noise[:, idx])
            series_list.append(ts)

        ts_ens = pyleo.EnsembleSeries(series_list, label=label)

        fig, ax = ts_ens.plot_traces(
            alpha=0.2, num_traces=8
        )  # test transparency and num_traces at the same time
        pyleo.closefig(fig)


class TestUIEnsembleSeriesQuantiles:
    def test_quantiles_t0(self):
        nn = 30  # number of noise realizations
        nt = 500
        series_list = []

        t, v = pyleo.utils.gen_ts(model="colored_noise", nt=nt, alpha=1.0)
        signal = pyleo.Series(t, v)

        for idx in range(nn):  # noise
            noise = np.random.randn(nt, nn) * 100
            ts = pyleo.Series(
                time=signal.time, value=signal.value + noise[:, idx], verbose=False
            )
            series_list.append(ts)

        ts_ens = pyleo.EnsembleSeries(series_list)

        ens_qs = ts_ens.quantiles()

    def test_quantiles_t1(self):

        nn = 30  # number of age models
        time = np.arange(1, 20000, 100)  # create a time vector
        std_dev = 20  # Noise to be considered

        t, v = pyleo.utils.gen_ts(model="colored_noise", nt=len(time), alpha=1.0)

        series_list = []

        for i in range(nn):
            noise = np.random.normal(0, std_dev, len(time))
            ts = pyleo.Series(time=np.sort(time + noise), value=v, verbose=False)
            series_list.append(ts)

        time_ens = pyleo.EnsembleSeries(series_list)

        ens_qs = time_ens.quantiles(axis="time")


class TestUIEnsembleSeriesDataFrame:
    @pytest.mark.parametrize("axis", ["time", "value"])
    def test_to_dataframe_t0(self, axis):
        nn = 30  # number of age models
        time = np.arange(1, 20000, 100)  # create a time vector
        std_dev = 20  # Noise to be considered

        t, v = pyleo.utils.gen_ts(model="colored_noise", nt=len(time), alpha=1.0)

        series_list = []

        for i in range(nn):
            noise = np.random.normal(0, std_dev, len(time))
            ts = pyleo.Series(time=np.sort(time + noise), value=v, verbose=False)
            series_list.append(ts)

        time_ens = pyleo.EnsembleSeries(series_list)
        ens_qs = time_ens.quantiles(axis="time")

        if axis == "time":
            df = ens_qs.to_dataframe(axis="time")
        elif axis == "value":
            df = time_ens.to_dataframe(axis="value")


class TestUIEnsembleSeriesArray:

    @pytest.mark.parametrize(
        ("labels", "mode"),
        [
            (True, "time"),
            (True, "value"),
            (False, "time"),
            (False, "value"),
        ],
    )
    def test_to_array_t0(self, labels, mode):
        nn = 30  # number of age models
        time = np.arange(1, 20000, 100)  # create a time vector
        std_dev = 20  # Noise to be considered

        t, v = pyleo.utils.gen_ts(model="colored_noise", nt=len(time), alpha=1.0)

        series_list = []

        for i in range(nn):
            noise = np.random.normal(0, std_dev, len(time))
            ts = pyleo.Series(time=np.sort(time + noise), value=v, verbose=False)
            series_list.append(ts)

        time_ens = pyleo.EnsembleSeries(series_list)
        ens_qs = time_ens.quantiles(axis="time")

        if labels == True:
            vals, headers = ens_qs.to_array(axis=mode)
        else:
            vals = ens_qs.to_array(axis=mode)


class TestUIEnsembleSeriesfromAgeEnsembleArray:
    def test_fromAgeEnsembleArray_t0(self, pinkseries):
        series = pinkseries
        length = len(series.time)
        num = 3
        age_array = np.array([np.arange(length) for _ in range(num)]).T
        _ = pyleo.EnsembleSeries.from_AgeEnsembleArray(
            series=series, age_array=age_array
        )

    def test_fromAgeEnsembleArray_t1(self, pinkseries):
        series = pinkseries
        length = len(series.time)
        value_depth = np.arange(length)
        age_depth = np.arange(length)
        num = 3
        age_array = np.array([np.arange(length) for _ in range(num)]).T
        _ = pyleo.EnsembleSeries.from_AgeEnsembleArray(
            series=series,
            age_array=age_array,
            value_depth=value_depth,
            age_depth=age_depth,
        )


class TestUIEnsembleSeriesfromPaleoEnsembleArray:
    def test_fromPaleoEnsembleArray_t0(self, pinkseries):
        series = pinkseries
        length = len(series.time)
        num = 3
        paleo_array = np.array([np.random.normal(0, 1, length) for _ in range(num)]).T
        _ = pyleo.EnsembleSeries.from_PaleoEnsembleArray(
            series=series, paleo_array=paleo_array
        )

    def test_fromPaleoEnsembleArray_t1(self, pinkseries):
        series = pinkseries
        length = len(series.time)
        paleo_depth = np.arange(length)
        age_depth = np.arange(length)
        num = 3
        paleo_array = np.array([np.random.normal(0, 1, length) for _ in range(num)]).T
        _ = pyleo.EnsembleSeries.from_PaleoEnsembleArray(
            series=series,
            paleo_array=paleo_array,
            paleo_depth=paleo_depth,
            age_depth=age_depth,
        )


# class TestUIEnsembleSeriesDistplot():
#     def test_histplot_t0(self):
#         '''Test for EnsembleSeries.distplot()
#         '''
#         nn = 30 # number of noise realizations
#         nt = 500
#         series_list = []

#         signal = gen_ts(model='colored_noise', nt=nt, alpha=1.0).standardize()
#         noise = np.random.randn(nt, nn)

#         for idx in range(nn):  # noise
#             ts = pyleo.Series(time=signal.time, value=signal.value+noise[:,idx])
#             series_list.append(ts)

#         ts_ens = pyleo.EnsembleSeries(series_list)

#         ts_ens.histplot()
#         pyleo.closefig()
