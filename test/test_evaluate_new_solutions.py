def test_evaluate_new_solutions():
    """
    Test evaluate new solutions method
    """
    import numpy as np
    from spotPython.fun.objectivefunctions import analytical
    from spotPython.spot.spot import Spot
    from spotPython.utils.repair import repair_non_numeric
    import pytest

    fun = analytical().fun_sphere

    nn = 3
    ni = 4

    spot_test = Spot(
        fun=fun,
        lower=np.array([-10,-1]),
        upper=np.array([10,1]),
        n_points=nn,
        design_control={"init_size": ni}
    )


    # (S-2) Initial Design:
    spot_test.X = spot_test.generate_design(size=spot_test.design_control["init_size"],
                                            repeats=spot_test.design_control["repeats"], 
                                            lower=spot_test.lower,
                                            upper=spot_test.upper)
    spot_test.X = repair_non_numeric(spot_test.X,
                                        spot_test.var_type)

    # (S-3): Eval initial design:
    spot_test.y = spot_test.fun(spot_test.X)
    spot_test.surrogate.fit(spot_test.X, spot_test.y)
    X0 = spot_test.suggest_new_X()
    X0 = repair_non_numeric(X0, spot_test.var_type)

    # (S-18): Evaluating New Solutions:
    y0 = spot_test.fun(X0)
    assert y0.ndim == 1
    assert y0.shape[0] == nn
